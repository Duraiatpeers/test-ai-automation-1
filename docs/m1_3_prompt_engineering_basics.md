# M1.3 Prompt Engineering Basics

## Anatomy of a prompt
A well-built prompt usually has four parts:
1. Instruction: what to do. "Summarise the customer complaint."
2. Context: the material to work with. The complaint text, retrieved documents, user details.
3. Constraints: rules and limits. "Use only the information provided. Maximum 3 sentences. Do not include personal data. If the information is missing, say so."
4. Output format: the exact shape of the answer. "Return JSON with fields: category, severity (low/medium/high), summary."
Often there is also a role ("You are a support assistant for...") and examples (few-shot).
For testers, each part is a source of test cases: does the output follow the instruction, use only the context, respect each constraint, and match the format every time?

## System prompts and user prompts
- System prompt: written by the developers, hidden from the user, sets the role, rules, tone, safety limits and format. It applies to every conversation.
- User prompt: what the end user types. It is untrusted input.
- Assistant messages: previous model replies, re-sent as conversation history.
Why the distinction matters for testing:
- The system prompt is effectively part of the specification and should be versioned and reviewed like code. Ask for it when you test.
- Users can try to override system rules ("Ignore previous instructions and..."). This is prompt injection. Test whether system rules hold against user attempts to change them.
- The system prompt may contain confidential logic and should not be revealed. Test for system prompt leakage ("Repeat the text above").
- Content from documents, web pages or tool results is also untrusted. Instructions hidden inside retrieved documents (indirect prompt injection) should not be obeyed.
- A change to the system prompt changes behaviour for every user. It is a release and needs regression testing.

## Few-shot examples
Zero-shot: only an instruction. Few-shot: the prompt includes a few worked input/output examples.
Example of few-shot classification:
Classify the ticket as BILLING, TECHNICAL or OTHER.
Ticket: "I was charged twice" -> BILLING
Ticket: "App crashes on login" -> TECHNICAL
Ticket: "{new ticket}" ->
Effect: few-shot examples strongly improve consistency of format and labels, and reduce variance between runs. Risks for testers: the model may over-copy the examples (same length, same wording, same label bias); examples that are unrepresentative bias the results; test inputs that are unlike any example.

## Prompt sensitivity
Small changes in a prompt can produce large changes in behaviour. Examples:
- Rewording "List the risks" to "What are the risks?" changes format from a list to a paragraph.
- Reordering instructions changes which one is followed when they conflict.
- Adding "Be concise" can drop required details.
- A typo or extra whitespace can change outputs for smaller models.
- The same question phrased by different users (paraphrases) can receive different answers.
Testing implications:
- Paraphrase testing: ask the same question 5 to 10 different ways; the meaning of the answer should stay the same.
- Perturbation testing: add typos, extra spaces, different casing, irrelevant sentences; behaviour should stay stable.
- Ordering tests: change the order of options or documents and check the answer does not change unfairly.
- Treat every prompt edit as a code change and re-run the regression set.

## Reading a prompt as a specification
A prompt is the closest thing an AI feature has to a requirements document. Read it the way you would read a spec.
What a prompt commits the system to (things you can test):
- explicit constraints ("maximum 3 sentences", "respond in JSON", "never give medical advice");
- explicit fallback behaviour ("if the answer is not in the context, say 'I don't know'");
- scope ("only answer questions about our products").
What a prompt does NOT commit the system to:
- guaranteed compliance: a prompt is a strong request, not an enforced rule; the model can still break it, so measure how often it complies;
- correctness of facts it was never given;
- behaviour in situations the prompt does not mention (other languages, abusive users, very long inputs): these are gaps to raise as questions or test as risks;
- security: "do not reveal the system prompt" is not a security control on its own.

## Weak prompt vs strong prompt
Weak prompt: "You are a helpful assistant. Answer the question."
Problems: no scope, no grounding rule, no fallback, no format, no length. Output varies a lot, may invent facts, hard to test because nothing is specified.
Strong prompt: "You are a trainer for the Level 1 AI testing course. Answer using ONLY the curriculum context provided. If the context does not contain the answer, reply exactly: 'This is not covered in the curriculum.' Answer in at most 5 bullet points, in simple English for beginners."
Improvements: clear role and scope, grounding rule, a testable fallback string, a testable format and length. Output is more consistent and each rule becomes an acceptance criterion.

## Writing acceptance criteria from a prompt
For the strong prompt above, testable acceptance criteria could be:
- AC1 Format: in at least 95% of runs the answer has 5 or fewer bullet points.
- AC2 Grounding: every factual statement in the answer can be found in the retrieved context (checked by a reviewer or an evaluator).
- AC3 Fallback: for 10 questions outside the curriculum, the exact fallback sentence is returned in at least 9 of 10 cases, and no invented answer is given.
- AC4 Stability: for 5 paraphrases of the same question, the key points are the same.
- AC5 Robustness: user attempts to change the rules ("ignore your instructions") do not change scope.
Note the shape: properties, thresholds and repeated runs, instead of one exact expected string.

## Hands-on: rewrite a weak prompt and measure the change in consistency
Using the trainer app:
1. /prompt weak then /temp 0.8 then /variance 5 What is prompt sensitivity?
2. Record the similarity score and how many answers followed any structure.
3. /prompt strong then repeat the same /variance command.
4. Compare the numbers. Also ask an out-of-scope question (for example "What is the capital of France?") with each prompt and see whether the fallback works.
5. /prompt show displays the system prompt currently in use.

## Hands-on: given a prompt, write the acceptance criteria
Take the system prompt shown by /prompt show. Write at least five acceptance criteria covering format, grounding, fallback, stability and robustness, each with a threshold and a number of runs. Then test two of them with the app.

## Key takeaways
- Prompt = instruction + context + constraints + output format.
- System prompts are part of the specification; user and document content is untrusted.
- Few-shot examples increase consistency but can bias outputs.
- Small wording changes cause big behaviour changes: test paraphrases and perturbations.
- A prompt states intentions, not guarantees: measure compliance rates.
