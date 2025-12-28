---
title: "Review — Index"
layer: "governance"
concept: "review"
status: "stable"
version: "1.0"
last_updated: "2025-01-01"
depends_on:
  - "../00-index.md"
  - "../../30-control-mechanisms/validation/00-spec.md"
---

# Review — Index

Review is the **governed inspection of specs, controls, and outputs** before they are accepted.

This section will define:
- what must be reviewed (intent, controls, evidence)
- who can approve or reject
- how review outcomes are recorded and enforced

```mermaid
flowchart TD
    Sub[Submission] --> Rev[Reviewer Analysis]
    Rev --> Out[Outcome: Approve/Reject/Revise]
    Out --> Log[Recorded with Rationale]
    Log --> Enf[Enforced in Acceptance]
```

Review documents make explicit the authority and criteria for acceptance. They do not add new controls.
