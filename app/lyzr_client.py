import requests
import json
import re

LYZR_API_URL = "https://agent-prod.studio.lyzr.ai/v3/inference/chat/"
LYZR_API_KEY = "sk-default-H4xWX7uC1GYpMD9Nv8PTExKCeQ3wt7GP"  # Replace with your key

def extract_skills_from_resume_via_lyzr(user_id, agent_id, session_id, resume_text):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": LYZR_API_KEY,
    }
    payload = {
        "user_id": "rudrampanchal@gmail.com",
        "agent_id": "684bbacbe5203d8a7b64bdc2",
        "session_id": "684bbacbe5203d8a7b64bdc2-6kt7ackzafp",
        "message": resume_text
    }

    response = requests.post(LYZR_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()

    raw_response = data.get("response", "")

    # Remove markdown code block wrappers like ```json ... ```
    cleaned = re.sub(r"```json|```", "", raw_response).strip()

    try:
        # Parse JSON skills list from cleaned string
        skills_list = json.loads(cleaned)
    except json.JSONDecodeError:
        # If JSON parse fails, fallback to splitting by commas
        skills_list = [s.strip() for s in cleaned.split(",")]

    # Clean each skill string (remove quotes and extra spaces)
    skills = [s.strip().strip('"').strip("'") for s in skills_list if s.strip()]

    return skills
