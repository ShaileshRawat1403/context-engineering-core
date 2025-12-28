---
title: "Checklists — Index"
status: "stable"
version: "1.0"
last_updated: "2025-01-01"
---

# Checklists — Index

Checklists are **execution aids** derived from specs and skills. They are not substitutes for the full documents; they enforce minimal steps, checks, and stop conditions.

```mermaid
flowchart TD
    Spec[Spec/Skill] --> Checklist[Checklist]
    Checklist --> Run[Execute Steps]
    Run --> Checks[Validate Outcomes]
    Checks --> Esc[Stop/Escalate on failure]
```

Use the checklist that corresponds to the spec/skill you are executing. If a checklist conflicts with a spec, the spec prevails.
