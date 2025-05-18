from fastapi import FastAPI
import os
from dotenv import load_dotenv
from common.logger import setup_logging
from common.exception import AppException
import logging

from fastapi.middleware.cors import CORSMiddleware
from .core.config import get_settings
from .api import auth, chat, pdf_ingest,memory


settings = get_settings()

# Initialize logging at startup
setup_logging(service_name="backend")
logger = logging.getLogger(__name__)


# Compute the .env path relative to this file’s location
base_dir = os.path.abspath(os.path.dirname(__file__))      # backend/app
project_root = os.path.dirname(os.path.dirname(base_dir))  # backend
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)

print("======Basic checks====")
print(f"Base dir path: {base_dir}")
print(f"Root path: {project_root}")
print(f".env path: {env_path}")
print("======================")

app = FastAPI(title="Research Chatbot API")


@app.on_event("startup")
def on_startup():
    logger.info("Application startup: FastAPI is starting up.")

# CORS (if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(memory.router)
app.include_router(pdf_ingest.router)

@app.get("/")
def root():
    try:
        logger.info("Received request at root endpoint.")
        return {"message": "API is up and running!"}
    except Exception as e:
        # Wrap unexpected errors in CustomException
        raise AppException("Failed to handle root endpoint", e)

