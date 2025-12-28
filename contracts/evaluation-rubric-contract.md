---
title: "Evaluation Rubric Contract"
status: stable
version: "1.0"
last_updated: "2025-01-01"
---

# Evaluation Rubric Contract

Defines the structure and governance for rubrics used in evaluation.

```mermaid
flowchart TD
    Rubric[Rubric] --> Scope[Scope/Phase]
    Rubric --> Metrics[Metrics + Weights]
    Rubric --> Fresh[Freshness/Expiry]
    Rubric --> Mask[Mask from Generation]
```

## Required Fields

- `name`, `version`, `owner`
- Scope (tasks, roles, phases where rubric applies)
- Criteria with scoring guidance and weights
- Expiration/review date and provenance for test data

## Governance Rules

- Rubrics must be masked from generation contexts.
- Changes require review/acceptance and version bump.
- Expired rubrics must be refreshed before reuse.
- Conflicts between rubric success and outcomes trigger escalation.
