---
applyTo: "**/*"
---

# Repository guardrails

Follow these rules for any implementation performed inside this repository.

## Repository-aware behavior

- Reuse the repository's existing package manager, project layout, and code conventions before creating new ones.
- Identify the current application entry point, module layout, service boundaries, and testing convention before making changes.
- Prefer minimal changes that fit the repository over introducing a new framework or architectural style.
- Keep naming consistent with the files and modules already present in the repository.

## Implementation safety

- Do not build a specific business use case unless the user explicitly requests it.
- Do not add unrelated features or extra dependencies for a single task.
- If a repository pattern is unclear, create the smallest clean structure required for the job, not a large generalized system.
- Treat mock or demo data as explicitly labeled and separate from production data.

## Domain independence

- Keep prompts, designs, and implementations reusable across many use cases.
- Use generic terms like `entity`, `workflow`, `request`, `response`, `repository`, `service`, and `adapter` rather than hard-coded domain assumptions.
- Resist hard-coding app-specific claims or user examples unless they are in the input payload.

## Validation expectations

- Run the repository's relevant tests after implementation changes.
- If a task changes behavior, add or update tests to cover the new or corrected contract.
- Keep validation focused on the changed behavior and repository conventions.
