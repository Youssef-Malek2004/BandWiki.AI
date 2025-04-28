from fastapi import FastAPI, HTTPException
from .models import QueryRequest, QueryResponse
from .chroma_store import get_chroma_db
from .agent import build_agent
from langchain_community.chat_message_histories import ChatMessageHistory
from starlette.datastructures import State
from bandwiki_graph.graph import build_bandwiki_graph

app = FastAPI()
app.state = State()

store = {}

def get_session_history(session_id: str):
    return store.setdefault(session_id, ChatMessageHistory())

@app.on_event("startup")
def startup_event():
    db = get_chroma_db()
    retriever = db.as_retriever()
    app.state.band_agent, app.state.judge_agent = build_agent(retriever, get_session_history)
    app.state.bandwiki_graph = build_bandwiki_graph()

    print("[✓] App initialized.")

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    try:
        chat_history = get_session_history(request.session_id)

        initial_state = {
            "query": request.query,
            "chat_history": chat_history.messages,
            "band_agent": app.state.band_agent,
            "judge_chain": app.state.judge_agent,
        }

        response = app.state.bandwiki_graph.invoke(
            initial_state,
            config={"configurable": {"session_id": request.session_id}}
        )

        return {"result": response["final_answer"]}
    except Exception as e:
        import traceback
        traceback.print_exc()  # Print full error in server log
        raise HTTPException(status_code=500, detail=str(e))