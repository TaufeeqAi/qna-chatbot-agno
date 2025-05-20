import streamlit as st
from src.utils.api import login as api_login, get_current_user
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def require_login():
    """
    Ensures user is authenticated. If not, shows login form.
    Returns user dict on success.
    """
    if "token" not in st.session_state:
        st.session_state.token = None

    if st.session_state.token is None:
        with st.form("login_form"):
            st.write("## Please log in")
            email = st.text_input("Email")
            pwd = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

            st.divider()

            # Google OAuth Login Button
            # IMPORTANT: This URL must match your backend's `/auth/google` endpoint.
            # The backend will then redirect to Google's auth page.
            # The Streamlit app must be running on a port that the backend can redirect to
            # (e.g. http://localhost:8501/callback as configured in backend)
            # Use os.getenv to fetch API_URL, ensuring .env is loaded
            backend_url = os.getenv("API_URL", "http://localhost:8000") 
            google_login_url = f"{backend_url}/auth/google"
            
            # Using a regular button with meta refresh for same-tab redirect
            # Note: Streamlit's st.link_button opens in a new tab by default.
            # For a same-tab redirect, JavaScript or a meta refresh tag is typically needed,
            # but st.link_button is the simplest Streamlit-native way to create a clickable link.
            # For a more seamless same-page redirect, we'd typically use HTML/JS or a
            # different component structure if available. Given Streamlit's execution model,
            # a full redirect is cleaner.
            if st.button("Login with Google"):
                st.markdown(f'<meta http-equiv="refresh" content="0;url={google_login_url}">', unsafe_allow_html=True)
                st.info("Redirecting to Google for login...")
                st.stop() # Stop further execution to allow redirect

            if submitted:
                token = api_login(email, pwd)
                if token:
                    st.session_state.token = token
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials")
        st.stop()

    # Once here, token exists
    user = get_current_user(st.session_state.token)
    return user
