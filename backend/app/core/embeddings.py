from sentence_transformers import SentenceTransformer
from typing import List

_model = None
MODEL_NAME = "all-MiniLM-L6-v2"


def _load_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed(texts: List[str]) -> List[List[float]]:
    model = _load_model()
    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False
    )
    return vectors.tolist()
