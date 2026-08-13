---
mode: agent
description: "Design and implement generic backend/API components"
tools: ["codebase", "search", "editFiles", "terminal"]
---

# Backend / API development

Design and implement the backend or API workflow for `{{USE_CASE}}` in a way that matches the repository's existing conventions.

## Inputs

- Requirements: `{{REQUIREMENTS}}`
- Constraints: `{{CONSTRAINTS}}`
- Existing API or service patterns: inspect before coding

## Goal

Create the smallest backend contract that satisfies the use case while preserving separation of concerns and repository conventions.

## Responsibilities

- Define routes, endpoints, or handlers required by the solution.
- Keep request/response contracts explicit and consistent.
- Implement validation and error handling.
- Separate business logic from transport concerns.
- Reuse services or domain logic when they already exist.

## Checklist

- Determine what operations are needed: create, read, update, delete, list, submit, approve, validate, search, or status.
- Define the input payload and output payload for each operation.
- Describe required and optional fields.
- Identify validation and error states.
- Decide whether the repository already provides the correct API style.
- Keep auth, rate limits, and operational concerns only if the repo already uses them.

## Output format

```text
API summary
- Endpoints or handlers:
- Request contracts:
- Response contracts:
- Validation rules:

Error handling
- Expected errors:
- Status codes or failure modes:

Implementation notes
- Files or modules to edit:
- Service/repository boundaries:
```

## Guardrails

- Do not put persistence logic directly into route handlers unless the repo's pattern already does so.
- Do not couple the API contract to a specific UI implementation.
- Do not invent downstream systems or external providers unless they are explicitly specified.
- Keep the implementation generic and reusable.
