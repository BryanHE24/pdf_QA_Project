from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def embed_chunks(chunks):
    return embedding_model.encode(chunks)

def find_most_relevant_chunks(query, chunks, top_k=3):
    query_embedding = embedding_model.encode([query])
    chunk_embeddings = embed_chunks(chunks)
    similarities = cosine_similarity(query_embedding, chunk_embeddings)
    top_indices = np.argsort(similarities[0])[-top_k:]
    return [chunks[i] for i in reversed(top_indices)]
