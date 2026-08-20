import sqlite3
conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()
cursor.execute("SELECT unique_key, user_id, job_title, employer_name, status FROM jobs")
for row in cursor.fetchall():
    print(row)
conn.close()