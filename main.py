import os
from dotenv import load_dotenv
import google.generativeai as genai

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

# Main app
if __name__ == "__main__":

    load_dotenv()
    genai.configure(api_key=os.getenv("google_gemini_api_key"))
    llm_model = genai.GenerativeModel("gemini-1.5-flash")

    vb_manager = VectorDatabase()
    user_login_manager = UserLogin()

    ui_manager = UI(user_login_manager, vb_manager, llm_model)

    ui_manager.run()

def main():

    load_dotenv()
    assign_vals()
    st.session_state["ui_manager"].run()
    # ui_manager

if __name__ == "__main__":
    
    main()




