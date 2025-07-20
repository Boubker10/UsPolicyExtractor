from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

def semantic_chunking(text, model, threshold=0.5, min_chunk_len=3):

    sentences = [s.strip() for s in text.split('.') if s.strip()]
    if len(sentences) <= 1:
        return sentences  

    embeddings = model.encode(sentences, normalize_embeddings=True)

    similarities = [np.dot(embeddings[i], embeddings[i+1]) for i in range(len(embeddings) - 1)]

    chunks = []
    current_chunk = [sentences[0]]

    for i, sim in enumerate(similarities):
        if sim < threshold and len(current_chunk) >= min_chunk_len:
            chunks.append('. '.join(current_chunk) + '.')
            current_chunk = [sentences[i + 1]]
        else:
            current_chunk.append(sentences[i + 1])

    if current_chunk:
        chunks.append('. '.join(current_chunk) + '.')

    return chunks
