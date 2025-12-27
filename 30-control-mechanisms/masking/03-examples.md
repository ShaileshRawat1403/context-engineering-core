---
title: "Masking — Examples"
layer: "control-mechanisms"
concept: "masking"
status: "stable"
version: "1.0"
last_updated: "2025-01-01"
depends_on:
  - "./00-spec.md"
  - "./01-failure-signals.md"
  - "./02-trade-offs.md"
related_primitives:
  - "../../10-primitives/scope/00-spec.md"
  - "../../10-primitives/boundaries/00-spec.md"
  - "../../10-primitives/signal-vs-noise/00-spec.md"
related_failures:
  - "../../20-failure-mechanics/interference/00-spec.md"
  - "../../20-failure-mechanics/poisoning/00-spec.md"
---

# Masking — Examples

This document provides **execution-grounded examples** showing how masking constrains influence without removing context, where failures appear, and how explicit masks change behavior.

Examples focus on **visibility and influence**, not correctness.

---

## Example 1: Policy Visible to Reasoning, Hidden from Execution

### Context

A system includes policy text to guide compliant reasoning.  
Execution output must be concise and user-facing.

---

### Failure (Without Masking)

Observed behavior:
- execution mirrors policy phrasing
- tone becomes legalistic
- usability degrades

Root cause:
- policy context visible to execution role

Downstream failures:
- interference

---

### Masking Applied

**Mask**: Role-based  
**Rule**: Policy visible to reasoning only

```mermaid
flowchart LR
    P[Policy Text]
    R[Reasoning Role]
    E[Execution Role]

    P --> R
    P -. masked .-> E
```

---

### Outcome

- compliant reasoning preserved
- execution becomes usable
- authority boundaries enforced

---

## Example 2: Planning Alternatives Hidden During Execution

### Context

An agent generates a plan with alternatives and assumptions.  
Execution should follow the chosen path only.

---

### Failure (Without Masking)

Observed behavior:

- hedging language persists
- alternatives reappear
- execution hesitates

Root cause:

- planning context visible during execution

Downstream failures:

- interference

---

### Masking Applied

**Mask**: Phase-based  
**Rule**: Planning artifacts hidden after plan selection

```mermaid
flowchart LR
    P[Planning Artifacts]
    X[Mask]
    E[Execution Context]

    P -. masked .-> X
    E --> A[Attention]
```

---

### Outcome

- decisive execution
- clean phase transition
- reduced interference

---

## Example 3: Task-Specific Constraints Isolated

### Context

Two parallel tasks run concurrently.  
Each has distinct constraints.

---

### Failure (Without Masking)

Observed behavior:

- constraints from Task A affect Task B
- outputs mix requirements

Root cause:

- task scope not masked

Downstream failures:

- interference

---

### Masking Applied

**Mask**: Task-based  
**Rule**: Context visible only within task scope

```mermaid
flowchart TD
    TA[Task A Context]
    TB[Task B Context]
    A1[Task A Execution]
    B1[Task B Execution]

    TA --> A1
    TB --> B1
    TA -. masked .-> B1
    TB -. masked .-> A1
```

---

### Outcome

- tasks execute independently
- no cross-contamination
- predictable behavior

---

## Example 4: Evaluation Criteria Hidden from Generation

### Context

Evaluation rubric exists to score outputs.  
Generation should not optimize against the rubric.

---

### Failure (Without Masking)

Observed behavior:

- outputs anticipate scoring criteria
- reasoning becomes self-optimizing
- diversity collapses

Root cause:

- evaluation context visible during generation

Downstream failures:

- interference

---

### Masking Applied

**Mask**: Role + Phase  
**Rule**: Evaluation visible only during evaluation

```mermaid
flowchart LR
    G[Generation]
    E[Evaluation]
    R[Rubric]

    R -. masked .-> G
    R --> E
```

---

### Outcome

- unbiased generation
- cleaner evaluation signal
- reduced interference

---

## Example 5: Authority Masking of Untrusted Input

### Context

User input is combined with untrusted external text.  
System-level decisions must not be influenced by untrusted sources.

---

### Failure (Without Masking)

Observed behavior:

- speculative text affects decisions
- untrusted claims treated as fact

Root cause:

- authority boundaries not enforced

Downstream failures:

- poisoning
- interference

---

### Masking Applied

**Mask**: Authority-based  
**Rule**: Untrusted context hidden from high-impact decisions

```mermaid
flowchart TD
    U[Untrusted Input]
    S[System Logic]
    M[Mask]

    U -. masked .-> S
    S --> A[Attention]
```

---

### Outcome

- reduced poisoning risk
- authority preserved
- predictable behavior

---

## Example Invariants

Across all examples:

- masking restricts influence, not existence
- failures appear as leakage, not absence
- masking clarifies responsibility boundaries
- improper masking causes interference

If context must exist but must not influence, masking is required.

---

## Status

This document is **stable**.

Examples provided here are sufficient to demonstrate masking as a control mechanism governing visibility and influence.
