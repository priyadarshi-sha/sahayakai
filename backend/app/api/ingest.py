from fastapi import APIRouter, HTTPException
from app.services.pdf_loader import ingest_all_pdfs

router = APIRouter(prefix="/ingest", tags=["Ingest"])

@router.post("/")
def ingest():
    try:
        ingest_all_pdfs()
        return {
            "status": "success",
            "message": "PDFs ingested successfully into Chroma DB"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error ingesting PDFs: {str(e)}"
        )
