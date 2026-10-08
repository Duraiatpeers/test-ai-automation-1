"""Shared helper: ask the trainer app (rag.py) one question, the same way a user would."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # so "import rag" works
import rag  # noqa: E402

rag.LAB.update(temperature=0, prompt="strong", retrieval="normal")
INDEX = json.loads(rag.INDEX_FILE.read_text(encoding="utf-8"))


def ask(question):
    """Returns (answer, retrieved_chunks)."""
    task, query, k, hits = rag.training_task(INDEX, "", "", question)
    answer, hits, _ = rag.ask(INDEX, None, task, query, echo=False, k=k, hits=hits)
    return answer, [r["text"] for _, r in hits]
