---
title: "Escalation — Process"
layer: "governance"
concept: "escalation-process"
status: "stable"
version: "1.0"
last_updated: "2025-01-01"
depends_on:
  - "./00-index.md"
---

# Escalation — Process

Escalation defines when execution must **stop** and control is handed to higher authority.

It prevents silent continuation when validation, isolation, or authority fails.

---

## Triggers (Non-Negotiable)

- Validation failure on reused/persistent artifacts
- Isolation breach or cross-domain leakage
- Authority conflict that cannot be resolved locally
- Critical checks fail (safety, policy, governance)
- Untrusted input would need to override protected logic

---

## Roles

- **Operator**: detects trigger, halts execution
- **Escalation owner**: role authorized to decide next steps
- **Observer/log**: audit trail recipient

Roles must be named per system; defaults are not allowed.

---

## Process Steps

1. Detect trigger; stop execution immediately.
2. Capture state and evidence (artifacts, logs, decisions).
3. Notify escalation owner with context and trigger reason.
4. Owner decides: remediate, roll back, or accept risk with documented approval.
5. Record decision and actions; resume only with explicit approval.

---

## Time and SLA

- Escalation windows must be defined (e.g., owner response within N hours).
- If SLA breaches, escalate further (e.g., governance board).

---

## Non-Bypassability

- Operators cannot ignore triggers to “keep things moving.”
- Agents cannot override escalation; authority is human.

---

## Status

This process is **stable**.  
Changes require governance approval and must not weaken stop conditions or authority.
