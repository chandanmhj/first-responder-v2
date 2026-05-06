"""
ingest.py
Run this ONCE to embed all BCLS chunks and store them in ChromaDB.
Usage: python knowledge_base/ingest.py
"""

import os
import sys

# Allow running from root directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb
from chromadb.utils import embedding_functions
from data import BCLS_KNOWLEDGE_BASE

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")
COLLECTION_NAME = "bcls_guidelines"


def ingest():
    print("Initializing ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    try:
        client.delete_collection(COLLECTION_NAME)
        print("Deleted existing collection.")
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )

    documents = []
    metadatas = []
    ids = []

    for chunk in BCLS_KNOWLEDGE_BASE:
        doc_text = f"{chunk['title']}. {chunk['content']}"
        metadata = {
            "scenario": chunk["scenario"],
            "step": chunk["step"],
            "title": chunk["title"],
            "keywords": ", ".join(chunk["keywords"]),
            "source": chunk["source"],
        }
        chunk_id = f"{chunk['scenario']}_step_{chunk['step']}"
        documents.append(doc_text)
        metadatas.append(metadata)
        ids.append(chunk_id)

    print(f"Embedding {len(documents)} chunks...")
    collection.add(documents=documents, metadatas=metadatas, ids=ids)
    print(f"Done! {len(documents)} chunks stored in ChromaDB at: {CHROMA_PATH}")


if __name__ == "__main__":
    ingest()
