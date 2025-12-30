---
title: "Case Study — Incident Response Agent"
status: draft
version: "1.0"
last_updated: "2025-01-01"
tags:
  - masking
  - ordering
  - compression
  - human-review
---

# Case Study — Incident Response Agent

## Context
- Chat-based agent assisting incident commanders during outages.
- Inputs: noisy logs, on-call chat, runbooks, mitigation steps.
- Requirement: preserve authority of runbooks and on-call lead; hide sensitive PII.

## Failure Signals (observed)
- Agent elevated noisy Slack chatter over runbook steps.
- PII from logs surfaced in summaries.
- Mitigation orders arrived out of sequence, causing duplicated actions.

## Root Causes
- No masking on raw tool logs.
- Ordering flattened; chat noise interleaved with runbook steps.
- Compression absent; context ballooned, displacing constraints.

## Intervention (controls applied)
- **Masking:** log ingestion reduced to `{timestamp, severity, message}`; PII stripped.
- **Ordering:** runbook + lead directives first; telemetry summaries after; chat advisories last.
- **Compression:** rolling summaries for chat noise; last N directives kept verbatim.
- **Human Review:** escalation gate when mitigation steps conflict or exceed budget.

## Outcome
- PII no longer surfaced in summaries (spot audits).
- Mitigation execution matched runbook order; duplicated actions dropped.
- Attention budget stayed under target; no constraint displacement during long incidents.

## How to Reproduce/Map to Repo
- Mirrors the Long Session Stability Harness: run `pytest examples/long-session-stability-harness/tests -q`.
- Experiment by adding noisy artifacts to `examples/long-session-stability-harness/fixtures/session.json` and rerun `python3 examples/long-session-stability-harness/src/runner.py` to see the masking/ordering effects.
