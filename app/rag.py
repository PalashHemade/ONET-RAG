from sqlalchemy import text
import google.generativeai as genai

from app.db import engine
from app.embeddings import embed_model
from app.config import GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Load model
model = genai.GenerativeModel("models/gemini-2.5-flash")


def get_relevant_careers(query: str, top_k: int = 5) -> str:
    query_embedding = embed_model.encode(query).tolist()

    sql = text("""
        SELECT content
        FROM career_kb.embedding_store
        ORDER BY embedding <-> (:query_embedding)::vector
        LIMIT :top_k
    """)

    with engine.connect() as conn:
        rows = conn.execute(
            sql,
            {
                "query_embedding": query_embedding,
                "top_k": top_k
            }
        ).fetchall()

    if not rows:
        return "No relevant career data found."

    return "\n\n".join(row[0] for row in rows)


def explain_careers(query: str) -> str:
    context = get_relevant_careers(query)

    prompt = f"""
You are a professional career advisor.

User interest:
{query}

Relevant career information:
{context}

Based on the above data, explain which careers fit the user
and why. Be concise, structured, and helpful.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"
