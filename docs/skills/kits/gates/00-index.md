---
title: "Gates — Index"
status: stable
version: "1.0"
last_updated: "2025-01-01"
---

# Gates — Index

Gates are **single-control, copy-paste artifacts** derived from operator skills.  
They enforce one control against one failure class.

```mermaid
flowchart TD
    Sel[Selection Gate] --> Deg[Degradation]
    Ord[Ordering Policy] --> Int[Interference]
    Mask[Masking Map] --> Pois[Poisoning]
    Val[Validation Rule] --> Drift
    Iso[Isolation Boundary] --> Blast[Blast Radius Containment]
```

Use the gate that matches the dominant failure mechanic; do not stack gates without operator review.
