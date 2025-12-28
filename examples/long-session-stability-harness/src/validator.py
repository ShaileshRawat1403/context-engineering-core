from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


@dataclass
class Artifact:
    artifact_id: str
    kind: str
    authority: str
    priority: int
    title: str
    content: str


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


def validate_no_pii(artifacts: List[Artifact]) -> bool:
    return all(not PII_RE.search(a.content) for a in artifacts)


def validate_budget(artifacts: List[Artifact], budget_tokens: int) -> bool:
    counter = HeuristicTokenCounter()
    total = sum(counter.count(a.content) for a in artifacts)
    return total <= budget_tokens


def validate_authority_order(artifacts: List[Artifact]) -> bool:
    """System/developer should appear before user/tool content."""
    ids = [a.kind for a in artifacts]
    try:
        first_user = ids.index("message")
    except ValueError:
        return True
    try:
        first_system = ids.index("system")
    except ValueError:
        return False
    try:
        first_task = ids.index("task")
    except ValueError:
        first_task = first_system
    return first_system <= first_user and first_task <= first_user
