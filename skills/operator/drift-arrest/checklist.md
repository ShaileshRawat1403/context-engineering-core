---
title: Drift Arrest — Operator Checklist
archetype: checklist
status: stable
owner: context-engineering-core
maintainer: context-engineering-core
version: 1.0
tags:
  - skills
  - operator
  - drift-arrest
  - checklist
last_reviewed: 2025-12-26
---

# Drift Arrest — Operator Checklist

Condensed aid; use only when SKILL is understood.

---

## Preconditions

- [ ] Current intent is explicit, versioned, and owned
- [ ] Proxies/metrics listed and owned
- [ ] Validation rules for persistent artifacts in place
- [ ] External reference/ground truth accessible

If any unchecked, stop.

---

## Execution Checklist

### 1) Confirm intent and scope
- [ ] Retrieve intent; verify ownership/version
- [ ] Identify domains where intent may have shifted

### 2) Audit proxies/benchmarks
- [ ] List proxies/metrics
- [ ] Validate they still represent intent
- [ ] Mark stale/invalid proxies

### 3) Validate persistent artifacts
- [ ] Run validation on memory/summaries/caches
- [ ] Quarantine/Reject artifacts with stale lifetime, missing provenance, or scope mismatch

### 4) Re-ground
- [ ] Bring in current external data/policy
- [ ] Compare outputs vs outcomes; record divergence

### 5) Update constraints/state
- [ ] Restate intent if legitimately changed (approved)
- [ ] Refresh proxies/benchmarks; invalidate obsolete ones
- [ ] Roll back/replace poisoned or stale artifacts

### 6) Re-run checks
- [ ] Drift signals cleared
- [ ] Authority/scope preserved after updates

---

## Validation Checks (must pass)

- [ ] Intent explicit and current
- [ ] Proxies/benchmarks validated
- [ ] Stale/poisoned artifacts quarantined or removed
- [ ] Outcome–intent alignment restored

---

## Stop/Escalate

Stop and escalate if:
- [ ] Intent ambiguous or disputed
- [ ] External reference unavailable
- [ ] Authority conflicts on proxy/intent changes
- [ ] Validation failures cannot be resolved

Escalate to governance lead/system owner.

---

## Outputs

- [ ] Drift audit log (findings/actions)
- [ ] Updated intent/proxies (versioned)
- [ ] Validation/quarantine log
