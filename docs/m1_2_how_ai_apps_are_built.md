# M1.2 How AI Applications Are Built

## The anatomy of an AI feature
Almost every AI feature is built from the same five parts. A tester should be able to name each one for any feature under test.
1. Prompt: the instructions sent to the model. Usually a hidden system prompt written by developers plus the user's message, often built from a template.
2. Context: extra information placed into the prompt at run time, such as retrieved documents, conversation history, user profile data or results from earlier steps.
3. Model: the LLM that generates the response (for example GPT, Claude, Llama), with its version and settings such as temperature and maximum tokens.
4. Tools: functions the model can ask the application to run, such as search, database queries, calculators, sending an email or creating a ticket.
5. Output handling: what the application does with the model's text: parsing JSON, applying guardrails and filters, formatting, showing citations, storing it, or triggering actions.
Key insight: the model is only one part. Many AI defects are actually in the prompt template, retrieval, tool integration or output parsing, which are ordinary software and can be tested with ordinary techniques.

## Retrieval-Augmented Generation (RAG)
RAG means: before asking the model, retrieve relevant information from your own documents and put it in the prompt, then instruct the model to answer using that information.
Typical RAG pipeline:
1. Ingestion (offline): load documents, split them into chunks, convert each chunk into an embedding, store chunks and embeddings in a vector store (index).
2. Retrieval (per question): convert the user question into an embedding, find the most similar chunks (top-k), optionally re-rank them.
3. Generation: build a prompt containing the instructions, the retrieved chunks and the question; the model writes the answer, ideally with citations.

## Why grounding exists
Grounding means tying the model's answer to supplied source material. It exists because:
- the model's training data does not include your private or recent documents;
- the model will otherwise invent plausible answers (hallucinate);
- users and auditors need to see where an answer came from (citations);
- updating documents is far cheaper than retraining a model.

## What RAG does not fix
RAG reduces hallucination; it does not eliminate it. Remaining failure modes:
- Retrieval miss: the right chunk exists but is not retrieved, so the model answers from general knowledge or invents.
- Retrieval noise: irrelevant chunks are retrieved and the model blends them into a wrong answer.
- Confident synthesis from nothing: no relevant context at all, yet the model still produces a fluent answer instead of saying "I don't know".
- Unfaithful generation: the right chunk is retrieved but the model misreads, over-generalises or contradicts it.
- Bad source data: outdated, duplicated or conflicting documents are faithfully repeated.
- Chunking problems: a table or procedure split across chunks loses its meaning.
- Access control: a user receives content from documents they are not permitted to see.
- Wrong citations: the answer cites a source that does not actually support it.

## Embeddings, vector search and retrieval in plain terms
An embedding is a list of numbers (a vector, often several hundred numbers long) that represents the meaning of a piece of text. An embedding model is trained so that texts with similar meaning get vectors that are close together.
Example: "How do I reset my password?" and "I forgot my login credentials" have very different words but close embeddings. "Password" and "pass the salt" share letters but have distant embeddings.
Vector search: compare the question's vector against every stored chunk vector using a similarity measure (commonly cosine similarity, from -1 to 1, higher is more similar) and return the top-k closest chunks. Vector databases such as Chroma, pgvector or Azure AI Search do this efficiently at scale.
What testers should know:
- Similarity is not correctness. The most similar chunk can still be the wrong one (for example version 1 of a procedure instead of version 2).
- Embeddings handle meaning well but can miss exact identifiers like part numbers, error codes or names. Many systems combine vector search with keyword search (hybrid search).
- Changing the embedding model, chunk size or top-k changes which chunks are retrieved, so it is a change that needs regression testing.
- Retrieval can be tested on its own: for a set of questions, is the right chunk in the top-k? This is called retrieval recall or context recall.

## Agents and tool calling: suggesting vs acting
Tool calling: the model is given a list of tools with descriptions and parameters. Instead of answering directly, it can output a structured request like "call get_order_status with order_id 123". The application runs the tool and returns the result to the model, which then continues.
Agent: a loop in which the model plans, calls tools, looks at results and decides the next step, until it believes the goal is done.
Suggesting vs acting:
- A suggesting system produces text that a human reads and decides on (a drafted reply, a recommended fix). Errors are caught if the human reviews properly.
- An acting system executes real changes (sends the email, issues a refund, deletes a file, changes a configuration). Errors have direct consequences.
Testing implications for agents: test which tools are allowed and with what permissions, whether the agent asks for confirmation before risky actions, whether it stops (no infinite loops), whether it handles tool errors, the cost of a full run, and whether malicious text in a tool result or document can make it take an unintended action (indirect prompt injection).

## Where each component can fail
- Prompt: ambiguous instructions, conflicting rules, template bugs (missing variable), system prompt leaked or overridden by the user.
- Context and retrieval: wrong, missing, stale or unauthorised chunks; too much context; history truncated; poor chunking.
- Model: hallucination, refusing valid requests, ignoring format instructions, inconsistency between runs, behaviour change after a model update, timeouts and rate limits.
- Tools: wrong tool chosen, wrong parameters, tool error not handled, excessive permissions, action without confirmation.
- Output handling: JSON parse failure, guardrail blocks good answers or misses bad ones, citations not linked to real sources, answer truncated, unsafe content shown.

## Failures that look identical from the outside
The user just sees "a wrong answer". The same symptom can have different root causes:
- Wrong answer because the right document was never retrieved (retrieval failure).
- Wrong answer because the right document was retrieved but misread (generation failure).
- Wrong answer because the document itself is outdated (data failure).
- Wrong answer because a prompt change removed an instruction (prompt regression).
- Wrong answer because the provider updated the model (model change).
To tell them apart you need visibility into the pipeline: the exact prompt sent, the retrieved chunks with scores, the model version and settings, tool calls and timing. This is why tracing and logging are essential for testing AI systems. A defect report for an AI feature should include this trace, not only the question and the answer.

## This trainer app as a worked example
The trainer app you are using is itself a small RAG system:
1. Ingestion: the documents in the docs folder are split into chunks of about 900 characters, each chunk is embedded with the nomic-embed-text model, and the vectors are saved in index.json.
2. Retrieval: your question is embedded and compared with every chunk using cosine similarity; the top 4 chunks are selected.
3. Prompt: a system prompt (the trainer rules) plus the retrieved chunks plus your task are sent to the llama3.2 model.
4. Output: the answer is streamed to the screen with the source file names.
Possible failure points: documents not indexed after a change, a heading separated from its content during chunking, a wrong chunk ranked highest, the model ignoring the "only use the context" rule, the model answering when context is empty, wrong source labels, history pushing the context window.

## Hands-on: trace a working AI feature end to end (Lab 1)
1. Ask the trainer app a question, then type /trace.
2. Record: the model and temperature, retrieval mode, the retrieved chunks with scores and sources, prompt tokens, output tokens and latency.
3. Draw the pipeline: docs -> chunks -> embeddings -> index -> query embedding -> top-k -> prompt -> model -> output.
4. For each step, write at least one way it could fail and how you would detect it. This is your failure-point register.

## Hands-on: break a retrieval step deliberately
1. Ask a question and note the answer quality and sources.
2. /break off (no context is retrieved) and ask the same question. Does the model admit it lacks information, or answer anyway?
3. /break noise (random, irrelevant chunks) and ask again. Does it blend irrelevant content into a confident answer?
4. /break worst (the least relevant chunks) and ask again.
5. /break fix to restore. Write down how each failure presented to the user, and whether a user could tell anything was wrong. This shows why retrieval must be tested separately from generation.

## Key takeaways
- An AI feature = prompt + context + model + tools + output handling; test each part.
- RAG grounds answers in your documents but does not remove hallucination.
- Embeddings measure similarity of meaning, not correctness.
- Acting agents carry far more risk than suggesting systems.
- The same wrong answer can have different root causes; you need traces to diagnose.
