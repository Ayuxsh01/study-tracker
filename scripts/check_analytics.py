"""
Pulls real data from the database and runs the analytics functions on it.
This proves the whole pipeline works: DB -> log_service -> analytics.
"""

from app.services.log_service import get_subjects, get_logs
from app.services.analytics import (
    rolling_7day_average,
    current_streak,
    completion_rate,
    project_completion_date,
)

USER_ID = 1

subjects = get_subjects(USER_ID)

for _, subject in subjects.iterrows():
    logs = get_logs(subject["id"])

    print(f"\n=== {subject['name']} (total syllabus: {subject['total_syllabus_hours']}h) ===")
    print(f"Logs recorded: {len(logs)}")
    print(f"7-day rolling average: {rolling_7day_average(logs)} hrs/day")
    print(f"Current streak: {current_streak(logs)} days")
    print(f"Completion rate: {completion_rate(logs, subject['total_syllabus_hours'])}%")

    projected = project_completion_date(logs, subject["total_syllabus_hours"])
    print(f"Projected finish date: {projected.date() if projected is not None else 'N/A'}")
