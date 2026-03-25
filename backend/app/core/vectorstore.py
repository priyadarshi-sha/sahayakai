import faiss
import numpy as np


class VectorStore:
    def __init__(self, dim=384):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)
        self.texts = []

    def reset(self):
        self.index.reset()
        self.texts = []

    def add(self, texts, embeddings):
        if not texts or not embeddings:
            return

        vectors = np.array(embeddings).astype("float32")

        # 🔥 Normalize for cosine similarity
        faiss.normalize_L2(vectors)

        self.index.add(vectors)
        self.texts.extend(texts)

    def search(self, query_vector, k=5):
        if self.index.ntotal == 0:
            return []

        q = np.array([query_vector]).astype("float32")

        # 🔥 Normalize query too
        faiss.normalize_L2(q)

        scores, indices = self.index.search(q, k)

        results = []
        for i in indices[0]:
            if 0 <= i < len(self.texts):
                results.append(self.texts[i])

        return results


vector_store = VectorStore()
