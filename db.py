import sqlite3
import hashlib
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def make_unique_key(job_title, employer_name):
    combined = f"{job_title.lower().strip()}_{employer_name.lower().strip()}"
    return hashlib.md5(combined.encode()).hexdigest()


def init_db():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        unique_key TEXT,
        user_id INTEGER NOT NULL,
        job_id TEXT,
        job_title TEXT,
        employer_name TEXT,
        job_location TEXT,
        job_posted_at TEXT,
        score INTEGER,
        reason TEXT,
        status TEXT,
        PRIMARY KEY (unique_key, user_id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def create_user(email, password):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    hashed_password = pwd_context.hash(password)
    created_at = datetime.now().isoformat()

    try:
        cursor.execute("""
            INSERT INTO users (email, hashed_password, created_at)
            VALUES (?, ?, ?)
        """, (email, hashed_password, created_at))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        # this happens if the email already exists (UNIQUE constraint)
        success = False

    conn.close()
    return success

def get_user_by_email(email):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, email, hashed_password FROM users WHERE email = ?
    """, (email,))
    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "email": row[1],
        "hashed_password": row[2]
    }

def save_jobs(tracked_jobs, user_id):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    for job in tracked_jobs:
        unique_key = make_unique_key(job["job_title"], job["employer_name"])

        cursor.execute("""
            INSERT INTO jobs (unique_key, user_id, job_id, job_title, employer_name, job_location, job_posted_at, score, reason, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(unique_key, user_id) DO UPDATE SET
                job_id = excluded.job_id,
                job_location = excluded.job_location,
                job_posted_at = excluded.job_posted_at,
                score = excluded.score,
                reason = excluded.reason,
                status = excluded.status
        """, (unique_key, user_id, job["job_id"], job["job_title"], job["employer_name"], job.get("job_location"), job.get("job_posted_at"), job["score"], job["reason"], job["status"]))

    conn.commit()
    conn.close()


def update_job_status(job_title, employer_name, new_status, user_id):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    unique_key = make_unique_key(job_title, employer_name)

    cursor.execute("""
        UPDATE jobs
        SET status = ?
        WHERE unique_key = ? AND user_id = ?
    """, (new_status, unique_key, user_id))

    conn.commit()
    conn.close()

def get_preference_summary():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("SELECT job_title, employer_name FROM jobs WHERE status = 'applied'")
    applied = cursor.fetchall()

    cursor.execute("SELECT job_title, employer_name FROM jobs WHERE status = 'rejected'")
    rejected = cursor.fetchall()

    conn.close()

    return {"applied": applied, "rejected": rejected}


def get_preference_text():
    prefs = get_preference_summary()

    applied_titles = [f"{title} at {company}" for title, company in prefs["applied"]]
    rejected_titles = [f"{title} at {company}" for title, company in prefs["rejected"]]

    text = "User's past behavior:\n"
    text += "Applied to: " + ", ".join(applied_titles) if applied_titles else "Applied to: none yet"
    text += "\nRejected: " + ", ".join(rejected_titles) if rejected_titles else "\nRejected: none yet"

    return text

def get_jobs_for_user(user_id):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT unique_key, job_id, job_title, employer_name, job_location, job_posted_at, score, reason, status
        FROM jobs WHERE user_id = ?
    """, (user_id,))
    rows = cursor.fetchall()

    conn.close()
    return rows