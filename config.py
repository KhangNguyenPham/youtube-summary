import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "False") == "True"
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "vi")
    TRANSCRIPT_TIMEOUT = os.getenv("TRANSCRIPT_TIMEOUT", 5)
    GEMINI_TIMEOUT = os.getenv("GEMINI_TIMEOUT", 15)
