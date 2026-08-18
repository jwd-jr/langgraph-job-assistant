import sqlite3
import hashlib

def make_unique_key(job_title, employer_name):
    combined = f"{job_title.lower().strip()}_{employer_name.lower().strip()}"
    return hashlib.md5(combined.encode()).hexdigest()


def init_db():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            unique_key TEXT PRIMARY KEY,
            job_id TEXT,
            job_title TEXT,
            employer_name TEXT,
            job_location TEXT,
            job_posted_at TEXT,
            score INTEGER,
            reason TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_jobs(tracked_jobs):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    for job in tracked_jobs:
        unique_key = make_unique_key(job["job_title"], job["employer_name"])

        cursor.execute("""
            INSERT INTO jobs (unique_key, job_id, job_title, employer_name, job_location, job_posted_at, score, reason, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(unique_key) DO UPDATE SET
                job_id = excluded.job_id,
                job_location = excluded.job_location,
                job_posted_at = excluded.job_posted_at,
                score = excluded.score,
                reason = excluded.reason,
                status = excluded.status
        """, (unique_key, job["job_id"], job["job_title"], job["employer_name"], job.get("job_location"), job.get("job_posted_at"), job["score"], job["reason"], job["status"]))

    conn.commit()
    conn.close()


def update_job_status(job_title, employer_name, new_status):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    unique_key = make_unique_key(job_title, employer_name)

    cursor.execute("""
        UPDATE jobs
        SET status = ?
        WHERE unique_key = ?
    """, (new_status, unique_key))

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