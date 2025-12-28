#!/usr/bin/env python3
"""
Purpose: Demonstrate simple authority + priority reordering for Context Triage
Skill: skills/operator/context-triage/SKILL.md
Note: Illustrative script. Not production code. Authority: human-supervised execution.

What this script does
- Loads a context bundle (JSON) from a file path or stdin
- Normalizes artifacts and enforces allowed authority/kind values
- Computes an admission score (authority weight + kind weight + explicit priority)
- Outputs the reordered artifact list for operator review

What this script does not do
- It does not decide scope correctness
- It does not enforce budget
- It does not alter or summarize content
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Artifact:
    artifact_id: str
    kind: str
    authority: str
    priority: int
    title: str
    content: str


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


def load_json_from_path_or_stdin(path: Optional[str]) -> Dict[str, Any]:
    if path and path != "-":
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return json.load(sys.stdin)


def normalize_bundle(bundle: Dict[str, Any]) -> List[Artifact]:
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
            )
        )
    return artifacts


def score(a: Artifact) -> int:
    """
    Admission score: authority weight + kind weight + explicit priority.
    Higher score ranks earlier.
    """
    return (
        DEFAULT_AUTHORITY_WEIGHT.get(a.authority, 0)
        + DEFAULT_KIND_WEIGHT.get(a.kind, 0)
        + a.priority
    )


def reorder(artifacts: List[Artifact]) -> List[Tuple[Artifact, int]]:
    ranked = sorted(artifacts, key=lambda a: score(a), reverse=True)
    return [(a, score(a)) for a in ranked]


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
        description="Context Triage demo: reorder artifacts by authority + kind + priority."
    )
    parser.add_argument(
        "--input",
        "-i",
        default="-",
        help="Path to context bundle JSON. Use '-' to read from stdin.",
    )
    args = parser.parse_args()

    try:
        bundle = load_json_from_path_or_stdin(args.input)
        artifacts = normalize_bundle(bundle)
    except Exception as e:
        print(f"ERROR: failed to load/parse context bundle: {e}", file=sys.stderr)
        return 2

    if not artifacts:
        print("No artifacts found in bundle.artifacts", file=sys.stderr)
        return 1

    ranked = reorder(artifacts)

    print("")
    print("Reorder by Authority + Kind + Priority")
    print("--------------------------------------")
    print(f"Artifacts: {len(artifacts)}")
    print("")

    rows: List[List[str]] = []
    for a, s in ranked:
        rows.append([
            a.artifact_id,
            a.kind,
            a.authority,
            str(a.priority),
            str(s),
            a.title[:40],
        ])

    print_table(
        rows,
        headers=["id", "kind", "authority", "priority", "score", "title"],
    )
    print("")

    print("Operator reminder")
    print("-----------------")
    print("This is a ranking aid, not an admission decision.")
    print("Scope filtering and budget enforcement must run separately.")
    print("")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
