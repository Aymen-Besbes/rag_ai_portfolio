import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL, INDEX_PATH, CHUNKS_PATH

# Global resources (lazy-loaded)
_model = None
_index = None
_chunks = None


def _load_resources():
    """Lazy-load the model, FAISS index, and chunks."""
    global _model, _index, _chunks

    if _model is None:
        print(f"Loading embedding model '{EMBEDDING_MODEL}'...")
        _model = SentenceTransformer(EMBEDDING_MODEL)
        print("Model loaded.")

    if _index is None:
        if not os.path.exists(INDEX_PATH):
            raise FileNotFoundError(f"FAISS index not found at {INDEX_PATH}")
        print(f"Loading FAISS index from {INDEX_PATH}...")
        _index = faiss.read_index(INDEX_PATH)
        print("FAISS index loaded.")

    if _chunks is None:
        if not os.path.exists(CHUNKS_PATH):
            raise FileNotFoundError(f"Chunks file not found at {CHUNKS_PATH}")
        print(f"Loading chunks from {CHUNKS_PATH}...")
        with open(CHUNKS_PATH, 'r', encoding='utf-8') as f:
            _chunks = json.load(f)
        print(f"Loaded {_chunks and len(_chunks)} chunks.")

    if _index.ntotal != len(_chunks):
        print("Warning: Number of vectors in the index and number of chunks do not match.")


def retrieve(query: str, k: int = 10) -> list[str]:
    """
    Retrieve the top-k most relevant chunks for a given query.
    
    Args:
        query (str): The search query.
        k (int): Number of top results to return.
        
    Returns:
        list[str]: Top-k chunks matching the query.
    """
    _load_resources()

    # Compute query embedding
    query_embedding = np.array(_model.encode([query])).astype('float32')

    # Search in FAISS
    distances, indices = _index.search(query_embedding, k)

    # Collect matching chunks
    results = []
    for idx in indices[0]:
        if 0 <= idx < len(_chunks):
            results.append(_chunks[idx])

    return results


if __name__ == "__main__":
    _load_resources()
    print("Ready to accept queries. Type 'quit' to exit.")

    while True:
        query = input("Query: ").strip()
        if query.lower() == "quit":
            print("Exiting...")
            break

        top_chunks = retrieve(query, k=10)
        if not top_chunks:
            print("No relevant chunks found.\n")
            continue

        for i, chunk in enumerate(top_chunks, start=1):
            print(f"--- Chunk {i} ---\n{chunk}\n")
