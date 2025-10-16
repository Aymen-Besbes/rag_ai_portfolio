import json
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from chunking import chunk_resume_data
from config import INDEX_PATH, CHUNKS_PATH,RESUME_PATH,EMBEDDING_MODEL


def load_chunks_from_file(chunks_file_path):
    """
    Loads chunks from a JSON file.
    """
    if not os.path.exists(chunks_file_path):
        return None 
    with open(chunks_file_path, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    print(f"Loaded {len(chunks)} chunks from {chunks_file_path}")
    return chunks

def save_chunks_to_file(chunks, chunks_file_path):
    """
    Saves chunks to a JSON file.
    """
    os.makedirs(os.path.dirname(chunks_file_path), exist_ok=True)
    with open(chunks_file_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2)
    print(f"Saved {len(chunks)} chunks to {chunks_file_path}")


def create_and_save_embeddings(chunks, index_path, chunks_path, model_name=EMBEDDING_MODEL):
    """
    Generates embeddings for the provided chunks using a Sentence Transformer model,
    creates a FAISS index, and saves both the index and the chunks.
    """
    if not chunks:
        print("No chunks provided to embed. Exiting.")
        return

    print(f"Loading embedding model: {model_name}...")
    model = SentenceTransformer(model_name)
    print("Model loaded.")

    print(f"Generating embeddings for {len(chunks)} chunks...")
    embeddings = model.encode(chunks, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32') 
    print("Embeddings generated.")
    
    dimension = embeddings.shape[1]
    print(f"Embedding dimension: {dimension}")

    print("Creating FAISS index...")
    index = faiss.IndexFlatL2(dimension) 
    index.add(embeddings)
    print(f"FAISS index created with {index.ntotal} vectors.")

    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    os.makedirs(os.path.dirname(chunks_path), exist_ok=True)

    print(f"Saving FAISS index to {index_path}...")
    faiss.write_index(index, index_path)
    print("FAISS index saved.")

    print(f"Saving chunks to {chunks_path}...")
    save_chunks_to_file(chunks, chunks_path)
    print("Chunks saved.")

    print("Embedding generation and saving complete!")

def main():
    #Load Document
    if not os.path.exists(RESUME_PATH):
        print(f"Error: Raw resume file not found at {RESUME_PATH}.")
        print("Please create 'my_resume.txt' in the same directory as embedding.py and paste your resume template content there.")
        return

    print(f"Loading raw resume text from {RESUME_PATH}...")
    with open(RESUME_PATH, 'r', encoding='utf-8') as f:
        raw_resume_text = f.read()
    print("Raw resume text loaded.")

    # Call the chunking function
    print("Calling chunk_resume_data to generate chunks...")
    chunks = chunk_resume_data(raw_resume_text)
    print(f"Chunking complete. Generated {len(chunks)} chunks.")

    # Create and save embeddings
    create_and_save_embeddings(chunks, INDEX_PATH, CHUNKS_PATH)

if __name__ == "__main__":
    main()