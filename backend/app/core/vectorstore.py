import chromadb
import os
from app.core.config import CHROMA_DB_PATH


class VectorStore:
    def __init__(self):
        # Ensure the Chroma DB directory exists
        os.makedirs(CHROMA_DB_PATH, exist_ok=True)
        
        # Create a persistent Chroma client
        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        
        # Get or create a collection
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )

    def reset(self):
        """Delete and recreate the collection"""
        try:
            self.client.delete_collection(name="documents")
        except Exception:
            pass
        
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )

    def add(self, texts, embeddings):
        """Add texts and embeddings to the collection"""
        if not texts or not embeddings:
            return

        # Generate unique IDs for each text
        ids = [f"doc_{i}_{hash(text) % 10**8}" for i, text in enumerate(texts)]
        
        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=[{"source": "pdf"} for _ in texts]
        )

    def search(self, query_vector, k=5):
        """Search for similar texts using query embedding"""
        if self.collection.count() == 0:
            return []

        # Query the collection
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=k
        )

        # Extract documents from results
        if results and results.get("documents") and len(results["documents"]) > 0:
            return results["documents"][0]  # Return the list of documents
        
        return []


# Initialize global vector store instance
vector_store = VectorStore()
