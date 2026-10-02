"""
Call require_login() at the top of any page that needs a logged-in user.
Returns the user_id so the page can use it immediately.
"""

import streamlit as st


def require_login() -> int:
    user = st.session_state.get("user")
    if user is None:
        st.warning("Please log in first.")
        st.page_link("main.py", label="Go to login page")
        st.stop()
    return user["id"]
