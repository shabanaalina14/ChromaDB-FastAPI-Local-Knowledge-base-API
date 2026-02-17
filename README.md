# Offline Document Intelligence API (Full CRUD + PDF)

## Supports:
GET - Read data
POST - Create document
PUT - Full update
PATCH - Partial update
DELETE - Remove document

## Setup
1. Install Ollama
   ollama pull llama3

2. Install dependencies
   pip install -r requirements.txt

3. Run
   uvicorn app.main:app --reload

Open:
http://127.0.0.1:8000/docs
