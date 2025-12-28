from __future__ import annotations

import re
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
                artifact_id=str(raw.get("id") or f"a{i}"),
                kind=str(raw.get("kind") or "other"),
                authority=str(raw.get("authority") or "other"),
                priority=_safe_int(raw.get("priority"), 0),
                title=str(raw.get("title") or ""),
                content=str(raw.get("content") or ""),
            )
        )
    return artifacts


class HeuristicTokenCounter:
    def __init__(self, chars_per_token: int = 4, overhead: int = 8) -> None:
        self.chars_per_token = max(1, chars_per_token)
        self.overhead = max(0, overhead)

    def count(self, text: str) -> int:
        base = len(text) // self.chars_per_token
        if base == 0:
            return 0
        return base + self.overhead


PII_RE = re.compile(r"[0-9]{3,}")


def mask_pii(text: str) -> str:
    return PII_RE.sub("[REDACTED]", text)


def truncate_session(bundle: Dict[str, Any], budget_tokens: int = 400) -> Tuple[List[Artifact], int]:
    """
    Simple stabilizer:
    - Masks obvious PII
    - Keeps system/task and latest 2 messages
    - Drops verbose tool logs if over budget
    """
    artifacts = load_bundle(bundle)
    if not artifacts:
        return [], 0

    counter = HeuristicTokenCounter()
    kept: List[Artifact] = []

    # Always keep system/task
    system_like = [a for a in artifacts if a.kind in {"system", "task"}]
    messages = [a for a in artifacts if a.kind == "message"]
    others = [a for a in artifacts if a.kind not in {"system", "task", "message"}]

    # Mask PII in messages
    for m in messages:
        m.content = mask_pii(m.content)

    kept.extend(system_like)
    kept.extend(messages[-2:])  # keep last 2 messages

    used = sum(counter.count(a.content) for a in kept)
    for a in others:
        t = counter.count(a.content)
        if used + t <= budget_tokens:
            kept.append(a)
            used += t
        else:
            # skip if over budget
            continue

    # Ensure deterministic ordering: system/task first, then remaining by priority
    kept = sorted(kept, key=lambda a: (-1 if a.kind in {"system", "task"} else 0, -a.priority))
    total_tokens = sum(counter.count(a.content) for a in kept)
    return kept, total_tokens
