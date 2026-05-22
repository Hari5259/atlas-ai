"""Load and search structured mathematics knowledge offline."""

import json
from pathlib import Path
from typing import Any

TOPICS_DIR = Path(__file__).parent / "topics"


class MathKnowledgeBase:
    """In-memory mathematics reference with keyword search."""

    def __init__(self, topics_dir: Path | None = None):
        self._topics_dir = topics_dir or TOPICS_DIR
        self._entries: list[dict[str, Any]] = []
        self._load_all()

    def _load_all(self) -> None:
        self._entries.clear()
        if not self._topics_dir.exists():
            return
        for path in sorted(self._topics_dir.glob("*.json")):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            self._entries.extend(data.get("entries", []))

    def reload(self) -> int:
        """Reload JSON files from disk. Returns entry count."""
        self._load_all()
        return len(self._entries)

    @property
    def count(self) -> int:
        return len(self._entries)

    @property
    def topics(self) -> list[str]:
        return sorted({e["topic"] for e in self._entries})

    def get_by_id(self, entry_id: str) -> dict[str, Any] | None:
        for entry in self._entries:
            if entry["id"] == entry_id:
                return entry
        return None

    def list_by_topic(self, topic: str) -> list[dict[str, Any]]:
        topic_lower = topic.lower()
        return [e for e in self._entries if e["topic"].lower() == topic_lower]

    def search(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        """Score entries by keyword and text overlap with the query."""
        if not query.strip():
            return []
        terms = [t.lower() for t in query.split() if len(t) > 1]
        scored: list[tuple[int, dict[str, Any]]] = []

        for entry in self._entries:
            score = 0
            title = entry.get("title", "").lower()
            content = entry.get("content", "").lower()
            formula = entry.get("formula", "").lower()
            keywords = [k.lower() for k in entry.get("keywords", [])]
            blob = f"{title} {content} {formula} {' '.join(keywords)}"

            for term in terms:
                if term in title:
                    score += 4
                if term in keywords:
                    score += 3
                if term in formula:
                    score += 2
                if term in content:
                    score += 1

            if score > 0:
                scored.append((score, entry))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [entry for _, entry in scored[:limit]]

    def format_entry(self, entry: dict[str, Any]) -> str:
        """Plain-text block for RAG or API responses."""
        lines = [
            f"**{entry['title']}** ({entry['topic']})",
            entry["content"],
        ]
        if entry.get("formula"):
            lines.append(f"Formula: {entry['formula']}")
        if entry.get("example"):
            lines.append(f"Example: {entry['example']}")
        lines.append(f"Difficulty: {entry.get('difficulty', 'unknown')}")
        return "\n".join(lines)

    def search_formatted(self, query: str, limit: int = 3) -> str:
        results = self.search(query, limit=limit)
        if not results:
            return "No matching mathematics entries found."
        return "\n\n---\n\n".join(self.format_entry(e) for e in results)
