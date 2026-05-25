"""General knowledge base (science, CS, study skills, Atlas)."""

from pathlib import Path
from knowledge.kb_loader import KnowledgeBase

TOPICS_DIR = Path(__file__).parent / "general" / "topics"
general_kb = KnowledgeBase(TOPICS_DIR, domain="general")
