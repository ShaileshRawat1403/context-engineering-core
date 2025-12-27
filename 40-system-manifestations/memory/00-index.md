---
title: "Memory — Index"
layer: "system-manifestations"
concept: "memory"
status: "stable"
version: "1.0"
last_updated: "2025-01-01"
depends_on:
  - "../00-index.md"
  - "../../10-primitives/lifetimes/00-spec.md"
  - "../../10-primitives/boundaries/00-spec.md"
  - "../../30-control-mechanisms/validation/00-spec.md"
  - "../../30-control-mechanisms/isolation/00-spec.md"
---

# Memory — Index

Memory is treated as an **attack surface and persistence boundary**.

This section will describe:
- how lifetimes, validation, and isolation govern memory stores
- how poisoning and drift surface through persistence
- how to constrain promotion, retention, and rollback

Memory documents must never override primitives or controls; they instantiate them.

---

## Manifestation Focus

- **Promotion/Demotion**: Rules for moving artifacts across lifetimes (ephemeral → session → durable → persistent).
- **Validation**: Required metadata and checks before any write/refresh.
- **Isolation**: Separating untrusted/experimental memory from production state.
- **Rollback**: How to revert corrupted or stale memory deterministically.

---

## Failure Mapping

- **Poisoning**: corrupted writes, untrusted sources persisted.
- **Drift**: stale assumptions retained past lifetime.
- **Interference**: shared memory across roles/agents without scope.

Controls: validation, isolation, masking (visibility), selection (what can be persisted), ordering (what dominates on read).

---

## Governance Hooks

- Owner of memory schema and promotion rules
- Acceptance criteria for persistent changes
- Escalation triggers (validation failure, provenance missing, rollback required)
