---
mode: agent
description: "Create concise, repository-aligned documentation"
tools: ["codebase", "search", "editFiles"]
---

# Documentation

Create concise, accurate documentation for `{{USE_CASE}}` that matches the repository's current documentation style and level of detail.

## Inputs

- Requirements: `{{REQUIREMENTS}}`
- Design summary: `{{DESIGN_SUMMARY}}`
- Constraints: `{{CONSTRAINTS}}`

## Goal

Document what exists, how it works, and how to maintain or extend it without inventing unsupported details.

## Documentation checklist

- Summarize the solution purpose and scope.
- Describe the main components, responsibilities, and boundaries.
- Explain how to run or validate the work in this repo.
- Document assumptions, constraints, and known limitations.
- Keep docs aligned with the actual implementation.

## Output format

```text
Overview
- Use case:
- Objective:
- Scope:

Architecture summary
- Main components:
- Key flows:

Usage / validation
- How to run:
- How to test:

Notes
- Assumptions:
- Risks:
```

## Guardrails

- Do not document speculative or invented functionality.
- Keep documentation short, practical, and in line with repository conventions.
- Do not duplicate large sections of code in prose; explain behavior and boundaries instead.
