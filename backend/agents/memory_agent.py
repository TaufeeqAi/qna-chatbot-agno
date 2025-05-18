from mem0 import Mem0
from agno.vectordb.pinecone import PineconeClient
from agno.embedder.openai import OpenAIEmbedder

class MemoryAgent:
    """
    Manages:
      - Short-term memory: Mem0 session cache
      - Long-term memory: vector store summaries
    """
    mem0 = Mem0()

    @classmethod
    def load_short_term(cls, user_id: str) -> list:
        return cls.mem0.load_session(user_id) or []

    @classmethod
    def update(cls, user_id: str, user_msg: str, bot_resp: str):
        cls.mem0.append(user_id, {"user": user_msg, "bot": bot_resp})
        # Summarize when session > N messages
        if len(cls.mem0.load_session(user_id)) > 20:
            cls.summarize_to_long_term(user_id)

    @classmethod
    def summarize_to_long_term(cls, user_id: str):
        session = cls.mem0.load_session(user_id)
        summary = cls.mem0.summarize(session)
        # Upsert to vector DB
        pinecone = PineconeClient(api_key="PINECONE_API_KEY", environment=None, index_name=f"user_{user_id}")
        pinecone.upsert([{"id": f"sum_{i}", "vector": OpenAIEmbedder(id="text-embedding-3-small").embed(summary), "metadata": {"text": summary}}])
        cls.mem0.clear_session(user_id)
