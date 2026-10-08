"""
Ragas sample: 2 RAG metrics on the trainer app, run with pytest.

  pytest tool_tests/test_ragas.py -s

Ragas is built for RAG apps. Each metric returns a score from 0 to 1, and we assert a threshold.
The judge LLM runs locally on Ollama (through its OpenAI-compatible API).
"""
import instructor
from openai import AsyncOpenAI
from ragas.llms import llm_factory
from ragas.metrics.collections import ContextRecall, Faithfulness

from app_under_test import ask

# ---- judge setup (Ollama) --------------------------------------------------------
client = AsyncOpenAI(base_url="http://localhost:11434/v1", api_key="ollama")   # key is not checked

# Small local models need Ollama to FORCE the JSON shape Ragas expects. Ollama does that for
# response_format "json_schema", so we convert the request to that format.
_create = client.chat.completions.create


async def _create_with_schema(*args, response_format=None, **kwargs):
    if response_format and "schema" in response_format:
        response_format = {"type": "json_schema",
                           "json_schema": {"name": "output", "schema": response_format["schema"]}}
    return await _create(*args, response_format=response_format, **kwargs)


client.chat.completions.create = _create_with_schema
judge = llm_factory("llama3.2", provider="openai", client=client, temperature=0)
judge.client = instructor.from_openai(client, mode=instructor.Mode.JSON_SCHEMA)


# ---- tests ------------------------------------------------------------------------
def test_faithfulness():
    """Groundedness (generation): share of the answer's claims supported by the retrieved chunks."""
    question = "What is temperature in an LLM?"
    answer, chunks = ask(question)
    result = Faithfulness(llm=judge).score(user_input=question, response=answer, retrieved_contexts=chunks)
    print(f"\nfaithfulness = {result.value:.2f}\n{answer}")
    assert result.value >= 0.7


def test_context_recall():
    """Retrieval: did the app fetch the chunks needed to give the reference (expected) answer?"""
    question = "What is a golden dataset?"
    reference = ("A golden dataset is a curated, representative set of test inputs "
                 "with reference answers or expected properties.")
    _, chunks = ask(question)
    result = ContextRecall(llm=judge).score(user_input=question, retrieved_contexts=chunks, reference=reference)
    print(f"\ncontext recall = {result.value:.2f}")
    assert result.value >= 0.8
