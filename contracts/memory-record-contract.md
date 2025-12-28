---
title: "Memory Record Contract"
status: stable
version: "1.0"
last_updated: "2025-01-01"
---

# Memory Record Contract

Defines the required fields and governance rules for any artifact persisted to memory.

```mermaid
flowchart TD
    Artifact[Memory Record] --> Meta[Provenance + Scope + Authority]
    Meta --> Life[Lifetime/Expiry]
    Life --> Valid[Validation Gate]
    Valid --> Store[Store/Reject]
```

## Required Fields

- `id`, `source`, `authority`, `scope`, `timestamp`
- `lifetime` (ephemeral/session/durable/persistent) with expiry timestamp
- `content` (text or structured data)
- `integrity` indicators (hash, signature if available)

## Governance Rules

- Validation on write and read; UNKNOWN provenance rejected.
- Promotion between lifetimes requires approval.
- Rollback path must exist for persistent entries.
- Access controlled by role/scope; auditing enabled.
