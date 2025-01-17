import fitz

from PIL import Image
import cv2

import streamlit as st

import os
import io
import numpy as np
import json
from tqdm import tqdm
import time

from google.cloud import vision
import google.generativeai as genai

from prompt_templates import *
from utils import *

from google.oauth2 import service_account
import json

class HTROCR:

    def __init__(self, verbose = 0):

        self.img_context = vision.ImageContext(language_hints=["en"]) 

        if "supabase_client" not in st.session_state:
            self.supabase_client = get_supabase_client()
        else:
            self.supabase_client = st.session_state["supabase_client"]

        response = self.supabase_client.storage.from_("EduAICreds").download(
                                                        "gc_vision_creds.json"
                                                    )
        creds_dict = json.loads(response)

        # Authenticate using the credentials
        creds = service_account.Credentials.from_service_account_info(creds_dict)
        self.client = vision.ImageAnnotatorClient(credentials = creds)

        if "llm_model" in st.session_state:
            self.llm_model = st.session_state["llm_model"]

        else:
            genai.configure(api_key=os.getenv("google_gemini_api_key"))
            self.llm_model = genai.GenerativeModel("gemini-1.5-flash")

        self.verbose = verbose

    def preprocess_img(self, img, scale = 3):

        if(self.verbose): print("Pre processing images...")
        img = np.array(img)
        # print(img.shape)
        new_height,new_width = img.shape[0]*scale, img.shape[1]*scale
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
        
        return img

    def find_cntrs(self, img):
        
        if(self.verbose): print("Finding contours...")
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) # grayscale
        ret, thresh2 = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY_INV) # filter with thresh
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (150,2))
        mask = cv2.morphologyEx(thresh2, cv2.MORPH_DILATE, kernel)

        contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        return contours
    
    def crop_cntr_imgs(self, img, contours, crop_img_ht_thresh = 30):
        
        if(self.verbose): print("Cropping text areas in image based on contours...")
        cropped_images = []
        height,width = int(img.shape[0]), int(img.shape[1])
        # print(img.shape)

        for cntr in contours:
            x,y,w,h = cv2.boundingRect(cntr)
            if(h > crop_img_ht_thresh):
                cropped_images.append(img[max(0, y-15):min(y+h+15,height) , x: x+w, :])

        self.cropped_images = cropped_images
        return cropped_images

    def postprocess_img(self, img):

        if(self.verbose): print("Post processing images...")
        # Apply Gaussian Blur
        blurred = cv2.GaussianBlur(img, (9, 9), 10)

        # Create an unsharp mask
        unsharp_image = cv2.addWeighted(img, 1.5, blurred, -0.5, 0)
        
        return unsharp_image

    def extract_pdf_images(self, pdf_file):
        
        if(self.verbose): print("Extracting pages as images...")
        
        pdf_file = open(pdf_file, "rb")
        pdf_document = fitz.open(pdf_file)

        images = []

        # Loop through each page of the PDF
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            
            # Convert the page to an image
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes()))  # Convert bytes to image
            
            img = self.preprocess_img(img)
            
            images.append(img)

        self.images = images
        return images
    
    def extract_text_from_img(self, img_bytes):

        if(self.verbose): print("Performing HTR on images...")

        gcv_image = vision.Image(content=img_bytes)

        # Perform text detection
        response = self.client.text_detection(image=gcv_image, 
                                              image_context = self.img_context)
        annotations = response.text_annotations

        # Extract and add the detected text
        if annotations:
            return annotations[0].description
        
        else: return ""

        # Check for errors
        if response.error.message:
            raise Exception(f"API error: {response.error.message}")

    def img_to_bytes(self, img):

        if(self.verbose): print("Converting image to bytes...")
        success, encoded_image = cv2.imencode('.png', img)
        img_bytes = encoded_image.tobytes()

        return img_bytes
    
    def correct_htr_text(self, text):

        if(self.verbose): print("Correcting HTR output...")
        text = text.replace("\n", "")
        output = self.llm_model.generate_content(htr_correction_template.format(final_text = text)).text

        return output

    def extract_text_from_pdf(self, pdf_file):
        
        final_text = ""
        page_images = self.extract_pdf_images(pdf_file)

        for img in tqdm(page_images):
            
            # start_time = time.time()
            contours = self.find_cntrs(img)
            cropped_images = self.crop_cntr_imgs(img, contours)
            
            cropped_img_bytes = []

            # print("1", time.time() - start_time)
            for cropped_img in cropped_images:
                
                postprocessed_img = self.postprocess_img(cropped_img)
                img_bytes = self.img_to_bytes(postprocessed_img)
                cropped_img_bytes.append(img_bytes)

            page_texts = []
            # print("2", time.time() - start_time)
            for img_bytes in cropped_img_bytes:

                page_text = self.extract_text_from_img(img_bytes)
                page_texts.append(page_text)
            
            # print("3", time.time() - start_time)
            final_text = final_text + " " + self.correct_htr_text(" ".join(page_texts))

        return final_text
                




