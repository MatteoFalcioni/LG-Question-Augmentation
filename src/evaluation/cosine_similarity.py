import numpy as np
from langchain_openai import OpenAIEmbeddings

def compute_similarity(string1, string2, embedding_model="text-embedding-3-large"):

    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(model=embedding_model)

    vector1 = embeddings.embed_query(string1)
    vector2 = embeddings.embed_query(string2)

    # Compute cosine similarity
    def cosine_similarity(vec1, vec2):
        dot = np.dot(vec1, vec2)
        return dot / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    similarity_score = cosine_similarity(vector1, vector2)
    
    return similarity_score