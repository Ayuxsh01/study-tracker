"""
Populates the database with one fake user, two subjects, and ~2 weeks of
logs each, so you can see analytics run against real DB data.

Run it once; running it again will create a second duplicate user
(since email must be unique, it will fail the second time unless you
change the email below or clear the tables first).
"""

import random
from datetime import date, timedelta

from app.services.log_service import create_user, create_subject, add_log

EMAIL = "demo@example.com"


def seed():
    user_id = create_user(name="Demo User", email=EMAIL, password_hash="not_a_real_hash")
    print(f"Created user id={user_id}")

    subjects = [
        ("Math", 40),
        ("Physics", 30),
    ]

    today = date.today()

    for subject_name, total_hours in subjects:
        subject_id = create_subject(user_id, subject_name, total_hours)
        print(f"  Created subject '{subject_name}' id={subject_id}")

        for days_ago in range(13, -1, -1):  # last 14 days, oldest first
            log_date = today - timedelta(days=days_ago)

            # simulate skipping some days (80% chance of studying)
            if random.random() < 0.8:
                hours = round(random.uniform(0.5, 3.0), 1)
                add_log(subject_id, log_date, hours, notes="seeded")

    print("Done seeding.")


if __name__ == "__main__":
    seed()
