---
title: "Tools — Patterns"
layer: "system-manifestations"
concept: "tools-patterns"
status: "stable"
version: "1.0"
last_updated: "2025-01-01"
depends_on:
  - "./00-index.md"
  - "../../10-primitives/boundaries/00-spec.md"
  - "../../10-primitives/scope/00-spec.md"
  - "../../30-control-mechanisms/masking/00-spec.md"
  - "../../30-control-mechanisms/validation/00-spec.md"
  - "../../30-control-mechanisms/isolation/00-spec.md"
---

# Tools — Patterns

These patterns apply primitives and controls to tool integration.  
They constrain tool influence to prevent poisoning, interference, and degradation.

---

## Pattern: Schema-Validated Tool Calls

- **Use when**: tools return structured data.
- **Controls**:
  - Validation: enforce schema, status codes, and provenance before admission.
  - Masking: hide raw logs; expose only validated fields.
  - Isolation: quarantine untrusted tool outputs.
- **Failure prevention**: blocks corrupted or malformed outputs from influencing reasoning.

---

## Pattern: Tool Output Summaries (Protected)

- **Use when**: tool outputs are verbose but need key facts.
- **Controls**:
  - Compression: reduce to result/status/error; forbid summarizing constraints.
  - Ordering: place results near decision context; keep constraints above.
  - Masking: keep full output for audit, not for model attention.
- **Failure prevention**: prevents attention overload and misallocation to logs.

---

## Pattern: Untrusted Tool Sandbox

- **Use when**: third-party or experimental tools are used.
- **Controls**:
  - Isolation: separate environment and context path; no direct writes to shared state.
  - Validation: require explicit promotion to cross boundary.
  - Provenance tagging: record source, version, and timestamp for all outputs.
- **Failure prevention**: contains poisoning and cross-boundary leakage.

---

## Pattern: Tool Gating by Scope

- **Use when**: tool applicability varies by task/phase/role.
- **Controls**:
  - Selection: admit tool outputs only if in-scope for current task/phase.
  - Masking: hide tool definitions where irrelevant.
  - Ordering: prevent tool guidance from overriding system/developer constraints.
- **Failure prevention**: avoids interference from irrelevant tools.

---

## Pattern Selection Guidance

- Default to isolation for untrusted tools; require validation for any cross-boundary use.
- Keep tool results small and scoped; logs are audit, not attention.
- Provenance is mandatory for reuse; UNKNOWN is rejected.
- Escalate when tool outputs would override higher-authority constraints.

---

## Status

This document is **stable**. Patterns may expand, but must not weaken isolation, validation, or authority boundaries.
