from app.core.embeddings import embed
from app.core.vectorstore import vector_store
from app.core.llm import generate_answer
from app.services.youtube_service import get_youtube_videos
from app.services.notebook_service import save_chat


def chat(user_id: str, question: str):
    """
    Process a chat query and return answer with videos.
    
    Response Schema:
    {
        "answer": str,
        "videos": list,
        "context_found": bool,
        "sources": int
    }
    """
    try:
        # Generate embedding for the question
        query_vector = embed([question])[0]

        # Search for relevant context
        contexts = vector_store.search(query_vector, k=5)
        
        # Prepare context text
        context_text = "\n".join(contexts) if contexts else "No context found."
        context_found = len(contexts) > 0

        # Generate answer using LLM
        answer = generate_answer(context_text, question)
        
        # Get related videos
        videos = get_youtube_videos(question)

        # Save to notebook
        save_chat(user_id, question, answer)

        # Return consistent response schema
        return {
            "answer": answer,
            "videos": videos,
            "context_found": context_found,
            "sources": len(contexts)
        }
    
    except Exception as e:
        return {
            "answer": f"Error processing query: {str(e)}",
            "videos": [],
            "context_found": False,
            "sources": 0
        }
