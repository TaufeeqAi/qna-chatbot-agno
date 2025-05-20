import streamlit as st
import time

def render_callback():
    st.title("Login Callback")

    # Try to get the token from query parameters
    try:
        # In Streamlit versions 1.28+, query_params is a property
        # For older versions, it might be st.experimental_get_query_params()
        # This code assumes a modern Streamlit version.
        query_params = st.query_params
        token = query_params.get("token")
    except AttributeError: # Fallback for older Streamlit if needed
        try:
            token = st.experimental_get_query_params().get("token", [None])[0]
        except: # Broad except if experimental_get_query_params also fails or not available
            token = None


    if token:
        # If token is a list, take the first element
        if isinstance(token, list):
            token = token[0]
            
        st.session_state.token = token
        st.session_state.logged_in = True  # Assuming you use this flag
        st.success("Login successful! Redirecting to the home page...")
        
        # Give a moment for the user to see the message
        time.sleep(2)
        
        # Redirect to the main application page (Home)
        # Ensure 'Home.py' or your main app page exists in the 'pages' folder or is the main app file
        # For Streamlit, page navigation is done by providing the page's Python file name
        # If your main page is app.py at the root of streamlit_app, this might need adjustment
        # or you use st.switch_page("app") - check Streamlit's current best practices for page navigation.
        # Assuming 'Home.py' is the target page in the 'pages' directory.
        try:
            st.switch_page("home") # Try to switch to 'home.py'
        except Exception as e:
            # Fallback if 'home.py' is not found by that name or if st.switch_page has issues
            # This might happen if 'home' is the main app.py page.
            # In such cases, a rerun might be enough if require_login() handles the logged_in state.
            st.warning(f"Could not switch to home page automatically ({e}). Please navigate manually or refresh.")
            st.experimental_rerun()


    else:
        st.error("Login failed. Token not found in URL. Please try logging in again.")
        st.info("Redirecting to login page in 5 seconds...")
        time.sleep(5)
        # Attempt to redirect to a login page if it exists, e.g., 'Login.py'
        # If your login is part of the main app or auth module, this might need to go to the root.
        try:
            st.switch_page("Login") # Assuming you have a 'Login.py' or it's handled by require_login
        except:
            st.experimental_rerun() # Rerun to trigger login flow in require_login

if __name__ == "__main__":
    # This check ensures that the function is called when the script is run directly
    # or when Streamlit navigates to this page.
    # Initialize session state if it's not already (e.g., if this page is hit directly)
    if "token" not in st.session_state:
        st.session_state.token = None
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        
    render_callback()
