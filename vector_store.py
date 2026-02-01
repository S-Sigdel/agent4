import faiss
import numpy as np

INDEX_FILE = "employee_vectors.index"
METADATA_FILE = "employee_metadata.json"

# Keep metadata in memory for quick lookup
METADATA = []

def create_index(dim):
    return faiss.IndexFlatL2(dim)

def upsert_employee(index, embedding, metadata):
    global METADATA
    vec = np.array([embedding], dtype="float32")
    index.add(vec)
    METADATA.append(metadata)

def search(index, query_embedding, top_k=5):
    vec = np.array([query_embedding], dtype="float32")
    D, I = index.search(vec, top_k)
    results = []
    for dist, idx in zip(D[0], I[0]):
        metadata = METADATA[idx]
        results.append({
            "employee_id": metadata["employee_id"],
            "score": float(dist),
            "skills": metadata["skills"]
        })
    return results
