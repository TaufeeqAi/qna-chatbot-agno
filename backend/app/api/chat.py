# backend/app/api/chat.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.secuirty import verify_access_token
from app.db.session import get_db
from backend.agents.retrieval_agents import RetrievalAgent
from backend.agents.reasoning_agent import ReasoningAgent
from backend.agents.memory_agent import MemoryAgent
from app.db import schemas

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(schemas.BaseModel):
    message: str
    mode: str  # "chain_of_thought", "tree_of_thought", or "graph_of_thought"

class ChatResponse(schemas.BaseModel):
    response: str
    trace: list

@router.post("/", response_model=ChatResponse)
def chat_endpoint(
    req: ChatRequest,
    token_data: dict = Depends(verify_access_token),
    db: Session = Depends(get_db)
):
    user_id = int(token_data["sub"])

    # 1. Load short-term context
    stm = MemoryAgent.load_short_term(user_id)

    # 2. Retrieve relevant docs (long-term + PDF)
    docs = RetrievalAgent.query(user_id, req.message)

    # 3. Run reasoning
    try:
        resp_text, trace = ReasoningAgent.reason(req.message, stm, docs, req.mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reasoning failed: {e}")

    # 4. Update memory
    MemoryAgent.update(user_id, req.message, resp_text)

    return ChatResponse(response=resp_text, trace=trace)
