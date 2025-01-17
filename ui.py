import os
import streamlit as st
from dotenv import load_dotenv
from user_login_info import *
from vector_database import *

import google.generativeai as genai

class UI:

    def __init__(self, user_login_manager):

        x = 1
        
    def add_header(self):
        logo_url = "https://raw.githubusercontent.com/RoobanSappani/TestRagProject/refs/heads/main/logo.png"
        st.markdown(
            f"""
            <div style="display: flex; align-items: center;">
                <img src="{logo_url}" alt="Logo" style="height: 50px; margin-right: 10px;">
                <h1 style="display: inline;">MeritoBuddy AI</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    def set_page(self, page):
        st.session_state.page = page

    def check_logged_in(self):

        if(st.session_state["logged_in"]):
            return True
        return False

    def login_page(self):

        self.add_header()
        st.subheader("Login")
        
        # Login form
        username_mail_id = st.text_input("Enter your mail address or username")
        password = st.text_input("Password", type="password")

        # Handle login
        if st.button("Login"):
            if st.session_state["user_login_manager"].login_user(username_mail_id, password):
                st.success("Logged in successfully!")
                st.session_state["logged_in"] = True
                st.session_state["username"] = username_mail_id
                return
            else:
                st.error("Invalid mail/username or password.")

        # Link to Signup page
        st.write("Don't have an account?")
        st.button("Create an account", on_click=self.set_page, args=['signup'])
        
    def signup_page(self):
        
        self.add_header()
        st.subheader("Signup")
        
        # Signup form
        mail_id = st.text_input("Enter your E-Mail")
        username = st.text_input("Enter your Username")
        password = st.text_input("Password", type="password")

        # Handle signup
        if st.button("Sign Up"):
            result = st.session_state["user_login_manager"].create_user(mail_id, username, password)

            if result is True:
                st.success("User created successfully!")
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                return
            elif result is False:
                st.error("Mail/Username already exists.")
            else:
                st.error("Error creating user. Please try again.")
            
        # Link to Login page
        st.write("Already have an account?")
        st.button("Back to Login", on_click=self.set_page, args=['login'])

    def chat_ui(self):
        
        self.add_header()
        st.sidebar.text(f"Logged in as: {st.session_state['username']}")
        st.title("Go ahead, ask me anything (quite ambitious at the moment)")

        uploaded_files = st.file_uploader("Upload PDF(s)", type="pdf", accept_multiple_files=True)
        
        if st.button("Process PDFs"):
            st.session_state["vb_manager"].process_pdfs(uploaded_files)
            st.success("PDFs processed and vector store created!")
            st.session_state["pdfs"] = True
            
        query = st.text_input("Enter your query:")

        matches = []
        if(query):
            matches = st.session_state["vb_manager"].query_vector_database(query)

            context = ""
            
            for i, (doc, score) in enumerate(matches, start=1):
                
                context += f"\n{i}. "
                context += doc.page_content
                
            prompt = llm_context_query_template.format(context = context,
                                                       query = query)

            response = st.session_state["llm_model"].generate_content(prompt)
            st.write("**Response:**")
            st.write(response.text)

    def run(self):

        # Page setup
        # st.set_page_config(page_title="Login/Signup System", layout="centered")

        # Page navigation
        if "page" not in st.session_state:
            st.session_state.page = "login"
        
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False

        if not st.session_state["logged_in"]:
            if st.session_state.page == "login":
                self.login_page()
            elif st.session_state.page == "signup":
                self.signup_page()
        else:
            self.chat_ui()
