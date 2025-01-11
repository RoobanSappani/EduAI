import os
from dotenv import load_dotenv
import google.generativeai as genai

import streamlit as st
from vector_database import *
from user_login_info import *
from ui import *

@st.cache_resource()
def assign_vals():
    st.session_state["pdfs"] = False
    st.session_state["vb_manager"] = VectorDatabase()

    genai.configure(api_key=os.getenv("google_gemini_api_key"))
    llm_model = genai.GenerativeModel("gemini-1.5-flash")

    st.session_state["llm_model"] = llm_model
    st.session_state["user_login_manager"] = UserLogin()
    st.session_state["ui_manager"] = UI(st.session_state["user_login_manager"])
    print("assigned values")

def main():

    load_dotenv()
    assign_vals()
    print("this is a test message")

    st.session_state["ui_manager"].run()
    # ui_manager

if __name__ == "__main__":
    
    main()




