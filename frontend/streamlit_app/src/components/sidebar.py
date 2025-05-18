import streamlit as st

def render_sidebar():
    st.sidebar.title("Settings")
    mode = st.sidebar.selectbox(
        "Reasoning Strategy",
        ["chain_of_thought", "tree_of_thought", "graph_of_thought"]
    )
    show_trace = st.sidebar.checkbox("Show Reasoning Steps", value=False)
    uploaded = st.sidebar.file_uploader("Upload Research PDF", type=["pdf"])
    return mode, show_trace, uploaded
