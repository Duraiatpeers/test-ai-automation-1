# Glossary of AI Testing Terms (Level 1)

## Core AI terms
- LLM (Large Language Model): a deep learning model trained on large amounts of text to predict the next token; used to generate text.
- Generative AI: AI that creates new content (text, images, code, audio).
- Token: a piece of text (word or part of a word) the model processes; about 4 characters of English.
- Context window: the maximum number of tokens the model can take in one request, including the answer.
- Temperature: sampling setting controlling randomness; 0 is focused and repeatable, higher is more varied.
- Inference: running a trained model to get an output.
- Training cut-off: the date after which the model has no built-in knowledge.
- Hallucination: fluent output that is false or not supported by the provided sources.
- Non-determinism: the same input can produce different outputs.

## Application terms
- System prompt: hidden developer instructions that set role, rules and format.
- User prompt: the end user's input; untrusted.
- Few-shot prompting: including worked examples in the prompt.
- RAG (Retrieval-Augmented Generation): retrieving relevant document chunks and adding them to the prompt so the answer is grounded.
- Grounding / groundedness / faithfulness: the degree to which an answer is supported by the supplied sources.
- Embedding: a vector of numbers representing the meaning of text.
- Vector store / vector database: storage that finds the most similar embeddings (Chroma, pgvector, Azure AI Search).
- Chunk: a piece of a document stored and retrieved in RAG.
- Top-k: the number of most similar chunks retrieved.
- Cosine similarity: a measure of how close two embeddings are, higher means more similar.
- Tool calling / function calling: the model requests the application to run a function.
- Agent: a system where the model plans and calls tools in a loop to achieve a goal.
- Guardrail: a check before or after the model that blocks or modifies unsafe or invalid input or output.

## Testing terms
- Oracle: the means of deciding whether an output is correct.
- Golden dataset: a curated, representative set of test inputs with reference answers or expected properties.
- Property-based assertion: checking characteristics of an output (contains X, valid JSON, under N words) instead of exact text.
- Threshold: the minimum acceptable score or pass rate (for example 95% of runs).
- Variance testing: running the same input many times to measure output variability.
- Paraphrase testing: asking the same thing in different words and comparing answers.
- Perturbation testing: adding small changes (typos, noise) to check stability.
- Prompt injection: input that tries to override the system's instructions; indirect when it arrives via documents or tool results.
- System prompt leakage: the system prompt being revealed to users.
- Counterfactual testing: changing only one attribute (such as a name or gender) and comparing outputs, used for fairness.
- LLM-as-judge: using an LLM with a rubric to score another model's output.
- Retrieval failure vs generation failure: the right information was not retrieved vs it was retrieved but the model used it wrongly.
- Model drift / behaviour change: the system's behaviour changes over time, for example after a model update.
- Trace: a record of every step of an AI request (prompt, retrieved chunks, model, tool calls, timings).
