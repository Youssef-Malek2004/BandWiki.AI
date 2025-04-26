from fastapi import FastAPI, HTTPException
from .models import QueryRequest, QueryResponse
from .chroma_store import get_chroma_db
from .agent import build_agent
from langchain_community.chat_message_histories import ChatMessageHistory

app = FastAPI()

store = {}

@app.on_event("startup")
def startup_event():
    db = get_chroma_db()
    retriever = db.as_retriever()
    def get_session_history(session_id: str):
        return store.setdefault(session_id, ChatMessageHistory())

    global qa_agent
    qa_agent = build_agent(retriever, get_session_history)
    print("[✓] App initialized.")

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    try:
        response = qa_agent.invoke(
            {"input": request.query},
            config={"configurable": {"session_id": request.session_id}}
        )
        return {"result": response["output"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))