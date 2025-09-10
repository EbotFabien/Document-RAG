from mistralai import Mistral
import numpy as np
import faiss
import os
from getpass import getpass
from config import Config

# Initialize Mistral client

client = Mistral(api_key=Config.MISTRAL_API_KEY)


def get_text_embedding(text: str):
    """Generate embedding for a given text using Mistral embeddings."""
    response = client.embeddings.create(
        model="mistral-embed",
        inputs=text
    )
    return response.data[0].embedding


def load_db(chunks: list[str]):
    """Create and return a FAISS index from text chunks."""
    # Get embeddings for all chunks
    embeddings = [get_text_embedding(chunk) for chunk in chunks]
    embeddings = np.array(embeddings).astype("float32")

    # Build FAISS index
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)

    return index, embeddings


def create_question_embedding(question: str):
    """Generate embedding for a question query."""
    return np.array([get_text_embedding(question)]).astype("float32")


def search(index, question_embedding, chunks, k: int = 2):
    """Search for the most relevant chunks given a question embedding."""
    D, I = index.search(question_embedding, k)
    retrieved_chunks = [chunks[i] for i in I[0]]
    return retrieved_chunks, D[0]  # return chunks and distances


def run_mistral(user_message, model="mistral-small"):
    """Run a chat completion using Mistral API."""
    messages = [{"role": "user", "content": user_message}]
    response = client.chat.complete(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content
