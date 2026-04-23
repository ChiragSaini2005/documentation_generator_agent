"""
graph/nodes.py
Three agent nodes for the documentation pipeline:
  1. fetch_repo    – pulls file tree + contents from GitHub
  2. analyze_code  – uses Gemma to summarize the repo and each module
  3. generate_docs – uses Gemma to write the full documentation
"""
from __future__ import annotations

from langchain_core.messages import HumanMessage

from graph.state import AgentState
from utils.github import fetch_repository
from utils.llm import get_llm
from utils.prompts import (
    REPO_OVERVIEW_PROMPT,
    MODULE_SUMMARY_PROMPT,
    GENERATE_DOCS_PROMPT,
)


# ── Node 1: fetch_repo ────────────────────────────────────────────────────────

def fetch_repo(state: AgentState) -> AgentState:
    """
    Fetch the GitHub repository's file tree and the content of
    the most relevant source files.
    """
    try:
        file_tree, file_contents = fetch_repository(state["repo_url"])
        return {
            **state,
            "file_tree":     file_tree,
            "file_contents": file_contents,
            "error":         None,
        }
    except Exception as exc:
        return {**state, "error": f"fetch_repo failed: {exc}"}


# ── Node 2: analyze_code ──────────────────────────────────────────────────────

def analyze_code(state: AgentState) -> AgentState:
    """
    Ask Gemma to:
      a) produce a high-level technical overview of the whole repo
      b) produce a one-paragraph summary for each fetched file
    """
    if state.get("error"):
        return state

    llm = get_llm()

    # ── a) Repo-level overview ────────────────────────────────────────────────
    file_tree_str = "\n".join(state["file_tree"][:200])   # cap list length
    file_contents_str = "\n\n".join(
        f"### {path}\n{content}"
        for path, content in state["file_contents"].items()
    )

    overview_prompt = REPO_OVERVIEW_PROMPT.format(
        title=state["title"],
        description=state["description"],
        repo_url=state["repo_url"],
        file_tree=file_tree_str,
        file_contents=file_contents_str,
    )
    overview_response = llm.invoke([HumanMessage(content=overview_prompt)])
    repo_overview = overview_response.content.strip()

    # ── b) Per-module summaries ───────────────────────────────────────────────
    module_summaries: list[str] = []

    for path, content in state["file_contents"].items():
        summary_prompt = MODULE_SUMMARY_PROMPT.format(
            file_path=path,
            content=content[:6000],   # hard cap per file
        )
        response = llm.invoke([HumanMessage(content=summary_prompt)])
        summary  = response.content.strip()
        module_summaries.append(f"**{path}**: {summary}")

    return {
        **state,
        "repo_overview":    repo_overview,
        "module_summaries": module_summaries,
        "error":            None,
    }


# ── Node 3: generate_docs ─────────────────────────────────────────────────────

def generate_docs(state: AgentState) -> AgentState:
    """
    Use Gemma to write the complete documentation in Markdown,
    using the overview and module summaries produced by analyze_code.
    """
    if state.get("error"):
        return state

    llm = get_llm()

    module_summaries_str = "\n\n".join(state["module_summaries"])

    docs_prompt = GENERATE_DOCS_PROMPT.format(
        title=state["title"],
        description=state["description"],
        repo_url=state["repo_url"],
        repo_overview=state["repo_overview"],
        module_summaries=module_summaries_str,
    )

    response  = llm.invoke([HumanMessage(content=docs_prompt)])
    final_doc = response.content.strip()

    # Prepend the project title as an H1
    header    = f"# {state['title']}\n\n> {state['description']}\n\n"
    final_doc = header + final_doc

    return {**state, "final_doc": final_doc, "error": None}