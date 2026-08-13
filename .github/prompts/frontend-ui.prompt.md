---
mode: agent
description: "Implement UI pages, components, and workflows in the repo's existing UI stack"
tools: ["codebase", "search", "editFiles", "terminal"]
---

# Purpose

Implement the required user interface for `{{USE_CASE}}` using the repository's existing UI framework and component conventions.

# Inputs

- `{{REQUIREMENTS}}`
- `{{UI_REQUIREMENTS}}`
- `{{ARCHITECTURE_CONTEXT}}`
- `{{CONSTRAINTS}}`

# Responsibilities

- Inspect the repo's current UI framework and conventions.
- Define the required screens, pages, components, and workflows.
- Reuse existing components and layout patterns before creating new ones.
- Implement forms, validation, loading states, and error states.
- Integrate the UI with backend APIs or services in the repo's existing way.
- Preserve separation between presentation and business logic.

# Execution Instructions

1. Inspect the repository to understand the current UI framework, component structure, and styling conventions.
2. Identify the minimal screens and interactions required by the use case.
3. Reuse existing UI components and patterns before creating new ones.
4. Implement forms, actions, validation, and state handling consistent with repo conventions.
5. Ensure the UI handles loading, success, and failure states clearly.
6. Keep business logic out of UI components.
7. Consider accessibility and usability requirements when they are relevant to the project.

# Output / Handoff

Return a UI summary containing:

- screens or pages
- components and workflows
- form and validation behavior
- API or service integration points
- loading/error/success state handling
- accessibility considerations

Pass the UI requirements to testing and documentation.

# Rules and Constraints

- Do not assume a particular UI framework or library without checking the repo.
- Do not put business rules, validation logic, or persistence logic directly into UI components if the repo expects separation.
- Reuse repo conventions for styling, state, and component structure.
- Keep the experience generic and adaptable to different domains.
- Do not fabricate fake data or static content that does not match the architecture or repo context.
