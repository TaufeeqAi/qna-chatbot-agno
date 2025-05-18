# backend/app/utils/vector_client.py

from typing import List, Dict
from agno.vectordb.pineconedb import PineconeClient
from agno.embedder.openai import OpenAIEmbedder

class VectorClient:
    """
    Wraps a PineconeClient + OpenAIEmbedder to upsert text chunks as embeddings.
    """

    def __init__(self, user_id: int, api_key: str, environment: str):
        # Initialize Pinecone index scoped to this user
        self.index = PineconeClient(
            api_key=api_key,
            environment=environment,
            index_name=f"user_{user_id}"
        )
        # Use OpenAI small text-embedding model
        self.embedder = OpenAIEmbedder(id="text-embedding-3-small")

    def upsert_chunks(self, chunks: List[str]) -> None:
        """
        Embed each chunk and upsert into the vector index.
        """
        # Prepare bulk upsert payload
        vectors: List[Dict] = []
        for i, text in enumerate(chunks):
            embedding = self.embedder.embed(text)
            vectors.append({
                "id": f"{i}",
                "vector": embedding,
                "metadata": {"text": text}
            })
        # Upsert all at once
        self.index.upsert(vectors)
