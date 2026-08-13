---
mode: agent
description: "Convert a software request into structured, reusable requirements"
tools: ["codebase", "search", "editFiles"]
---

# Requirements analysis

Analyze the software request for `{{USE_CASE}}` and convert it into a clear, reusable requirements set.

## Goal

Capture the problem clearly enough to design and implement the solution without guessing at business facts.

## Inputs

- Use case: `{{USE_CASE}}`
- Business objective: `{{BUSINESS_OBJECTIVE}}`
- Primary users: `{{PRIMARY_USERS}}`
- Functional requirements: `{{FUNCTIONAL_REQUIREMENTS}}`
- Non-functional requirements: `{{NON_FUNCTIONAL_REQUIREMENTS}}`
- Business rules: `{{BUSINESS_RULES}}`
- Constraints: `{{CONSTRAINTS}}`

## Required output

Produce a requirements summary with:

- actors and stakeholders
- user and system inputs
- expected outputs and user-visible behaviors
- core entities and their relationships
- workflows and lifecycle stages
- business rules and validation rules
- permissions and access constraints
- edge cases and error conditions
- assumptions and unresolved questions

## Instructions

- Identify what is known, what is inferred, and what is missing.
- Do not invent critical behavior or domain facts.
- Separate functional requirements from non-functional requirements.
- List validation rules clearly, including required vs optional fields and error conditions.
- Note external dependencies or integrations only when they are relevant to the request.
- Keep the requirements reusable and generic rather than tied to one vertical domain.

## Output format

```text
Summary
- Use case:
- Objective:
- Users:
- Constraints:

Requirements
- Functional:
- Non-functional:
- Business rules:
- Validation:
- Permissions:
- Edge cases:

Assumptions / gaps
- 
```
