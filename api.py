from fastapi import FastAPI
from db import update_job_status
from db import save_jobs
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
from resume_reader import extract_resume_text
import shutil
from db import init_db, save_jobs, update_job_status

init_db()
from graph import app as langgraph_app

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


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
def update_status_endpoint(job_title: str, employer_name: str, new_status: str):
    update_job_status(job_title, employer_name, new_status)
    return {"message": "Status updated", "job_title": job_title, "new_status": new_status}




@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    file_path = f"uploaded_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_text = extract_resume_text(file_path)

    with open("current_resume.txt", "w", encoding="utf-8") as f:
        f.write(resume_text)

    return {"message": "Resume uploaded successfully", "preview": resume_text[:200]}

@app.post("/update-status")
def update_status_endpoint(job_title: str, employer_name: str, new_status: str):
    update_job_status(job_title, employer_name, new_status)
    return {"message": "Status updated", "job_title": job_title, "new_status": new_status}