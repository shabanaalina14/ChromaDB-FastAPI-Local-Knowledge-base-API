from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL, TOP_K
from app.vector_store import query_collection

model = SentenceTransformer(EMBEDDING_MODEL)

def retrieve_relevant_chunks(query: str):
    query_embedding = model.encode(query).tolist()
    results = query_collection(query_embedding, TOP_K)
    return results["documents"][0], results["metadatas"][0]
