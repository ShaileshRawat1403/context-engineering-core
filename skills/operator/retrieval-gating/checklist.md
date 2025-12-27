---
title: Retrieval Gating — Operator Checklist
archetype: checklist
status: stable
owner: context-engineering-core
maintainer: context-engineering-core
version: 1.0
tags:
  - skills
  - operator
  - retrieval
  - gating
  - checklist
last_reviewed: 2025-12-26
---

# Retrieval Gating — Operator Checklist

Condensed aid; use only when SKILL is understood.

---

## Preconditions

- [ ] Source allowlist/denylist defined
- [ ] Authority model for sources declared
- [ ] Relevance criteria for task/phase/role defined
- [ ] Retrieval budget declared (K or tokens)
- [ ] Validation rules for retrieved artifacts in place

If any unchecked, stop.

---

## Execution Checklist

### 1) Normalize and tag
- [ ] Each candidate has source, authority, timestamp (if available)
- [ ] UNKNOWN sources tagged as low authority

### 2) Apply source policy
- [ ] Deny/unknown sources excluded or quarantined
- [ ] Trust tiering applied per authority model

### 3) Relevance/scope gating
- [ ] Apply relevance thresholds per task/phase
- [ ] Out-of-scope content excluded (no force-fit)

### 4) Deduplicate/compress
- [ ] Near-duplicates removed; keep best (authority/score)
- [ ] Long items compressed as allowed; provenance retained

### 5) Enforce budget
- [ ] Admit in authority+relevance order until budget reached
- [ ] No partial admissions unless explicitly allowed

### 6) Validate before admission
- [ ] Provenance/authority/scope/lifetime checked
- [ ] UNKNOWN provenance rejected or quarantined

### 7) Finalize
- [ ] Ordered, budget-compliant retrieval set produced
- [ ] Exclusion log recorded (reasons)
- [ ] Provenance report recorded

---

## Validation Checks (must pass)

- [ ] Budget respected
- [ ] No denied/unknown sources admitted
- [ ] Out-of-scope items excluded
- [ ] Provenance present for all admitted items
- [ ] Authority ordering preserved

---

## Stop/Escalate

Stop and escalate if:
- [ ] Unknown/denied source is required
- [ ] Scope/relevance ambiguous
- [ ] Validation fails for required items
- [ ] Authority conflicts arise

Escalate to system owner/governance lead.

---

## Outputs

- [ ] Admitted retrieval list (ordered)
- [ ] Exclusion log with reasons
- [ ] Provenance report
