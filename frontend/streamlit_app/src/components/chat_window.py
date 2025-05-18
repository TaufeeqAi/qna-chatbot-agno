import streamlit as st

def render_chat(history):
    for entry in history:
        speaker, text = entry
        if speaker == "You":
            st.markdown(f"**You:** {text}")
        elif speaker == "Bot":
            st.markdown(f"**Bot:** {text}")
        else:  # Trace
            with st.expander("Reasoning Trace"):
                st.write(text)
