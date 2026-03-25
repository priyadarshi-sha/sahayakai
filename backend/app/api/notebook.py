from fastapi import APIRouter, HTTPException
import os, json
from app.core.config import NOTEBOOK_DIR

router = APIRouter(prefix="/notebook", tags=["Notebook"])

@router.get("/{user_id}")
def get_notebook(user_id: str):
    path = os.path.join(NOTEBOOK_DIR, user_id, "chat.json")
    if not os.path.exists(path):
        raise HTTPException(404, "No notebook found")

    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]
