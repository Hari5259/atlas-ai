"""Route queries across all Atlas knowledge bases."""

from typing import Any

from knowledge.math.math_kb import MathKnowledgeBase
from knowledge.general_kb import general_kb
from response_formatter import format_knowledge_response

math_kb = MathKnowledgeBase()


def _math_entries(scored: list) -> list[dict[str, Any]]:
    return [e for _, e in scored]


def search_knowledge(query: str, limit: int = 4) -> tuple[str | None, str, list[str]]:
    """
    Search math + general KBs. Returns (response_text, response_type, source_ids).
    """
    math_scored = math_kb.search(query, limit=limit + 2, min_score=2)
    general_scored = general_kb.search(query, limit=limit + 2, min_score=2)

    combined: list[tuple[int, dict[str, Any], str]] = []
    for score, entry in math_scored:
        combined.append((score, entry, "mathematics"))
    for score, entry in general_scored:
        combined.append((score, entry, entry.get("domain", "general")))

    if not combined:
        return None, "none", []

    combined.sort(key=lambda x: x[0], reverse=True)
    top_score = combined[0][0]

    # Keep only highly relevant matches if we have a strong match (score >= 5)
    if top_score >= 5:
        threshold = max(4, top_score - 1)
        filtered_combined = [item for item in combined if item[0] >= threshold]
    else:
        filtered_combined = combined

    top_items = filtered_combined[:limit]
    top = [e for _, e, _ in top_items]
    domains = {d for _, _, d in top_items}
    intro = "Here's what I found in the Atlas knowledge base:"
    if len(domains) == 1:
        domain = next(iter(domains))
        intro = f"Here's a clear explanation from **{domain.replace('_', ' ').title()}**:"

    text = format_knowledge_response(top, intro=intro)
    source_ids = [e.get("id", "") for e in top if e.get("id")]
    rtype = "mathematics" if domains == {"mathematics"} else "knowledge"
    return text, rtype, source_ids
