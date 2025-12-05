import numpy as np

def compute_similarity(string1, string2, embeddings):
    """
    Computes the cosine similarity between two vectors given an embedding.
    """

    vector1 = embeddings.embed_query(string1)
    vector2 = embeddings.embed_query(string2)

    # Compute cosine similarity
    def cosine_similarity(vec1, vec2):
        dot = np.dot(vec1, vec2)
        return dot / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    similarity_score = cosine_similarity(vector1, vector2)
    
    return similarity_score