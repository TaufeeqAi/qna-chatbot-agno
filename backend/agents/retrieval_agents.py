from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.embedder.openai import OpenAIEmbedder
from agno.vectordb.pinecone import PineconeClient
from agno.knowledge.pdf import PDFKnowledgeBase

class RetrievalAgent:
    """
    Retrieves relevant document chunks from:
      1. Long-term memory (vector DB)
      2. User-uploaded PDFs
    """

    @staticmethod
    def initialize(user_id: str, vector_db_url: str):
        # Initialize Pinecone (or your chosen vector store)
        return PineconeClient(
            api_key="PINECONE_API_KEY",
            environment=vector_db_url,
            index_name=f"user_{user_id}"
        )

    @classmethod
    def query(cls, user_id: str, query: str):
        # 1. Connect to vector DB
        pinecone = cls.initialize(user_id, vector_db_url=None)
        # Perform vector search
        long_term_docs = pinecone.query(
            query, top_k=5, embedder=OpenAIEmbedder(id="text-embedding-3-small")
        )
        # 2. PDF KB (if any)
        pdf_kb = PDFKnowledgeBase(user_id=user_id, embedder=OpenAIEmbedder(id="text-embedding-3-small"))
        pdf_docs = pdf_kb.search(query, top_k=5)
        # Combine and return
        return long_term_docs + pdf_docs
