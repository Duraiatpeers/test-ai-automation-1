"""promptfoo calls call_api() for every test: we pass the prompt to the trainer app and return its answer."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # so "import app_under_test" works
from app_under_test import ask  # noqa: E402


def call_api(prompt, options, context):
    answer, _ = ask(prompt)
    return {"output": answer}
