# 📑 Doc Generator Agent

> **An AI-powered documentation generator that analyzes GitHub repositories and automatically creates comprehensive, human-readable technical documentation.**

Built with **LangGraph**, **Llama 3.1**, **Streamlit**, and the **GitHub API**.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic%20Workflow-orange)](https://www.langchain.com/langgraph)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)](https://streamlit.io/)
[![Llama](https://img.shields.io/badge/LLM-Llama%203.1-purple)](https://www.llama.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ Overview

Writing and maintaining documentation for software projects can be time-consuming, especially when working with unfamiliar or large codebases.

**Doc Generator Agent** automates this process.

Simply provide a public GitHub repository URL, and the agent:

1. Fetches the repository structure.
2. Identifies relevant source files.
3. Analyzes the codebase using **Llama 3.1**.
4. Builds a structured understanding of the project.
5. Generates comprehensive technical documentation.
6. Presents the result through an interactive Streamlit interface.
7. Allows the generated documentation to be exported as a PDF.

The entire process is orchestrated using a **LangGraph stateful agent workflow**.

---

## 🚀 Features

### 🤖 Agentic Code Analysis

Uses a **LangGraph workflow** to coordinate multiple stages of repository analysis and documentation generation.

### 🔍 GitHub Repository Analysis

Provide a GitHub repository URL and the agent retrieves its structure and source code through the GitHub API.

### 🧠 LLM-Powered Documentation

Uses **Meta's Llama 3.1** to understand source code and generate documentation based on the actual implementation.

### 📝 Comprehensive Documentation

Generated documentation can cover:

* Project overview
* Architecture
* Module descriptions
* Code organization
* Important implementation details
* Dependencies
* Usage information
* Technical explanations
* Code references

### 🖥️ Streamlit Interface

A simple web interface makes the documentation generation process accessible without requiring users to interact with the agent through a terminal.

### 📄 PDF Export

Generated documentation can be exported as a PDF for easy sharing and offline access.

### 🏠 Local LLM Support

The project can optionally use **Ollama** to run Llama 3.1 locally instead of relying on a cloud API.

---

## 🏗️ Architecture

The application follows an agentic workflow built with LangGraph:

```text
                         ┌──────────────────────┐
                         │    Streamlit UI      │
                         │       app.py         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      LangGraph       │
                         │     StateGraph       │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
      │  Fetch Repo  │      │ Analyze Code │      │ Generate Docs│
      │ GitHub API   │      │  Llama 3.1   │      │  Llama 3.1   │
      └──────┬───────┘      └──────┬───────┘      └──────┬───────┘
             │                     │                     │
             └─────────────────────┼─────────────────────┘
                                   ▼
                         ┌──────────────────────┐
                         │     Agent State      │
                         │   Generated Docs     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    PDF Generator     │
                         └──────────────────────┘
```

### Workflow

```text
GitHub Repository
       │
       ▼
Fetch Repository
       │
       ▼
Analyze Structure
       │
       ▼
Read Source Files
       │
       ▼
Llama 3.1 Code Analysis
       │
       ▼
Generate Documentation
       │
       ▼
Display in Streamlit
       │
       ├──────────────► Markdown
       │
       └──────────────► PDF
```

---

## 🛠️ Tech Stack

| Technology          | Purpose                                         |
| ------------------- | ----------------------------------------------- |
| **Python**          | Core programming language                       |
| **LangGraph**       | Agentic workflow orchestration                  |
| **Llama 3.1**       | Code understanding and documentation generation |
| **Streamlit**       | Interactive web interface                       |
| **GitHub REST API** | Repository and source-code retrieval            |
| **Ollama**          | Local Llama 3.1 inference                       |
| **ReportLab**       | PDF generation                                  |
| **python-dotenv**   | Environment configuration                       |

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/ChiragSaini2005/documentation_generator_agent.git

cd documentation_generator_agent
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`.

For example:

```env
LLM_MODEL=llama3.1

USE_OLLAMA=true

OLLAMA_BASE_URL=http://localhost:11434

GITHUB_TOKEN=your_github_token

MAX_FILES_TO_READ=20

MAX_FILE_CHARS=8000
```

---

## ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

Open the URL in your browser and provide the GitHub repository you want to document.

---

## 🏠 Running Llama 3.1 Locally with Ollama

The project supports running **Llama 3.1 locally through Ollama**.

### 1. Install Ollama

Install Ollama for your operating system.

### 2. Pull Llama 3.1

```bash
ollama pull llama3.1
```

### 3. Start Ollama

```bash
ollama serve
```

### 4. Configure the application

Set the following in `.env`:

```env
USE_OLLAMA=true

OLLAMA_BASE_URL=http://localhost:11434

LLM_MODEL=llama3.1
```

### 5. Run the application

```bash
streamlit run app.py
```

The documentation agent will now use your local **Llama 3.1** model for code analysis and documentation generation.

---

## 📖 How It Works

### Step 1 — Repository Fetching

The GitHub API retrieves the repository structure and relevant source files.

```text
GitHub URL
    ↓
GitHub API
    ↓
Repository Tree
    ↓
Relevant Files
```

### Step 2 — Code Analysis

The selected source files are processed by **Llama 3.1** to understand:

* What the project does
* How components interact
* What each module is responsible for
* Important implementation details
* Dependencies and relationships

### Step 3 — Documentation Generation

The analyzed repository context is passed to the documentation-generation stage.

Llama 3.1 generates structured Markdown documentation based on the codebase.

### Step 4 — Output

The generated documentation is displayed through the Streamlit interface and can be exported as a PDF.

---

## 🎯 Why LangGraph?

LangGraph provides a structured framework for building stateful agent workflows.

Instead of treating the LLM as a single black-box call, the project separates the workflow into distinct stages:

```text
Fetch → Analyze → Generate
```

Each stage operates on shared agent state, making the workflow easier to understand, debug, and extend.

Future versions can extend this architecture with:

* Multi-agent code analysis
* Documentation verification
* Iterative refinement
* Dependency analysis
* Documentation quality evaluation
* Additional output formats

---

## 🔮 Future Improvements

* [ ] Multi-agent parallel code analysis
* [ ] Documentation quality verification
* [ ] Automatic README updates through GitHub PRs
* [ ] Support for private repositories
* [ ] Repository dependency graphs
* [ ] Architecture diagram generation
* [ ] Mermaid diagram generation
* [ ] Support for additional LLM providers
* [ ] Incremental documentation updates
* [ ] Documentation versioning
* [ ] Improved handling of large repositories

---

## ⚠️ Limitations

The quality of generated documentation depends on the quality and amount of source code available to the model.

For very large repositories, configuration limits such as:

```env
MAX_FILES_TO_READ
MAX_FILE_CHARS
```

may restrict how much source code is analyzed.

Generated documentation should therefore be reviewed before being treated as authoritative project documentation.

---

## 🤝 Contributing

Contributions are welcome.

```bash
git checkout -b feature/your-feature

git add .

git commit -m "Add your feature"

git push origin feature/your-feature
```

Then open a Pull Request.

---


## 👨‍💻 Author

**Chirag Saini**

[![GitHub](https://img.shields.io/badge/GitHub-ChiragSaini2005-black?logo=github)](https://github.com/ChiragSaini2005)

### Project

[Documentation Generator Agent](https://github.com/ChiragSaini2005/documentation_generator_agent)

---

## ⭐ Support

If you find this project useful, consider giving it a **star** on GitHub.

It helps others discover the project and supports further development.

---

<p align="center">
  Built with ❤️ using Python, LangGraph, Llama 3.1, and Streamlit.
</p>
