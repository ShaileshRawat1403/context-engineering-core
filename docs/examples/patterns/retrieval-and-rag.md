---
title: "Pattern — Retrieval & RAG"
status: draft
version: "1.0"
last_updated: "2025-01-01"
tags:
  - selection
  - ordering
  - validation
---

# Pattern — Retrieval & RAG

## Problem
Retrieved text displaces constraints or injects noise; budgets are exceeded; authority is ambiguous.

## Failure Signals
- Long snippets bury short constraints (interference).
- Budget exceeded by retrieval alone (degradation).
- Untrusted sources treated as authoritative (poisoning).

## Controls
- **Selection:** filter by relevance/authority; cap items and tokens.
- **Ordering:** constraints first; current task next; retrieval last.
- **Validation:** provenance tags; reject untrusted sources; dedupe near-identical hits.

## Minimal Procedure
1) Score and filter retrieved chunks by authority + relevance.  
2) Deduplicate overlapping chunks.  
3) Enforce token budget; drop lowest-priority chunks first.  
4) Order context: constraints → task → user → retrieval.  
5) Emit rationale/log of inclusions/exclusions.

## Minimal Code (authoritative filter + budget gate)
```python
from typing import List, Tuple

def gate_retrieval(chunks: List[dict], budget_tokens: int) -> Tuple[List[dict], List[dict]]:
    """
    chunks: [{"text": str, "relevance": float, "authority": "spec|release|ticket|advisory", "tokens": int}]
    Returns: (admitted, excluded) with simple authority + budget policy.
    """
    authority_rank = {"spec": 3, "release": 2, "ticket": 1, "advisory": 0}

    # Filter low authority first
    filtered = [c for c in chunks if authority_rank.get(c["authority"], 0) >= 1]

    # Sort by (authority desc, relevance desc)
    filtered.sort(key=lambda c: (authority_rank.get(c["authority"], 0), c["relevance"]), reverse=True)

    admitted, excluded, used = [], [], 0
    for c in filtered:
        if used + c["tokens"] <= budget_tokens:
            admitted.append(c)
            used += c["tokens"]
        else:
            excluded.append((c, "budget"))
    return admitted, excluded


# Example usage
chunks = [
    {"text": "Spec: API contract v2", "relevance": 0.9, "authority": "spec", "tokens": 80},
    {"text": "Forum post", "relevance": 0.8, "authority": "advisory", "tokens": 60},
    {"text": "Release note patch", "relevance": 0.7, "authority": "release", "tokens": 50},
]

admitted, excluded = gate_retrieval(chunks, budget_tokens=120)
print("Admitted:", [c["authority"] for c in admitted])  # ['spec', 'release']
print("Excluded reasons:", excluded)  # advisory filtered by authority; budget overflow entries marked
```

This mirrors the policy in `examples/minimal-rag-context-gate/src/gates.py` and can be adapted directly.

## References
- Runnable: `examples/minimal-rag-context-gate/` (tests + runner).  
- Controls: `30-control-mechanisms/selection`, `ordering`, `validation`.  
- Skill hooks: operator/agent context triage and retrieval gating.
