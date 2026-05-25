"""Load and search structured mathematics knowledge offline."""

from pathlib import Path
from knowledge.kb_loader import KnowledgeBase

TOPICS_DIR = Path(__file__).parent / "topics"


class MathKnowledgeBase(KnowledgeBase):
    def __init__(self, topics_dir: Path | None = None):
        super().__init__(topics_dir or TOPICS_DIR, domain="mathematics")

    def search_entries(self, query: str, limit: int = 5, min_score: int = 2):
        return [e for _, e in self.search(query, limit=limit, min_score=min_score)]

    def format_entry(self, entry: dict) -> str:
        from response_formatter import format_entry as fmt
        return fmt(entry)

    def search_formatted(self, query: str, limit: int = 3) -> str:
        from response_formatter import format_knowledge_response
        entries = self.search_entries(query, limit=limit)
        if not entries:
            return "No matching mathematics entries found."
        return format_knowledge_response(entries, intro="Here's the math reference:")
