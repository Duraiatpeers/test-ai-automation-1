"""
DeepEval sample: 2 tests on the trainer app, run with pytest.

  pytest tool_tests/test_deepeval.py -s

DeepEval uses an LLM "judge" to score answers. Here the judge is llama3.2 on Ollama (local, free).
"""
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.models import OllamaModel
from deepeval.test_case import LLMTestCase

from app_under_test import ask

judge = OllamaModel(model="llama3.2", base_url="http://localhost:11434", temperature=0)


def test_answer_relevancy():
    """Relevance: is the answer about what was asked?"""
    question = "What is prompt injection?"
    answer, _ = ask(question)
    test_case = LLMTestCase(input=question, actual_output=answer)
    assert_test(test_case, [AnswerRelevancyMetric(threshold=0.7, model=judge, async_mode=False)])


def test_faithfulness():
    """Groundedness: is every claim in the answer supported by the retrieved documents?"""
    question = "What is a golden dataset?"
    answer, chunks = ask(question)
    test_case = LLMTestCase(input=question, actual_output=answer, retrieval_context=chunks)
    assert_test(test_case, [FaithfulnessMetric(threshold=0.7, model=judge, async_mode=False)])
