"""
graph/state.py
Shared state passed between every LangGraph node.
"""
from typing import Optional
from typing_extensions import TypedDict


class AgentState(TypedDict):
    # ── Inputs (set by user) ──────────────────────────────────────────────────
    repo_url:    str
    title:       str
    description: str

    # ── Populated by fetch_repo node ──────────────────────────────────────────
    file_tree:     list[str]          # all file paths in the repo
    file_contents: dict[str, str]     # path → raw text for selected files

    # ── Populated by analyze_code node ───────────────────────────────────────
    repo_overview:    str             # high-level LLM summary of the project
    module_summaries: list[str]       # per-file summaries

    # ── Populated by generate_docs node ──────────────────────────────────────
    final_doc: str                    # complete markdown documentation

    # ── Control / error ───────────────────────────────────────────────────────
    error: Optional[str]