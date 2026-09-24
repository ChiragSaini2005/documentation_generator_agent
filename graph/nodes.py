"""
graph/nodes.py
Three agent nodes for the documentation pipeline:
    1. fetch_repo    - pulls file tree + contents from GitHub
    2. assign_id     - stores each file as a uniquely identified code chunk
    3. analyze_code  - uses Llama to summarize the repo and each module
    4. generate_docs - uses Llama to write the full documentation
"""
from __future__ import annotations

import re

from langchain_core.messages import HumanMessage

from graph.state import AgentState
from utils.github import fetch_repository
from utils.llm import get_llm
from utils.prompts import (
    REPO_OVERVIEW_PROMPT,
    MODULE_SUMMARY_PROMPT,
    GENERATE_DOCS_PROMPT,
)


def extract_citations(text: str, valid_chunks: set[str]) -> list[str]:
    """Return bracketed source citations that reference known code chunks."""
    citations: list[str] = []
    citation_pattern = re.compile(r"\[([^\[\]\s]+#chunk_\d+)\]")

    for match in citation_pattern.finditer(text):
        citation_id = match.group(1)
        chunk_id = citation_id
        if chunk_id in valid_chunks:
            citations.append(match.group(0))

    return citations


def build_references(chunk_ids: list[str], code_chunks: dict[str, str]) -> str:
    """Build a numbered Markdown reference section for cited code chunks."""
    references: list[str] = []
    seen: set[str] = set()

    for citation in chunk_ids:
        chunk_id = citation.removeprefix("[").removesuffix("]")
        if chunk_id in seen or chunk_id not in code_chunks:
            continue

        seen.add(chunk_id)
        filepath = chunk_id.split("#", 1)[0]
        references.append(
            f"[{len(references) + 1}] `{filepath}`\n\n"
        )

    if not references:
        return ""

    return "## References\n\n" + "\n\n".join(references)


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


# ── Node 2: assign_id ─────────────────────────────────────────────────────────

def assign_id(state: AgentState) -> AgentState:
    """Store each fetched file as one uniquely identified code chunk."""
    if state.get("error"):
        return state

    code_chunks = {}
    for path, content in state["file_contents"].items():
        # Single file = single chunk
        chunk_id = f"{path}#chunk_0"
        code_chunks[chunk_id] = content

    return {**state, "code_chunks": code_chunks, "error": None}


# ── Node 3: analyze_code ──────────────────────────────────────────────────────

def analyze_code(state: AgentState) -> AgentState:
    """
    Ask LLM to:
      a) produce a high-level technical overview of the whole repo
      b) produce a one-paragraph summary for each fetched file
    """
    if state.get("error"):
        return state

    llm = get_llm()

    # ── a) Repo-level overview ────────────────────────────────────────────────
    file_tree_str = "\n".join(state["file_tree"][:200])   # cap list length
    file_contents_str = "\n\n".join(
        f"### {path}\n{content[:4000]}"
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
    valid_chunks = set(state["code_chunks"])
    doc_citations: dict[str, list[str]] = {
        "repo_overview": extract_citations(repo_overview, valid_chunks),
    }

    # ── b) Per-module summaries ───────────────────────────────────────────────
    module_summaries: list[str] = []

    for (path, _ ), (chunk_key, chunk_content) in zip(
        state["file_contents"].items(), state["code_chunks"].items()
    ):
        summary_prompt = MODULE_SUMMARY_PROMPT.format(
            file_path=path,
            chunk_id=chunk_key,
            content=chunk_content[:6000],   # hard cap per file
        )
        response = llm.invoke([HumanMessage(content=summary_prompt)])
        summary  = response.content.strip()
        module_summaries.append(f"**{path}**: {summary}")
        doc_citations[path] = extract_citations(summary, valid_chunks)

    return {
        **state,
        "repo_overview":    repo_overview,
        "module_summaries": module_summaries,
        "doc_citations":    doc_citations,
        "error":            None,
    }


# ── Node 4: generate_docs ─────────────────────────────────────────────────────

def generate_docs(state: AgentState) -> AgentState:
    """
    Use LLM to write the complete documentation in Markdown,
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
    citations = [
        citation
        for section_citations in state.get("doc_citations", {}).values()
        for citation in section_citations
    ]
    references = build_references(citations, state["code_chunks"])
    # if references:
    #     final_doc = f"{final_doc}\n\n{references}"

    return {
        **state,
        "final_doc": final_doc,
        "citation_map": references,
        "error": None,
    }