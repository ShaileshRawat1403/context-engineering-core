---
title: "Boundary Hardening — Examples"
archetype: examples
status: stable
owner: context-engineering-core
maintainer: context-engineering-core
version: "1.0"
tags:
  - skills
  - operator
  - boundaries
  - examples
last_reviewed: "2025-12-26"
---

# Boundary Hardening — Before / After

```mermaid
flowchart LR
    B[Leaky Boundaries] --> H[Hardening Actions]
    H --> A[Isolated, Scoped Context]
    A --> Checks[Leakage Tests Pass]
```

## ✅ Acceptable Execution

- **Before:** user instructions occasionally override policy; retrieved docs bleed into execution role.
- **Intervention:** mapped authority and scope, added role-based masking, isolated retrieval to advisory lane, retested leakage.
- **After:** policy persists across runs; retrieval cannot override constraints; leakage tests pass.

## ❌ Incorrect Execution

- **Before:** mixed system/user/tool content in shared buffer.
- **Error:** added more instructions but left shared buffer intact.
- **Outcome:** interference persisted; constraints still overwritten.
- **Correction:** apply isolation/masking instead of additive prompts; rerun leakage checks.
