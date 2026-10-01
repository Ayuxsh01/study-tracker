import pandas as pd
from app.services.analytics import (
    rolling_7day_average,
    current_streak,
    completion_rate,
    project_completion_date,
)


def make_logs(rows):
    """Helper: rows is a list of (date_str, hours) tuples."""
    return pd.DataFrame(rows, columns=["date", "hours_studied"])


def test_rolling_7day_average():
    logs = make_logs([
        ("2026-09-26", 2),
        ("2026-09-27", 1),
        ("2026-09-28", 0),
        ("2026-09-29", 3),
        ("2026-09-30", 2),
        ("2026-10-01", 1),
        ("2026-10-02", 4),
    ])
    assert rolling_7day_average(logs) == round((2 + 1 + 0 + 3 + 2 + 1 + 4) / 7, 2)


def test_current_streak_breaks_on_gap():
    logs = make_logs([
        ("2026-09-28", 1),
        ("2026-09-30", 1),  # gap on the 29th
        ("2026-10-01", 1),
        ("2026-10-02", 1),
    ])
    assert current_streak(logs) == 3  # 30th, 1st, 2nd


def test_current_streak_empty():
    assert current_streak(make_logs([])) == 0


def test_completion_rate_caps_at_100():
    logs = make_logs([("2026-10-01", 50)])
    assert completion_rate(logs, total_syllabus_hours=20) == 100.0


def test_completion_rate_normal():
    logs = make_logs([("2026-10-01", 5)])
    assert completion_rate(logs, total_syllabus_hours=20) == 25.0


def test_projection_returns_none_without_logs():
    assert project_completion_date(make_logs([]), total_syllabus_hours=20) is None


def test_projection_future_date():
    logs = make_logs([
        ("2026-09-26", 2),
        ("2026-09-27", 2),
        ("2026-09-28", 2),
        ("2026-09-29", 2),
        ("2026-09-30", 2),
        ("2026-10-01", 2),
        ("2026-10-02", 2),
    ])
    # avg daily rate = 2 hrs/day, 14 hrs done, say 28 total -> 14 remaining -> 7 more days
    result = project_completion_date(logs, total_syllabus_hours=28)
    assert result is not None
    assert result > pd.Timestamp("2026-10-02")
