---
title: Context Triage — Agent Execution Contract
archetype: agent-skill
status: stable
owner: context-engineering-core
maintainer: context-engineering-core
version: 1.0
tags:
  - skills
  - agent
  - context-triage
last_reviewed: 2025-12-26
---

# Context Triage — Agent Execution Contract

Canonical definition: `skills/operator/context-triage/SKILL.md`  
If instructions conflict, the operator skill prevails.

---

## Scope and Authority

- **Authority:** human-governed; agent has no decision rights beyond allowed actions.
- **Override rights:** none.
- **Autonomy:** constrained; halt on ambiguity or conflict.

---

## Preconditions (must be true)

- Operator skill is approved and in force.
- Authority model and scope for the task are defined.
- Context budget is declared.
- Inputs provided match the required format (see below).
- No isolation boundary is being crossed.

If any precondition is unmet, **stop and escalate**.

---

## Allowed Inputs

- `candidate_context[]` (messages, documents, tool outputs) with metadata if available
- `context_budget` (token budget)
- `authority_model` (precedence rules)
- `scope_definition` (task scope)

The agent must not fabricate or fetch additional inputs.

---

## Allowed Actions

- Normalize artifacts (attach source/authority/scope if provided).
- Apply scope filtering (exclude out-of-scope items).
- Apply authority ordering (system > developer > user > tool > other).
- Detect redundancy (exact/near-duplicate) and mark lower-priority duplicates.
- Estimate token contribution per artifact (heuristic).
- Admit artifacts in priority order until budget is reached.
- Produce ordered final context and exclusion log.

---

## Forbidden Actions

- Change authority or scope definitions.
- Admit out-of-scope or unknown-provenance artifacts.
- Override or ignore context budget.
- Introduce new artifacts or retrievals.
- Persist or cache results.

---

## Execution Steps

1. Verify preconditions.
2. Normalize inputs; reject malformed bundles.
3. Exclude out-of-scope artifacts; do not summarize them.
4. Sort by authority + kind + explicit priority.
5. Remove/mark duplicates; keep highest authority/relevance.
6. Admit artifacts in order until budget reached.
7. Emit outputs (final context, exclusion log, budget usage).
8. Halt on any forbidden action requirement; escalate.

---

## Required Checks

- Context budget not exceeded.
- No system/developer constraints excluded.
- All admitted artifacts are in scope.
- Authority ordering preserved.
- Exclusion reasons recorded.

If any check fails, halt and report failure.

---

## Required Reporting

- Final ordered context (IDs/titles, decisions).
- Excluded artifacts with reasons.
- Estimated budget utilization.
- Any anomalies (missing metadata, duplicate handling).

---

## Stop and Escalation Conditions

Stop immediately and escalate if:
- Preconditions are not met.
- Scope or authority is ambiguous.
- Budget cannot be met without excluding high-authority constraints.
- Unknown/forbidden inputs appear.

Escalation target: human operator.

---

## Non-Goals

- The agent does not decide task scope or authority.
- The agent does not alter controls or policies.
- The agent does not persist or cache results.
