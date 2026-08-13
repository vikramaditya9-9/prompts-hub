---
mode: agent
description: "Design a minimal, repository-aware software architecture"
tools: ["codebase", "search", "editFiles"]
---

# Architecture and design

Design the smallest viable architecture that fits the repository and the requirements for `{{USE_CASE}}`.

## Inputs

- Requirements: `{{REQUIREMENTS}}`
- Constraints: `{{CONSTRAINTS}}`
- Existing repo conventions: inspect before deciding

## Goal

Produce a design that preserves repository structure, preserves separation of concerns, and remains reusable across similar use cases.

## Design checklist

- Determine whether the solution requires a UI layer, API layer, domain logic, persistence, or all of the above.
- Identify the logical layers and their responsibilities.
- Keep boundary rules explicit:
  - UI handles presentation only
  - API handles contract and validation
  - services handle business logic
  - repositories handle persistence access
- Decide whether the design should reuse existing patterns or create a minimal new structure.
- Identify configuration, error handling, and operational concerns.

## Output format

```text
Architecture summary
- Primary components:
- Layer boundaries:
- Repository patterns:
- External integrations:

Design decisions
- Why this shape fits the repo:
- Risks or tradeoffs:

Implementation plan
- Files or modules to create/update:
- Sequence of delivery:
```

## Guardrails

- Do not force a framework that the repository does not already use.
- Do not put business rules in UI code.
- Do not bypass validation or persistence boundaries without a clear reason.
- Keep the design domain-agnostic and easy to adapt.
