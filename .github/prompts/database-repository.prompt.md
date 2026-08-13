---
mode: agent
description: "Implement repository and persistence behavior in the repo's current style"
tools: ["codebase", "search", "editFiles", "terminal"]
---

# Purpose

Implement the repository, persistence, and data-access behavior for `{{USE_CASE}}` using the repository's existing data conventions.

# Inputs

- `{{REQUIREMENTS}}`
- `{{DATA_MODEL}}`
- `{{ARCHITECTURE_CONTEXT}}`
- `{{CONSTRAINTS}}`

# Responsibilities

- Inspect the repo's existing persistence approach.
- Define entities, fields, and relationships needed by the use case.
- Implement repository or data-access behavior consistent with the project.
- Handle CRUD or equivalent lifecycle behavior.
- Support validation, persistence testing, and seed or mock data where appropriate.
- Keep storage concerns separate from UI, controller, and service logic.

# Execution Instructions

1. Inspect the repository to identify the current persistence approach and repository conventions.
2. Identify the entities and relationship rules required by the use case.
3. Determine whether data should be persisted in an existing datastore, in-memory structure, file-based store, or repo-specific abstraction.
4. Define repository responsibilities and operations needed by the application.
5. Add or update data validation constraints and persistence-level safeguards.
6. Decide whether migrations or schema definitions are needed and align with the repo's patterns.
7. Use mock or seed data only when the repo already uses that pattern and clearly label it as non-production data.
8. Validate the repository behavior with repository-compatible tests.

# Output / Handoff

Return a persistence summary containing:

- entity model
- relationships
- repository methods and responsibilities
- storage decisions
- validation and CRUD behaviors
- mock or seed data strategy
- testing notes

Pass this data contract to the backend, testing, and documentation stages.

# Rules and Constraints

- Do not assume SQL, NoSQL, PostgreSQL, MySQL, MongoDB, or any other database technology.
- Reuse the repository's existing persistence approach before introducing a new storage pattern.
- Keep mock data clearly labeled and separate from production data.
- Do not place repository logic directly into UI or request-handling code.
- Keep the data model general and reusable rather than domain-specific.
- Do not invent invalid relationship schemas or unsupported persistence behavior.
