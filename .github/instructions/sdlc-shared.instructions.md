---
applyTo: "**/*"
---

# Shared SDLC prompt instructions

Use these instructions for any software delivery workflow in this repository.

## Core operating rules

- Inspect the repository before changing code, config, or prompts.
- Determine the existing language, framework, package manager, entry point, testing approach, and structural conventions.
- Prefer the repository's existing patterns over introducing a new framework, library, or architecture.
- Keep the implementation generic and reusable across many use cases.
- Do not assume a specific industry, domain, or business process unless the user explicitly provides it.
- Use placeholders such as `{{USE_CASE}}`, `{{BUSINESS_OBJECTIVE}}`, `{{REQUIREMENTS}}`, `{{CONSTRAINTS}}`, and `{{PRIMARY_USERS}}` wherever context is needed.
- Treat missing information as a gap to document, not as a reason to invent facts.
- Clearly state assumptions and unresolved questions.
- Avoid unnecessary dependencies or broad architecture churn.
- Keep scope small, testable, and aligned with the repository's current conventions.

## Expected workflow

1. Discover the repository and understand its existing stack.
2. Clarify the use case and the business goal.
3. Convert the use case into structured requirements.
4. Design the smallest viable architecture that fits the repo.
5. Implement the needed layers in the appropriate files.
6. Add or update tests for the changed behavior.
7. Write or update documentation that reflects reality.
8. Perform a final quality review before handoff.

## Quality bar

- Separate concerns clearly across domain, service, API, persistence, UI, tests, and documentation.
- Keep business logic out of presentation layers.
- Keep persistence details out of UI or service layers unless the repository already follows that pattern.
- Validate edge cases, invalid input, error states, and missing data.
- Prefer deterministic, reviewable outputs over hidden magic.

## Output expectations

When creating or modifying code, produce:

- a clear summary of the current repository context
- the assumptions and open questions
- the structured requirements or design decisions
- the implementation or patch plan
- the validation approach
- a final review note that signals completeness or remaining risk
