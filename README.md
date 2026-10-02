# Study Nook

A habit & syllabus tracker with a real analytics engine, built for students, self-learners, and exam-prep crammers who want more than a spreadsheet to track their study hours.

**Live app:** [study-nook.streamlit.app](https://study-nook.streamlit.app)

---

## Who is this for?

- **Students preparing for exams** who want to know, honestly, whether they're on pace to finish their syllabus before the exam date.
- **Self-learners** (online courses, language learning, upskilling) who want a streak-based habit tracker instead of a generic to-do list.
- **Anyone juggling multiple subjects/skills** who wants a single dashboard comparing progress across all of them, instead of scattered notes.

If you've ever asked yourself *"am I actually going to finish this syllabus in time?"* — that question is the entire reason this app's analytics engine exists.

---

## Features

### Account & data privacy
- Email/password signup and login, with passwords hashed using `bcrypt` (never stored or visible as plain text).
- Each user's subjects and logs are private to their account.

### Subject management
- Add subjects with an estimated total syllabus length (in hours).
- View all your subjects and how many hours you've logged against each at a glance.

### Daily logging
- Log study hours per subject, per day, with optional notes (e.g. "covered chapter 4 — integrals").
- Designed for a 30-second daily habit, not a heavyweight time-tracker.

### Analytics dashboard
The core feature — a small but real analytics engine (no external APIs, just math on your own data):

| Metric | What it tells you |
|---|---|
| **7-day rolling average** | Your average hours/day over the last week, including missed days as zero — an honest pace indicator, not a cherry-picked average. |
| **Current streak** | How many consecutive days in a row you've studied a subject, ending today. |
| **Completion rate** | What percentage of your estimated total syllabus hours you've covered so far. |
| **Projected finish date** | A linear projection — at your current weekly pace, the date you'll finish the subject — calculated as `days_remaining = hours_remaining / avg_daily_rate`. |

Plus:
- A line chart of hours studied over time per subject.
- A bar chart comparing total hours logged across all your subjects.

### Visual design
- A custom "pastel notebook" theme — soft lavender/peach palette, rounded cards, handwritten accents — built to feel personal and motivating rather than corporate.
- Consistent color-coding per subject across every chart and table.

---

## Tech stack

| Layer | Technology | Why |
|---|---|---|
| Frontend / dashboard | [Streamlit](https://streamlit.io) | Fast way to build an interactive data app in pure Python, no separate frontend needed. |
| Database | [PostgreSQL](https://www.postgresql.org) (hosted on [Neon](https://neon.tech)) | Reliable, persistent cloud storage that survives app restarts/redeploys. |
| ORM / DB access | [SQLAlchemy](https://www.sqlalchemy.org) + `psycopg` | Clean, parameterized SQL access from Python — no raw string concatenation (prevents SQL injection). |
| Analytics | [Pandas](https://pandas.pydata.org) | All streak/average/projection logic operates on Pandas DataFrames, fully unit-tested independent of the UI or database. |
| Charts | [Plotly](https://plotly.com/python/) | Interactive line/bar charts embedded directly in the dashboard. |
| Auth | `bcrypt` | Industry-standard one-way password hashing. |
| Hosting | [Streamlit Community Cloud](https://streamlit.io/cloud) | Free, zero-config deployment directly from this GitHub repo. |
| Testing | `pytest` | Automated tests for every analytics function. |

---

## Project structure

```
study-tracker/
├── app/
│   ├── main.py                 # Entry point: login/signup screen
│   ├── config.py               # Loads DATABASE_URL (local .env or Streamlit Cloud secrets)
│   │
│   ├── models/
│   │   ├── database.py         # Shared SQLAlchemy engine
│   │   └── schema.py           # Table definitions (users, subjects, logs)
│   │
│   ├── services/
│   │   ├── auth_service.py     # Signup/login, password hashing
│   │   ├── log_service.py      # All database reads/writes (the only file with SQL)
│   │   └── analytics.py        # Streaks, rolling average, completion %, projection — pure functions, DB-free
│   │
│   ├── pages/                  # Streamlit multipage app
│   │   ├── 1_Log_Hours.py
│   │   ├── 2_Dashboard.py
│   │   └── 3_Subjects.py
│   │
│   └── utils/
│       ├── auth_guard.py       # Redirects unauthenticated users
│       └── theme.py            # Injects the custom visual theme
│
├── scripts/
│   ├── seed_dummy_data.py      # Populates test data for local development
│   └── check_analytics.py      # Verifies the full DB → analytics pipeline
│
├── tests/
│   └── test_analytics.py       # Unit tests for every analytics function
│
├── .streamlit/config.toml      # Streamlit theme configuration
├── requirements.txt
└── README.md
```

---

## Running locally

1. **Clone the repo and create a virtual environment:**
   ```bash
   git clone https://github.com/Ayuxsh01/study-tracker.git
   cd study-tracker
   python -m venv .venv
   ./.venv/Scripts/python.exe -m pip install -r requirements.txt
   ```

2. **Set up a Postgres database** (e.g. a free [Neon](https://neon.tech) project), then create a `.env` file in the project root:
   ```
   DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
   ```

3. **Create the database tables:**
   ```bash
   ./.venv/Scripts/python.exe -m app.models.schema
   ```

4. **Run the app:**
   ```bash
   ./.venv/Scripts/python.exe -m streamlit run app/main.py
   ```

5. **Run the test suite:**
   ```bash
   ./.venv/Scripts/python.exe -m pytest tests/
   ```

---

## Design philosophy

Three strict layers, each only aware of the one below it:

```
Streamlit Dashboard  →  Services (plain Python)  →  Postgres Database
   (what you see)           (the logic)               (the storage)
```

The analytics engine in particular has **zero dependency on the database or UI** — it's pure functions over Pandas DataFrames, which is what makes it fully unit-testable and the most reusable part of the codebase.

---

## Roadmap

- [ ] Optional reminder system for missed study days
- [ ] Export logs to CSV
- [ ] Weekly/monthly summary emails
