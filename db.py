import sqlite3

def init_db():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
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
            INSERT INTO jobs (job_title, employer_name, score, reason, status)
            VALUES (?, ?, ?, ?, ?)
        """, (job["job_title"], job["employer_name"], job["score"], job["reason"], job["status"]))

    conn.commit()
    conn.close()