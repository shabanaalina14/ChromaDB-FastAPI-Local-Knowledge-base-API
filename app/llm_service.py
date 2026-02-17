import ollama
from app.config import OLLAMA_MODEL

def generate_grounded_answer(question: str, context_chunks: list):
    context = "\n\n".join(context_chunks)
    prompt = f"""
You are a strictly grounded AI assistant.
Answer ONLY from provided context.
If not found say: Information not found in document.

Context:
{context}

Question:
{question}

Answer:
"""
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]
