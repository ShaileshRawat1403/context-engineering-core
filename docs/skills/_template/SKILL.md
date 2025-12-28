---
title: "<Skill Name>"
archetype: skill-template
status: stable
owner: context-engineering-core
maintainer: context-engineering-core
version: "1.0"
tags:
  - skills
  - template
last_reviewed: "2025-12-26"
---

# <Skill Name>

This template is a starting point for new skills. Replace placeholders with concrete, governed content.

```mermaid
flowchart TD
    Why[Define Intent + Failure Class] --> Inputs[Specify Inputs/Preconditions]
    Inputs --> Steps[Document Procedure]
    Steps --> Checks[Executable Checks]
    Checks --> Outputs[Outputs + Reporting]
    Outputs --> Esc[Stop/Escalate Rules]
```

## Overview
- What intervention does the skill perform?
- Which failure mechanics does it address?
- Where in the pipeline does it run?

## Preconditions
- Authority, scope, and isolation boundaries defined
- Required inputs available and trusted
- Validation and logging enabled

## Procedure
1. Step-by-step actions with decision points.
2. Controls applied (selection, ordering, masking, validation, isolation).
3. Expected intermediate artifacts.

## Outputs
- Required artifacts and their formats
- Logs and evidence to record

## Checks
- List checks that must pass; include pass/fail criteria.

## Stop and Escalation
- Conditions that require halt
- Escalation target and required evidence

> Replace all placeholder text when instantiating this template.
