# 📑 Doc Generator Agent

> Agentic documentation generator powered by **LangGraph**, **Google Gemma 4**, and **Streamlit**.

Point it at any public GitHub repository and get polished, comprehensive documentation in seconds — with a one-click PDF export.

---

## Architecture

```
┌─────────────────────────────────────────────┐
│              Streamlit UI (app.py)           │
└───────────────────┬─────────────────────────┘
                    │
          ┌─────────▼──────────┐
          │  LangGraph Graph   │
          │  (graph/graph.py)  │
          └─────────┬──────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
  fetch_repo  analyze_code  generate_docs
  (GitHub API) (Gemma 4 ×N) (Gemma 4 ×1)
        │           │           │
        └───────────▼───────────┘
               AgentState
```

## Quick Start

### 1. Clone & install

```bash
git clone <this-repo>
cd doc-generator
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

**Option A — Google AI Studio (recommended, free tier available)**
1. Get a key at https://aistudio.google.com
2. Set `GOOGLE_API_KEY=your_key` in `.env`

**Option B — Local Ollama**
```bash
ollama pull gemma3:12b   # or gemma3:27b
# Set USE_OLLAMA=true in .env
```

### 3. Run

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## Project Structure

```
doc-generator/
├── app.py                  # Streamlit UI entry point
├── requirements.txt
├── .env.example
├── graph/
│   ├── __init__.py
│   ├── state.py            # AgentState TypedDict
│   ├── nodes.py            # fetch_repo · analyze_code · generate_docs
│   └── graph.py            # LangGraph StateGraph
└── utils/
    ├── __init__.py
    ├── llm.py              # LLM provider (Google / Ollama)
    ├── github.py           # GitHub REST API helpers
    ├── prompts.py          # All prompt templates
    └── pdf_generator.py    # ReportLab PDF builder
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `GOOGLE_API_KEY` | — | Google AI Studio API key |
| `USE_OLLAMA` | `false` | Use local Ollama instead |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `MODEL_NAME` | `gemma-3-27b-it` | Model to use |
| `GITHUB_TOKEN` | — | Optional, raises rate limit to 5000/hr |
| `MAX_FILES_TO_READ` | `20` | Max source files to analyze |
| `MAX_FILE_CHARS` | `8000` | Max characters per file |