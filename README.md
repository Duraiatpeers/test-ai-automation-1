# Level 1 AI Testing Trainer (local RAG on Ollama)

A small RAG app that (1) teaches "Level 1 - AI Fundamentals for Testers" from the files in `docs/`,
and (2) acts as the **AI system under test** in the Level 1 labs.

## Setup
```
pip install -r requirements.txt
python rag.py index      # re-run whenever docs/ changes
python -m streamlit run app.py   # browser UI (recommended for demos)
python rag.py            # or the terminal chat
```

## Browser UI (`app.py`)
The sidebar holds the lab settings (temperature, weak/strong system prompt, retrieval mode) and a
"Rebuild index" button. Each lab has its own tab, so no commands are needed:

| Tab | Exercise |
|---|---|
| Trainer | Ask / teach / quiz / exercise, plus "Show modules & labs" |
| Variance (M1.1) | Same question N times with similarity metrics; compare at temperature 0.9 vs 0 |
| Compare models (M1.1) | `CHAT_MODEL` vs `COMPARE_MODEL` side by side |
| Trace (M1.2) | Retrieved chunks, scores, exact prompt, tokens and latency of the last request |
| Break retrieval (M1.2) | Same question under normal / off / noise / worst retrieval, side by side |
| Weak vs strong prompt (M1.3) | Same question with both system prompts, side by side |

The CLI commands below remain available in `python rag.py`.
Models used: `llama3.2` (chat) and `nomic-embed-text` (embeddings). For `/compare`, also run
`ollama pull llama3.2:1b` (1.3 GB), or set `COMPARE_MODEL` in rag.py to another installed model.

## Knowledge source
`docs/` contains the Level 1 curriculum plus starter teaching notes for M1.1-M1.4 and a glossary.
Add or replace files with your own material (.docx/.pdf/.txt/.md), then run `python rag.py index`.
Markdown `#`/`##` headings and Word heading styles keep sections together for better retrieval.

## Training commands
| Command | Use |
|---|---|
| `/topics` | Module and lab outline |
| `/teach <topic>` | Short lesson |
| `/quiz <topic>` | 5 scenario-based MCQs with answers |
| `/exercise <topic>` | Hands-on task |
| any text | Ask a question |

## Lab commands (trainees test the app itself)
| Exercise (curriculum) | Steps in the app |
|---|---|
| M1.1 / Lab 2: variance | `/temp 0.9` then `/variance 5 What is a token?`; repeat after `/temp 0`; compare similarity and distinct answers |
| M1.1 / Lab 2: model comparison | `/compare Explain temperature in 3 bullets` and document what differs |
| M1.2 / Lab 1: trace end to end | Ask a question, then `/trace` (or `/trace full` for the exact prompt); build a failure-point register |
| M1.2: break retrieval | `/break off`, `/break noise`, `/break worst`, ask the same question each time; `/break fix` to restore |
| M1.3: weak vs strong prompt | `/prompt weak` + `/variance 5 ...` vs `/prompt strong` + same; try an out-of-scope question with both; `/prompt show` |
| M1.3: acceptance criteria | `/prompt show`, write ACs with thresholds, then test them with `/variance` |
| M1.4: rewrite a test case | Pick a question, run `/variance 5`, and turn the exact-match expectation into properties + a pass rate |

## Quality test demo (`quality_tests.py`)
Two simple test cases per dimension: correctness, relevance & completeness, groundedness,
robustness, safety, fairness and privacy. Each test checks properties of the answer, not exact text.
```
python quality_tests.py                  # all dimensions
python quality_tests.py privacy fairness # just some
```

## Resource tuning (top of rag.py)
`CHAT_MODEL = "llama3.2:1b"` for less RAM, `NUM_CTX = 2048`, `TOP_K = 3`.

## Tool samples (`tool_tests/`)
The same kind of checks written with real AI-testing tools. All judges run locally on Ollama.

| File | Tool | Tests |
|---|---|---|
| `test_deepeval.py` | DeepEval + pytest | answer relevancy, faithfulness |
| `test_ragas.py` | Ragas + pytest | faithfulness, context recall (retrieval) |
| `promptfoo/promptfooconfig.yaml` | promptfoo (YAML) | prompt injection, safety (LLM rubric) |

```
pip install -r requirements-tools.txt
pytest tool_tests -s                       # DeepEval + Ragas
cd tool_tests/promptfoo && npx promptfoo@latest eval
```
