"""
Database read/write functions. This is the ONLY file that should contain
SQL. Everything else (analytics, dashboard) calls these functions instead
of talking to the database directly.
"""

import pandas as pd
from sqlalchemy import text
from app.models.database import engine


def create_user(name: str, email: str, password_hash: str) -> int:
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO users (name, email, password_hash)
                VALUES (:name, :email, :password_hash)
                RETURNING id
            """),
            {"name": name, "email": email, "password_hash": password_hash},
        )
        return result.scalar_one()


def get_user_by_email(email: str):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, name, email, password_hash FROM users WHERE email = :email"),
            {"email": email},
        )
        row = result.mappings().first()
        return dict(row) if row else None


def create_subject(user_id: int, name: str, total_syllabus_hours: float) -> int:
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO subjects (user_id, name, total_syllabus_hours)
                VALUES (:user_id, :name, :total_syllabus_hours)
                RETURNING id
            """),
            {"user_id": user_id, "name": name, "total_syllabus_hours": total_syllabus_hours},
        )
        return result.scalar_one()


def get_subjects(user_id: int) -> pd.DataFrame:
    with engine.connect() as conn:
        return pd.read_sql(
            text("SELECT id, name, total_syllabus_hours FROM subjects WHERE user_id = :user_id"),
            conn,
            params={"user_id": user_id},
        )


def add_log(subject_id: int, date, hours_studied: float, notes: str = None):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO logs (subject_id, date, hours_studied, notes)
                VALUES (:subject_id, :date, :hours_studied, :notes)
            """),
            {"subject_id": subject_id, "date": date, "hours_studied": hours_studied, "notes": notes},
        )


def get_logs(subject_id: int) -> pd.DataFrame:
    with engine.connect() as conn:
        return pd.read_sql(
            text("""
                SELECT date, hours_studied, notes
                FROM logs
                WHERE subject_id = :subject_id
                ORDER BY date
            """),
            conn,
            params={"subject_id": subject_id},
        )
