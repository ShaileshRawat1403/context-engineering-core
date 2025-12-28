---
title: "Long Session Stability Harness — README"
status: stable
version: "1.0"
last_updated: "2025-01-01"
---

# Long Session Stability Harness

Demonstrates session stabilization with compression, validation, and drift detection.

```mermaid
flowchart TD
    Hist[Long History] --> Prune[Prune/Compress]
    Prune --> Validate[Validate/Refresh]
    Validate --> Assemble[Assemble Next Turn Context]
    Assemble --> Tests[Regression Tests]
```

- PRD: scope and acceptance criteria  
- Architecture: harness flow and data paths  
- Source: `src/`  
- Tests: `tests/`
