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

```mermaid
flowchart TD
    O[Orchestrator] --> A1[Agent: Research]
    O --> A2[Agent: Execute]
    O --> A3[Agent: Review]
    A1 -. typed handoff .-> A2
    A2 -. typed handoff .-> A3
    O -->|arbitration + ordering| D[Decision]
    classDef agent fill:#eef,stroke:#336;
    class A1,A2,A3 agent;
```

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

---

## Execution Path (quick)

- **Inputs**: authority model; allowed/forbidden actions; scope per role; tool/memory access policy; logging/reporting requirements
- **Steps**: bind agent to role/scope; restrict actions and tool access; require validation gates; log actions/outputs; separate channels (instruction/data/tools)
- **Checks**: actions within allowlist; authority order preserved; outputs validated; isolation boundaries intact
- **Stop/escate**: scope/role ambiguous; required validation unavailable; privilege escalation detected

---
