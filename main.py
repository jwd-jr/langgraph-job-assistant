from graph import app
from db import init_db, save_jobs, update_job_status


init_db()

result = app.invoke({
    "query": "python developer jobs in chicago",
    "jobs": [],
    "resume_text": "",
    "scored_jobs": [],
    "retry_count": 0,
    "tracked_jobs": []
})

print("Retries used:", result["retry_count"])

for job in result["tracked_jobs"]:
    print(job["job_title"], "-", job["employer_name"])
    print("Score:", job["score"])
    print("Reason:", job["reason"])
    print("Status:", job["status"])
    print("---")

save_jobs(result["tracked_jobs"])
print("Jobs saved to database.")


def update_status(tracked_jobs, job_title, new_status):
    for job in tracked_jobs:
        if job["job_title"] == job_title:
            job["status"] = new_status
            return tracked_jobs
    print("Job not found:", job_title)
    return tracked_jobs


updated_jobs = update_status(result["tracked_jobs"], "Software Engineer(Python)", "applied")
update_job_status("Software Engineer(Python)", "applied")
update_status(result["tracked_jobs"], "Python Developer Pandas", "rejected")
update_job_status("Python Developer Pandas", "rejected")
for job in updated_jobs:
    print(job["job_title"], "-", job["status"])