#!/usr/bin/env python3
"""
Model Initialization Script
Downloads and caches embedding and LLM models locally for offline use
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import (
    EMBEDDINGS_MODEL_PATH, 
    EMBEDDINGS_MODEL_NAME,
    MODELS_DIR,
    OLLAMA_URL,
    OLLAMA_MODEL
)
from app.core.embeddings import _load_model, get_embedding_dimension
import requests


def download_embedding_model():
    """Download and cache the embedding model locally"""
    print("\n" + "="*60)
    print("📥 DOWNLOADING EMBEDDING MODEL")
    print("="*60)
    
    print(f"\n📦 Model: {EMBEDDINGS_MODEL_NAME}")
    print(f"📁 Cache directory: {EMBEDDINGS_MODEL_PATH}")
    
    try:
        print("\n⏳ Downloading model (this may take a few minutes on first run)...")
        model = _load_model()
        
        print(f"\n✅ Model downloaded successfully!")
        dim = get_embedding_dimension()
        print(f"📊 Embedding dimension: {dim}")
        print(f"📍 Model cached at: {EMBEDDINGS_MODEL_PATH}")
        
        return True
    except Exception as e:
        print(f"\n❌ Error downloading embedding model: {str(e)}")
        return False


def verify_ollama_connection():
    """Verify Ollama is running and check available models"""
    print("\n" + "="*60)
    print("🔍 CHECKING OLLAMA CONNECTION")
    print("="*60)
    
    print(f"\n🌐 Ollama URL: {OLLAMA_URL}")
    print(f"🤖 Ollama Model: {OLLAMA_MODEL}")
    
    try:
        # Check if Ollama is running
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        
        if response.status_code == 200:
            print(f"\n✅ Ollama is running!")
            
            try:
                models = response.json().get("models", [])
                if models:
                    print(f"\n📋 Available models:")
                    for model in models:
                        name = model.get("name", "Unknown")
                        size = model.get("size", "Unknown")
                        print(f"   • {name} ({format_size(size)})")
                    
                    # Check if our model is available
                    model_names = [m.get("name", "") for m in models]
                    if any(OLLAMA_MODEL in name for name in model_names):
                        print(f"\n✅ Model '{OLLAMA_MODEL}' is available!")
                    else:
                        print(f"\n⚠️  Model '{OLLAMA_MODEL}' not found. Available models above.")
                        print(f"    To download: ollama pull {OLLAMA_MODEL}")
                else:
                    print(f"\n⚠️  No models found. Download one using:")
                    print(f"    ollama pull {OLLAMA_MODEL}")
            except Exception as e:
                print(f"\n⚠️  Could not parse model list: {str(e)}")
        else:
            print(f"\n❌ Ollama returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Cannot connect to Ollama at {OLLAMA_URL}")
        print(f"   Make sure Ollama is running!")
        print(f"   For Docker: docker run -d -p 11434:11434 ollama/ollama")
        return False
    except requests.exceptions.Timeout:
        print(f"\n❌ Connection to Ollama timed out")
        return False
    except Exception as e:
        print(f"\n❌ Error checking Ollama: {str(e)}")
        return False
    
    return True


def format_size(size_bytes):
    """Format bytes to human readable format"""
    if isinstance(size_bytes, str):
        return size_bytes
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f}TB"


def create_env_template():
    """Create a template .env file"""
    print("\n" + "="*60)
    print("📝 ENVIRONMENT CONFIGURATION")
    print("="*60)
    
    env_file = Path(__file__).parent / ".env"
    
    if env_file.exists():
        print(f"\n✅ .env file already exists at: {env_file}")
    else:
        template = """# Ollama Configuration (for container-based Ollama)
# OLLAMA_URL=http://ollama:11434  # Use this if Ollama is in Docker network
OLLAMA_URL=http://localhost:11434  # Use this if Ollama is on host machine
OLLAMA_MODEL=qwen2.5

# HuggingFace Token (optional, for private models)
# HF_API_TOKEN=your_token_here

# YouTube API Key (optional, for video search)
# YOUTUBE_API_KEY=your_key_here
"""
        
        try:
            with open(env_file, 'w') as f:
                f.write(template)
            print(f"\n✅ Created template .env file at: {env_file}")
            print(f"📝 Edit it to configure your settings")
        except Exception as e:
            print(f"\n⚠️  Could not create .env file: {str(e)}")


def print_summary(embedding_ok, ollama_ok):
    """Print setup summary"""
    print("\n" + "="*60)
    print("📊 SETUP SUMMARY")
    print("="*60)
    
    print(f"\n✅ Embedding Model: {'Ready' if embedding_ok else 'Failed'}")
    print(f"✅ Ollama Connection: {'Connected' if ollama_ok else 'Not Connected'}")
    
    print(f"\n📁 Storage Directories:")
    print(f"   • Models: {MODELS_DIR}")
    print(f"   • Embeddings Cache: {EMBEDDINGS_MODEL_PATH}")
    
    print(f"\n🚀 Next Steps:")
    if embedding_ok:
        print(f"   ✅ Embedding model is cached locally")
    else:
        print(f"   ⚠️  Embedding model download failed - will download on first use")
    
    if ollama_ok:
        print(f"   ✅ Ollama is ready to use")
    else:
        print(f"   ⚠️  Start Ollama first:")
        print(f"      - Local: ollama run {OLLAMA_MODEL}")
        print(f"      - Docker: docker run -d -p 11434:11434 ollama/ollama")
        print(f"      - Then: ollama run {OLLAMA_MODEL}")
    
    print(f"\n   Run the backend server:")
    print(f"      python run.py")
    
    print(f"\n💡 Tips:")
    print(f"   • Models are cached at: {MODELS_DIR}")
    print(f"   • Embedding model downloads on first use if not cached")
    print(f"   • For container Ollama, set OLLAMA_URL in .env")
    print(f"   • Check .env for configuration options")
    
    print("\n" + "="*60 + "\n")


def main():
    """Main setup function"""
    print("\n🚀 SAHAYAKAI MODEL INITIALIZATION")
    print("=" * 60)
    
    # Create directories
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(EMBEDDINGS_MODEL_PATH, exist_ok=True)
    
    # Download embedding model
    embedding_ok = download_embedding_model()
    
    # Check Ollama
    ollama_ok = verify_ollama_connection()
    
    # Create .env template if needed
    create_env_template()
    
    # Print summary
    print_summary(embedding_ok, ollama_ok)
    
    return 0 if embedding_ok else 1


if __name__ == "__main__":
    sys.exit(main())
