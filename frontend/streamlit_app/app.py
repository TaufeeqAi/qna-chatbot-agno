import streamlit as st
from src.utils.auth import require_login
from src.pages.home import render_home
from src.pages.profile import render_profile

# Ensure ENV variables are loaded
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Research Q/A Chatbot", layout="wide")

# Enforce login
user = require_login()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Profile"])

if page == "Home":
    render_home(user)
else:
    render_profile(user)
