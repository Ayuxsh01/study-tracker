import streamlit as st
import plotly.express as px

from app.services.log_service import get_subjects, get_logs
from app.services.analytics import (
    rolling_7day_average,
    current_streak,
    completion_rate,
    project_completion_date,
)
from app.utils.auth_guard import require_login

st.title("Analytics Dashboard")

user_id = require_login()
subjects = get_subjects(user_id)

if subjects.empty:
    st.warning("You don't have any subjects yet. Add one on the Subjects page first.")
    st.stop()

subject_name = st.selectbox("Subject", subjects["name"])
subject_row = subjects.loc[subjects["name"] == subject_name].iloc[0]
logs = get_logs(int(subject_row["id"]))

if logs.empty:
    st.info("No logs yet for this subject. Log some hours first.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("7-day avg", f"{rolling_7day_average(logs)} hrs/day")
col2.metric("Current streak", f"{current_streak(logs)} days")
col3.metric("Completion", f"{completion_rate(logs, subject_row['total_syllabus_hours'])}%")

projected = project_completion_date(logs, subject_row["total_syllabus_hours"])
col4.metric("Projected finish", projected.date().isoformat() if projected is not None else "N/A")

st.subheader("Hours studied over time")
fig = px.line(logs, x="date", y="hours_studied", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("All subjects comparison")
all_rows = []
for _, s in subjects.iterrows():
    s_logs = get_logs(int(s["id"]))
    total_hours = s_logs["hours_studied"].sum() if not s_logs.empty else 0
    all_rows.append({"subject": s["name"], "hours_logged": total_hours})

if all_rows:
    import pandas as pd
    comparison_df = pd.DataFrame(all_rows)
    fig2 = px.bar(comparison_df, x="subject", y="hours_logged")
    st.plotly_chart(fig2, use_container_width=True)
