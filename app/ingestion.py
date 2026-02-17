from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP
from app.vector_store import add_documents

model = SentenceTransformer(EMBEDDING_MODEL)

def chunk_text(text: str):
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end])
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks

def ingest_document(text: str, filename: str):
    chunks = chunk_text(text)
    embeddings = model.encode(chunks).tolist()
    ids = [f"{filename}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": filename, "chunk_id": i} for i in range(len(chunks))]
    add_documents(ids, chunks, embeddings, metadatas)
