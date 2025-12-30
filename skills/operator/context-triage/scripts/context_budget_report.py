#!/usr/bin/env python3
"""
Purpose: Demonstrate Context Triage budget reporting for a candidate context set
Skill: skills/operator/context-triage/SKILL.md
Note: Illustrative script. Not production code. Authority: human-supervised execution.

What this script does
- Loads a context bundle (JSON) from a file path or stdin
- Estimates token usage per artifact using a consistent heuristic
- Produces a budget report and a ranked admission preview

What this script does not do
- It does not tokenize accurately
- It does not decide scope or authority correctness
- It does not fetch or retrieve content
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


# ----------------------------
# Token counting (consistent heuristic)
# ----------------------------

class HeuristicTokenCounter:
    """
    Consistent heuristic token counter.

    Rule:
    - Roughly 4 characters per token for English prose
    - Adds a small fixed overhead per artifact to account for framing

    This is intentionally simple and stable for demos.
    """

    def __init__(self, chars_per_token: int = 4, per_artifact_overhead: int = 10) -> None:
        if chars_per_token <= 0:
            raise ValueError("chars_per_token must be > 0")
        if per_artifact_overhead < 0:
            raise ValueError("per_artifact_overhead must be >= 0")
        self.chars_per_token = chars_per_token
        self.per_artifact_overhead = per_artifact_overhead

    def count_text(self, text: str) -> int:
        if not text:
            return 0
        return max(1, len(text) // self.chars_per_token)

    def count_artifact(self, text: str) -> int:
        base = self.count_text(text)
        if base == 0:
            return 0
        return base + self.per_artifact_overhead


# ----------------------------
# Data model
# ----------------------------

@dataclass
class Artifact:
    artifact_id: str
    kind: str  # system | task | message | document | tool_output | other
    authority: str  # system | developer | user | tool | other
    priority: int  # higher means earlier admission
    title: str
    content: str
    scope: Optional[str] = None
    timestamp: Optional[str] = None


# ----------------------------
# Loading and normalization
# ----------------------------

ALLOWED_AUTHORITIES = {"system", "developer", "user", "tool", "other"}
ALLOWED_KINDS = {"system", "task", "message", "document", "tool_output", "other"}

DEFAULT_AUTHORITY_WEIGHT = {
    "system": 1000,
    "developer": 800,
    "user": 600,
    "tool": 400,
    "other": 200,
}

DEFAULT_KIND_WEIGHT = {
    "system": 120,
    "task": 110,
    "message": 60,
    "document": 50,
    "tool_output": 40,
    "other": 10,
}


def _safe_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:
        return default


def normalize_bundle(bundle: Dict[str, Any]) -> List[Artifact]:
    """
    Accepts a JSON dict with a top-level key "artifacts" containing list items.

    Minimal accepted artifact shape:
    {
      "id": "A1",
      "kind": "document",
      "authority": "tool",
      "priority": 5,
      "title": "Doc title",
      "content": "..."
    }

    Optional:
    - scope, timestamp
    """
    artifacts_raw = bundle.get("artifacts", [])
    if not isinstance(artifacts_raw, list):
        raise ValueError("bundle.artifacts must be a list")

    artifacts: List[Artifact] = []
    for i, a in enumerate(artifacts_raw):
        if not isinstance(a, dict):
            raise ValueError(f"artifact at index {i} must be an object")

        artifact_id = str(a.get("id") or a.get("artifact_id") or f"artifact_{i}")
        kind = str(a.get("kind") or "other").strip()
        authority = str(a.get("authority") or "other").strip()
        priority = _safe_int(a.get("priority"), default=0)
        title = str(a.get("title") or artifact_id).strip()
        content = str(a.get("content") or "").strip()
        scope = a.get("scope")
        timestamp = a.get("timestamp")

        if kind not in ALLOWED_KINDS:
            kind = "other"
        if authority not in ALLOWED_AUTHORITIES:
            authority = "other"

        artifacts.append(
            Artifact(
                artifact_id=artifact_id,
                kind=kind,
                authority=authority,
                priority=priority,
                title=title,
                content=content,
                scope=str(scope) if scope is not None else None,
                timestamp=str(timestamp) if timestamp is not None else None,
            )
        )

    return artifacts


def load_json_from_path_or_stdin(path: Optional[str]) -> Dict[str, Any]:
    if path and path != "-":
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return json.load(sys.stdin)


# ----------------------------
# Reporting and admission preview
# ----------------------------

def score_for_admission(a: Artifact) -> int:
    """
    Admission score: authority weight + kind weight + explicit priority.
    Higher score admitted earlier.
    """
    return (
        DEFAULT_AUTHORITY_WEIGHT.get(a.authority, 0)
        + DEFAULT_KIND_WEIGHT.get(a.kind, 0)
        + a.priority
    )


def compute_breakdown(artifacts: List[Artifact], counter: HeuristicTokenCounter) -> Dict[str, int]:
    breakdown: Dict[str, int] = {
        "system_prompt": 0,
        "task": 0,
        "message_history": 0,
        "retrieved_documents": 0,
        "tool_outputs": 0,
        "other": 0,
    }

    for a in artifacts:
        tokens = counter.count_artifact(a.content)
        if a.kind == "system":
            breakdown["system_prompt"] += tokens
        elif a.kind == "task":
            breakdown["task"] += tokens
        elif a.kind == "message":
            breakdown["message_history"] += tokens
        elif a.kind == "document":
            breakdown["retrieved_documents"] += tokens
        elif a.kind == "tool_output":
            breakdown["tool_outputs"] += tokens
        else:
            breakdown["other"] += tokens

    return breakdown


def admission_preview(
    artifacts: List[Artifact],
    counter: HeuristicTokenCounter,
    budget_tokens: int,
) -> Tuple[List[Tuple[Artifact, int]], List[Tuple[Artifact, int]]]:
    """
    Returns (admitted, excluded) lists with their token estimates.
    Admits artifacts by admission score until budget is exhausted.
    """
    ranked = sorted(artifacts, key=score_for_admission, reverse=True)

    admitted: List[Tuple[Artifact, int]] = []
    excluded: List[Tuple[Artifact, int]] = []

    used = 0
    for a in ranked:
        t = counter.count_artifact(a.content)
        if t == 0:
            # Empty content, exclude by default to avoid false admission.
            excluded.append((a, t))
            continue

        if used + t <= budget_tokens:
            admitted.append((a, t))
            used += t
        else:
            excluded.append((a, t))

    return admitted, excluded


def fmt_pct(x: float) -> str:
    return f"{x * 100:.1f}%"


def print_table(rows: List[List[str]], headers: List[str]) -> None:
    cols = list(zip(*([headers] + rows))) if rows else [headers]
    widths = [max(len(str(cell)) for cell in col) for col in cols]

    def _line(parts: List[str]) -> str:
        return "  ".join(str(p).ljust(w) for p, w in zip(parts, widths))

    print(_line(headers))
    print(_line(["-" * w for w in widths]))
    for r in rows:
        print(_line(r))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Context Triage demo: estimate context budget usage and preview admission."
    )
    parser.add_argument(
        "--input",
        "-i",
        default="-",
        help="Path to context bundle JSON. Use '-' to read from stdin.",
    )
    parser.add_argument(
        "--budget",
        "-b",
        type=int,
        default=8000,
        help="Token budget for admission preview (heuristic tokens).",
    )
    parser.add_argument(
        "--chars-per-token",
        type=int,
        default=4,
        help="Heuristic: characters per token.",
    )
    parser.add_argument(
        "--overhead",
        type=int,
        default=10,
        help="Heuristic: per artifact overhead tokens.",
    )
    parser.add_argument(
        "--max-content-preview",
        type=int,
        default=0,
        help="If > 0, prints a short content preview per artifact (first N chars).",
    )
    args = parser.parse_args()

    counter = HeuristicTokenCounter(
        chars_per_token=args.chars_per_token,
        per_artifact_overhead=args.overhead,
    )

    if args.budget <= 0:
        print("ERROR: budget must be a positive integer", file=sys.stderr)
        return 2

    try:
        bundle = load_json_from_path_or_stdin(args.input)
        artifacts = normalize_bundle(bundle)
    except Exception as e:
        print(f"ERROR: failed to load/parse context bundle: {e}", file=sys.stderr)
        return 2

    if not artifacts:
        print("No artifacts found in bundle.artifacts", file=sys.stderr)
        return 1

    # Compute totals
    per_artifact_tokens = [(a, counter.count_artifact(a.content)) for a in artifacts]
    total_tokens = sum(t for _, t in per_artifact_tokens)
    utilization = total_tokens / float(args.budget) if args.budget > 0 else 0.0

    breakdown = compute_breakdown(artifacts, counter)
    admitted, excluded = admission_preview(artifacts, counter, args.budget)

    admitted_tokens = sum(t for _, t in admitted)
    excluded_tokens = sum(t for _, t in excluded)

    # Summary
    print("")
    print("Context Budget Report (heuristic)")
    print("--------------------------------")
    print(f"Artifacts:          {len(artifacts)}")
    print(f"Budget (tokens):    {args.budget}")
    print(f"Estimated total:    {total_tokens}")
    print(f"Utilization:        {fmt_pct(utilization)}")
    print("")

    # Breakdown
    print("Breakdown by kind")
    b_rows = [[k, str(v)] for k, v in breakdown.items()]
    print_table(b_rows, headers=["kind", "tokens"])
    print("")

    # Admission preview
    print("Admission preview (ranked by authority + kind + priority)")
    rows: List[List[str]] = []
    for a, t in admitted:
        rows.append([
            "ADMIT",
            a.artifact_id,
            a.kind,
            a.authority,
            str(a.priority),
            str(score_for_admission(a)),
            str(t),
            a.title[:40],
        ])
    for a, t in excluded:
        rows.append([
            "EXCLUDE",
            a.artifact_id,
            a.kind,
            a.authority,
            str(a.priority),
            str(score_for_admission(a)),
            str(t),
            a.title[:40],
        ])

    print_table(
        rows,
        headers=["decision", "id", "kind", "authority", "priority", "score", "tokens", "title"],
    )
    print("")

    print("Totals")
    print("------")
    print(f"Admitted artifacts: {len(admitted)}")
    print(f"Admitted tokens:    {admitted_tokens}")
    print(f"Excluded artifacts: {len(excluded)}")
    print(f"Excluded tokens:    {excluded_tokens}")
    print("")

    if args.max_content_preview > 0:
        n = args.max_content_preview
        print("Content preview (first N characters)")
        print("-----------------------------------")
        for a, t in admitted[: min(10, len(admitted))]:
            preview = (a.content[:n] + ("…" if len(a.content) > n else "")).replace("\n", " ")
            print(f"[ADMIT] {a.artifact_id} ({t} tokens): {preview}")
        for a, t in excluded[: min(10, len(excluded))]:
            preview = (a.content[:n] + ("…" if len(a.content) > n else "")).replace("\n", " ")
            print(f"[EXCL ] {a.artifact_id} ({t} tokens): {preview}")
        print("")

    # Guardrail reminder
    print("Operator reminder")
    print("-----------------")
    print("This report does not determine scope correctness or authority correctness.")
    print("If system or developer instructions appear excluded, halt and escalate.")
    print("")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
