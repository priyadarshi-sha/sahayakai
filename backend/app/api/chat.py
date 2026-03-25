from fastapi import APIRouter
from pydantic import BaseModel
from app.services.chat_service import chat

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    user_id: str
    question: str

@router.post("/")
def ask(request: ChatRequest):
    return chat(request.user_id, request.question)
