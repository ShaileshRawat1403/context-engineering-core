---
title: "Primitive Index"
layer: "primitives"
status: "stable"
version: "1.0"
last_updated: "2025-01-01"
---

# Primitive Index

This document defines the **canonical set of primitives** used throughout this repository.

Primitives are **non-negotiable structural concepts**.  
They describe constraints that exist regardless of model choice, framework, or tooling.

```mermaid
graph TD
    A[Attention] --> B[Boundaries]
    B --> Sc[Scope]
    B --> L[Lifetimes]
    A --> N[Signal vs Noise]
    Sc -->|feeds| FM[Failure Mechanics]
    L -->|feeds| FM
    N -->|feeds| FM
```

Primitives are not techniques.  
They are **facts of system behavior**.

---

## What a Primitive Is

A **primitive** is a property of context-engineered systems that:

- cannot be removed through better prompting
- cannot be optimized away
- constrains all higher-level mechanisms
- manifests consistently across architectures

If a concept disappears when tooling changes, it is not a primitive.

---

## Why This Index Exists

This index exists to:

- lock vocabulary
- prevent conceptual drift
- avoid redefinition across layers
- force consistency in later controls and examples

Every higher-layer document must map back to one or more primitives here.

---

## Canonical Primitives (defined)

All primitives below are fully specified and include failure signals, trade-offs, examples, and checks.

---

### 1. Attention

**Constrains**: How much of the context can meaningfully influence behavior.  
**Core insight**: Context size ≠ usable signal.  
**Primary failures**: degradation, interference amplification.  
**Docs**: `10-primitives/attention/`

---

### 2. Boundaries

**Constrains**: Where influence is allowed to flow (authority, scope, time, persistence, channel).  
**Core insight**: Influence without boundaries becomes ambient and accidental.  
**Primary failures**: interference, poisoning, drift acceleration.  
**Docs**: `10-primitives/boundaries/`

---

### 3. Scope

**Constrains**: Where an instruction or signal applies across tasks, roles, phases, agents, and artifacts.  
**Core insight**: Global applicability is the default failure mode.  
**Primary failures**: interference, role collapse.  
**Docs**: `10-primitives/scope/`

---

### 4. Lifetimes

**Constrains**: How long context remains valid or influential.  
**Core insight**: Context does not decay automatically; persistence is a decision.  
**Primary failures**: drift, poisoning.  
**Docs**: `10-primitives/lifetimes/`

---

### 5. Signal vs Noise

**Constrains**: What deserves attention at all, per task/role/phase.  
**Core insight**: Correct-but-irrelevant content is noise; verbosity ≠ salience.  
**Primary failures**: degradation, interference.  
**Docs**: `10-primitives/signal-vs-noise/`

---

## Primitive–Failure Mapping

This table is normative.

| Primitive | Primary Failures Governed |
|--------|---------------------------|
| Attention | Degradation, Interference |
| Boundaries | Interference, Poisoning, Drift |
| Scope | Interference |
| Lifetimes | Drift, Poisoning |
| Signal vs Noise | Degradation |

Any failure explanation that bypasses this mapping is incomplete.

---

## Primitive–Control Relationship

Primitives **precede controls**.

- Primitives define constraints.
- Controls operate *within* those constraints.

If a control attempts to override a primitive, the design is invalid.

---

## What This Index Forbids

This index forbids:

- introducing new primitives casually
- redefining primitives per layer
- collapsing primitives into techniques
- skipping primitives when designing controls

If a concept cannot be grounded here, it does not belong in the repo.

---

## How to Use This Index

When writing or reviewing any document:

1. Identify which primitives it depends on.
2. Verify definitions match this index.
3. Reject any implicit redefinition.
4. Escalate if a new primitive is required.

This is a **governance document**, not a summary.

---

## Status

This index is **stable**.

It may only change if:
- a genuinely new structural constraint is discovered
- existing primitives are proven insufficient

Such changes require explicit justification and review.
