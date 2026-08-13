---
mode: agent
description: "Design and implement a generic frontend/UI workflow"
tools: ["codebase", "search", "editFiles", "terminal"]
---

# Frontend / UI development

Design and implement the frontend experience for `{{USE_CASE}}` in a way that matches the repository's existing UI approach.

## Inputs

- Requirements: `{{REQUIREMENTS}}`
- Constraints: `{{CONSTRAINTS}}`
- Existing UI conventions: inspect before coding

## Goal

Deliver a user-facing interface that is clear, maintainable, and aligned with the repo's conventions without embedding business logic inside the view layer.

## Responsibilities

- Define the screens, components, flows, and interactions required by the use case.
- Keep layout, state, and component responsibilities clear.
- Connect UI to the appropriate API or service boundaries.
- Surface validation feedback and error states clearly.
- Keep display logic separate from domain logic.

## Checklist

- Identify screens, views, or pages needed.
- Identify reusable components and layout patterns.
- Define input controls, validation messages, and state transitions.
- Decide whether a local or server-backed data flow is needed.
- Keep the UI consistent with repository conventions and style.

## Output format

```text
UI summary
- Screens / views:
- Components:
- User flows:
- State handling:

Interaction rules
- Validation:
- Error states:
- Accessibility / usability considerations:

Implementation notes
- Files or modules to update:
- API contract assumptions:
```

## Guardrails

- Do not put business rules or persistence code directly into UI components.
- Do not invent a new UI framework unless the repo already supports one.
- Keep the experience generic and adaptable to multiple use cases.
