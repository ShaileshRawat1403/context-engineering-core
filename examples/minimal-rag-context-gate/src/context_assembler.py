from __future__ import annotations

from typing import List

from .gates import Artifact


def assemble_context(artifacts: List[Artifact]) -> str:
    """
    Produces a simple ordered context string for demo/testing.
    System/developer/tasks appear first by virtue of pre-ordering in inputs.
    """
    parts: List[str] = []
    for a in artifacts:
        parts.append(f"[{a.kind}:{a.artifact_id}] {a.content}")
    return "\n".join(parts)
