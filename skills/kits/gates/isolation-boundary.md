---
title: "Isolation Boundary"
status: stable
version: "1.0"
last_updated: "2025-01-01"
failure_class: interference
control: isolation
---

# Isolation Boundary

Use this gate to **prevent any cross-domain influence** between contexts, agents, or environments.

```mermaid
flowchart LR
    A[Domain A] -. no shared state .-> B[Domain B]
    A -->|typed handoff only| H[Reviewed Artifact]
    H --> B
```

**Inputs**: boundary definition (domains, allowed handoffs)  
**Outputs**: enforcement rules + verification checklist

**Stop if** a non-reviewed path would be required to proceed or if the boundary is bypassable.
