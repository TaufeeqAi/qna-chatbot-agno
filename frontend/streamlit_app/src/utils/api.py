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

def ingest_document(
    token: str,
    source_type: str, # 'file', 'arxiv', 'url'
    source_identifier: str = None, # arXiv ID or URL
    file_widget = None # Streamlit UploadedFile object
):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"source_type": source_type}
    files_payload = None

    if source_type == "file":
        if file_widget:
            # Ensure filename is a string, not None
            filename = file_widget.name if file_widget.name else "uploaded_file.pdf"
            files_payload = {"file": (filename, file_widget.getvalue(), file_widget.type)}
        else:
            # This case should be prevented by UI logic
            raise ValueError("File widget is required for source_type 'file'.")
    elif source_type in ["arxiv", "url"]:
        if not source_identifier:
            # This case should be prevented by UI logic
            raise ValueError(f"Source identifier is required for source_type '{source_type}'.")
        params["source_identifier"] = source_identifier
    else:
        raise ValueError(f"Unsupported source_type: {source_type}")

    # The backend endpoint is /pdf_ingest/ (based on previous backend work)
    # It was changed from /pdf/ to /pdf_ingest/ and then the main endpoint is at its root
    # So, the URL should be f"{API_URL}/pdf_ingest/"
    ingest_url = f"{API_URL}/pdf_ingest/" 
    
    response = requests.post(ingest_url, headers=headers, params=params, files=files_payload)
    
    # It's good practice to check for specific success codes, e.g., 201 Created
    if response.status_code == 201:
        return response.json() # Contains {"detail": "..."}
    else:
        # Try to parse error detail from response, otherwise raise for status
        try:
            error_detail = response.json().get("detail", response.text)
        except requests.exceptions.JSONDecodeError:
            error_detail = response.text
        raise HTTPException(status_code=response.status_code, detail=error_detail)


class HTTPException(Exception):
    """Custom exception to mimic FastAPI's HTTPException for error handling."""
    def __init__(self, status_code: int, detail: str = None):
        self.status_code = status_code
        self.detail = detail
    
    def __str__(self):
        return f"HTTP {self.status_code}: {self.detail}"


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
