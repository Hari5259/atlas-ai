"""Format knowledge and AI responses as readable markdown."""

from typing import Any


def format_entry(entry: dict[str, Any]) -> str:
    lines = [f"### {entry['title']}"]
    topic = entry.get("topic", "").replace("_", " ").title()
    if topic:
        lines.append(f"*{topic}* · {entry.get('difficulty', 'general')}")
    lines.append("")
    lines.append(entry["content"])
    if entry.get("formula"):
        lines.append(f"\n**Formula:** `{entry['formula']}`")
    if entry.get("example"):
        lines.append(f"\n**Example:** {entry['example']}")
    return "\n".join(lines)


def format_knowledge_response(entries: list[dict[str, Any]], intro: str | None = None) -> str:
    if not entries:
        return ""
    parts = []
    if intro:
        parts.append(intro)
        parts.append("")
    for i, entry in enumerate(entries):
        if i > 0:
            parts.append("---")
            parts.append("")
        parts.append(format_entry(entry))
    parts.append("")
    parts.append("*Would you like a worked example or a practice question on this topic?*")
    return "\n".join(parts)


def format_error(message: str) -> str:
    return f"**Notice:** {message}\n\nStart the backend with `cd backend && python -m uvicorn main:app --reload` for full AI responses."


def format_topics_list(topics: list[str]) -> str:
    grouped = ", ".join(t.replace("_", " ").title() for t in topics)
    return (
        "### Topics I can help with\n\n"
        f"{grouped}\n\n"
        "Ask me anything specific — e.g. *Explain Newton's second law* or *What is the quadratic formula?*"
    )
