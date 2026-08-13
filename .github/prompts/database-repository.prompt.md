---
mode: agent
description: "Design and implement repository/data-access patterns"
tools: ["codebase", "search", "editFiles", "terminal"]
---

# Database / repository development

Design and implement the persistence and repository layer for `{{USE_CASE}}` using the repository's existing data conventions.

## Inputs

- Requirements: `{{REQUIREMENTS}}`
- Constraints: `{{CONSTRAINTS}}`
- Existing persistence or repository patterns: inspect before coding

## Goal

Provide the cleanest possible data-access contract without overengineering the solution.

## Responsibilities

- Define the required entities and their fields.
- Decide whether a database, in-memory store, file-based store, or abstraction layer is appropriate.
- Keep repository logic isolated from API and UI logic.
- Define retrieval, creation, update, deletion, and search boundaries.

## Checklist

- Identify entities and relationships.
- Decide which data must persist and which can be transient.
- Determine repository methods needed for the solution.
- Define validation constraints at the data layer where appropriate.
- Document any mock or demo data clearly.

## Output format

```text
Persistence summary
- Entities:
- Relationships:
- Storage method:
- Repository methods:

Data rules
- Required fields:
- Validation constraints:
- Status or lifecycle states:

Implementation notes
- Files or modules to update:
- Mock data handling:
```

## Guardrails

- Reuse existing persistence patterns when they already exist.
- Keep mock data explicitly labeled as non-production data.
- Do not bypass service-layer boundaries unless the repository pattern clearly requires it.
- Keep the design domain-independent and reusable.
