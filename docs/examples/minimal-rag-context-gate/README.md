---
title: "Minimal RAG Context Gate — README"
status: stable
version: "1.0"
last_updated: "2025-01-01"
---

# Minimal RAG Context Gate

Demonstrates retrieval gating and context assembly with budget enforcement.

```mermaid
flowchart TD
    Q[User Query] --> Ret[Retrieve Docs]
    Ret --> Gate[Selection + Dedup + Budget Gate]
    Gate --> Order[Ordering/Masking]
    Order --> Gen[Generation]
```

- PRD: requirements and scope  
- Architecture: high-level diagram of gates  
- Source: `src/context_assembler.py`, `src/gates.py`, `src/runner.py`  
- Tests: see `tests/`
