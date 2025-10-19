import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL, INDEX_PATH, CHUNKS_PATH,TOP_K

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

def retrieve(query: str, k: int = TOP_K) -> list[tuple[str, float]]:
    """
    Retrieve the top-k most relevant chunks for a query using cosine similarity.
    Returns a list of (chunk_text, similarity_score) tuples.
    """
    _load_resources()

    # Compute query embedding
    query_embedding = np.array(_model.encode([query])).astype('float32')
    faiss.normalize_L2(query_embedding)  # normalize for cosine similarity

    # Search in FAISS (inner product on normalized vectors = cosine similarity)
    distances, indices = _index.search(query_embedding, k)

    results = []
    for i, idx in enumerate(indices[0]):
        if 0 <= idx < len(_chunks):
            results.append((_chunks[idx], float(distances[0][i])))

    return results

# ------------------------------
# Interactive CLI
# ------------------------------
if __name__ == "__main__":
    _load_resources()
    print("Ready to accept queries. Type 'quit' to exit.\n")

    while True:
        query = input("Query: ").strip()
        if query.lower() == "quit":
            print("Exiting...")
            break

        top_chunks = retrieve(query, k=TOP_K)
        if not top_chunks:
            print("No relevant chunks found.\n")
            continue

        for i, (chunk, score) in enumerate(top_chunks, start=1):
            print(f"--- Chunk {i} (score: {score:.4f}) ---\n{chunk}\n")
