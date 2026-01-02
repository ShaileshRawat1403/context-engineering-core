---
title: "Glossary"
layer: "core"
concept: "glossary"
status: "stable"
version: "1.0"
last_updated: "2025-01-01"
depends_on:
  - "./00-intent-and-scope.md"
  - "./01-how-to-use-this-repo.md"
related_controls: []
related_failures: []
---

# Glossary

This glossary defines **canonical terms** as they are used in this repository.

Definitions here are **operational**, not linguistic.
If a term is ambiguous in common usage, this glossary resolves that ambiguity for the purpose of this repository.

---

## Core Terms

### Context

The **bounded set of information** made available to a model or agent at a given moment, subject to attention constraints.

Context includes:

- instructions
- retrieved data
- memory
- tool definitions
- intermediate outputs

Context is not unlimited storage. It is a **competitive attention space**.

---

### Attention

The mechanism by which a model allocates limited focus across context elements.

Attention is:

- scarce
- position-sensitive
- non-uniform across the context window

Adding more context does not increase attention capacity.

---

### Signal

Information that **materially influences** model behavior toward an intended outcome.

Signal is defined relative to:

- task intent
- constraints
- decision requirements

Signal is not synonymous with relevance; it is **impactful information under attention limits**.

---

### Noise

Information that **consumes attention without improving outcomes**.

Noise may be:

- redundant
- outdated
- weakly related
- conflicting

Noise is often introduced unintentionally through accumulation.

---

### Scope

The **explicit boundary of what a system is allowed to consider** for a task.

Scope constrains:

- what information may enter context
- what decisions may be made
- what outputs are acceptable

Unscoped systems drift by default.

---

### Boundary

A **hard exclusion rule** that prevents certain information or behaviors from entering or influencing context.

Boundaries differ from scope:

- scope limits _what is considered_
- boundaries prohibit _what must not be considered_

---

### Lifetime

The **temporal validity** of a context element.

Lifetimes determine:

- when information is introduced
- how long it persists
- when it must be removed or refreshed

Expired context is a primary source of silent failure.

---

## Failure-Related Terms

### Failure

A **predictable breakdown** in system behavior caused by violated constraints, not by randomness.

Failures are structural and repeatable.

---

### Failure Signal

An **observable symptom** indicating that a failure is occurring or imminent.

Signals may be:

- behavioral
- qualitative
- quantitative
- delayed

Absence of signals does not imply absence of failure.

---

### Degradation

Progressive loss of output quality as context grows or attention is diluted.

Often manifests without explicit errors.

---

### Poisoning

Introduction of misleading or adversarial information that corrupts reasoning.

Poisoning can be accidental or intentional.

---

### Interference

Mutual disruption between context elements competing for attention.

Interference increases with unstructured accumulation.

---

### Drift

Gradual deviation from original intent over time or iterations.

Drift is often mistaken for “emergent behavior”.

---

## Control-Related Terms

### Control

An **intentional mechanism** used to constrain, shape, or prioritize context.

Controls do not eliminate failure; they **trade one risk for another**.

---

### Selection

Choosing which information enters context.

Selection is exclusionary by nature.

---

### Ordering

Arranging context elements to influence attention allocation.

Ordering creates implicit priority.

---

### Masking

Preventing certain information from being attended to or used.

Masking hides information without deleting it.

---

### Compression

Reducing information volume while attempting to preserve signal.

Compression always loses information.

---

## System-Level Terms

### Agent

A system component that:

- receives context
- makes decisions
- may invoke tools
- may persist state

Agents are not autonomous by default.

---

### Memory

Persisted information available across interactions.

Memory is a system manifestation, not a primitive.

---

### Tool

An external capability callable by an agent.

Tools extend action space but increase coordination complexity.

---

### Evaluation

A mechanism for assessing outputs, decisions, or behavior.

Evaluation is a system manifestation, not a control.

---

## Governance Terms

### Review

Human inspection of system inputs, outputs, or decisions.

Review exists to catch failures automation cannot detect reliably.

---

### Acceptance

A human decision to allow an output or action to proceed.

Acceptance is an accountability boundary.

---

### Escalation

Routing control to a human when predefined conditions are met.

Escalation is a design choice, not an exception.

---

### Accountability

Explicit assignment of responsibility for system outcomes.

Accountability cannot be delegated to a model.

---

## Conceptual Relationships

The following diagram illustrates how core terms relate across layers:

```mermaid
graph TD
    A[Context] --> B[Attention]
    B --> C[Signal]
    B --> D[Noise]

    A --> E[Scope]
    A --> F[Boundary]
    A --> G[Lifetime]

    B --> H[Failure]
    H --> I[Degradation]
    H --> J[Poisoning]
    H --> K[Interference]
    H --> L[Drift]

    H --> M[Control]
    M --> N[Selection]
    M --> O[Ordering]
    M --> P[Masking]
    M --> Q[Compression]
```
---

## Terminology Discipline

- Terms defined here must be used consistently.
- If a term is not defined here, it must not be introduced casually.
- Redefinitions require explicit justification and versioning.

---

## Status

This glossary is **stable**.

Additions are permitted only when a new concept cannot be expressed using existing terms.


## Failure Mechanics

### Selection (control)

Admitting or excluding context items based on authority, relevance, freshness, and provenance under a budget.

---

### Ordering (control)

Deliberate placement of context to preserve authority and salience; constraints first, then task, then references.

---

### Masking (control)

Redaction or removal of sensitive/irrelevant fields (e.g., tool logs) before context admission.

---

### Compression (control)

Reducing size while preserving required signal and provenance; non-compressible constraints stay intact.

---

### Validation (control)

Gate that checks provenance, scope, authority, and freshness before admission or persistence.

---

### Isolation (control)

Separating tasks/roles/tenants/tools and their memories to prevent cross-domain influence.

---

### Authority Model

Explicit precedence of instructions and sources (system > developer > task > user > references > tools).

---

### Provenance

Trace of where a context element came from; required for validation, trust, and rollback.

---

### Budget

Declared limit on attention/tokens for a task; governs selection, compression, ordering.

---

### TTL (Time To Live)

Lifetime bound after which a context element must expire or be refreshed.

---

### Handoff Artifact

Structured output passed between scoped roles/tasks (result/status/error), not the upstream prompt.

---

