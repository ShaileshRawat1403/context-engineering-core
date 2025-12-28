---
title: "Retrieval Gating — Examples"
archetype: examples
status: stable
owner: context-engineering-core
maintainer: context-engineering-core
version: "1.0"
tags:
  - skills
  - operator
  - retrieval
  - examples
last_reviewed: "2025-12-26"
---

# Retrieval Gating — Before / After

```mermaid
flowchart LR
    B[Raw Retrieval] --> Gate[Scoring + Filtering + Budget]
    Gate --> A[Admitted Set]
    A --> Checks[Authority/Scope Verified]
```

## ✅ Acceptable Execution

- **Before:** 20 retrieved docs; many off-topic; total size 3x budget.
- **Intervention:** scored by relevance and authority, removed duplicates, enforced retrieval token cap.
- **After:** 4 docs admitted; exclusion log captured; constraints remain visible.
- **Checks:** no scope violations; budget within limit.

## ❌ Incorrect Execution

- **Before:** mix of current and outdated policies retrieved.
- **Error:** admitted all docs; trusted by default.
- **Outcome:** outdated policy overrode new one; misaligned outputs.
- **Correction:** require freshness/authority scoring; reject stale items.
