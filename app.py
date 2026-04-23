"""
app.py  –  Documentation Generator Agent
Streamlit UI  ·  LangGraph pipeline  ·  Google Gemma 4  ·  PDF export
"""
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="DocGen Agent",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

  /* ── Reset & base ─────────────────────────────────────────────────── */
  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

  .main .block-container {
    max-width: 820px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
  }

  /* ── Hero header ──────────────────────────────────────────────────── */
  .hero {
    text-align: center;
    margin-bottom: 2.5rem;
  }
  .hero-badge {
    display: inline-block;
    background: #f0f0ff;
    color: #4f46e5;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 1rem;
    border: 1px solid #e0e0ff;
  }
  .hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem;
    font-weight: 400;
    color: #64748b;
    line-height: 1.15;
    margin: 0 0 0.75rem 0;
    letter-spacing: -0.02em;
  }
  .hero p {
    font-size: 1.05rem;
    color: #64748b;
    font-weight: 300;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.6;
  }

  /* ── Card ─────────────────────────────────────────────────────────── */
  .card {
    background: #ffffff;
    border: 1px solid #e8eaed;
    border-radius: 16px;
    padding: 2rem 2rem 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.03);
  }
  .card-title {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 1.2rem;
  }

  /* ── Input Fields ─────────────────────────────────────────────────────────── */
    
    .stTextArea label, .stTextInput label {
        color: #ffffff !important;
        font-weight: bold !important;
    }
    
    textarea {
        background-color: #ffffff !important;
        color: #64748b !important;
        font-family: 'Courier New', monospace;
        border: 1px solid #e2e8f0 !important; /* Lighter border for a cleaner look */
        border-radius: 10px !important;
    }

    textarea::placeholder {
        color: #64748b !important;
        opacity: 0.6;
    }

    .stTextInput input {
        color: #64748b !important;
        border-radius: 10px !important;
    }
    
    .stTextInput input::placeholder {
        color: #64748b !important;
        opacity: 0.6;
    }
    .stTextInput div[data-baseweb="input"] {{
        border-color: #64748b55 !important;
    }}


  /* ── Pipeline steps ───────────────────────────────────────────────── */
  .steps {
    display: flex;
    gap: 0;
    margin: 1.5rem 0 2rem;
  }
  .step {
    flex: 1;
    text-align: center;
    position: relative;
  }
  .step:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 18px;
    right: -1px;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, #e2e8f0 0%, #e2e8f0 100%);
    z-index: 0;
  }
  .step-dot {
    width: 36px; height: 36px;
    border-radius: 50%;
    background: #f8fafc;
    border: 2px solid #e2e8f0;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 8px;
    font-size: 1rem;
    position: relative; z-index: 1;
    transition: all 0.3s;
  }
  .step-dot.active  { background: #6366f1; border-color: #6366f1; }
  .step-dot.done    { background: #10b981; border-color: #10b981; }
  .step-label {
    font-size: 0.72rem;
    color: #94a3b8;
    font-weight: 500;
  }

  /* ── Status pill ──────────────────────────────────────────────────── */
  .status-pill {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 500;
  }
  .status-running { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; }
  .status-done    { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
  .status-error   { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }

  /* ── Metric row ───────────────────────────────────────────────────── */
  .metrics {
    display: flex; gap: 1rem; margin: 1rem 0;
  }
  .metric {
    flex: 1;
    background: #f8fafc;
    border: 1px solid #f1f5f9;
    border-radius: 10px;
    padding: 0.9rem 1rem;
    text-align: center;
  }
  .metric-value {
    font-family: 'DM Mono', monospace;
    font-size: 1.5rem;
    font-weight: 500;
    color: #0f172a;
  }
  .metric-label {
    font-size: 0.72rem;
    color: #94a3b8;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-top: 2px;
  }

  /* ── Streamlit overrides ──────────────────────────────────────────── */
  div[data-testid="stTextInput"] input,
  div[data-testid="stTextArea"] textarea {
    border-radius: 10px !important;
    border: 1px solid #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    background: #fafafa !important;
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  div[data-testid="stTextInput"] input:focus,
  div[data-testid="stTextArea"] textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
    background: #fff !important;
  }
  div[data-testid="stTextInput"] label,
  div[data-testid="stTextArea"] label {
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    color: #374151 !important;
  }
  .stButton > button {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
  }
  .stButton > button[kind="primary"] {
    background: #6366f1 !important;
    border: none !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.35) !important;
  }
  .stButton > button[kind="primary"]:hover {
    background: #4f46e5 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.4) !important;
  }
  .stDownloadButton > button {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
  }
  div[data-testid="stTab"] button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
  }
  .stSpinner { color: #6366f1 !important; }

  /* ── Doc preview ──────────────────────────────────────────────────── */
  .doc-preview {
    background: #fafafa;
    border: 1px solid #f1f5f9;
    border-radius: 12px;
    padding: 2rem;
  }
  .doc-preview h1 { font-family: 'DM Serif Display', serif !important; }
  .doc-preview code {
    font-family: 'DM Mono', monospace !important;
    background: #f1f5f9;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.88em;
  }
  .doc-preview pre {
    background: #1e293b !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
    padding: 1rem 1.2rem !important;
  }

  /* ── Footer ───────────────────────────────────────────────────────── */
  .footer {
    text-align: center;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid #f1f5f9;
    color: #cbd5e1;
    font-size: 0.78rem;
  }
  .footer a { color: #94a3b8; text-decoration: none; }
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    "final_doc":    "",
    "doc_title":    "",
    "doc_desc":     "",
    "doc_repo_url": "",
    "pdf_bytes":    None,
    "file_count":   0,
    "module_count": 0,
    "stage":        "idle",   # idle | fetching | analyzing | generating | done | error
    "error_msg":    "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">⚡ Agentic AI · LangGraph · Gemma 4</div>
  <h1>Documentation<br>Generator</h1>
  <p>Point it at any GitHub repo. Get beautiful, comprehensive docs in seconds.</p>
</div>
""", unsafe_allow_html=True)


# ── Pipeline stage indicator ──────────────────────────────────────────────────
stage = st.session_state.stage

def _dot_cls(step_stage: str) -> str:
    order = ["idle", "fetching", "analyzing", "generating", "done"]
    current = order.index(stage) if stage in order else 0
    target  = order.index(step_stage)
    if current == target and stage not in ("idle", "done", "error"): return "active"
    if current > target or stage == "done": return "done"
    return ""

if stage != "idle":
    st.markdown(f"""
    <div class="steps">
      <div class="step">
        <div class="step-dot {_dot_cls('fetching')}">{'✓' if _dot_cls('fetching')=='done' else '📥'}</div>
        <div class="step-label">Fetch repo</div>
      </div>
      <div class="step">
        <div class="step-dot {_dot_cls('analyzing')}">{'✓' if _dot_cls('analyzing')=='done' else '🔍'}</div>
        <div class="step-label">Analyze code</div>
      </div>
      <div class="step">
        <div class="step-dot {_dot_cls('generating')}">{'✓' if _dot_cls('generating')=='done' else '✍️'}</div>
        <div class="step-label">Generate docs</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Input card ────────────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">Repository details</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="medium")
with col1:
     title = st.text_area("Project Title",
        placeholder="My Awesome Project", height = 104)
with col2:
    description = st.text_area("Short Description",
        placeholder="What does this project do?",
        height=104)

repo_url = st.text_input(label = "GitHub Repository URL",
    placeholder="https://github.com/owner/repository",
    help="Public GitHub repository URL")

st.markdown('</div>', unsafe_allow_html=True)


# ── Run button ────────────────────────────────────────────────────────────────
run = st.button("🚀  Generate Documentation", type="primary", use_container_width=True)


# ── Agent pipeline ────────────────────────────────────────────────────────────
if run:
    if not repo_url.strip():
        st.warning("Please enter a GitHub repository URL.")
    elif not title.strip():
        st.warning("Please enter a project title.")
    else:
        # reset
        st.session_state.update({
            "final_doc": "", "pdf_bytes": None,
            "doc_title": title, "doc_desc": description,
            "doc_repo_url": repo_url,
            "file_count": 0, "module_count": 0,
            "stage": "fetching", "error_msg": "",
        })

        status_box = st.empty()

        try:
            from graph.graph import build_graph

            graph = build_graph()

            # ── Stage 1: fetch ────────────────────────────────────────────
            status_box.markdown(
                '<div class="status-pill status-running">⏳ Fetching repository…</div>',
                unsafe_allow_html=True)

            result = graph.invoke({
                "repo_url":    repo_url,
                "title":       title,
                "description": description,
                # initial empty values
                "file_tree":        [],
                "file_contents":    {},
                "repo_overview":    "",
                "module_summaries": [],
                "final_doc":        "",
                "error":            None,
            })

            if result.get("error"):
                raise RuntimeError(result["error"])

            st.session_state.update({
                "final_doc":    result.get("final_doc", ""),
                "file_count":   len(result.get("file_tree", [])),
                "module_count": len(result.get("module_summaries", [])),
                "stage":        "done",
            })

            status_box.markdown(
                '<div class="status-pill status-done">✅ Documentation generated successfully!</div>',
                unsafe_allow_html=True)

        except Exception as exc:
            st.session_state.stage     = "error"
            st.session_state.error_msg = str(exc)
            status_box.markdown(
                f'<div class="status-pill status-error">❌ Error: {exc}</div>',
                unsafe_allow_html=True)


# ── Error display ─────────────────────────────────────────────────────────────
if st.session_state.stage == "error":
    st.error(f"**Pipeline error:** {st.session_state.error_msg}")
    with st.expander("Troubleshooting tips"):
        st.markdown("""
- Make sure the repository is **public**
- Check your `.env` — `GOOGLE_API_KEY` must be set (or `USE_OLLAMA=true`)
- For Ollama: ensure the service is running (`ollama serve`) and the model is pulled
- GitHub rate limit? Add a `GITHUB_TOKEN` to `.env`
        """)


# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.final_doc:
    st.markdown("---")

    # ── Metrics row ───────────────────────────────────────────────────────────
    fc = st.session_state.file_count
    mc = st.session_state.module_count
    wc = len(st.session_state.final_doc.split())
    st.markdown(f"""
    <div class="metrics">
      <div class="metric">
        <div class="metric-value">{fc}</div>
        <div class="metric-label">Files found</div>
      </div>
      <div class="metric">
        <div class="metric-value">{mc}</div>
        <div class="metric-label">Modules analyzed</div>
      </div>
      <div class="metric">
        <div class="metric-value">{wc:,}</div>
        <div class="metric-label">Words generated</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Action bar ────────────────────────────────────────────────────────────
    st.markdown('<div class="card"><div class="card-title">Export</div>', unsafe_allow_html=True)

    col_md, col_gen, col_dl = st.columns([1, 1, 1], gap="small")

    with col_md:
        st.download_button(
            label="⬇️  Download Markdown",
            data=st.session_state.final_doc,
            file_name=f"{st.session_state.doc_title.replace(' ', '_')}_docs.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with col_gen:
        if st.button("📄  Generate PDF", use_container_width=True):
            with st.spinner("Building PDF…"):
                try:
                    from utils.pdf_generator import generate_pdf
                    st.session_state.pdf_bytes = generate_pdf(
                        title=st.session_state.doc_title,
                        description=st.session_state.doc_desc,
                        repo_url=st.session_state.doc_repo_url,
                        markdown_content=st.session_state.final_doc,
                    )
                    st.success("PDF ready — click Download below!")
                except Exception as e:
                    st.error(f"PDF error: {e}")

    with col_dl:
        if st.session_state.pdf_bytes:
            st.download_button(
                label="⬇️  Download PDF",
                data=st.session_state.pdf_bytes,
                file_name=f"{st.session_state.doc_title.replace(' ', '_')}_docs.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary",
            )
        else:
            st.button("⬇️  Download PDF", disabled=True, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Preview tabs ──────────────────────────────────────────────────────────
    tab_preview, tab_raw = st.tabs(["📖  Preview", "📝  Raw Markdown"])

    with tab_preview:
        st.markdown('<div class="doc-preview">', unsafe_allow_html=True)
        st.markdown(st.session_state.final_doc)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_raw:
        st.code(st.session_state.final_doc, language="markdown")


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Built with LangGraph · Google Gemma 4 · Streamlit &nbsp;·&nbsp;
  <a href="https://github.com">View on GitHub</a>
</div>
""", unsafe_allow_html=True)