from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def retrieve_top_k_chunks(question_embedding, chunks, chunk_embeddings, k=3):
    question_embedding = np.array(question_embedding)
    sims = cosine_similarity(question_embedding, chunk_embeddings)[0]
    top_indices = sims.argsort()[-k:][::-1]
    return [(chunks[i], i, sims[i]) for i in top_indices]
