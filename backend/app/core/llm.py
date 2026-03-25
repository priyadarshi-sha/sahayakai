import requests
from app.core.config import OLLAMA_URL, OLLAMA_MODEL


def generate_answer(context: str, question: str) -> str:
    """Generate answer using Ollama Chat API with provided context
    
    Uses the /api/chat endpoint with proper message formatting and system prompt.
    Ensures LLM uses 100% of context and provides detailed, structured answers.
    Works with both local and container-based Ollama instances.
    OLLAMA_URL can be set via environment variable or defaults to http://localhost:11434
    """
    try:
        if not context or context.strip() == "No context found.":
            return "Answer not found in the uploaded SPPU study material."

        system_prompt = """You are an expert assistant for SPPU (Savitribai Phule Pune University) students.

YOUR RESPONSIBILITIES:
1. ALWAYS use the provided context - never ignore any part of it
2. Provide DETAILED, COMPREHENSIVE answers with examples and explanations
3. Structure your answer clearly with:
   - Direct answer to the question
   - Detailed explanation using ALL provided context
   - Key points and important concepts
   - Practical examples if applicable
4. ONLY answer from the provided context - do NOT add external information
5. If information is incomplete, acknowledge it
6. Use academic language appropriate for university students

GUIDELINES:
- Quote or reference specific parts of the context
- Explain why the information is relevant
- Connect different parts of the context
- Provide step-by-step explanations when needed
- Use formatting (bullet points, numbering) for clarity"""

        user_message = f"""Context Information:
{context}

Question:
{question}

Please provide a detailed answer using all the context provided above."""

        payload = {
            "model": OLLAMA_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "stream": False
        }

        response = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        answer = data.get("message", {}).get("content", "No answer generated.")
        
        return answer if answer.strip() else "Unable to generate answer."
    
    except requests.exceptions.ConnectionError:
        error_msg = f"Cannot connect to Ollama at {OLLAMA_URL}. Make sure Ollama is running."
        print(error_msg)
        return error_msg
    except requests.exceptions.Timeout:
        error_msg = "Ollama request timed out. Please try again."
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Error generating answer: {str(e)}"
        print(error_msg)
        return error_msg

        return error_msg
