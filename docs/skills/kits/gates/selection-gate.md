---
title: "Selection Gate"
status: stable
version: "1.0"
last_updated: "2025-01-01"
failure_class: degradation
control: selection
---

# Selection Gate

Use this gate to **admit only relevant context** before attention is spent.

```mermaid
flowchart TD
    Cand[Candidate Context] --> Score[Score by relevance/authority/scope]
    Score --> Filter[Reject out-of-scope or low-score]
    Filter --> Admit[Admit top items until budget]
    Filter --> Log[Log rejections]
```

**Inputs**: candidate_context[], scope, authority model, budget (optional)  
**Outputs**: admitted_context[], exclusion_log[]

**Stop if** scope/authority is unclear or budget forces exclusion of mandatory constraints.
