---
mode: agent
description: "Design a repository-aware solution architecture"
tools: ["codebase", "search", "editFiles"]
---

# Purpose

Design the smallest viable solution architecture for `{{USE_CASE}}` using the repository's current stack, project structure, and conventions.

# Inputs

- `{{REQUIREMENTS}}`
- `{{CONSTRAINTS}}`
- `{{ARCHITECTURE_CONTEXT}}`

# Responsibilities

- Inspect the current repository and detect existing architecture patterns.
- Identify required layers such as UI, API/backend, service logic, repository/data access, configuration, and tests.
- Reuse existing conventions before inventing new ones.
- Define clear responsibilities and boundaries between components.
- Document architecture decisions, tradeoffs, and constraints.
- Keep the design generic and adaptable across multiple use cases.

# Execution Instructions

1. Inspect the repository structure, entry point, package manager, frameworks, and patterns.
2. Determine what layers are already present and how they are organized.
3. Identify the minimal set of components needed to satisfy the requirements.
4. Define the architecture boundaries between:
   - UI / presentation
   - API / request handling
   - service / business logic
   - repository / data access
   - persistence / storage
   - configuration / environment
5. Reuse existing project conventions instead of adding a new framework or stack.
6. Document tradeoffs and reasons for the chosen structure.
7. Identify gaps, missing abstractions, and any assumptions that need follow-up.

# Output / Handoff

Return an architecture summary containing:

- current repo context
- chosen structural pattern
- required layers and responsibilities
- data/API/UI boundaries
- key files or modules affected
- architecture decisions and tradeoffs
- unresolved assumptions or risks

Pass this architecture context to the backend-api, database-repository, frontend-ui, and testing stages.

# Rules and Constraints

- Do not force a new framework, database, or UI stack unless the repository has no suitable pattern.
- Keep business logic out of UI components and out of request handlers where the repo expects separation.
- Preserve separation of concerns.
- Do not invent domain-specific requirements or business rules that were not provided.
- Prefer the smallest clean structure that satisfies the current use case.
- Clearly document when the repo lacks a clear pattern and what minimal structure is being introduced.
