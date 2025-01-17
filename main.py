import os
from dotenv import load_dotenv
import google.generativeai as genai

import streamlit as st
from vector_database import *
from user_login_info import *
from ui import *
from htr_ocr import *

def init_session():

    if "pdfs" not in st.session_state:
        st.session_state["pdfs"] = False
    
    if "vb_manager" not in st.session_state:
        st.session_state["vb_manager"] = VectorDatabase()

    if "llm_model" not in st.session_state:
        genai.configure(api_key=os.getenv("google_gemini_api_key"))
        st.session_state["llm_model"] = genai.GenerativeModel("gemini-1.5-flash")

    if "user_login_manager" not in st.session_state:
        st.session_state["user_login_manager"] = UserLogin()
    
    if "ui_manager" not in st.session_state:
        st.session_state["ui_manager"] = UI(st.session_state["user_login_manager"])

    if "supabase_client" not in st.session_state:
        supabase_url = os.getenv("supabase_url")
        supabase_key = os.getenv("supabase_key")

        supabase_client = create_client(supabase_url, supabase_key)
        with open("./gc_vision_creds_check.json", "wb+") as f:
            response = supabase_client.storage.from_("EduAICreds").download(
                "gc_vision_creds.json"
            )
            f.write(response)

        st.session_state["supabase_client"] = supabase_client

    st.write("initialized vars")

def main():

    load_dotenv()
    init_session()
    print("this is a test message")

    st.session_state["ui_manager"].run()
    # ui_manager

if __name__ == "__main__":
    
    main()




