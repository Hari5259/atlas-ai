"""Print Atlas knowledge base stats (data loads automatically at startup)."""

from knowledge.math.math_kb import MathKnowledgeBase
from knowledge.general_kb import general_kb

if __name__ == "__main__":
    math = MathKnowledgeBase()
    print(f"Mathematics entries: {math.count}")
    print(f"  Topics: {', '.join(math.topics)}")
    print(f"General entries:   {general_kb.count}")
    print(f"  Topics: {', '.join(general_kb.topics)}")
    print(f"Total:             {math.count + general_kb.count}")
