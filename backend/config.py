import os
from dotenv import load_dotenv

# Load .env at import time so Config picks it up
load_dotenv()

class Config:
    SECRET_KEY            = os.getenv("SECRET_KEY", "fallback_value")
    UPLOAD_FOLDER         = os.getenv("UPLOAD_FOLDER", "./uploads")
    CELERY_BROKER_URL     = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    OPENAI_API_KEY        = os.getenv("OPENAI_API_KEY", "")
    HF_TOKEN              = os.getenv("HF_TOKEN", "")