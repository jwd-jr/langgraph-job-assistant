import sqlite3

def init_db():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            job_title TEXT,
            employer_name TEXT,
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
        cursor.execute("""
            INSERT INTO jobs (job_id, job_title, employer_name, score, reason, status)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(job_id) DO UPDATE SET
                score = excluded.score,
                reason = excluded.reason,
                status = excluded.status
        """, (job["job_id"], job["job_title"], job["employer_name"], job["score"], job["reason"], job["status"]))

    conn.commit()
    conn.close()

def update_job_status(job_title, new_status):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE jobs
        SET status = ?
        WHERE job_title = ?
    """, (new_status, job_title))

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