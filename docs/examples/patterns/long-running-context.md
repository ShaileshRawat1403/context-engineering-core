---
title: "Pattern — Long-Running Context"
status: draft
version: "1.0"
last_updated: "2025-01-01"
tags:
  - compression
  - ordering
  - validation
  - scope
---

# Pattern — Long-Running Context

## Problem
Sessions accumulate redundancy and stale assumptions; constraints get displaced; drift emerges over time.

## Failure Signals
- Constraints inconsistently honored mid-session (degradation).
- Stale summaries influence new tasks (drift).
- Tool logs dominate attention (interference).

## Controls
- **Compression:** keep last N turns verbatim; summarize older turns to deltas.  
- **Deduplication:** drop near-duplicates and low-signal chatter.  
- **Scope Reset:** clear task-specific instructions between phases.  
- **Ordering:** constraints first; current task/phase next; then validated summaries.  
- **Validation:** expire stale summaries; validate provenance/authority before reuse.

## Minimal Procedure
1) Estimate budget; mark duplicates and low-signal items.  
2) Compress older turns; mask tool logs to result/status/error.  
3) Reset scope on task/phase change.  
4) Reorder context per authority and phase.  
5) Validate/refresh summaries; expire stale ones.  
6) Emit stabilized context + exclusion/summary logs.

## Minimal Code (compress + mask + reorder)
```python
from typing import List, Dict, Tuple

def stabilize(history: List[Dict], budget: int = 400) -> Tuple[List[Dict], List[Dict]]:
    """
    history: list of artifacts with keys {"kind": "msg|tool|summary", "text": str, "authority": str, "tokens": int}
    Returns (stabilized, excluded_log)
    """
    excluded = []

    # 1) Mask tool logs
    for item in history:
        if item["kind"] == "tool":
            item["text"] = item.get("result", "")  # assume upstream kept result/status/error only
            item["tokens"] = len(item["text"].split())

    # 2) Compress older turns (keep last 4 verbatim)
    if len(history) > 4:
        for item in history[:-4]:
            item["text"] = item["text"][:100]  # naive delta compression
            item["tokens"] = len(item["text"].split())

    # 3) Order: constraints/system > task > user/tool > summaries
    def rank(item: Dict) -> int:
        authority = item.get("authority", "")
        if authority in ("system", "policy"):
            return 3
        if item["kind"] == "summary":
            return 1
        return 2

    ordered = sorted(history, key=rank, reverse=True)

    # 4) Enforce budget
    stabilized, used = [], 0
    for item in ordered:
        if used + item["tokens"] <= budget:
            stabilized.append(item)
            used += item["tokens"]
        else:
            excluded.append({"item": item, "reason": "budget"})

    return stabilized, excluded

# Example usage (trimmed)
history = [
    {"kind": "msg", "text": "System: follow policy", "authority": "system", "tokens": 4},
    {"kind": "tool", "text": "Very long log...", "result": "OK", "tokens": 200},
    {"kind": "msg", "text": "User question...", "authority": "user", "tokens": 20},
]
stabilized, excluded = stabilize(history, budget=50)
print([h["text"] for h in stabilized])
print(excluded)
```

This mirrors the behavior in `examples/long-session-stability-harness/src/truncator.py` but inlined for clarity.

## References
- Runnable: `examples/long-session-stability-harness/` (tests + runner).  
- Controls: `30-control-mechanisms/compression`, `ordering`, `validation`, `isolation`.  
- Skill hooks: session-stabilization operator/agent.
