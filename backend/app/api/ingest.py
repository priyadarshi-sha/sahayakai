from fastapi import APIRouter
from app.services.pdf_loader import ingest_all_pdfs

router = APIRouter(prefix="/ingest", tags=["Ingest"])

@router.post("/")
def ingest():
    ingest_all_pdfs()
    return {"status": "PDFs ingested successfully"}
