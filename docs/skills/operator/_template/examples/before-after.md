---
title: "<Skill Name> — Examples"
archetype: examples
status: stable
owner: context-engineering-core
maintainer: context-engineering-core
version: "1.0"
tags:
  - skills
  - operator
  - examples
last_reviewed: "2025-12-26"
---

# <Skill Name> — Before / After Examples

Use these slots to document concrete, operator-ready examples that prove the skill is executable.

```mermaid
flowchart LR
    B[Before State] --> I[Intervention Steps]
    I --> A[After State]
    A --> Checks[Checks Passed]
```

## ✅ Acceptable Execution

- **Before**: describe the initial context, inputs, and constraints.
- **Intervention**: list the steps you applied from `SKILL.md`.
- **After**: show the resulting state or output.
- **Checks**: record which checks passed with evidence.

## ❌ Incorrect Execution

- **Before**: describe the initial context.
- **Error**: what was done incorrectly (skipped check, wrong scope, etc.).
- **Outcome**: failure signal observed.
- **Correction**: how to avoid this in the future.
