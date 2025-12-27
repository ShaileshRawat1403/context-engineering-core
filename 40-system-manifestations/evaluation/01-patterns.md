---
title: "Evaluation — Patterns"
layer: "system-manifestations"
concept: "evaluation-patterns"
status: "stable"
version: "1.0"
last_updated: "2025-01-01"
depends_on:
  - "./00-index.md"
  - "../../10-primitives/scope/00-spec.md"
  - "../../10-primitives/signal-vs-noise/00-spec.md"
  - "../../30-control-mechanisms/masking/00-spec.md"
  - "../../30-control-mechanisms/validation/00-spec.md"
---

# Evaluation — Patterns

These patterns apply primitives and controls to evaluation so it remains a governance activity, not a source of interference or drift.

---

## Pattern: Rubric Isolation

- **Use when**: generation and evaluation share a system.
- **Controls**:
  - Masking: hide rubrics/metrics from generation context.
  - Isolation: separate evaluation harness/environment.
  - Scope: rubrics scoped to evaluation phase only.
- **Failure prevention**: prevents outputs optimizing for rubric instead of intent.

---

## Pattern: Freshness-Gated Benchmarks

- **Use when**: benchmarks risk becoming stale.
- **Controls**:
  - Validation: enforce benchmark freshness/expiration.
  - Selection: include only in-scope, current cases.
  - Provenance: track source/version of test sets.
- **Failure prevention**: avoids drift from outdated benchmarks.

---

## Pattern: Outcome Validation vs Proxy Metrics

- **Use when**: metrics can diverge from intent.
- **Controls**:
  - Validation: compare outputs to intended outcomes, not just proxies.
  - Escalation: trigger when metric success conflicts with observed outcomes.
  - Governance: approval required for metric changes.
- **Failure prevention**: stops proxy drift and hidden misalignment.

---

## Pattern: Red-Team / Adversarial Evaluation

- **Use when**: assessing robustness and poisoning risk.
- **Controls**:
  - Isolation: run adversarial tests in sandboxed environment.
  - Selection: keep adversarial inputs out of production caches.
  - Validation: quarantine artifacts produced during red-team runs.
- **Failure prevention**: prevents adversarial artifacts from contaminating production state.

---

## Pattern Selection Guidance

- Keep evaluation artifacts (rubrics, metrics, test cases) scoped and masked from generation.
- Treat benchmarks as expiring artifacts; revalidate regularly.
- Prefer outcome validation over proxy success; escalate on conflicts.
- Never reuse adversarial artifacts in production without explicit acceptance.

---

## Status

This document is **stable**. Patterns may expand but must preserve scope, masking, validation, and isolation of evaluation context.
