# M1.1 GenAI and LLM Fundamentals for Testers

## AI, machine learning, deep learning and generative AI: how they nest
Think of four nested circles.
- Artificial Intelligence (AI): the broad field of making machines perform tasks that normally need human intelligence. Includes old rule-based "expert systems" with hand-written if/then rules.
- Machine Learning (ML): a subset of AI where the system learns patterns from data instead of being explicitly programmed. Example: a spam filter trained on labelled emails. Classic ML outputs are usually a class or a number (spam / not spam, a price).
- Deep Learning (DL): a subset of ML that uses large neural networks with many layers. It powers image recognition, speech-to-text and modern language models.
- Generative AI (GenAI): a subset of deep learning whose models generate new content (text, images, code, audio) rather than only classifying. Large Language Models (LLMs) such as GPT, Claude, Llama, Gemini and Mistral are generative AI for text.
Why testers care: a classic ML classifier has a finite set of correct answers that can be measured with accuracy, precision and recall. A generative model produces open-ended output where many different answers can be acceptable and some wrong answers look perfectly fluent. That is why GenAI testing needs new techniques.

## How a large language model produces output
An LLM is trained on huge amounts of text to do one thing: predict the next token given all the tokens before it.
When you send a prompt:
1. The text is split into tokens.
2. The model computes a probability for every possible next token (for example "Paris" 92%, "the" 3%, "a" 1%...).
3. One token is picked from that distribution (this is called sampling).
4. The chosen token is appended and the process repeats, one token at a time, until a stop condition.
Important consequences for testers:
- The model does not look facts up. It generates what is statistically plausible. Plausible is not the same as true, which is why hallucinations happen.
- The model has no memory between calls. "Memory" in chat apps is the application re-sending previous messages inside the prompt.
- The model's knowledge stops at its training cut-off date unless the application supplies fresh information (for example through RAG).

## Why the same input can produce different output
Because the next token is sampled from a probability distribution, two runs of the same prompt can take a different path at the first uncertain token, and from there the answers diverge. Other causes:
- Temperature and other sampling settings above zero.
- Different model version behind the same name (provider updated the model).
- Changes in hidden inputs: system prompt, retrieved documents, conversation history, tool results.
- Infrastructure effects: batching and hardware can cause tiny numeric differences even at temperature 0, so "temperature 0" is near-deterministic, not a guarantee.
Testing implication: one passing run proves very little. You must run the same test several times and judge the distribution of results (for example "9 of 10 runs met the criteria"), not a single output.

## Tokens
A token is a chunk of text the model works with, often a word or part of a word. Rough rule for English: 1 token is about 4 characters or 0.75 words, so 100 tokens is roughly 75 words. Numbers, code and non-English text often use more tokens.
Why tokens matter for testing:
- Cost: cloud providers bill per input token and per output token. Cost is a quality attribute you can test.
- Limits: the context window and maximum output length are measured in tokens. Long answers can be cut off mid-sentence when the output limit is reached.
- Latency: more output tokens means a longer response time, because tokens are generated one at a time.
- Odd failures: tasks like counting letters in a word or reversing strings are hard for LLMs because they see tokens, not letters.

## Context window
The context window is the maximum number of tokens the model can consider at once: system prompt + conversation history + retrieved documents + the user question + the answer being generated. Sizes range from a few thousand to over a million tokens depending on the model.
What happens when it fills up: the application must drop or summarise something (often the oldest chat messages), or the request fails. Information in the middle of very long contexts is sometimes used less reliably than information at the start or end ("lost in the middle").
Test ideas: long conversations where an early instruction must still be honoured; very large documents; check the behaviour at and beyond the limit; check that truncation does not silently drop the system prompt or safety rules.

## Temperature and other sampling settings
Temperature controls how random the token selection is.
- Temperature 0 (or close): almost always picks the most likely token. Output is focused and repeatable. Good for extraction, classification and factual Q&A.
- Temperature around 0.7 to 1.0: more varied and creative output, more variance between runs, and higher risk of drifting off facts.
Related settings: top_p and top_k limit which tokens are allowed to be sampled; seed fixes the random generator in some systems for repeatability; max tokens caps output length.
Testing implication: always record the sampling settings as part of the test environment, exactly like you would record a browser version. A test result without the temperature and model version is not reproducible.

## Direct effect on testability: summary
- Non-determinism: assert properties and thresholds over multiple runs, not exact strings.
- Tokens: test for cost, truncation and latency.
- Context window: test long inputs, long chats and what gets dropped.
- Temperature: control and record it; test at the production setting, not just at 0.

## Model families, versions and provider updates
Model families: GPT (OpenAI), Claude (Anthropic), Gemini (Google), Llama (Meta, open weights), Mistral, Phi (Microsoft), Qwen and others. Within a family there are sizes (for example Llama 3.2 1B and 3B parameters): smaller models are cheaper and faster but weaker at reasoning and following complex instructions.
Versions: providers release new versions and retire old ones. Some offer pinned dated snapshots; a generic alias (like "latest") can silently point to a new model.
What can change when a provider updates a model, with no code change on your side:
- answer style, length and formatting (which can break parsers expecting JSON or a fixed format);
- refusal behaviour (more or less willing to answer);
- factual accuracy, sometimes better overall but worse on your specific cases;
- latency and cost per request;
- how strictly the system prompt is followed.
Testing implication: a model version change is a release. Pin model versions where possible, keep a regression set of prompts and expected properties, and re-run it whenever the model, the prompt, the retrieved data or the settings change.

## Where AI is genuinely capable and where it is unreliable
Usually strong: summarising, rewriting and translating text; drafting; extracting fields from text; classifying intent; explaining concepts; generating boilerplate code; answering questions when the correct information is supplied in the prompt.
Usually unreliable: precise facts not supplied in the prompt (names, dates, figures, citations, URLs); arithmetic and counting; recent events after the training cut-off; long multi-step logic; consistency across many runs; knowing when it does not know; following many constraints at once.
How to tell the difference as a tester:
- Can the answer be verified against a source? If the model was given the source, test groundedness. If not, treat factual claims as suspect.
- Does it stay correct when you paraphrase the question or run it again? Stability is evidence of capability; flip-flopping is evidence of guessing.
- Confidence of tone is not evidence of correctness. LLMs sound equally confident when they are wrong.
- Ask questions whose answer is NOT in the available information. A trustworthy system says it does not know; an unreliable one invents an answer.

## Hands-on: run the same request repeatedly and record the variance (Lab 2)
Using the trainer app:
1. /temp 0.8 then /variance 5 What is a context window?
2. Record: how many distinct answers, average semantic similarity, word overlap, length range, latency range.
3. /temp 0 and repeat the same /variance command. Compare.
4. Write down: what would a single-run test have told you? What threshold would you set (for example "at least 4 of 5 runs mention the token limit")?

## Hands-on: compare two models on one task (Lab 2)
Using the trainer app: /compare Explain temperature to a new tester in 3 bullet points.
Document for each model: correctness, whether it followed the "3 bullet points" constraint, tone, length, output tokens and latency. Note which differences would break a test that asserted exact text, and which differences actually matter to a user.

## Key takeaways for testers
- An LLM predicts plausible next tokens; it does not look things up.
- The same input can give different output, so test distributions, not single runs.
- Record model version, temperature and prompt as part of the test environment.
- A model update is a change that needs regression testing, even with no code change.
- Fluent and confident does not mean correct.
