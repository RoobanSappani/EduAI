
from user_login_info import *

import streamlit as st

# User Login/Signup

supabase_url = "https://doktxbahrydntggxbqcz.supabase.co"
supabase_anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRva3R4YmFocnlkbnRnZ3hicWN6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY0MTMzNTQsImV4cCI6MjA1MTk4OTM1NH0.UExuMAT4HZ_o89BLlJCISmmckl1iOQQRbnGucxdeKkE"

user_login = UserLogin(supabase_url, supabase_anon_key)

# Streamlit UI
st.title("Welcome to MeritoBuddy AI")

menu = st.sidebar.selectbox("Menu", ["Login", "Sign Up"])

if menu == "Sign Up":
    st.subheader("Create an Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        result = user_login.create_user(new_user, new_password)
        if result is True:
            st.success("User created successfully!")
        elif result is False:
            st.error("Username already exists.")
        else:
            st.error("Error creating user. Please try again.")

elif menu == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if user_login.login_user(username, password):
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password.")