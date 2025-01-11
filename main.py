import os
from dotenv import load_dotenv
import google.generativeai as genai

import streamlit as st
from vector_database import *
from user_login_info import *
from ui import *

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

def main():

    load_dotenv()
    init_session()
    print("this is a test message")

    st.session_state["ui_manager"].run()
    # ui_manager

if __name__ == "__main__":
    
    main()




