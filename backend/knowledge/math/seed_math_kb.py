"""Seed mathematics entries into ChromaDB via Ollama embeddings."""

import sys
from pathlib import Path

import requests

# Allow running as script from backend/
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from knowledge.math.math_kb import MathKnowledgeBase  # noqa: E402

OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"
COLLECTION_NAME = "mathematics"


def get_embedding(text: str) -> list[float]:
    response = requests.post(
        OLLAMA_EMBED_URL,
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=120,
    )
    response.raise_for_status()
    return response.json().get("embedding", [])


def seed(collection) -> dict:
    kb = MathKnowledgeBase()
    added = 0
    skipped = 0

    for entry in kb._entries:
        doc_id = entry["id"]
        text = kb.format_entry(entry)
        try:
            embedding = get_embedding(text)
            collection.upsert(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[text],
                metadatas=[{
                    "title": entry["title"],
                    "topic": entry["topic"],
                    "difficulty": entry.get("difficulty", "unknown"),
                    "source": "math_kb",
                }],
            )
            added += 1
            print(f"  + {doc_id}: {entry['title']}")
        except Exception as exc:
            skipped += 1
            print(f"  ! skip {doc_id}: {exc}")

    return {"added": added, "skipped": skipped, "total": kb.count}


def main():
    import chromadb

    data_dir = Path(__file__).resolve().parents[2] / "data"
    data_dir.mkdir(exist_ok=True)
    client = chromadb.PersistentClient(path=str(data_dir))
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    print(f"Seeding {MathKnowledgeBase().count} math entries into '{COLLECTION_NAME}'...")
    result = seed(collection)
    print(f"Done: {result['added']} added, {result['skipped']} skipped, collection size {collection.count()}")


if __name__ == "__main__":
    main()
