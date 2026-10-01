from sqlalchemy import text
from app.models.database import engine

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS subjects (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    total_syllabus_hours NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    hours_studied NUMERIC NOT NULL,
    notes TEXT
);
"""


def init_db():
    with engine.begin() as conn:
        conn.execute(text(SCHEMA_SQL))


if __name__ == "__main__":
    init_db()
    print("Database tables created.")
