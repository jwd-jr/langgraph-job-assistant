from fastapi import FastAPI
from db import update_job_status
from db import save_jobs

from graph import app as langgraph_app

app = FastAPI()

@app.get("/search-jobs")
@app.get("/search-jobs")
def search_jobs():
    initial_state = {
        "query": "python developer jobs in chicago",
        "jobs": [],
        "resume_text": "",
        "scored_jobs": [],
        "retry_count": 0,
        "tracked_jobs": []
    }

    result = langgraph_app.invoke(initial_state)
    save_jobs(result["tracked_jobs"])

    return {"tracked_jobs": result["tracked_jobs"]}


@app.post("/update-status")
def update_status_endpoint(job_id: str, new_status: str):
    update_job_status(job_id, new_status)
    return {"message": "Status updated", "job_id": job_id, "new_status": new_status}