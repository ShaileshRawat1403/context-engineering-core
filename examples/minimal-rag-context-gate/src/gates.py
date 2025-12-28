from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


@dataclass
class Artifact:
    artifact_id: str
    kind: str
    authority: str
    priority: int
    title: str
    content: str


AUTHORITY_WEIGHT = {
    "system": 1000,
    "developer": 800,
    "user": 600,
    "tool": 400,
    "other": 200,
}

KIND_WEIGHT = {
    "system": 120,
    "task": 100,
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


def load_bundle(bundle: Dict[str, Any]) -> List[Artifact]:
    artifacts: List[Artifact] = []
    for i, raw in enumerate(bundle.get("artifacts", [])):
        if not isinstance(raw, dict):
            continue
        artifacts.append(
            Artifact(
                artifact_id=str(raw.get("id") or raw.get("artifact_id") or f"a{i}"),
                kind=str(raw.get("kind") or "other"),
                authority=str(raw.get("authority") or "other"),
                priority=_safe_int(raw.get("priority"), 0),
                title=str(raw.get("title") or ""),
                content=str(raw.get("content") or ""),
            )
        )
    return artifacts


class HeuristicTokenCounter:
    """Stable heuristic; keeps tests predictable."""

    def __init__(self, chars_per_token: int = 4, per_artifact_overhead: int = 8) -> None:
        self.chars_per_token = max(1, chars_per_token)
        self.per_artifact_overhead = max(0, per_artifact_overhead)

    def count(self, text: str) -> int:
        base = len(text) // self.chars_per_token
        if base == 0:
            return 0
        return base + self.per_artifact_overhead


def _relevance_score(text: str, question: str) -> int:
    """Tiny overlap heuristic to filter obviously off-topic docs."""
    q_tokens = {t.lower() for t in question.split() if len(t) > 2}
    t_tokens = {t.lower() for t in text.split() if len(t) > 2}
    if not q_tokens:
        return 0
    return len(q_tokens & t_tokens)


def score(artifact: Artifact) -> int:
    return AUTHORITY_WEIGHT.get(artifact.authority, 0) + KIND_WEIGHT.get(artifact.kind, 0) + artifact.priority


def gate_bundle(
    bundle: Dict[str, Any],
    budget_tokens: int = 120,
    max_docs: int = 3,
) -> Tuple[List[Artifact], List[Tuple[Artifact, str]]]:
    """
    Applies a minimal selection/ordering/budget gate.

    Returns (admitted, excluded_with_reason).
    """
    artifacts = load_bundle(bundle)
    if not artifacts:
        return [], []

    # Identify user question for simple relevance check
    user_q = next((a.content for a in artifacts if a.kind == "message"), "")

    counter = HeuristicTokenCounter()
    admitted: List[Artifact] = []
    excluded: List[Tuple[Artifact, str]] = []

    # Filter obviously off-topic documents
    filtered: List[Artifact] = []
    for a in artifacts:
        if a.kind == "document":
            rel = _relevance_score(a.content, user_q)
            if rel == 0:
                excluded.append((a, "out_of_scope"))
                continue
        filtered.append(a)

    # Sort by authority/kind/priority
    ranked = sorted(filtered, key=score, reverse=True)

    used = 0
    doc_count = 0
    for a in ranked:
        t = counter.count(a.content)
        if t == 0:
            excluded.append((a, "empty"))
            continue
        if a.kind == "document":
            doc_count += 1
            if doc_count > max_docs:
                excluded.append((a, "doc_cap"))
                continue
        if used + t > budget_tokens:
            excluded.append((a, "budget"))
            continue
        admitted.append(a)
        used += t

    return admitted, excluded
