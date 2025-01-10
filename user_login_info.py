import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import bcrypt
import os

load_dotenv

class UserLogin:

    def __init__(self):

        self.supabase_url = os.getenv("supabase_url")
        self.supabase_key = os.getenv("supabase_key")

        self.supabase_client = create_client(self.supabase_url, self.supabase_key)

    def create_user(self, mail_id, username, password):

        # Hash the password
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        insert_data = {'mail_id': mail_id, 
                       'username' : username, 
                       'password': hashed_password}
        
        # Insert user into Supabase
        response = self.supabase_client.table('user_login_info').insert(insert_data).execute()

        if response.status_code == 201:
            return True
        
        elif response.status_code == 409:  # Conflict error (username already exists)
            return False
        
        return None

    def login_user(self, username_mail_id, password):
        
        # Fetch user from Supabase
        response1 = self.supabase_client.table('user_login_info').select('*').eq('mail_id', username_mail_id).execute()
        response2 = self.supabase_client.table('user_login_info').select('*').eq('username', username_mail_id).execute()
        
        if response1.data or response2.data:
            stored_password1 = response1.data[0]['password']
            stored_password2 = response2.data[0]['password']

            # Verify password
            if bcrypt.checkpw(password, stored_password1) or bcrypt.checkpw(password, stored_password2):
                return True
            
        return False
