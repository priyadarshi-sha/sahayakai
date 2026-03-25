import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ FIX: Set UTF-8 encoding for Windows console support
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

from app.api import chat, ingest, notebook, youtube

app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(chat.router, prefix="/api")
app.include_router(ingest.router, prefix="/api")
app.include_router(notebook.router, prefix="/api")
app.include_router(youtube.router, prefix="/api")
