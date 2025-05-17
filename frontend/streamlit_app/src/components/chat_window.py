import streamlit as st
def render(history):
    for h in history:
        role, text = h
        st.markdown(f"**{role}:** {text}")
