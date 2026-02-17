from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.ingestion import ingest_document
from app.retrieval import retrieve_relevant_chunks
from app.llm_service import generate_grounded_answer
from app.vector_store import get_all_documents, delete_document_by_source
from app.pdf_utils import extract_text_from_pdf
import io

app = FastAPI(title="Offline Document Intelligence API - Full CRUD")

# ---------------- CREATE (POST) ----------------
@app.post("/documents")
async def create_document(file: UploadFile = File(...)):
    content = await file.read()
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(io.BytesIO(content))
    else:
        text = content.decode("utf-8")
    ingest_document(text, file.filename)
    return {"status": "Created", "filename": file.filename}

# ---------------- READ (GET ALL DOCS) ----------------
@app.get("/documents")
def read_documents():
    data = get_all_documents()
    return {"status": "Success", "documents": data}

# ---------------- QUERY (GET) ----------------
@app.get("/query")
def query_documents(question: str):
    docs, meta = retrieve_relevant_chunks(question)
    answer = generate_grounded_answer(question, docs)
    return {
        "question": question,
        "answer": answer,
        "sources": meta
    }

# ---------------- UPDATE FULL (PUT) ----------------
@app.put("/documents/{filename}")
async def update_document(filename: str, file: UploadFile = File(...)):
    delete_document_by_source(filename)
    content = await file.read()
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(io.BytesIO(content))
    else:
        text = content.decode("utf-8")
    ingest_document(text, filename)
    return {"status": "Fully Updated", "filename": filename}

# ---------------- UPDATE PARTIAL (PATCH) ----------------
class UpdateText(BaseModel):
    extra_text: str

@app.patch("/documents/{filename}")
def partial_update(filename: str, update: UpdateText):
    ingest_document(update.extra_text, filename)
    return {"status": "Partially Updated", "filename": filename}

# ---------------- DELETE ----------------
@app.delete("/documents/{filename}")
def delete_document(filename: str):
    success = delete_document_by_source(filename)
    if success:
        return {"status": "Deleted", "filename": filename}
    raise HTTPException(status_code=404, detail="Document not found")
