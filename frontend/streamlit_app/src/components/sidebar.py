import streamlit as st
import time 
from src.utils.api import ingest_document, HTTPException # Import the updated API function and custom exception

def render_sidebar():
    st.sidebar.title("Settings")
    mode = st.sidebar.selectbox(
        "Reasoning Strategy",
        ["chain_of_thought", "tree_of_thought", "graph_of_thought"]
    )
    show_trace = st.sidebar.checkbox("Show Reasoning Steps", value=False)
    
    st.sidebar.divider()
    st.sidebar.title("Document Ingestion")

    source_type = st.sidebar.radio(
        "Select Source Type",
        options=["File Upload", "arXiv ID", "Web URL"],
        key="source_type_selection"
    )

    uploaded_file = None
    arxiv_id_input = None
    web_url_input = None

    if source_type == "File Upload":
        uploaded_file = st.sidebar.file_uploader("Upload Research PDF", type=["pdf"], key="pdf_file_uploader")
    elif source_type == "arXiv ID":
        arxiv_id_input = st.sidebar.text_input("Enter arXiv ID (e.g., '1706.03762')", key="arxiv_id_input")
    elif source_type == "Web URL":
        web_url_input = st.sidebar.text_input("Enter Web Page URL", key="web_url_input")

    # Placeholder for the actual API call logic, will be connected later
    # For now, just returning the selected values for testing the UI part.
    # The actual API call will be handled by a function in api_utils.py (or similar)
    # and triggered by an "Ingest" button.
    
    # This button should trigger the ingestion logic
    # The ingestion logic will be moved to a separate function or handled within api_utils.py
    # This button should trigger the ingestion logic
    if st.sidebar.button("Ingest Document", key="ingest_button"):
        token = st.session_state.get("token")
        if not token:
            st.sidebar.error("Authentication token not found. Please log in.")
            # Optionally, redirect to login or stop execution
            return mode, show_trace, source_type, uploaded_file, arxiv_id_input, web_url_input


        api_source_type = ""
        source_id = None
        file_to_upload = None
        valid_input = False

        if source_type == "File Upload":
            api_source_type = "file"
            if uploaded_file:
                file_to_upload = uploaded_file
                valid_input = True
            else:
                st.sidebar.error("Please upload a PDF file.")
        elif source_type == "arXiv ID":
            api_source_type = "arxiv"
            if arxiv_id_input and arxiv_id_input.strip():
                source_id = arxiv_id_input.strip()
                valid_input = True
            else:
                st.sidebar.error("Please enter an arXiv ID.")
        elif source_type == "Web URL":
            api_source_type = "url"
            if web_url_input and web_url_input.strip():
                source_id = web_url_input.strip()
                valid_input = True
            else:
                st.sidebar.error("Please enter a Web URL.")

        if valid_input:
            try:
                with st.spinner(f"Ingesting document from {source_type}..."):
                    response = ingest_document(
                        token=token,
                        source_type=api_source_type,
                        source_identifier=source_id,
                        file_widget=file_to_upload
                    )
                st.sidebar.success(response.get("detail", "Document ingested successfully!"))
            except HTTPException as e: # Catch custom HTTP errors from api.py
                 st.sidebar.error(f"Error: {e.detail} (Status code: {e.status_code})")
            except ValueError as e: # Catch validation errors from api.py or UI logic
                 st.sidebar.error(f"Input Error: {str(e)}")
            except Exception as e: # Catch any other unexpected errors
                 st.sidebar.error(f"An unexpected error occurred: {str(e)}")
        # else: error messages are already shown by the checks above

    st.sidebar.divider()
    if st.sidebar.button("Logout"):
        if "token" in st.session_state:
            del st.session_state.token
        if "logged_in" in st.session_state: # Assuming you use this flag
            del st.session_state.logged_in
        st.success("Logged out successfully.")
        time.sleep(1) 
        st.experimental_rerun()

    # The 'uploaded' variable is now conditional. 
    # The main app structure might need adjustment if it directly expects 'uploaded'
    # For now, we return all possible inputs. The calling function will decide what to do.
    return mode, show_trace, source_type, uploaded_file, arxiv_id_input, web_url_input
