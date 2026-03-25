from fastapi import APIRouter
from app.services.youtube_service import get_youtube_videos

router = APIRouter(prefix="/youtube", tags=["YouTube"])

@router.get("/")
def search(query: str):
    return get_youtube_videos(query)
