import requests
from app.core.config import OLLAMA_URL, OLLAMA_MODEL, GEMINI_API_KEY, GEMINI_MODEL


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
        print(OLLAMA_URL)
        response = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=130)
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


def get_available_gemini_models() -> list:
    """Utility function to list all models accessible with your Gemini API key.
    Run this to find the correct string for GEMINI_MODEL.
    """
    url = f"https://generativelanguage.googleapis.com/v1/models?key={GEMINI_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        models_data = response.json()
        model_names = [m["name"].replace("models/", "") for m in models_data.get("models", [])]
        print("Available Gemini Models:", model_names)
        return model_names
    except Exception as e:
        print(f"Failed to fetch models: {e}")
        return []
    
def generate_answer_gemini(context: str, question: str) -> str:
    """Generate answer using Google Gemini API with provided context
    
    Uses the Google Gemini REST API. 
    Maintains the same system persona and constraints as the Ollama version.
    """

    get_available_gemini_models()

    try:
        if not context or context.strip() == "No context found.":
            return "Answer not found in the uploaded SPPU study material."

        # The system instructions for Gemini
        system_instruction = """You are an expert assistant for SPPU (Savitribai Phule Pune University) students.

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

        user_prompt = f"Context Information:\n{context}\n\nQuestion:\n{question}\n\nPlease provide a detailed answer using all the context provided above."

        # Gemini API Endpoint (using v1beta for system_instruction support)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "system_instruction": {
                "parts": {
                    "text": system_instruction
                }
            },
            "contents": [
                {
                    "parts": [
                        {"text": user_prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.2, # Lower temperature for academic accuracy
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 2048,
            }
        }

        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        
        # Extracting content from Gemini's nested response structure
        if "candidates" in data and len(data["candidates"]) > 0:
            candidate = data["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                answer = candidate["content"]["parts"][0].get("text", "No answer generated.")
                return answer if answer.strip() else "Unable to generate answer."
        
        return "Gemini could not generate a response. Please check the context."

    except requests.exceptions.HTTPError as e:
        error_msg = f"Gemini API Error: {response.status_code} - {response.text}"
        print(error_msg)
        return "Error communicating with Gemini API."
    except Exception as e:
        error_msg = f"Unexpected error with Gemini: {str(e)}"
        print(error_msg)
        return error_msg