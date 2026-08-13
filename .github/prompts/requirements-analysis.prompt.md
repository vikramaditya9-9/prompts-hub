---
mode: agent
description: "Convert a use case into a reusable requirements specification"
tools: ["codebase", "search", "editFiles"]
---

# Purpose

Convert the requested work for `{{USE_CASE}}` into a clear, reusable requirements specification that can drive design, implementation, testing, and review.

# Inputs

- `{{USE_CASE}}`
- `{{BUSINESS_OBJECTIVE}}`
- `{{USERS}}`
- `{{REQUIREMENTS}}`
- `{{CONSTRAINTS}}`
- `{{BUSINESS_RULES}}`

# Responsibilities

- Identify actors, users, and system participants.
- Define functional requirements.
- Define non-functional requirements.
- Capture workflows, states, and lifecycle events.
- Identify entities and their relationships.
- Document business rules and validation logic.
- Identify edge cases, error conditions, and assumptions.
- Capture unresolved information and missing requirements.
- Define acceptance criteria for implementation and validation.

# Execution Instructions

1. Inspect the repository only to understand the project context and constraints.
2. Interpret the use case in a domain-independent way.
3. Separate confirmed information from assumptions and unknowns.
4. Identify the main users, actors, and stakeholders.
5. List functional requirements using clear, testable statements.
6. List non-functional requirements including quality, performance, usability, security, reliability, and operational needs where relevant.
7. Identify entities, relationships, and state transitions.
8. Document validation logic and business rules.
9. Identify edge cases, failure scenarios, and assumptions.
10. State acceptance criteria in a way that can be validated later.
11. Capture missing information explicitly rather than inventing it.

# Output / Handoff

Return a requirements summary with:

- actors and users
- functional requirements
- non-functional requirements
- workflows and states
- entities and relationships
- business rules
- validation rules
- edge cases and failure modes
- assumptions and missing information
- acceptance criteria

Pass this specification to the architecture-design stage as a stable requirements baseline.

# Rules and Constraints

- Keep the prompt domain-independent in structure and language.
- Do not invent business facts or requirements that are not supported by the request or repository.
- Clearly distinguish confirmed information, assumptions, estimates, and missing information.
- Use simple, testable language that downstream prompts can implement and validate.
- Do not prescribe implementation details before requirements are finalized.
- Keep the requirements reusable across many kinds of software use cases.
