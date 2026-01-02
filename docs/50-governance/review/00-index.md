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

---

## Execution Path (quick)

- **Inputs**: change scope; authority model; checklists/controls touched; evidence to review; reviewers/approvers
- **Steps**: identify impacted controls; collect evidence; run review checklist; log findings; require approval before acceptance
- **Checks**: reviewer assigned; evidence complete; blockers documented; approval recorded
- **Stop/escate**: scope unclear; missing evidence; reviewer conflict of interest

---
