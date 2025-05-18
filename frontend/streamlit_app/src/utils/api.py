import os
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")

def login(email: str, password: str) -> str:
    resp = requests.post(f"{API_URL}/auth/login", data={"username": email, "password": password})
    if resp.status_code == 200:
        return resp.json()["access_token"]
    return None

def get_current_user(token: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{API_URL}/auth/me", headers=headers)
    resp.raise_for_status()
    return resp.json()

def upload_pdf(file, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": (file.name, file.getvalue(), file.type)}
    return requests.post(f"{API_URL}/pdf/", headers=headers, files=files)

def chat(message: str, mode: str, token: str) -> dict:
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"message": message, "mode": mode}
    resp = requests.post(f"{API_URL}/chat/", json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()

def get_progress(token: str) -> list:
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{API_URL}/profile/progress", headers=headers)
    resp.raise_for_status()
    return resp.json()
