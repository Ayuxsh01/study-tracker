import streamlit as st

from app.services.log_service import get_subjects, create_subject
from app.utils.auth_guard import require_login

st.title("Manage Subjects")

user_id = require_login()

st.subheader("Your subjects")
subjects = get_subjects(user_id)
st.dataframe(subjects, use_container_width=True)

st.subheader("Add a new subject")
name = st.text_input("Subject name")
total_hours = st.number_input("Total syllabus hours", min_value=1.0, step=1.0)

if st.button("Add subject"):
    if not name.strip():
        st.error("Subject name can't be empty.")
    else:
        create_subject(user_id, name.strip(), total_hours)
        st.success(f"Added subject '{name}'.")
        st.rerun()
