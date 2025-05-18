import streamlit as st
from src.components.sidebar import render_sidebar
from src.components.chat_window import render_chat
from src.utils.api import chat, upload_pdf

def render_home(user):
    st.header("🔬 AI Research Assistant")
    mode, show_trace, uploaded = render_sidebar()

    # PDF upload handling
    if uploaded:
        result = upload_pdf(uploaded, st.session_state.token)
        if result.status_code == 201:
            st.sidebar.success("PDF ingested successfully!")
        else:
            st.sidebar.error(f"Failed to ingest: {result.text}")

    # Initialize chat history
    if "history" not in st.session_state:
        st.session_state.history = []

    # Input and submit
    user_input = st.text_input("Enter your question:", key="query")
    if st.button("Ask"):
        with st.spinner("Thinking..."):
            resp = chat(user_input, mode, st.session_state.token)
        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("Bot", resp["response"]))
        if show_trace:
            st.session_state.history.append(("Trace", resp["trace"]))

    # Render the chat
    render_chat(st.session_state.history)
