"""
features/rag.py
Query ChromaDB with a user message and return relevant BCLS chunks.
"""

import os
import chromadb
from chromadb.utils import embedding_functions

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "..", "knowledge_base", "chroma_db")
COLLECTION_NAME = "bcls_guidelines"

_client = None
_collection = None


def _get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=CHROMA_PATH)
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        _collection = _client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=ef,
        )
    return _collection


def query_knowledge_base(user_message: str, n_results: int = 5) -> str:
    try:
        collection = _get_collection()
        results = collection.query(
            query_texts=[user_message],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )

        if not results["documents"] or not results["documents"][0]:
            return ""

        context_parts = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            context_parts.append(
                f"[Scenario: {meta['scenario']} | Step {meta['step']}: {meta['title']}]\n"
                f"{doc}\n"
                f"Source: {meta['source']}"
            )

        return "\n\n---\n\n".join(context_parts)

    except Exception as e:
        print(f"[RAG ERROR] {e}")
        return ""
