import requests
import os
from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")

url = "https://jsearch.p.rapidapi.com/search-v2"
querystring = {"query": "python developer jobs in chicago", "page": "1", "num_pages": "1", "country": "us"}
headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring, timeout=15)
data = response.json()
job = data["data"]["jobs"][0]

print(list(job.keys()))