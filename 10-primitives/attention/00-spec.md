---
title: "Attention"
layer: "primitives"
concept: "attention"
status: "stable"
version: "1.0"
last_updated: "2025-01-01"
depends_on: []
related_primitives:
  - "../signal-vs-noise/00-spec.md"
  - "../boundaries/00-spec.md"
  - "../scope/00-spec.md"
  - "../lifetimes/00-spec.md"
related_failures:
  - "../../20-failure-mechanics/degradation/00-spec.md"
  - "../../20-failure-mechanics/interference/00-spec.md"
---

# Attention

This specification defines **attention** as the hard capacity constraint in context-engineered systems.

Attention is the **limiting resource** that governs how much context can influence behavior.  
Tokens are an approximation; usable attention is the constraint.

Without explicit attention management, context accumulation produces degradation and interference.

---

## Definition

**Attention** is the finite cognitive budget a model allocates to contextual signals when producing an output.

Properties:
- **Bounded**: cannot be expanded by adding more tokens
- **Competitive**: signals compete for salience
- **Order-sensitive**: position and recency bias allocation
- **Non-linear**: overload causes collapse, not graceful decay

---

## Why Attention Is Primitive

- All controls ultimately arbitrate attention (selection, ordering, compression).
- Failure mechanics (degradation, interference) are attention-mediated.
- Primitives that ignore attention become aspirational, not operational.

---

## Attention vs Context Size

- Large context windows do **not** imply large attention.
- Adding tokens can reduce effective attention to high-signal constraints.
- Attention must be **budgeted**, not assumed.

---

## Attention Pressure Sources

- Long message histories
- Redundant retrievals
- Verbose tool outputs
- Parallel tasks or roles
- Unscoped policies or rubrics

---

## Attention Invariants

- Increasing context without arbitration **reduces** effective attention.
- Weak but critical signals are the first to be displaced.
- Overload causes non-linear failure (sudden collapse, not gradual fade).

---

## Design Implications

- Declare an explicit attention budget per task.
- Bias toward exclusion when salience is uncertain.
- Elevate constraints before background.
- Measure utilization; do not guess.

---

## Non-Claims

This specification does not claim:
- A universal token-to-attention ratio
- That attention can be fully predicted per model
- That larger windows improve outcomes
- That attention can be “optimized away”

It defines the constraint, not its vendor-specific behavior.

---

## Status

This specification is **stable**.  
Changes require explicit justification and must not weaken the primacy of attention as a binding constraint.
