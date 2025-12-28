---
title: "Ordering Policy"
status: stable
version: "1.0"
last_updated: "2025-01-01"
failure_class: interference
control: ordering
---

# Ordering Policy

Use this gate to **enforce precedence** among admitted context so constraints are not displaced.

```mermaid
flowchart TD
    Con[Constraints/System] --> Pos1[Position 1]
    Pol[Policies/Rules] --> Pos2[Position 2]
    User[User/Tool Inputs] --> Pos3[Position 3+]
    Pos1 --> Asm[Context Assembly]
    Pos2 --> Asm
    Pos3 --> Asm
```

**Inputs**: admitted_context[], authority model  
**Outputs**: ordered_context[]

**Stop if** authority cannot be enforced or reordering changes outcomes unexpectedly.
