"""Shared knowledge base loader and search for Atlas."""

import json
from pathlib import Path
from typing import Any

STOP_WORDS = {
    "the", "and", "for", "what", "how", "why", "can", "you", "are", "is", "a", "an",
    "to", "of", "in", "me", "my", "do", "does", "did", "with", "this", "that", "from",
    "about", "when", "where", "which", "who", "will", "would", "could", "should",
}


class KnowledgeBase:
    def __init__(self, topics_dir: Path, domain: str = "general"):
        self._topics_dir = topics_dir
        self.domain = domain
        self._entries: list[dict[str, Any]] = []
        self._load_all()

    def _load_all(self) -> None:
        self._entries.clear()
        if not self._topics_dir.exists():
            return
        for path in sorted(self._topics_dir.glob("*.json")):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            for entry in data.get("entries", []):
                entry.setdefault("domain", self.domain)
                self._entries.append(entry)

    @property
    def count(self) -> int:
        return len(self._entries)

    @property
    def topics(self) -> list[str]:
        return sorted({e.get("topic", "general") for e in self._entries})

    def search(self, query: str, limit: int = 5, min_score: int = 2) -> list[tuple[int, dict[str, Any]]]:
        if not query.strip():
            return []
        terms = [t.lower() for t in query.split() if len(t) > 2 and t.lower() not in STOP_WORDS]
        if not terms:
            return []
        scored: list[tuple[int, dict[str, Any]]] = []
        for entry in self._entries:
            score = 0
            title = entry.get("title", "").lower()
            content = entry.get("content", "").lower()
            formula = entry.get("formula", "").lower()
            keywords = [k.lower() for k in entry.get("keywords", [])]
            for term in terms:
                if term in title:
                    score += 5
                if term in keywords:
                    score += 4
                if term in formula:
                    score += 3
                if term in content:
                    score += 1
            if score >= min_score:
                scored.append((score, entry))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:limit]
