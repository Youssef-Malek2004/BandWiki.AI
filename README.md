# AC/DC QA API

A FastAPI service with retrieval-augmented QA about the band AC/DC, using ChromaDB, HuggingFace embeddings, and Gemini.

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env
# Fill in API keys
uvicorn app.main:app --reload
```

## Endpoints
- `GET /healthcheck`
- `POST /query` (body: `{"query":"...","session_id":"..."}`)