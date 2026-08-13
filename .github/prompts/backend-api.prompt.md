---
mode: agent
description: "Implement backend or API functionality in the repository's current style"
tools: ["codebase", "search", "editFiles", "terminal"]
---

# Purpose

Implement the backend or API behavior for `{{USE_CASE}}` using the repository's existing conventions and technology stack.

# Inputs

- `{{REQUIREMENTS}}`
- `{{ARCHITECTURE_CONTEXT}}`
- `{{API_REQUIREMENTS}}`
- `{{CONSTRAINTS}}`

# Responsibilities

- Inspect the repository's backend patterns and routing conventions.
- Define the endpoints, handlers, or controller functions required for the use case.
- Define request and response contracts.
- Validate inputs and enforce business/service rules.
- Implement consistent error handling and status behavior.
- Connect the API layer to existing service or repository patterns.
- Respect authentication, authorization, and operational conventions already present in the repo.

# Execution Instructions

1. Inspect the repository to determine the current API style, routing, validation, and error-handling approach.
2. Define the API responsibilities needed by the use case.
3. Identify required endpoints or handlers and the operations they support.
4. Define request payloads, response payloads, and validation rules.
5. Keep business logic in service or domain layers when the repo already expects that separation.
6. Keep transport concerns separate from persistence concerns.
7. Implement consistent handling for success, validation failure, not-found, and conflict cases.
8. Add or update tests for the API behavior where the repo supports them.

# Output / Handoff

Return an API summary containing:

- endpoints or handlers
- request/response contract details
- validation rules
- error handling behavior
- service/repository boundaries
- testing notes

Pass the API contract and key behavior to testing and documentation.

# Rules and Constraints

- Do not assume REST, FastAPI, Django, Express, Java, or any other framework.
- Do not assume a specific protocol or serialization format without checking the repo.
- Reuse the repository's API, validation, and error conventions.
- Do not place persistence logic directly in route handlers unless that is already the repo pattern.
- Do not invent external dependencies, services, or auth systems unless the repo already uses them.
- Keep the solution generic and adaptable to different backend technologies.
