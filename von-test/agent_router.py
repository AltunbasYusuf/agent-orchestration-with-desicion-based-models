"""
Von On-Prem Agent Router (CUDA / RTX 3050 Ti) - Full English Test
Testing pure English performance to eliminate cross-lingual transfer issues.
"""

import sys
import time
import torch
import von

# ---------------------------------------------------------
# 1. Agent Definitions and Routing Instructions (English)
# ---------------------------------------------------------
AGENTS = {
    "workflow_agent": "Mobile workflows, business process analysis, customer journey steps, application flow, and operational procedures.",
    "confluence_agent": "Confluence documentation, wiki pages, onboarding guides, internal manuals, and company handbooks.",
    "code_search_agent": "TFS, Git, Azure DevOps, source code search, repo files, code analysis, and function definitions.",
    "grafana_agent": "Grafana dashboards, p95 latency metrics, telemetry graphs, server performance, and system monitoring.",
    "markdown_converter_agent": "Converting PDF files to Markdown, Word document transformation, and format conversion.",
}

ROUTING_INSTRUCTIONS = "Select the most suitable agent for the user's request."

CONFIDENCE_THRESHOLD = 0.25


def setup_hardware() -> str:
    if torch.cuda.is_available():
        try:
            von.set_backend("cuda")
        except Exception:
            pass
        return "cuda"
    return "cpu"


DEVICE = setup_hardware()


def warmup_engine():
    print("[INFO] Warming up GPU and caching model weights...")
    try:
        if DEVICE == "cuda":
            torch.cuda.synchronize()
        von.decide(state="ping", choices=AGENTS, instructions=ROUTING_INSTRUCTIONS)
        if DEVICE == "cuda":
            torch.cuda.synchronize()
        print("[SUCCESS] Warmup complete. Running tests...\n")
    except Exception as e:
        print(f"[WARNING] Warmup error: {e}")


def route(prompt: str) -> dict:
    if DEVICE == "cuda":
        torch.cuda.synchronize()

    start_time = time.perf_counter()

    ans = von.decide(
        state=prompt,
        choices=AGENTS,
        instructions=ROUTING_INSTRUCTIONS,
    )

    if DEVICE == "cuda":
        torch.cuda.synchronize()

    latency_ms = (time.perf_counter() - start_time) * 1000

    winner = getattr(ans, "choice", None) or getattr(ans, "winner", str(ans))
    confidence = getattr(ans, "confidence", 0.0) or 0.0
    probabilities = getattr(ans, "probabilities", {}) or {}

    final_choice = winner
    if confidence < CONFIDENCE_THRESHOLD:
        final_choice = "out_of_scope (Low Confidence)"

    return {
        "choice": final_choice,
        "raw_winner": winner,
        "confidence": confidence,
        "probabilities": probabilities,
        "latency_ms": latency_ms,
    }


def show(prompt: str) -> None:
    res = route(prompt)
    print(f"Prompt  : {prompt}")
    print(f"Agent   : {res['choice']} (confidence: {res['confidence']:.2f}) | {res['latency_ms']:.2f} ms")

    if res["probabilities"]:
        ranked = sorted(res["probabilities"].items(), key=lambda kv: kv[1], reverse=True)[:3]
        print("Top 3   : " + ", ".join(f"{k}={v:.2f}" for k, v in ranked))
    print("-" * 60)


DEMO_PROMPTS = [
    "How does the credit card application workflow work?",
    "Get the onboarding guide page from confluence for new starters",
    "Analyze and explain the mcp-atlassian code from TFS",
    "Fetch and interpret backend metrics from Grafana",
    "Convert this PDF file into markdown",
    "Which code file contains the search tool in mcp semantic search?",
    "Analyze and summarize all the codebase in the MCP-Atlassian project.",
    "Fetch the backend p95 graph and interpret it.",
    "What is the capital of Turkey?",
    "What is the weather like today?",
    "What permissions should I request for the newly joined intern?",
    "How do I create a subtask in Jira?",
]

if __name__ == "__main__":
    warmup_engine()
    for p in DEMO_PROMPTS:
        show(p)