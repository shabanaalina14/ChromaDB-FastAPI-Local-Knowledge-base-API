import chromadb
from app.config import CHROMA_PATH, COLLECTION_NAME

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

def add_documents(ids, documents, embeddings, metadatas):
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

def query_collection(query_embedding, top_k):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

def get_all_documents():
    return collection.get()

def delete_document_by_source(source_name):
    results = collection.get(where={"source": source_name})
    if results["ids"]:
        collection.delete(ids=results["ids"])
        return True
    return False
