---
title: "Case Study — Documentation Assistant"
status: draft
version: "1.0"
last_updated: "2025-01-01"
tags:
  - selection
  - ordering
  - validation
  - isolation
---

# Case Study — Documentation Assistant

## Context
- Internal doc assistant fed product specs, release notes, and Jira tickets.
- Long-running sessions; mix of authoritative specs and unvetted chatter.
- Hard requirement: never publish user-generated conjecture as product truth.

## Failure Signals (observed)
- Hallucinated features cited from Jira comments.
- Outdated constraints displaced by verbose retrieval snippets.
- Cross-issue leakage: one ticket’s workaround appeared in unrelated docs.

## Root Causes
- Retrieval admitted high-recall, low-authority content.
- Ordering allowed long snippets to bury short constraints.
- No validation on source authority before publication.

## Intervention (controls applied)
- **Selection:** gated retrieval to specs + release notes; Jira limited to linked tickets only.
- **Ordering:** system constraints first, then current release notes, then scoped Jira; comments demoted to advisory.
- **Validation:** source authority check before inclusion; untrusted snippets flagged for review.
- **Isolation:** per-ticket scope boundary; context cleared between tickets.

## Outcome
- Hallucinations eliminated in sampled outputs.
- Constraint adherence improved; no displacement in spot checks.
- Time-to-publish increased ~5%, offset by reduced rework.

## How to Reproduce/Map to Repo
- Mirrors the Minimal RAG Context Gate example: run `pytest examples/minimal-rag-context-gate/tests -q`.
- Adapt the gating policy in `examples/minimal-rag-context-gate/src/gates.py` to replicate the authority filters used here.
