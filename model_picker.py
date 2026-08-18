import requests
import os

def get_available_model():
    api_key = os.environ.get("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}

    response = requests.get(url, headers=headers)
    data = response.json()

    excluded_keywords = ["whisper", "prompt-guard", "orpheus", "safeguard", "compound"]

    for model in data["data"]:
        model_id = model["id"]
        if not any(keyword in model_id for keyword in excluded_keywords):
            return model_id

    return "openai/gpt-oss-20b"