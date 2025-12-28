---
title: "Kits and Gates"
status: stable
version: "1.0"
last_updated: "2025-01-01"
---

# Kits and Gates

Kits provide the smallest reusable control artifacts. They are intentionally narrow and copy-paste safe.

```mermaid
flowchart TD
    Gate[Gate Template] --> Control[Specific Control]
    Control --> Failure[Failure Class]
    Gate --> Paste[Copy/Paste into System Prompt or Orchestrator]
```

Use gates when you need a **single control** without the surrounding skill.
