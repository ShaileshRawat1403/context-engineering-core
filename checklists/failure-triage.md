---
title: "Failure Triage Checklist"
status: stable
version: "1.0"
last_updated: "2025-01-01"
---

# Failure Triage Checklist

```mermaid
flowchart TD
    Observe[Observe Failure Signals] --> Classify[Classify Failure Mechanic]
    Classify --> Contain[Contain/Isolate]
    Contain --> Investigate[Run Checks]
    Investigate --> Decide[Decide Controls + Escalation]
```

## Steps

- [ ] Collect failure signals and affected artifacts.
- [ ] Classify as degradation, drift, interference, or poisoning.
- [ ] Contain by masking/isolation before further action.
- [ ] Run relevant checks from the mapped mechanic.
- [ ] Decide remediation plan and owner.

## Escalate When

- Failure class cannot be determined.
- Containment requires authority change.
- Checks fail for safety/policy constraints.
