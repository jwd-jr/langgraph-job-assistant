import os
import requests
import json
from dotenv import load_dotenv
from groq import Groq
from state import JobSearchState

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")

DUMMY_RESUME = """
Name: Alex Kim
Title: Junior Python Developer

Skills: Python, SQL, Pandas, REST APIs, Git, basic Flask

Experience:
- 1 year as a Data Analyst Intern — wrote Python scripts to clean data, built small dashboards
- 6 months freelance — built a small Flask API for a client

Education: BS in Computer Science
"""


def load_resume_node(state: JobSearchState) -> JobSearchState:
    return {"resume_text": DUMMY_RESUME}


def search_jobs_node(state: JobSearchState) -> JobSearchState:
    query = state["query"]
    retry_count = state.get("retry_count", 0)

    if retry_count > 0:
        query = "python developer"

    url = "https://jsearch.p.rapidapi.com/search-v2"
    querystring = {"query": query, "page": "1", "num_pages": "1", "country": "us"}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring, timeout=15)
    data = response.json()
    jobs = data["data"]["jobs"]

    return {"jobs": jobs, "retry_count": retry_count + 1}


from db import get_preference_text

def score_jobs_node(state: JobSearchState) -> JobSearchState:
    scored_jobs = []
    preference_text = get_preference_text()

    for job in state["jobs"][:3]:
        prompt = f"""
Resume:
{state['resume_text']}

{preference_text}

Job:
Title: {job['job_title']}
Company: {job['employer_name']}

Give a match score from 1-10 and one short reason.
Consider the user's past applied/rejected pattern above when scoring, not just resume fit.
Reply with ONLY valid JSON, exactly in this format, nothing else:
{{"score": 7, "reason": "short sentence here"}}
"""
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        result_text = response.choices[0].message.content

        try:
            parsed = json.loads(result_text)
        except json.JSONDecodeError:
            parsed = {"score": None, "reason": "Could not parse LLM response"}

        job_with_score = job.copy()
        job_with_score["score"] = parsed["score"]
        job_with_score["reason"] = parsed["reason"]
        scored_jobs.append(job_with_score)

    return {"scored_jobs": scored_jobs}

def should_retry(state: JobSearchState) -> str:
    scores = [job["score"] for job in state["scored_jobs"] if job["score"] is not None]
    avg_score = sum(scores) / len(scores) if scores else 0

    if avg_score < 5 and state["retry_count"] < 2:
        return "retry"
    return "done"


def track_jobs_node(state: JobSearchState) -> JobSearchState:
    tracked_jobs = []
    for job in state["scored_jobs"]:
        job_with_status = job.copy()
        job_with_status["status"] = "not_applied"
        tracked_jobs.append(job_with_status)

    return {"tracked_jobs": tracked_jobs}




def load_resume_node(state: JobSearchState) -> JobSearchState:
    if os.path.exists("current_resume.txt"):
        with open("current_resume.txt", "r", encoding="utf-8") as f:
            resume_text = f.read()
    else:
        resume_text = DUMMY_RESUME

    return {"resume_text": resume_text}