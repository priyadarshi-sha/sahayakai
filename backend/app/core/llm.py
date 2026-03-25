import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"


def generate_answer(context: str, question: str) -> str:
    if not context or context.strip() == "No context found.":
        return "Answer not found in the uploaded SPPU study material."

    prompt = f"""
You are an assistant for SPPU university students.
Answer strictly from the provided context.
Do NOT add external information.

Context:
{context}

Question:
{question}

Answer:
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "No answer generated.")
    except Exception as e:
        return f"Ollama error: {str(e)}"
