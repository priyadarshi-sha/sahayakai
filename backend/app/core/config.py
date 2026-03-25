import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")

UPLOAD_DIR = os.path.join(STORAGE_DIR, "to_be_uploaded")
NOTEBOOK_DIR = os.path.join(STORAGE_DIR, "notebooks")
CHROMA_DB_PATH = os.path.join(STORAGE_DIR, "vectordb", "chroma")

# Model caching paths
MODELS_DIR = os.path.join(STORAGE_DIR, "models")
EMBEDDINGS_MODEL_PATH = os.path.join(MODELS_DIR, "embeddings")
EMBEDDINGS_MODEL_NAME = "all-MiniLM-L6-v2"

# HuggingFace settings
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
TRANSFORMERS_CACHE = EMBEDDINGS_MODEL_PATH
os.environ["TRANSFORMERS_CACHE"] = TRANSFORMERS_CACHE
os.environ["HF_HOME"] = MODELS_DIR

# Ollama settings (for container)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5")

# YouTube
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Other
HF_LLM_MODEL = "google/flan-t5-base"

