import os
import google.generativeai as genai

from vector_database import *
from user_login_info import *
from ui import *

# Main app
if __name__ == "__main__":

    genai.configure(api_key=os.getenv("google_gemini_api_key"))
    llm_model = genai.GenerativeModel("gemini-1.5-flash")

    vb_manager = VectorDatabase()
    user_login_manager = UserLogin()

    ui_manager = UI(user_login_manager, vb_manager, llm_model)

    ui_manager.run()




