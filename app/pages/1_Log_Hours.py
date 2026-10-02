import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import datetime
import streamlit as st

from app.services.log_service import get_subjects, add_log
from app.utils.auth_guard import require_login
from app.utils.theme import apply_theme
from app.utils.analytics_ga import inject_google_analytics

apply_theme()
inject_google_analytics()
st.title("Log Study Hours")

user_id = require_login()
subjects = get_subjects(user_id)

if subjects.empty:
    st.warning("You don't have any subjects yet. Add one on the Subjects page first.")
    st.stop()

subject_name = st.selectbox("Subject", subjects["name"])
subject_id = int(subjects.loc[subjects["name"] == subject_name, "id"].iloc[0])

log_date = st.date_input("Date", value=datetime.date.today())
hours = st.number_input("Hours studied", min_value=0.0, max_value=24.0, step=0.5)
notes = st.text_input("Notes (optional)")

if st.button("Save log"):
    if hours <= 0:
        st.error("Hours must be greater than 0.")
    else:
        add_log(subject_id, log_date, hours, notes or None)
        st.success(f"Logged {hours}h for {subject_name} on {log_date}.")
