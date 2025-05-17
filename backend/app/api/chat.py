from fastapi import APIRouter, Depends
from ..agents.retrieval_agent import RetrievalAgent
from ..agents.reasoning_agent import ReasoningAgent
from ..agents.memory_agent import MemoryAgent
from ..db.session import SessionLocal
from ..utils.pdf_utils import extract_and_chunk

router = APIRouter(tags=["chat"])

@router.post("/chat")
def chat(message: str, mode: str, user=Depends(get_current_user)):
    # 1. Short-term context
    stm = MemoryAgent.load_short_term(user.id)
    # 2. Retrieve relevant docs (long-term + PDF)
    docs = RetrievalAgent.query(user.id, message)
    # 3. Reasoning step
    response, trace = ReasoningAgent.reason(message, stm, docs, mode)
    # 4. Update memory
    MemoryAgent.update(user.id, message, response)
    return {"response": response, "trace": trace}
