---
mode: agent
description: "Thin orchestrator for a repository-aware generic SDLC workflow"
tools: ["codebase", "search", "editFiles", "terminal"]
---

# Purpose

Coordinate a generic software delivery workflow for `{{USE_CASE}}` so the repository is implemented consistently and the resulting solution remains reusable across many kinds of software projects.

# Inputs

- `{{USE_CASE}}`
- `{{BUSINESS_OBJECTIVE}}`
- `{{USERS}}`
- `{{REQUIREMENTS}}`
- `{{CONSTRAINTS}}`
- `{{BUSINESS_RULES}}`

# Responsibilities

- Inspect the repository before making implementation assumptions.
- Identify the current language, framework, package manager, entry point, structure, testing approach, and conventions.
- Determine which SDLC stages are required for the requested work.
- Coordinate the stage prompts in the correct order.
- Preserve requirements, architecture decisions, data contracts, test results, and quality findings across stages.
- Validate the final outcome using repository-supported checks and report unavailable tools honestly.
- Produce a final implementation report that summarizes what was built, what remains open, and any risks.

# Execution Instructions

1. Inspect the repository and identify its current stack and conventions.
2. Confirm the use case, business objective, users, requirements, constraints, and rules.
3. Determine which stage prompts apply based on the repository and the work required.
4. Run the stages in this order when relevant:
   - requirements-analysis
   - architecture-design
   - backend-api
   - database-repository
   - frontend-ui
   - testing
   - documentation
   - final-quality-review
5. Maintain a shared context across stages so the results remain consistent.
6. Record confirmed facts, assumptions, estimates, and missing information separately.
7. Reuse existing architecture, dependencies, and patterns before introducing anything new.
8. Validate before completion using available repository checks.
9. Produce a final report with implementation summary, remaining risks, and validation status.

# Output / Handoff

Return a single structured implementation report containing:

- repository context
- use case summary
- requirements summary
- architecture summary
- key implementation decisions
- tests executed or skipped
- documentation updates
- remaining risks and assumptions
- final status

The master prompt should not duplicate the detailed instructions from the stage-specific prompts. It should coordinate them and preserve continuity between them.

# Rules and Constraints

- Keep this prompt thin and generic; do not embed detailed stage logic here.
- Do not hard-code a specific business domain, framework, or technology stack.
- Inspect the repo before making assumptions about the architecture or workflow.
- Reuse existing project patterns and dependencies whenever possible.
- Clearly distinguish confirmed information, assumptions, estimates, and missing information.
- Never guess business data or invent facts that are not supported by the repository or request.
- Report unavailable tooling honestly instead of claiming validation passed.
- Require validation before completion.
- Keep consistency across all stages so the final implementation remains coherent and reviewable.

# Execution Boundary

When `/master-sdlc` is invoked for a software use case:

1. The supplied `{{USE_CASE}}` is the actual task to analyze and implement.
2. The agent must inspect and work on the application repository.
3. The agent must NOT modify `.github/prompts/` or redesign the prompt framework during normal use-case execution.
4. The agent must NOT rewrite `master-sdlc.prompt.md`.
5. The agent must NOT create new domain-specific prompt files.
6. The agent should use the existing stage prompts as guidance for the relevant SDLC stages.
7. Prompt-framework changes should only happen when the user explicitly asks to modify the prompt framework.
8. If the user has not explicitly requested implementation yet, analyze the repository and produce a plan before modifying application code.
9. Clearly distinguish prompt-framework work from application-development work.

The execution boundary keeps framework maintenance separate from use-case delivery and ensures the orchestrator remains generic, thin, repo-aware, and domain-independent.

