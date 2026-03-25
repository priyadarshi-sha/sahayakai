import os
from PyPDF2 import PdfReader
from app.core.config import UPLOAD_DIR
from app.core.embeddings import embed
from app.core.vectorstore import vector_store


def chunk_text(text, chunk_size=900, overlap=200):
    """Split text into overlapping chunks"""
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
    """Extract text from all PDFs and ingest into Chroma DB"""
    try:
        vector_store.reset()
        all_chunks = []

        # Check if upload directory exists
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            print(f"Created upload directory: {UPLOAD_DIR}")
            return

        # Process each PDF file
        for file in os.listdir(UPLOAD_DIR):
            if not file.lower().endswith(".pdf"):
                continue

            try:
                pdf_path = os.path.join(UPLOAD_DIR, file)
                reader = PdfReader(pdf_path)
                
                for page_num, page in enumerate(reader.pages):
                    try:
                        text = page.extract_text()
                        if not text or not text.strip():
                            continue

                        # Clean up text
                        text = " ".join(text.split())
                        chunks = chunk_text(text)
                        all_chunks.extend(chunks)
                    except Exception as e:
                        print(f"Error extracting text from page {page_num} of {file}: {str(e)}")
                        continue
                
                print(f"Successfully processed {file}")
            except Exception as e:
                print(f"Error processing PDF {file}: {str(e)}")
                continue

        if not all_chunks:
            print("No text extracted from PDFs")
            return

        # Generate embeddings and add to Chroma DB
        try:
            embeddings = embed(all_chunks)
            vector_store.add(all_chunks, embeddings)
            print(f"Successfully ingested {len(all_chunks)} chunks into Chroma DB")
        except Exception as e:
            print(f"Error during embedding/ingestion: {str(e)}")
            raise

    except Exception as e:
        print(f"Error in ingest_all_pdfs: {str(e)}")
        raise
