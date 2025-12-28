---
title: "Masking Map"
status: stable
version: "1.0"
last_updated: "2025-01-01"
failure_class: interference
control: masking
---

# Masking Map

Use this gate to **restrict visibility** of context by role/phase/task.

```mermaid
flowchart TD
    C[Context Item] -->|visible| R1[Role/Phase A]
    C -. masked .-> R2[Role/Phase B]
    C -. masked .-> R3[Role/Phase C]
```

**Inputs**: context items with role/phase/task labels  
**Outputs**: visibility map + masked context per consumer

**Stop if** masking would hide mandatory constraints or if labels are missing.
