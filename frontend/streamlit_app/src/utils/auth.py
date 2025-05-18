import streamlit as st
from src.utils.api import login as api_login, get_current_user

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
