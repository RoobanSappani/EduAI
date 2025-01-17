
from supabase import create_client, Client
import os

def get_supabase_client():

    supabase_url = os.getenv("supabase_url")
    supabase_key = os.getenv("supabase_key")

    supabase_client = create_client(supabase_url, supabase_key)
    
    return supabase_client