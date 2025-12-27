---
title: Session Stabilization — Operator Checklist
archetype: checklist
status: stable
owner: context-engineering-core
maintainer: context-engineering-core
version: 1.0
tags:
  - skills
  - operator
  - session-stabilization
  - checklist
last_reviewed: 2025-12-26
---

# Session Stabilization — Operator Checklist

Condensed execution aid. Use only when the full SKILL is understood.

---

## Preconditions

- [ ] Context assembly exists (history, summaries, retrievals, tool outputs)
- [ ] Attention/token budget declared
- [ ] Authority and scope models defined
- [ ] Validation rules for summaries/memory in place
- [ ] Isolation requirements known

If any unchecked, stop and resolve.

---

## Execution Checklist

### 1) Assess budget and redundancy
- [ ] Compute token estimates per artifact
- [ ] Identify duplicates/near-duplicates

### 2) Refresh summaries
- [ ] Regenerate summaries using deltas
- [ ] Validate summaries (provenance, scope, authority)
- [ ] Expire stale summaries per lifetime rules

### 3) Prune history
- [ ] Remove/compress redundant or low-signal turns
- [ ] Keep last N turns verbatim; compress older into deltas
- [ ] Mask tool logs; keep result/status/error only

### 4) Reset scope
- [ ] Clear task-specific instructions on task/phase change
- [ ] Ensure role prompts do not persist across phases

### 5) Re-order context
- [ ] Constraints first (system/developer)
- [ ] Current task/phase instructions next
- [ ] Latest user/task content, then validated summaries/references

### 6) Finalize
- [ ] Context within budget
- [ ] Exclusion and summary logs recorded

---

## Validation Checks (must pass)

- [ ] Budget utilization < target
- [ ] No stale summaries remain
- [ ] All summaries validated or rejected
- [ ] Authority ordering preserved
- [ ] Scope reset applied

If any fail, execution unsuccessful.

---

## Stop/Escalate

Stop and escalate if:
- [ ] Constraints risk exclusion
- [ ] Scope reset ambiguous
- [ ] Summary validation fails
- [ ] Isolation requirements are breached

Escalate to system owner/tech lead.

---

## Outputs to record

- [ ] Stabilized context list
- [ ] Exclusion log (what/why)
- [ ] Summary refresh log (status, timestamps)
- [ ] Budget utilization
