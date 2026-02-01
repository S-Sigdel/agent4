import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBEDDING_MODEL = "text-embedding-3-large"

def embed(text: str):
    """Return embedding vector for a given text"""
    if not text:
        text = " "  # OpenAI embedding cannot be empty
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding
