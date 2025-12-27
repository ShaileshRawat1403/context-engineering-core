---
title: "Minimal RAG Context Gate — Fixtures"
status: "stable"
last_updated: "2025-01-01"
---

# Minimal RAG Context Gate — Fixtures

Use `bundle.json` to exercise the Context Triage scripts.

## Contents

- `bundle.json` — candidate context with system/task constraints, 3 retrieved docs, 1 user question.
- `EXPECTED.md` — placeholder for expected outputs; update after running scripts locally.

## How to run (demo)

From repo root:

```bash
python3 skills/operator/context-triage/scripts/context_budget_report.py --input examples/minimal-rag-context-gate/fixtures/bundle.json --budget 500

python3 skills/operator/context-triage/scripts/duplicate_scan_demo.py --input examples/minimal-rag-context-gate/fixtures/bundle.json --near-threshold 0.8 --shingle-k 3

python3 skills/operator/context-triage/scripts/reorder_by_priority.py --input examples/minimal-rag-context-gate/fixtures/bundle.json
```

## Expected highlights (heuristic)

- **Budget report**: All artifacts fit; retrieval dominates token usage; system/task constraints rank highest.
- **Duplicate scan**: `doc1` and `doc2` may surface as near-duplicates depending on shingle settings; `doc3` should not match.
- **Reorder**: Ordering should be `sys` > `task` > `user` > `doc1` > `doc2` > `doc3` based on authority/kind/priority.

These outputs are heuristic (simple scoring, not true tokenization). Use them to validate wiring, not correctness.

Update `EXPECTED.md` with actual outputs from your environment after running the scripts.
