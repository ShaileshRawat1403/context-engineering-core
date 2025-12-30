---
title: "Pattern — Multi-Agent Orchestration"
status: draft
version: "1.0"
last_updated: "2025-01-01"
tags:
  - isolation
  - authority
  - validation
---

# Pattern — Multi-Agent Orchestration

## Problem
Multiple agents collaborate without clear authority or isolation; instructions bleed across roles; conflicts go unchecked.

## Failure Signals
- Agent outputs override coordinator policy (authority inversion).
- One agent’s context appears in another’s scope (cross-boundary leakage).
- Conflicting plans proceed simultaneously (coordination failure).

## Controls
- **Isolation:** per-agent context boundaries; no shared state without mediation.  
- **Authority Ordering:** coordinator/system constraints first; agent advisories after.  
- **Validation:** cross-check agent claims; require approvals for state changes.  
- **Masking:** redact sensitive data before inter-agent sharing.

## Minimal Procedure
1) Define authority and data-sharing rules per agent.  
2) Route all inter-agent messages through a mediator that enforces scope/authority.  
3) Validate critical claims with a second source or human review.  
4) Log provenance and approvals for shared state changes.  
5) Halt/resolve conflicts before execution.

## Minimal Code (mediated message passing)
```python
from typing import Dict, List

AUTHORITY = {"system": 3, "coordinator": 2, "agent": 1, "advisory": 0}

def mediate(message: Dict, allowed_scopes: List[str]) -> bool:
    """
    message: {"from": "agentA", "authority": "agent|coordinator", "scope": "task-x", "content": str}
    Enforces scope and authority before forwarding.
    """
    if message["scope"] not in allowed_scopes:
        return False
    if AUTHORITY.get(message["authority"], 0) < AUTHORITY["agent"]:
        return False
    # In a real system, add validation and logging here
    return True

# Example usage
msg = {"from": "agentA", "authority": "agent", "scope": "task-x", "content": "Proposed plan"}
if mediate(msg, allowed_scopes=["task-x"]):
    print("Forwarded to coordinator")
else:
    print("Rejected")
```

Use this pattern to gate cross-agent messages and prevent authority/scope violations.

## References
- Controls: `30-control-mechanisms/isolation`, `ordering`, `validation`, `masking`.  
- Skills: boundary-hardening, retrieval gating (for cross-agent data flow).  
- Apply similar gating/ordering as in the RAG and session harness examples for any shared context.
