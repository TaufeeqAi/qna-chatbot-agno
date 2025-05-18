import streamlit as st
from src.utils.api import get_progress

def render_profile(user):
    st.header("👤 Your Profile")
    st.write(f"**Email:** {user['email']}")
    st.write("**Interests:**", ", ".join(user.get("interests", [])))

    st.subheader("Research Progress")
    progress_list = get_progress(st.session_state.token)
    if not progress_list:
        st.write("No progress logged yet.")
    else:
        for item in progress_list:
            st.markdown(f"- **{item['topic']}** — {item['status']} _(updated {item['updated_at']})_")
