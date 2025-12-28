---
title: "Roadmap"
status: "draft"
last_updated: "2025-01-01"
---

# ROADMAP

```mermaid
flowchart TD
    Core[Core Docs] --> Primitives[Primitives Complete]
    Primitives --> Failures[Failure Mechanics Hardened]
    Failures --> Controls[Controls + Scripts]
    Controls --> Examples[Executable Examples]
    Examples --> Skills[Operator/Agent Skills]
    Skills --> Gov[Governance + Tests]
```

_This roadmap reflects current working intent. Timelines are indicative, not contractual._

## Next Priorities

- Keep specs/tests in sync as scripts evolve.
- Expand example coverage beyond triage harnesses.
- Harden governance automation (acceptance/review tracking).

## Deferred

- Vendor-specific adapters (out of scope).
- UI/UX layers (intentionally excluded).
