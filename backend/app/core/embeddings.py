import os
from sentence_transformers import SentenceTransformer
from typing import List
from app.core.config import EMBEDDINGS_MODEL_PATH, EMBEDDINGS_MODEL_NAME, MODELS_DIR

_model = None


def _ensure_model_cache_dir():
    """Ensure model cache directory exists"""
    os.makedirs(EMBEDDINGS_MODEL_PATH, exist_ok=True)
    os.makedirs(MODELS_DIR, exist_ok=True)


def _load_model():
    """Load model from local cache or download it"""
    global _model
    if _model is None:
        print(f"📦 Loading embedding model: {EMBEDDINGS_MODEL_NAME}")
        print(f"📁 Cache directory: {EMBEDDINGS_MODEL_PATH}")
        
        _ensure_model_cache_dir()
        
        # Load or download model - will cache locally automatically
        _model = SentenceTransformer(
            EMBEDDINGS_MODEL_NAME,
            cache_folder=EMBEDDINGS_MODEL_PATH
        )
        
        print(f"✅ Embedding model loaded successfully")
        print(f"📊 Model dimension: {_model.get_sentence_embedding_dimension()}")
    
    return _model


def embed(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for given texts using cached model"""
    model = _load_model()
    
    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False
    )
    
    return vectors.tolist()


def get_embedding_dimension():
    """Get the dimension of embeddings (useful for Chroma DB configuration)"""
    model = _load_model()
    return model.get_sentence_embedding_dimension()

