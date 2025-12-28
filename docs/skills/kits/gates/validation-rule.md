---
title: "Validation Rule"
status: stable
version: "1.0"
last_updated: "2025-01-01"
failure_class: drift
control: validation
---

# Validation Rule

Use this gate to **block stale, untrusted, or out-of-scope artifacts** from reuse.

```mermaid
flowchart TD
    Artifact --> Prov[Provenance/Authority Check]
    Prov --> Scope[Scope Match?]
    Scope --> Fresh[Freshness/Lifetime]
    Fresh --> Conflict[Conflict with higher authority?]
    Conflict -->|no| Admit[Admit]
    Prov -->|fail| Reject
    Scope -->|fail| Reject
    Fresh -->|fail| Refresh
    Conflict -->|yes| Reject
```

**Inputs**: artifact + metadata (provenance, authority, scope, timestamp)  
**Outputs**: decision (admit/reject/refresh) + log

**Stop if** metadata is missing or conflicts cannot be resolved automatically.
