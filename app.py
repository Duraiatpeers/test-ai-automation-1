"""
Browser UI for the Level 1 trainer and test lab. Same pipeline as rag.py, no CLI needed.

  python -m streamlit run app.py
"""
import json

import streamlit as st

import rag

st.set_page_config(page_title="AI Testing Trainer", page_icon="🧪", layout="wide")

TRAINING_MODES = {"Ask a question": "", "Teach a topic": "/teach", "Quiz on a topic": "/quiz",
                  "Exercise on a topic": "/exercise"}


# ---- state ----------------------------------------------------------------
@st.cache_resource
def load_index():
    if not rag.INDEX_FILE.exists():
        return None
    return json.loads(rag.INDEX_FILE.read_text(encoding="utf-8"))


ss = st.session_state
ss.setdefault("temperature", rag.LAB["temperature"])
ss.setdefault("prompt", rag.LAB["prompt"])
ss.setdefault("retrieval", rag.LAB["retrieval"])
ss.setdefault("history", [])   # what the model sees (rag.ask format)
ss.setdefault("chat", [])      # what the page shows
ss.setdefault("trace", None)


def apply_settings(**overrides):
    """Copy this browser session's settings into rag.LAB (shared module state) before each request."""
    rag.LAB.update(temperature=ss.temperature, prompt=ss.prompt, retrieval=ss.retrieval)
    rag.LAB.update(overrides)


def run(index, task, query, history=None, model=rag.CHAT_MODEL, k=rag.TOP_K, hits=None, **overrides):
    """One RAG request, streamed into the page. Returns (text, hits, stats) or None on error."""
    apply_settings(**overrides)
    box, buf = st.empty(), []

    def on_token(token):
        buf.append(token)
        box.markdown("".join(buf) + " ▌")

    try:
        with st.spinner("Retrieving context and generating..."):
            result = rag.ask(index, history, task, query, model=model, echo=False, k=k, hits=hits,
                             on_token=on_token)
    except OSError as e:
        box.empty()
        st.error(f"Could not reach Ollama at {rag.OLLAMA_URL} ({e}). Start it with `ollama serve`.")
        return None
    box.markdown(result[0])
    ss.trace = rag.LAB["last_trace"]
    return result


def footer(hits, stats):
    sources = ", ".join(sorted({r["source"] for _, r in hits})) or "none"
    st.caption(f"Sources: {sources} · {stats['output_tokens']} tokens · {stats['seconds']}s")


def hits_table(hits):
    if not hits:
        st.info("No chunks retrieved.")
        return
    st.dataframe([{"score": "random" if s is None else round(s, 3), "source": r["source"],
                   "chunk": " ".join(r["text"].split())[:200]} for s, r in hits],
                 hide_index=True, width="stretch")


# ---- sidebar: lab settings -------------------------------------------------
index = load_index()
with st.sidebar:
    st.header("🧪 Lab settings")
    st.slider("Temperature (M1.1)", 0.0, 2.0, step=0.1, key="temperature",
              help="0 = most repeatable. Higher = more varied answers.")
    st.radio("System prompt (M1.3)", list(rag.PROMPTS), key="prompt", horizontal=True,
             help="'weak' has no scope, grounding, fallback or format rules.")
    with st.expander("Show active system prompt"):
        st.code(rag.PROMPTS[ss.prompt], language=None, wrap_lines=True)
    st.radio("Retrieval (M1.2)", list(rag.RETRIEVAL_MODES), key="retrieval",
             format_func=lambda m: f"{m}: {rag.RETRIEVAL_MODES[m]}",
             help="Deliberately break retrieval to see how the answer degrades.")
    if ss.retrieval != "normal":
        st.warning(f"Retrieval is BROKEN ({ss.retrieval})")
    st.divider()
    st.caption(f"Chat model: `{rag.CHAT_MODEL}` · Embeddings: `{rag.EMBED_MODEL}`")
    st.caption(f"Index: {len(index) if index else 0} chunks from `{rag.DOCS_DIR.name}/`")
    if st.button("Rebuild index from docs/", width="stretch"):
        with st.spinner("Reading docs and embedding chunks..."):
            try:
                rag.build_index()
                load_index.clear()
                st.rerun()
            except (OSError, SystemExit) as e:
                st.error(f"Index build failed: {e}")
    if st.button("Clear conversation", width="stretch"):
        ss.history, ss.chat = [], []
        st.rerun()

st.title(rag.TRAINING_LEVEL)
if index is None:
    st.error("No index yet. Click **Rebuild index from docs/** in the sidebar.")
    st.stop()

tabs = st.tabs(["🎓 Trainer", "🎲 Variance (M1.1)", "⚖️ Compare models (M1.1)", "🔍 Trace (M1.2)",
                "💥 Break retrieval (M1.2)", "✍️ Weak vs strong prompt (M1.3)"])

# ---- Trainer ---------------------------------------------------------------
with tabs[0]:
    left, right = st.columns([3, 1])
    mode = left.radio("Mode", list(TRAINING_MODES), horizontal=True, label_visibility="collapsed")
    topics_clicked = right.button("📚 Show modules & labs", width="stretch")

    for msg in ss.chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("caption"):
                st.caption(msg["caption"])

    placeholder = "Type your question..." if not TRAINING_MODES[mode] else "Type a topic, e.g. temperature, RAG, tokens..."
    text = st.chat_input(placeholder)
    if topics_clicked or text:
        cmd = "/topics" if topics_clicked else TRAINING_MODES[mode]
        label = "Show modules & labs" if topics_clicked else (f"{mode}: {text}" if cmd else text)
        ss.chat.append({"role": "user", "content": label})
        with st.chat_message("user"):
            st.markdown(label)
        apply_settings()  # training_task reads the retrieval mode
        task, query, k, fixed_hits = rag.training_task(index, cmd, text or "", text or "")
        with st.chat_message("assistant"):
            result = run(index, task, query, history=ss.history, k=k, hits=fixed_hits)
            if result:
                _, hits, stats = result
                sources = ", ".join(sorted({r["source"] for _, r in hits})) or "none"
                caption = (f"Sources: {sources} · {stats['output_tokens']} tokens · {stats['seconds']}s · "
                           f"see the Trace tab for details")
                st.caption(caption)
                ss.chat.append({"role": "assistant", "content": result[0], "caption": caption})

# ---- Variance ----------------------------------------------------------------
with tabs[1]:
    st.markdown("Run the **same question several times** and measure how much the answers differ. "
                "Try it at temperature 0.9, then at 0, and compare.")
    c1, c2 = st.columns([4, 1])
    question = c1.text_input("Question", "What is a token?", key="var_q")
    n = c2.number_input("Runs", 2, 10, 5, key="var_n")
    if st.button("Run variance test", type="primary"):
        st.caption(f"temperature {ss.temperature} · prompt {ss.prompt} · retrieval {ss.retrieval}")
        answers, times, progress = [], [], st.progress(0.0)
        apply_settings()
        try:
            for i in range(n):
                text_i, _, stats = rag.ask(index, None, question, question, echo=False)
                answers.append(text_i.strip())
                times.append(stats["seconds"])
                progress.progress((i + 1) / n, f"Run {i + 1} of {n} done")
            v = rag.variance_report(answers)
        except OSError as e:
            st.error(f"Could not reach Ollama ({e}). Start it with `ollama serve`.")
            st.stop()
        ss.trace = rag.LAB["last_trace"]
        m = st.columns(5)
        m[0].metric("Distinct answers", f"{v['distinct']} of {n}")
        m[1].metric("Semantic similarity", f"{v['semantic']:.3f}", help="1.0 = same meaning")
        m[2].metric("Word overlap", f"{v['overlap']:.3f}", help="Jaccard, 1.0 = same words")
        m[3].metric("Length (words)", f"{min(v['lengths'])}–{max(v['lengths'])}")
        m[4].metric("Latency (s)", f"{min(times)}–{max(times)}")
        st.info("Would an exact-match assertion pass? What threshold would you set? "
                "Change temperature or the prompt in the sidebar and run again.")
        for i, (a, secs, words_n) in enumerate(zip(answers, times, v["lengths"]), 1):
            with st.expander(f"Run {i} · {words_n} words · {secs}s"):
                st.markdown(a)

# ---- Compare models ----------------------------------------------------------
with tabs[2]:
    st.markdown(f"Send the same question to **{rag.CHAT_MODEL}** and **{rag.COMPARE_MODEL}** and record "
                "the differences: correctness, constraint-following, length, tone, tokens and latency.")
    question = st.text_input("Question", "Explain temperature in 3 bullets", key="cmp_q")
    if st.button("Compare", type="primary"):
        try:
            missing = [m for m in (rag.CHAT_MODEL, rag.COMPARE_MODEL) if m not in rag.installed_models()]
        except OSError as e:
            missing = None
            st.error(f"Could not reach Ollama ({e}). Start it with `ollama serve`.")
        if missing:
            st.error(f"Model(s) not installed: {', '.join(missing)}. Run `ollama pull {missing[0]}` "
                     "or change COMPARE_MODEL in rag.py.")
        elif missing is not None:
            for col, model in zip(st.columns(2), (rag.CHAT_MODEL, rag.COMPARE_MODEL)):
                with col:
                    st.subheader(model)
                    result = run(index, question, question, model=model)
                    if result:
                        footer(result[1], result[2])

# ---- Trace -------------------------------------------------------------------
with tabs[3]:
    t = ss.trace
    if not t:
        st.info("Nothing to trace yet. Ask something in any tab first.")
    else:
        st.markdown("The pipeline for the **last request**, step by step. Use it to build a failure-point register.")
        st.markdown(f"**1. Settings**: model `{t['model']}` · temperature `{t['temperature']}` · "
                    f"prompt `{t['prompt']}` · retrieval `{t['retrieval']}`")
        st.markdown(f"**2. Query embedded** with `{rag.EMBED_MODEL}`: _{t['query'][:300]}_")
        st.markdown(f"**3. Retrieved {len(t['hits'])} chunk(s)** from `{rag.INDEX_FILE.name}`")
        hits_table(t["hits"])
        st.markdown(f"**4. Prompt sent**: {len(t['messages'])} messages, {t['prompt_tokens']} prompt tokens")
        for m in t["messages"]:
            with st.expander(f"[{m['role'].upper()}] message ({len(m['content'])} chars)"):
                st.code(m["content"], language=None, wrap_lines=True)
        st.markdown(f"**5. Output**: {t['output_tokens']} tokens in {t['seconds']}s")
        with st.expander("Answer", expanded=True):
            st.markdown(t["answer"])

# ---- Break retrieval ---------------------------------------------------------
with tabs[4]:
    st.markdown("Ask the **same question under different retrieval modes** side by side and watch the "
                "answer quality change. (This ignores the sidebar retrieval setting.)")
    question = st.text_input("Question", "What is RAG and why does it matter for testers?", key="brk_q")
    modes = st.multiselect("Retrieval modes", list(rag.RETRIEVAL_MODES), list(rag.RETRIEVAL_MODES),
                           format_func=lambda m: f"{m}: {rag.RETRIEVAL_MODES[m]}")
    if st.button("Run experiment", type="primary") and modes:
        for col, mode_i in zip(st.columns(len(modes)), modes):
            with col:
                st.subheader(mode_i)
                st.caption(rag.RETRIEVAL_MODES[mode_i])
                result = run(index, question, question, retrieval=mode_i)
                if result:
                    footer(result[1], result[2])
                    with st.expander("Retrieved chunks"):
                        hits_table(result[1])

# ---- Weak vs strong prompt ---------------------------------------------------
with tabs[5]:
    st.markdown("Ask the **same question with both system prompts** side by side. Try an in-scope question, "
                "then an out-of-scope one (e.g. *What is the capital of France?*). The strong prompt should "
                f"answer \"{rag.FALLBACK}\" for out-of-scope questions.")
    question = st.text_input("Question", "What is the capital of France?", key="pr_q")
    if st.button("Compare prompts", type="primary"):
        for col, name in zip(st.columns(2), rag.PROMPTS):
            with col:
                st.subheader(f"{name} prompt")
                with st.expander("System prompt"):
                    st.code(rag.PROMPTS[name], language=None, wrap_lines=True)
                result = run(index, question, question, prompt=name)
                if result:
                    footer(result[1], result[2])
