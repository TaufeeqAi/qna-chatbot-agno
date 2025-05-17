from fastapi import FastAPI
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from common.logger import setup_logging
from common.exception import AppException
import logging


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

app = FastAPI()


@app.on_event("startup")
def on_startup():
    logger.info("Application startup: FastAPI is starting up.")

@app.get("/")
def root():
    try:
        logger.info("Received request at root endpoint.")
        return {"message": "Hello, World!"}
    except Exception as e:
        # Wrap unexpected errors in CustomException
        raise AppException("Failed to handle root endpoint", e)

@app.get("/error-test")
def error_test():
    try:
        # Simulate an error
        1 / 0
    except Exception as e:
        logger.error(f"Division by zero occurred: {e}",exc_info=True)
        raise AppException("Division by zero occurred", e)


print("DB UR:", os.getenv("DATABASE_URL"))
