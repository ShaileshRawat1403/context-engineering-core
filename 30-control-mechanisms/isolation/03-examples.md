---
title: "Isolation — Examples"
layer: "control-mechanisms"
concept: "isolation"
status: "stable"
version: "1.0"
last_updated: "2025-01-01"
depends_on:
  - "./00-spec.md"
  - "./01-failure-signals.md"
  - "./02-trade-offs.md"
related_primitives:
  - "../../10-primitives/boundaries/00-spec.md"
  - "../../10-primitives/scope/00-spec.md"
  - "../../10-primitives/lifetimes/00-spec.md"
related_failures:
  - "../../20-failure-mechanics/interference/00-spec.md"
  - "../../20-failure-mechanics/poisoning/00-spec.md"
---

# Isolation — Examples

These examples show how hard isolation boundaries prevent cross-domain influence and contain failures.

---

## Example 1: Parallel Tasks Isolation

**Context**  
Two tasks run concurrently: billing and support.

**Failure (without isolation)**  
- Support context leaks into billing decisions.  
- Outputs change when tasks are reordered.

**Isolation Applied**  
- Separate context assemblies per task.  
- No shared summaries or memory.  
- Only explicit, typed handoff artifacts allowed.

**Outcome**  
- Tasks become order-invariant.  
- Cross-task contamination eliminated.

---

## Example 2: Untrusted Tool Sandbox

**Context**  
An external tool returns untrusted data and logs.

**Failure (without isolation)**  
- Tool output influences protected system policy.  
- Poisoning risk from manipulated responses.

**Isolation Applied**  
- Tool runs in a sandbox; outputs quarantined.  
- Only validated, schema-checked fields can cross boundary.

**Outcome**  
- Tool cannot alter policy or high-authority context.  
- Poisoned outputs contained.

---

## Example 3: Experimental vs Production Prompts

**Context**  
Experimenting with new prompts alongside production prompts.

**Failure (without isolation)**  
- Experimental behavior leaks into production runs.  
- A/B tests contaminate stable outputs.

**Isolation Applied**  
- Separate environments and context stores.  
- No shared caches or memories.  
- Results exported only through reviewed reports.

**Outcome**  
- Production behavior remains stable.  
- Experiments cannot influence production without approval.

---

## Example 4: Phase Isolation (Planning vs Execution)

**Context**  
Planning phase generates alternatives; execution should follow a chosen plan.

**Failure (without isolation)**  
- Alternatives leak into execution; outputs hedge or oscillate.

**Isolation Applied**  
- Planning context discarded or masked after selection.  
- Execution context rebuilt from selected plan only.

**Outcome**  
- Decisive execution; no hedging.  
- Planning failures contained to planning phase.

---

## Example Invariants

- Isolation prevents influence, not just visibility.  
- If removing shared state fixes leakage, isolation was missing.  
- Overrides must be rare and accountable.  
- Isolation is appropriate when blast-radius risk outweighs reuse benefits.
