---
title: "Agents — Index"
layer: "system-manifestations"
concept: "agents"
status: "stable"
version: "1.0"
last_updated: "2025-01-01"
depends_on:
  - "../00-index.md"
  - "../../10-primitives/boundaries/00-spec.md"
  - "../../10-primitives/scope/00-spec.md"
  - "../../30-control-mechanisms/ordering/00-spec.md"
  - "../../30-control-mechanisms/masking/00-spec.md"
  - "../../30-control-mechanisms/isolation/00-spec.md"
---

# Agents — Index

Agents are **orchestrated roles with explicit boundaries**, not free-form personas.

This section will describe:
- how scope, masking, ordering, and isolation apply to single- and multi-agent systems
- how agent collisions map to interference
- how authority and escalation are enforced in orchestration

Agent documents must not redefine governance; they apply existing primitives and controls to orchestration.

---

## Manifestation Focus

- **Role Boundaries**: explicit scopes per agent; no shared implicit context.
- **Coordination**: ordering and arbitration between agents; single-writer or turn-based constraints.
- **Isolation**: hard separation between experimental and production agents.
- **Handoffs**: typed artifacts for passing state; validation on receipt.

---

## Failure Mapping

- **Interference**: cross-agent contamination, arbitration failure.
- **Poisoning**: untrusted agent output influencing protected flows.
- **Drift**: long-lived shared state without refresh.

Controls: masking, selection, ordering, isolation, validation.

---

## Governance Hooks

- Authority model for orchestrator vs agents
- Escalation when arbitration fails
- Acceptance of new agent roles or behaviors
