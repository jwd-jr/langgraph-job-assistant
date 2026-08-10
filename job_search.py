import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")


url = "https://jsearch.p.rapidapi.com/search-v2"

querystring = {"query": "python developer jobs in chicago", "page": "1", "num_pages": "1", "country": "us"}

headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

data = response.json()

jobs = data["data"]["jobs"]

for job in jobs:
    title = job["job_title"]
    company = job["employer_name"]
    link = job.get("job_apply_link", "No link")
    print(f"{title} at {company}")
    print(link)
    print("---")