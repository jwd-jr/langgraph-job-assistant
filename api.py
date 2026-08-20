import os
import shutil
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import FastAPI, UploadFile, File,Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from db import create_user, update_job_status, get_user_by_email, save_jobs, init_db, pwd_context
from resume_reader import extract_resume_text
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
from graph import app as langgraph_app

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {
        "user_id": payload["user_id"],
        "email": payload["email"]
    }


class SignupRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@app.get("/search-jobs")
def search_jobs(current_user: dict = Depends(get_current_user)):
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


@app.post("/signup")
def signup(request: SignupRequest):
    success = create_user(request.email, request.password)

    if not success:
        return {"error": "Email already registered"}

    return {"message": "Signup successful"}


@app.post("/login")
def login(request: LoginRequest):
    user = get_user_by_email(request.email)

    if user is None:
        return {"error": "Invalid email or password"}

    if not pwd_context.verify(request.password, user["hashed_password"]):
        return {"error": "Invalid email or password"}

    payload = {
        "user_id": user["id"],
        "email": user["email"],
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {"access_token": token}