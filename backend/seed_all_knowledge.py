"""Print Atlas knowledge base stats (data loads automatically at startup)."""

from pathlib import Path
import json

from knowledge.math.math_kb import MathKnowledgeBase
from knowledge.general_kb import general_kb

if __name__ == "__main__":
    math = MathKnowledgeBase()
    math_files = list((Path(__file__).parent / "knowledge/math/topics").glob("*.json"))
    gen_files = list((Path(__file__).parent / "knowledge/general/topics").glob("*.json"))

    print("=" * 50)
    print("ATLAS KNOWLEDGE BASE")
    print("=" * 50)
    print(f"Mathematics:  {math.count:4d} entries  ({len(math_files)} files)")
    print(f"  Topics: {', '.join(math.topics)}")
    print(f"General:      {general_kb.count:4d} entries  ({len(gen_files)} files)")
    print(f"  Topics: {', '.join(general_kb.topics[:15])}...")
    print("-" * 50)
    print(f"TOTAL:        {math.count + general_kb.count:4d} factual entries")
    print("=" * 50)

    index_path = Path(__file__).parent / "knowledge/INDEX.json"
    if index_path.exists():
        with open(index_path, encoding="utf-8") as f:
            meta = json.load(f)
        print(f"Indexed domains: {len(meta.get('domains', []))}")
