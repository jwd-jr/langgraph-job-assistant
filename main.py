from graph import app

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