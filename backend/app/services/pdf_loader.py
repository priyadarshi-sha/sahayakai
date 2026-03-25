import os
from PyPDF2 import PdfReader
from app.core.config import UPLOAD_DIR
from app.core.embeddings import embed
from app.core.vectorstore import vector_store


def chunk_text(text, chunk_size=900, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if len(chunk.strip()) > 150:
            chunks.append(chunk)
        start = end - overlap
    return chunks


def ingest_all_pdfs():
    vector_store.reset()
    all_chunks = []

    for file in os.listdir(UPLOAD_DIR):
        if not file.lower().endswith(".pdf"):
            continue

        reader = PdfReader(os.path.join(UPLOAD_DIR, file))
        for page in reader.pages:
            text = page.extract_text()
            if not text:
                continue

            text = " ".join(text.split())
            all_chunks.extend(chunk_text(text))

    if not all_chunks:
        print("No text extracted from PDFs")
        return

    embeddings = embed(all_chunks)
    vector_store.add(all_chunks, embeddings)

    print(f"Ingested {len(all_chunks)} chunks")
