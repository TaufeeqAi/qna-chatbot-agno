# backend/app/api/memory.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.core.secuirty import verify_access_token
from backend.agents.memory_agent import MemoryAgent

router = APIRouter(prefix="/memory", tags=["memory"])

@router.get("/session")
def get_session_memory(token_data: dict = Depends(verify_access_token)):
    user_id = int(token_data["sub"])
    session = MemoryAgent.load_short_term(user_id)
    return {"session_memory": session}

@router.delete("/session", status_code=status.HTTP_204_NO_CONTENT)
def clear_session_memory(token_data: dict = Depends(verify_access_token)):
    user_id = int(token_data["sub"])
    MemoryAgent.mem0.clear_session(user_id)
