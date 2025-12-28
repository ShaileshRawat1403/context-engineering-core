---
title: "PRD — Minimal RAG Context Gate"
status: stable
version: "1.0"
last_updated: "2025-01-01"
---

# Product Requirements — Minimal RAG Context Gate

Goal: demonstrate selection, ordering, masking, and validation on retrieved context before generation.

```mermaid
flowchart TD
    Query[Query] --> Retrieve[Retriever]
    Retrieve --> Select[Selection/Dedup]
    Select --> Budget[Budget Gate]
    Budget --> Assemble[Context Assembler]
    Assemble --> Gen[LLM Generation]
```

## Requirements
- Input: user query + retrieved documents.
- Controls: selection, ordering, masking of rubrics/system constraints, optional validation of cached retrieval.
- Output: ordered context assembly + generation result + logs.
- Tests: ordering invariance, budget enforcement, masking correctness.

## Non-Goals
- Retriever quality benchmarking.
- Prompt optimization beyond gating steps.
- Vendor-specific integrations.
