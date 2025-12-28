---
title: "Evaluation Readiness Checklist"
status: stable
version: "1.0"
last_updated: "2025-01-01"
---

# Evaluation Readiness Checklist

```mermaid
flowchart TD
    Rubric[Rubrics Scoped/Masked] --> Bench[Benchmarks Fresh?]
    Bench --> Data[Data/Fixtures Validated]
    Data --> Roles[Roles + Authority Assigned]
    Roles --> Go[Ready to Run Evaluation]
```

## Steps

- [ ] Rubrics isolated from generation context.
- [ ] Benchmarks/fixtures current and scoped to task.
- [ ] Provenance recorded for all test data.
- [ ] Evaluation environment isolated from production.
- [ ] Success criteria and escalation paths defined.

## Escalate When

- Rubrics leak into generation.
- Benchmarks are stale or untrusted.
- Authority to accept results is unclear.
