import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from app.services.auth_service import login, signup
from app.utils.theme import apply_theme

st.set_page_config(page_title="Study Nook", page_icon="study", layout="wide")
apply_theme()

if "user" not in st.session_state:
    st.session_state["user"] = None

st.title("Study Nook")

if st.session_state["user"] is not None:
    user = st.session_state["user"]
    st.success(f"Logged in as {user['name']} ({user['email']})")
    st.write("Use the sidebar to log study hours, manage subjects, and view your dashboard.")

    if st.button("Log out"):
        st.session_state["user"] = None
        st.rerun()

    st.stop()

tab_login, tab_signup = st.tabs(["Log in", "Sign up"])

with tab_login:
    st.subheader("Log in")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in"):
        user = login(login_email.strip(), login_password)
        if user is None:
            st.error("Incorrect email or password.")
        else:
            st.session_state["user"] = user
            st.rerun()

with tab_signup:
    st.subheader("Sign up")
    signup_name = st.text_input("Name", key="signup_name")
    signup_email = st.text_input("Email", key="signup_email")
    signup_password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Create account"):
        if not signup_name.strip() or not signup_email.strip():
            st.error("Name and email are required.")
        elif len(signup_password) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            try:
                user = signup(signup_name.strip(), signup_email.strip(), signup_password)
                st.session_state["user"] = user
                st.rerun()
            except ValueError as e:
                st.error(str(e))
