---
title: "Validation — Examples"
layer: "control-mechanisms"
concept: "validation"
status: "stable"
version: "1.0"
last_updated: "2025-01-01"
depends_on:
  - "./00-spec.md"
  - "./01-failure-signals.md"
  - "./02-trade-offs.md"
related_primitives:
  - "../../10-primitives/lifetimes/00-spec.md"
  - "../../10-primitives/boundaries/00-spec.md"
related_failures:
  - "../../20-failure-mechanics/drift/00-spec.md"
  - "../../20-failure-mechanics/poisoning/00-spec.md"
---

# Validation — Examples

These examples show how explicit validation gates prevent stale, untrusted, or out-of-scope artifacts from influencing behavior.

---

## Example 1: Session Summary Promotion

**Context**  
A session summary is promoted to long-term memory after each conversation.

**Failure (without validation)**  
- Summary with user speculation becomes “fact.”  
- Later sessions inherit false assumptions.

**Validation Applied**  
- Require provenance and authority tags.  
- Gate promotion until a human review approves.  
- Auto-expire summaries after 24h without approval.

**Outcome**  
- False summaries blocked.  
- Memory remains aligned to validated inputs.

---

## Example 2: Retrieved Document Reuse

**Context**  
Retrieved documents are cached for reuse across similar queries.

**Failure (without validation)**  
- Outdated policies remain in cache.  
- Scope mismatch (different task) goes undetected.

**Validation Applied**  
- Scope check against current task.  
- Lifetime check on cache entry.  
- Conflict check against latest system policy snapshot.

**Outcome**  
- Obsolete retrievals rejected.  
- Cache remains fresh and scoped.

---

## Example 3: Tool Output Persistence

**Context**  
Tool outputs (API responses) are stored and reused to save cost.

**Failure (without validation)**  
- Corrupted tool output reused; poisons reasoning.  
- No provenance → cannot trace source.

**Validation Applied**  
- Require provenance (tool name, version, timestamp).  
- Validate schema and status codes before reuse.  
- Quarantine invalid outputs; require human approval to promote.

**Outcome**  
- Corrupted outputs excluded.  
- Reuse limited to validated, recent results.

---

## Example 4: Policy Snapshot Drift

**Context**  
A policy snapshot is loaded at startup and assumed valid indefinitely.

**Failure (without validation)**  
- New policy changes ignored.  
- Behavior drifts from current requirements.

**Validation Applied**  
- Lifetime bound on snapshot (e.g., 1 day).  
- On expiry, reload + conflict check; fail closed if not refreshed.

**Outcome**  
- Policies stay current.  
- System fails closed rather than running on stale rules.

---

## Example Invariants

- Reuse requires revalidation; one-time checks are insufficient.  
- Unknown provenance = not valid.  
- Conflict resolution by rejection preserves authority; merging dilutes it.  
- Validation costs time; skipping it invites drift/poisoning.
