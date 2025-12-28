---
title: "Governance Readiness Checklist"
status: stable
version: "1.0"
last_updated: "2025-01-01"
---

# Governance Readiness Checklist

```mermaid
flowchart TD
    Roles[Roles/Authority Defined] --> Evidence[Evidence + Checks Ready]
    Evidence --> Escalation[Escalation Paths Set]
    Escalation --> Acceptance[Acceptance/Review Scheduled]
```

## Steps

- [ ] Authority, ownership, and escalation roles named.
- [ ] Controls mapped to owners; checks documented and runnable.
- [ ] Review and acceptance criteria defined with expiry dates.
- [ ] Audit logging enabled for key actions.
- [ ] Stop conditions understood by operators and agents.

## Escalate When

- Ownership ambiguous.
- Checks cannot be run.
- Stop conditions are missing or unenforced.
