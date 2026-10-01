"""
Analytics functions. Each function takes a pandas DataFrame of logs
(columns: date, hours_studied) for a single subject and returns a metric.
This file has NO database code and NO Streamlit code on purpose —
it's pure logic, so it's easy to test and easy to explain.
"""

import pandas as pd


def rolling_7day_average(logs: pd.DataFrame) -> float:
    """Average hours/day over the last 7 calendar days (missing days count as 0)."""
    if logs.empty:
        return 0.0

    logs = logs.copy()
    logs["date"] = pd.to_datetime(logs["date"])

    today = logs["date"].max()
    window_start = today - pd.Timedelta(days=6)

    mask = (logs["date"] >= window_start) & (logs["date"] <= today)
    total_hours = logs.loc[mask, "hours_studied"].sum()

    return round(total_hours / 7, 2)


def current_streak(logs: pd.DataFrame) -> int:
    """Count consecutive days studied, ending at the most recent log date."""
    if logs.empty:
        return 0

    studied_days = pd.to_datetime(logs["date"]).dt.normalize().unique()
    studied_days = set(studied_days)

    streak = 0
    day = max(studied_days)
    while day in studied_days:
        streak += 1
        day -= pd.Timedelta(days=1)

    return streak


def completion_rate(logs: pd.DataFrame, total_syllabus_hours: float) -> float:
    """Percentage of total syllabus hours completed so far."""
    if total_syllabus_hours <= 0:
        return 0.0

    hours_done = logs["hours_studied"].sum() if not logs.empty else 0.0
    rate = (hours_done / total_syllabus_hours) * 100
    return round(min(rate, 100.0), 2)


def project_completion_date(logs: pd.DataFrame, total_syllabus_hours: float):
    """
    Linear projection: at the current daily pace, when will the subject be done?
    Returns a pandas Timestamp, or None if it can't be estimated
    (no logs yet, or average pace is 0 — can't divide by zero).
    """
    if logs.empty:
        return None

    hours_done = logs["hours_studied"].sum()
    hours_remaining = total_syllabus_hours - hours_done

    if hours_remaining <= 0:
        return pd.to_datetime(logs["date"]).max()  # already done

    avg_daily_rate = rolling_7day_average(logs)
    if avg_daily_rate <= 0:
        return None  # no recent pace to project from

    days_remaining = hours_remaining / avg_daily_rate
    last_date = pd.to_datetime(logs["date"]).max()

    return last_date + pd.Timedelta(days=days_remaining)
