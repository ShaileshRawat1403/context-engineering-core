---
title: "Pattern — Tool-Using Agent"
status: draft
version: "1.0"
last_updated: "2025-01-01"
tags:
  - masking
  - validation
  - isolation
---

# Pattern — Tool-Using Agent

## Problem
Tool outputs (logs/results) overwhelm context or inject untrusted data; authority of tools vs policy is unclear.

## Failure Signals
- Verbose logs displace constraints (degradation).  
- Tool errors echoed as facts (poisoning).  
- Sensitive data leaked from tool responses (interference/poisoning).

## Controls
- **Masking:** keep `{result,status,error}`; drop verbose logs.  
- **Validation:** cross-check critical tool outputs; require provenance.  
- **Isolation:** sandbox tool outputs; limit where they can flow.  
- **Ordering:** constraints and policy before tool outputs; advisory ordering for untrusted tools.

## Minimal Procedure
1) Normalize tool outputs to a compact schema.  
2) Tag outputs with provenance, authority, and timestamp.  
3) Validate critical claims via secondary tool or rules.  
4) Admit only validated outputs into the main context; keep raw logs out of attention.  
5) Escalate on conflicts or missing validation.

## Minimal Code (mask + validate tool output)
```python
from typing import Dict, Tuple

def normalize_tool_output(raw: Dict) -> Dict:
    """Keep only result/status/error; drop verbose logs."""
    return {
        "result": raw.get("result"),
        "status": raw.get("status", "unknown"),
        "error": raw.get("error"),
        "provenance": raw.get("provenance", "tool-x"),
        "authority": raw.get("authority", "tool"),
    }

def validate_tool_output(masked: Dict, fallback: Dict | None = None) -> Tuple[bool, str]:
    """Simple validation: require status=ok and optional cross-check."""
    if masked.get("status") != "ok":
        return False, "non-ok status"
    if fallback and fallback.get("result") != masked.get("result"):
        return False, "mismatch with fallback tool"
    return True, "validated"

# Example usage
raw = {"result": "42", "status": "ok", "log": "verbose...", "provenance": "tool-a"}
masked = normalize_tool_output(raw)
valid, reason = validate_tool_output(masked, fallback={"result": "42", "status": "ok"})
print(masked, valid, reason)
```

Aligns with the masking and validation steps you should apply before adding tool outputs to the active context.

## References
- Controls: `30-control-mechanisms/masking`, `validation`, `isolation`, `ordering`.  
- Apply the masking/ordering approach demonstrated in the long-session harness to tool outputs.
