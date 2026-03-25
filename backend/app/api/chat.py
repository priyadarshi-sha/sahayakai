from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chat_service import chat

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    user_id: str
    question: str

@router.post("/")
def ask(request: ChatRequest):
    try:
        if not request.user_id or not request.question:
            raise HTTPException(
                status_code=400,
                detail="user_id and question are required"
            )
        
        response = chat(request.user_id, request.question)
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )
