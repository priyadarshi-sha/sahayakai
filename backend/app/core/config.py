import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")

UPLOAD_DIR = os.path.join(STORAGE_DIR, "to_be_uploaded")
NOTEBOOK_DIR = os.path.join(STORAGE_DIR, "notebooks")

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

HF_LLM_MODEL = "google/flan-t5-base"

