---
title: Context Triage — Operator Checklist
archetype: checklist
status: stable
owner: context-engineering-core
maintainer: context-engineering-core
version: 1.0
tags:
  - skills
  - operator
  - context-triage
  - checklist
last_reviewed: 2025-12-26
---

# Context Triage — Operator Checklist

This checklist is a **condensed execution aid** for experienced operators.  
It does not replace the canonical procedure in `SKILL.md`.

Use this only when the Context Triage skill is already understood.

---

## Preconditions (verify before starting)

- [ ] A candidate context set exists (messages, retrievals, tool outputs)
- [ ] Fixed context budget is defined
- [ ] Authority hierarchy is agreed (system > developer > user > tool)
- [ ] Scope definition for the task is explicit
- [ ] No unresolved isolation or boundary violations

If any item is unchecked, **do not proceed**.

---

## Execution Checklist

### 1. Normalize inputs
- [ ] Convert all artifacts into comparable text units
- [ ] Attach metadata (source, authority, timestamp, scope)

---

### 2. Scope filtering
- [ ] Exclude all out-of-scope artifacts
- [ ] Do not summarize out-of-scope content
- [ ] Discard excluded artifacts containing sensitive data

---

### 3. Authority ordering
- [ ] Sort remaining artifacts by authority
- [ ] Ensure system and developer instructions are first
- [ ] Verify no lower-authority artifact can displace higher authority

---

### 4. Redundancy elimination
- [ ] Identify duplicate or near-duplicate artifacts
- [ ] Retain only the highest-authority or most recent version
- [ ] Remove drafts or superseded versions

---

### 5. Budget enforcement
- [ ] Estimate token contribution per artifact
- [ ] Admit artifacts in priority order
- [ ] Stop admission when budget is reached
- [ ] Do not partially admit artifacts unless explicitly allowed

---

### 6. Finalize context
- [ ] Produce ordered final context set
- [ ] Produce exclusion log with explicit reasons

---

## Validation Checks (must pass)

- [ ] Context budget utilization < defined limit
- [ ] No system or developer instruction excluded
- [ ] All admitted artifacts are in scope
- [ ] Ordering reflects authority hierarchy
- [ ] Exclusion reasons are documented

If any check fails, execution is unsuccessful.

---

## Stop and Escalation Conditions

Stop immediately and escalate if:

- [ ] System or developer instruction is excluded
- [ ] Scope boundaries are ambiguous
- [ ] Authority conflicts cannot be resolved
- [ ] Budget forces exclusion of required constraints

Escalation target: **system owner or tech lead**

---

## Output Artifacts (record)

- [ ] Final ordered context list
- [ ] Exclusion log with reasons
- [ ] Budget utilization estimate

---

## Reminder

- Do not trade authority for coverage
- Do not “keep just in case” artifacts
- Context admission errors are silent but severe

This checklist supports **controlled execution**, not exploration.
