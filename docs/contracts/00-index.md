---
title: "Contracts — Index"
status: "stable"
version: "1.0"
last_updated: "2025-01-01"
---

# Contracts — Index

Contracts define **schemas and governance rules** for artifacts that cross system boundaries (tools, memory, evaluation).

```mermaid
flowchart TD
    Artifact[Artifact] --> Schema[Schema + Required Fields]
    Schema --> Gov[Governance Rules]
    Gov --> Validate[Validation/Acceptance]
    Validate --> Use[Allowed in Context]
```

Each contract is binding; if an artifact does not meet its contract, it must be rejected, quarantined, or refreshed before use.
