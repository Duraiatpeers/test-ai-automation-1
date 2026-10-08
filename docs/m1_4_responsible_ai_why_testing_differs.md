# M1.4 Responsible AI and Why AI Testing Is Different

## Why conventional pass/fail testing breaks down on probabilistic systems
Conventional testing assumes: a fixed input produces a fixed, known output, and the test compares actual output with expected output exactly.
AI systems break each assumption:
- No single correct answer: "Summarise this report" has many acceptable summaries. An exact-match assertion fails good answers.
- Non-determinism: the same input gives different outputs, so a test can pass on one run and fail on the next (flaky by nature).
- Change without code change: a model update, a prompt edit or new documents in the index can change behaviour while the code is identical.
- Open input space: users can type anything, in any language, with any intent. You cannot enumerate all inputs, so failures appear on inputs nobody tried.
- Plausible wrongness: wrong answers are fluent and confident, so "looks reasonable" is not a valid oracle.
What replaces exact pass/fail:
- assert properties (contains the required fact, is valid JSON, under 100 words, cites a real source, no personal data);
- assert thresholds over many runs and many inputs (faithfulness at least 0.9 across a 50-question set; correct refusal in at least 95% of out-of-scope questions);
- compare against a golden dataset of representative questions with reference answers or required facts;
- use human review or an evaluator model with a clear rubric for judgement-based qualities.

## The quality dimensions that replace pass/fail
- Correctness: is the answer factually and functionally right? Measured against reference answers or required facts.
- Groundedness (faithfulness): is every claim supported by the supplied source material, with no invented content? Key for RAG.
- Robustness: does behaviour stay acceptable under paraphrases, typos, unusual inputs, long inputs and adversarial attempts such as prompt injection?
- Safety: does the system avoid harmful, toxic or dangerous output, refuse inappropriate requests, protect personal and confidential data, and resist misuse?
- Fairness: does quality stay consistent across user groups (for example gender, age, nationality, language)? Swap only the group attribute in a test and compare the outputs.
- Cost: tokens and money per request, plus latency. A correct answer that costs ten times the budget or takes 30 seconds is a defect.
Each dimension needs a defined metric, a threshold and a test set. Level 2 goes deep on each; Level 1 is about knowing they exist and why.

## Rewriting a conventional test case so it can actually pass or fail
Feature: an AI assistant that answers questions from the product manual.
Conventional (broken) test case:
- Step: ask "What is the warranty period?"
- Expected result: "The warranty period is 2 years from the date of purchase."
Why it breaks: a correct answer like "You get a 24-month warranty starting on the purchase date" fails exact match; a single run hides variance; nothing tests the "not in the manual" case.
Rewritten AI test case:
- Precondition: model version, temperature and system prompt version recorded; manual v3 indexed.
- Step: ask "What is the warranty period?" and 4 paraphrases ("How long is the guarantee?" etc.). Run each 3 times (15 runs).
- Expected result (properties): the answer states 2 years / 24 months; it mentions the purchase date as the start; it cites the manual warranty section; it contains no other durations; under 80 words.
- Pass criterion: at least 14 of 15 runs meet all properties, and 0 runs state a wrong duration.
- Negative test: ask "What is the warranty on batteries bought separately?" (not in the manual). Expected: the assistant says the manual does not cover it; pass if no invented duration in any of 5 runs.

## Responsible AI principles and where testing enforces them
Common Responsible AI principles (used by Microsoft, Google, OECD, the EU and many companies) and the tests that give them teeth:
- Fairness: counterfactual and paired tests across groups; compare quality metrics per group.
- Reliability and safety: robustness tests, harmful-content tests, refusal tests, behaviour under failure of dependencies.
- Privacy and security: tests for personal data leakage in outputs and logs, prompt injection, system prompt leakage, access control in retrieval.
- Transparency and explainability: users are told they are using AI; citations point to real supporting sources; limitations are documented.
- Accountability: every model, prompt and dataset version is recorded; test evidence is kept; a human owner signs off.
- Human oversight: humans can review, override and stop the system where needed, and the escalation path actually works.
Principles on a poster mean nothing until a test checks them. The tester turns principles into measurable checks and evidence.

## The regulatory backdrop (awareness level)
ISO/IEC 42001: an international standard (published 2023) for an AI Management System. Like ISO 27001 for information security, it defines organisational controls for developing and using AI responsibly: risk assessment, impact assessment, data management, monitoring, documentation and continual improvement. Testers contribute evidence that controls actually operate, such as test reports, evaluation results and version records.
EU AI Act: European Union law on AI, which entered into force in 2024 with obligations phased in over the following years. It takes a risk-based approach with tiers:
- Unacceptable risk: prohibited practices (for example social scoring, manipulative techniques).
- High risk: for example AI in critical infrastructure, employment, education, safety components of products. These carry strict obligations: risk management, data quality, technical documentation, logging, human oversight, accuracy, robustness and cybersecurity, which all need testing evidence.
- Limited risk: transparency obligations (for example users must be told they are interacting with an AI, and AI-generated content must be identifiable).
- Minimal risk: no specific obligations (for example spam filters).
There are also specific obligations for general-purpose AI models. At Level 1 you only need to know that these frameworks exist, that they demand evidence, and that testing produces much of that evidence. Level 3 covers verification in depth. This is not legal advice; compliance decisions belong to legal and governance teams.

## What a tester is accountable for when the system is non-deterministic
A tester cannot guarantee that an AI system will never give a wrong answer. A tester is accountable for:
- defining what "good enough" means with stakeholders: metrics, thresholds, and the test set they are measured on;
- testing a representative and risky set of inputs, including out-of-scope, adversarial and fairness cases, run multiple times;
- recording the full test environment: model version, prompt version, settings, data and index version;
- reporting results as rates with evidence ("faithfulness 0.92 on 60 questions; 3 hallucinations found, examples attached") rather than "passed";
- stating residual risk honestly: what was not tested and what could still go wrong;
- re-testing when the model, prompt, data or settings change.
The shift: from "I proved it works" to "I measured how well it works, under which conditions, with what remaining risk".

## Level 1 knowledge check readiness
By the end of Level 1 you should be able to:
- explain how an LLM generates text and why outputs vary;
- explain tokens, context window and temperature and their effect on testing;
- name the parts of an AI feature and the failure points of a RAG pipeline;
- distinguish a retrieval failure from a generation failure;
- read a prompt as a specification and write acceptance criteria with thresholds;
- rewrite an exact-match test case into a property-and-threshold test case;
- name the quality dimensions: correctness, groundedness, robustness, safety, fairness, cost;
- describe at awareness level what ISO/IEC 42001 and the EU AI Act expect.
Exit standard: you can read an AI feature and say what could go wrong.

## Key takeaways
- Exact pass/fail does not fit probabilistic systems; use properties, thresholds, repeated runs and golden datasets.
- Six quality dimensions: correctness, groundedness, robustness, safety, fairness, cost.
- Testing is where Responsible AI principles become real.
- Regulation demands evidence; testers produce much of it.
- Report measured rates and residual risk, not "pass".
