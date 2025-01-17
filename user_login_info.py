import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

import bcrypt
import os
import ast

load_dotenv

class UserLogin:

    def __init__(self):

        if "supabase_client" not in st.session_state:

            self.supabase_url = os.getenv("supabase_url")
            self.supabase_key = os.getenv("supabase_key")

            self.supabase_client = create_client(self.supabase_url, self.supabase_key)
        
        else:
            self.supabase_client = st.session_state["supabase_client"]

    def create_user(self, mail_id, username, password):

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        insert_data = {'mail_id': mail_id, 
                       'username' : username, 
                       'password': hashed_password.decode()}
        
        # Insert user into Supabase
        try:
            response = self.supabase_client.table('user_login_info').insert(insert_data).execute()
            print("Data inserted successfully")
            return True
        
        except Exception as api_error:
            # Catch the APIError and extract the JSON error object
            error_details = ast.literal_eval(api_error.args[0])  # The first argument contains the error JSON
            print("Error details:", error_details)
            
        if(error_details["code"] == "23505"):
            return False
        
        return None

    def login_user(self, username_mail_id, password):
        
        # Fetch user from Supabase
        response1 = self.supabase_client.table('user_login_info').select('*').eq('mail_id', username_mail_id).execute()
        response2 = self.supabase_client.table('user_login_info').select('*').eq('username', username_mail_id).execute()

        if len(response1.data):
            stored_password = response1.data[0]['password']
        else:
            stored_password = response2.data[0]['password']

            # Verify password
            if bcrypt.checkpw(password.encode(), stored_password.encode()):
                return True
            
        return False
