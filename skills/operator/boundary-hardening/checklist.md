---
title: Boundary Hardening — Operator Checklist
archetype: checklist
status: stable
owner: context-engineering-core
maintainer: context-engineering-core
version: 1.0
tags:
  - skills
  - operator
  - boundaries
  - checklist
last_reviewed: 2025-12-26
---

# Boundary Hardening — Operator Checklist

Condensed aid; use only when SKILL is understood.

---

## Preconditions

- [ ] Authority model defined (system > developer > user > tool/untrusted)
- [ ] Scope labels for task/role/phase available
- [ ] Isolation requirements identified
- [ ] Validation rules for persistence/handoffs in place
- [ ] Channel definitions separated (instruction/data/feedback/tool)

If any unchecked, stop.

---

## Execution Checklist

### 1) Inventory and classify
- [ ] All sources listed (system, policy, user, tool, retrieval, memory)
- [ ] Authority, scope, channel, lifetime tagged

### 2) Enforce authority
- [ ] Precedence encoded; lower authority cannot override higher
- [ ] Ordering reflects authority

### 3) Scope containment
- [ ] Masking applied per task/role/phase
- [ ] Scope reset on task/phase change

### 4) Channel separation
- [ ] Instruction vs data vs feedback vs tool outputs separated
- [ ] Instruction-as-data blocked; data-as-instruction blocked

### 5) Isolation (where required)
- [ ] Untrusted/experimental sources sandboxed
- [ ] Cross-boundary influence blocked without promotion

### 6) Validation on persistence/handoff
- [ ] Provenance/authority/scope/lifetime checked before reuse
- [ ] UNKNOWN provenance rejected or quarantined

### 7) Logging and ownership
- [ ] Boundary rules recorded
- [ ] Overrides/isolations logged with owner

---

## Validation Checks (must pass)

- [ ] No authority inversions detected
- [ ] No cross-scope leakage
- [ ] Untrusted inputs quarantined/isolated
- [ ] Provenance present for persistent artifacts
- [ ] Channel separation enforced

---

## Stop/Escalate

Stop and escalate if:
- [ ] Isolation override requested
- [ ] Authority conflict unresolved
- [ ] UNKNOWN provenance requires admission
- [ ] Scope labels missing/ambiguous

Escalate to governance lead/system owner.

---

## Outputs

- [ ] Boundary ruleset
- [ ] Exclusion/isolation log
- [ ] Handoff policy (allowed cross-boundary artifacts)
