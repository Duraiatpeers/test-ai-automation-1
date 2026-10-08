# Level 1 Curriculum: AI Fundamentals for Testers

## Programme overview
Level 1 "AI Fundamentals for Testers" is the first of three levels in the AI Testing Academy:
Level 1 AI Fundamentals for Testers (16 hours, 2 days) -> Level 2 AI Testing Practitioner (32 hours, 4 days) -> Level 3 Advanced AI Quality Engineering (40 hours, 5 days). Total 88 hours.
Level 1 is intended for the whole testing department. No coding is required.
Purpose: a shared and accurate mental model, so that when a tester looks at an AI feature they can say how it works, where it can fail, and what would need to be true for it to be trustworthy.
Exit standard for Level 1: the participant can read an AI feature and say what could go wrong.

## Why AI testing is a different discipline
A test function that is excellent at conventional software testing does not automatically transfer to AI. The discipline changes at the root:
- there is often no single correct answer;
- the same input can produce different output on consecutive runs;
- the system can change without any code change (for example a model update);
- a feature can pass every review and then fail in production on an input nobody thought to try.
Conventional pass/fail assertions do not reach any of these.

## The evolution of the tester role
AI does not remove the tester; it relocates where their value sits, away from executing cases toward designing the evaluation that decides whether a probabilistic system is fit to ship.
- Conventional tester: writes and executes test cases against a specification; asserts exact expected output (pass or fail); test basis is requirements and acceptance criteria; regression means "code changed, re-run the suite"; biggest risk is coverage gaps and slow regression.
- AI-aware tester: tests AI features largely by inspection; asserts whether output "looks reasonable"; regression meaning is unclear because the model may change without code change; biggest risk is a feature that passes review and fails in production on a different input.
- AI quality engineer: designs evaluation systems that measure AI behaviour continuously; asserts faithfulness, relevance, safety and stability against defined thresholds; test basis is golden datasets, evaluation criteria and a documented risk model; tracks and re-evaluates model, prompt, index and data changes; biggest risk is over-trust in an evaluation set that no longer represents live traffic.
Level 1 moves a conventional tester to a well-informed AI-aware tester, ready for Level 2.

## Module M1.1 GenAI and LLM Fundamentals for Testers (4 hours)
Topics:
- AI, machine learning, deep learning and generative AI: what each term means and how they nest
- How a large language model produces output, and why the same input can produce different output
- Tokens, context windows, temperature and their direct effect on testability
- Model families, versions and what changes when a provider updates a model
- Where AI is genuinely capable, where it is unreliable, and how to tell the difference
Hands-on activities:
- Run the same request repeatedly against one model and record the variance
- Compare two models on one task and document what differs

## Module M1.2 How AI Applications Are Built (4 hours)
Topics:
- The anatomy of an AI feature: prompt, context, model, tools, output handling
- Retrieval-Augmented Generation (RAG): why grounding exists and what it does not fix
- Embeddings, vector search and retrieval in plain terms
- Agents and tool calling: the difference between suggesting and acting
- Where each component can fail, and which failures look identical from the outside
Hands-on activities:
- Trace a working AI feature end to end and map every point at which it could fail
- Break a retrieval step deliberately and observe how the failure presents

## Module M1.3 Prompt Engineering Basics (4 hours)
Topics:
- Anatomy of a prompt: instruction, context, constraints, output format
- System prompts, user prompts and why the distinction matters for testing
- Few-shot examples and their effect on consistency
- Prompt sensitivity: how small changes produce large behavioural shifts
- Reading a prompt as a specification: what it does and does not commit the system to
Hands-on activities:
- Rewrite a weak prompt and measure the change in output consistency
- Given a prompt, write the acceptance criteria you would test it against

## Module M1.4 Responsible AI and Why AI Testing Is Different (4 hours)
Topics:
- Why conventional pass/fail testing breaks down on probabilistic systems
- The quality dimensions that replace it: correctness, groundedness, robustness, safety, fairness, cost
- Responsible AI principles and where testing enforces them
- The regulatory backdrop: ISO/IEC 42001 and the EU AI Act at awareness level
- What a tester is accountable for when the system is non-deterministic
Hands-on activities:
- Take a conventional test case for an AI feature and rewrite it so it can actually pass or fail
- Level 1 knowledge check and readiness review for Level 2

## Level 1 labs
Lab 1 (Level 1, 2 hours) Trace an AI Feature End to End: map every component of a working AI feature and identify each point of possible failure. Deliverable: annotated architecture map and failure-point register.
Lab 2 (Level 1, 2 hours) Variance and Model Comparison: run identical requests repeatedly and across models; quantify the variance a tester must design around. Deliverable: variance report with implications for test design.

## Level 1 assessment
- Daily knowledge checks at the end of each day: scenario-based questions on the day's material.
- Lab deliverables assessed against the lab rubric.
- Level 1 knowledge check at the close of Level 1: applied assessment and the gate to Level 2.

## Prerequisites
Testing fundamentals (test case design, defect lifecycle, unit vs integration vs system testing). Basic understanding of REST APIs and JSON. No prior AI, machine learning or data science background is required. Level 1 requires no coding.

## Suggested two-day schedule (trainer's plan)
Day 1 morning: M1.1 GenAI and LLM Fundamentals, including Lab 2 Variance and Model Comparison.
Day 1 afternoon: M1.2 How AI Applications Are Built, including Lab 1 Trace an AI Feature End to End and the broken-retrieval exercise. End of day knowledge check.
Day 2 morning: M1.3 Prompt Engineering Basics, weak vs strong prompt exercise and writing acceptance criteria from a prompt.
Day 2 afternoon: M1.4 Responsible AI and Why AI Testing Is Different, rewriting a conventional test case, then the Level 1 knowledge check.
