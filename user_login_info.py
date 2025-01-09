import streamlit as st
from supabase import create_client, Client
import bcrypt

class UserLogin:

    def __init__(self, supabase_url, supabase_key):

        self.supabase_url = supabase_url
        self.supabase_key = supabase_key

        self.supabase_client = create_client(self.supabase_url, self.supabase_key)

    def create_user(self, mail_id, password):

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Insert user into Supabase
        response = self.supabase_client.table('user_login_info').insert({'mail_id': mail_id, 'password': hashed_password.decode('utf-8')}).execute()

        if response.status_code == 201:
            return True
        elif response.status_code == 409:  # Conflict error (username already exists)
            return False
        return None

    def login_user(self, mail_id, password):
        
        # Fetch user from Supabase
        response = self.supabase_client.table('user_login_info').select('*').eq('mail_id', mail_id).execute()
        if response.data:
            stored_password = response.data[0]['password']

            # Verify password
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return True
        return False
