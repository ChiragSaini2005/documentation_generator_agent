"""
graph/graph.py
Builds and compiles the LangGraph StateGraph for the doc generator pipeline.

Flow:
  START → fetch_repo → analyze_code → generate_docs → END
                ↓ (on error at any node)
              END   (error is surfaced in state["error"])
"""
from langgraph.graph import StateGraph, END

from graph.state import AgentState
from graph.nodes import fetch_repo, analyze_code, generate_docs


def _should_continue(state: AgentState) -> str:
    """Route to END early if a node set an error."""
    return "end" if state.get("error") else "continue"


def build_graph() -> StateGraph:
    """Compile and return the runnable graph."""
    builder = StateGraph(AgentState)

    # ── Register nodes ────────────────────────────────────────────────────────
    builder.add_node("fetch_repo",    fetch_repo)
    builder.add_node("analyze_code",  analyze_code)
    builder.add_node("generate_docs", generate_docs)

    # ── Entry point ───────────────────────────────────────────────────────────
    builder.set_entry_point("fetch_repo")

    # ── Edges with error-short-circuit ────────────────────────────────────────
    builder.add_conditional_edges(
        "fetch_repo",
        _should_continue,
        {"continue": "analyze_code", "end": END},
    )
    builder.add_conditional_edges(
        "analyze_code",
        _should_continue,
        {"continue": "generate_docs", "end": END},
    )
    builder.add_edge("generate_docs", END)

    return builder.compile()