from app.core.embeddings import embed
from app.core.vectorstore import vector_store
from app.core.llm import generate_answer
from app.services.youtube_service import get_youtube_videos
from app.services.notebook_service import save_chat


def chat(user_id: str, question: str):
    # Generic SPPU-aware query expansion (NOT subject-specific)
    query_vector = embed([question])[0]

    contexts = vector_store.search(query_vector)

    context_text = "\n".join(contexts) if contexts else "No context found."

    answer = generate_answer(context_text, question)
    videos = get_youtube_videos(question)

    save_chat(user_id, question, answer)

    return {
        "answer": answer,
        "videos": videos
    }
