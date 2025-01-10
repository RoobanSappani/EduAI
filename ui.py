
from user_login_info import *
from vector_database import *
import streamlit as st

class UI:

    def __init__(self, 
                 user_login_manager, 
                 vb_manager, 
                 llm_model,
                 logo_url = "https://raw.githubusercontent.com/RoobanSappani/TestRagProject/refs/heads/main/logo.png"):

        st.session_state["user_login_manager"] = user_login_manager
        st.session_state["vb_manager"] = vb_manager
        st.session_state["llm_model"] = llm_model
        self.logo_url = logo_url

    # Function to add a title and logo to the top left corner
    def add_header(self):
        st.markdown(
            f"""
            <div style="display: flex; align-items: center;">
                <img src="{self.logo_url}" alt="Logo" style="height: 50px; margin-right: 10px;">
                <h1 style="display: inline;">MeritoBuddy AI</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    def login_page(self):

        self.add_header()
        st.title("Welcome to MeritoBuddy AI")

        menu = st.sidebar.selectbox("Menu", ["Login", "Sign Up"])

        if menu == "Sign Up":

            st.subheader("Create an Account")
            mail_id = st.text_input("Enter your E-Mail")
            username = st.text_input("Enter your Username")
            password = st.text_input("Password", type="password")

            if st.button("Sign Up"):
                
                result = st.session_state["user_login_manager"].create_user(mail_id, username, password)

                if result is True:
                    st.success("User created successfully!")
                elif result is False:
                    st.error("Mail/Username already exists.")
                else:
                    st.error("Error creating user. Please try again.")

        elif menu == "Login":

            st.subheader("Login")
            username_mail_id = st.text_input("Enter your mail address or username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if st.session_state["user_login_manager"].login_user(username, password):
                    st.success("Logged in successfully!")
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                else:
                    st.error("Invalid mail/username or password.")

    def chat_ui(self):

        self.add_header()
        st.sidebar.text(f"Logged in as: {st.session_state['username']}")
        st.title("Go ahead, ask me anything (quite ambitious at the moment)")

        uploaded_files = st.file_uploader("Upload PDF(s)", type="pdf", accept_multiple_files=True)
        if st.button("Process PDFs"):
            st.session_state["vb_manager"].process_pdfs(uploaded_files)
            st.success("PDFs processed and vector store created!")

        query = st.text_input("Enter your query:")
        matches = st.session_state["vb_manager"].query_vector_database(query)

        context = ""
        
        for i, (doc, score) in enumerate(matches, start=1):
            
            context += f"\n{i}. "
            context += doc.page_content
            
        prompt = f"You are an AI Assistant. Based on the given context, answer the given query. context: {context}, query: {query}"
        
        print(prompt)	

        response = st.session_state["llm_model"].generate_content(prompt)
        st.write("**Response:**")
        st.write(response.text)

    def run(self):

        if "logged_in" not in st.session_state:
            st.session_state["logged_in"] = False

            if st.session_state["logged_in"]:
                self.chat_ui()
            else:
                self.login_page()
