import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

from PyPDF2 import PdfReader

from constants import *
from htr_ocr import *

class VectorDatabase:

    def __init__(self, embeddings_model = None, chunk_size = 1000, chunk_overlap_size = 200):

        if(embeddings_model):
            self.embeddings_model = embeddings_model
        else: self.embeddings_model = EMBEDDINGS_MODEL

        self.chunk_size = chunk_size
        self.chunk_overlap_size = chunk_overlap_size
        
        self.files = []
        self.chunks = []

        self.vector_db = None

        self.htr_ocr_manager = HTROCR()
    
    def read_pdf(self, file):
        
        if(isinstance(file, str)):
            pdf_file = open(file, "rb")
            reader = PdfReader(pdf_file)
        else:
            reader = PdfReader(file)

        text = ""
        text = "".join(page.extract_text() for page in reader.pages)

        self.files.append(text)

        return text

    def chunk_texts(self, text = None):
        
        ### need intelligent chunking (like page wise)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap_size
            )
        
        if(text):
            return text_splitter.split_text(text)
        
        else:
            return text_splitter.split_text(" ".join(self.files))

    def create_vector_database(self, chunks):

        self.vector_db = FAISS.from_texts(chunks, self.embeddings_model)
        print("Created Vector Database")

    def update_vector_database(self, chunks):
        
        ### need to create a better logic to update current db.
        self.vector_db = FAISS.from_texts(self.chunks + chunks, self.embeddings_model)


    def process_pdfs(self, files, create_vb_db = True):

        chunks = []
        for file in files:
            text = self.read_pdf(file)
            
            if(len(text) == 0):
                st.write("No text found in pdf, assuming handwritten notes, will take a few minutes to process...")
                text = self.htr_ocr_manager.extract_text_from_pdf(file)

            chunks.extend(self.chunk_texts(text))
        
        if(len(self.chunks)):
            self.update_vector_database(chunks)
        else:
            self.create_vector_database(chunks)
            
        self.chunks.extend(chunks)

        return self.vector_db

    def query_vector_database(self, query, top_k=3):
        
        docs_with_scores = self.vector_db.similarity_search_with_score(query, k=top_k)
        return docs_with_scores
