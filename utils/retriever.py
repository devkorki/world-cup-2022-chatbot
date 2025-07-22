from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Retriever:
    def __init__(self, model_name="all-MiniLM-L6-v2", threshold=0.4):
        self.model = SentenceTransformer(model_name)
        self.corpus_embeddings = None
        self.corpus = None
        self.threshold = threshold  # Similarity threshold

    def fit(self, corpus):
        # Normalize corpus (optional, but improves quality)
        self.corpus = [doc.strip().lower() for doc in corpus]
        # Encode and ensure it's a NumPy array
        self.corpus_embeddings = np.array(self.model.encode(self.corpus, convert_to_tensor=False))

    def retrieve(self, query, top_k=5):
        # Normalize query
        query = query.strip().lower()
        query_embedding = np.array(self.model.encode([query], convert_to_tensor=False))
        similarities = cosine_similarity(query_embedding, self.corpus_embeddings)[0]

        # Sort and filter
        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = [(self.corpus[i], similarities[i]) for i in top_indices if similarities[i] >= self.threshold]

        # Optional debug
        if not results:
            print(f"[Retriever] No relevant tweets found for: '{query}'")
        else:
            print(f"[Retriever] Top results for: '{query}'")
            for doc, score in results:
                print(f"  > {score:.2f} - {doc[:80]}...")

        return results
