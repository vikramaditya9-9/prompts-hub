---
mode: agent
description: "Create and run the repo-appropriate validation strategy"
tools: ["codebase", "search", "editFiles", "terminal"]
---

# Purpose

Define and execute a focused testing strategy for `{{USE_CASE}}` that matches the repository's existing test framework and behavior.

# Inputs

- `{{REQUIREMENTS}}`
- `{{TEST_REQUIREMENTS}}`
- `{{ARCHITECTURE_CONTEXT}}`
- `{{CONSTRAINTS}}`

# Responsibilities

- Inspect the repository's current test framework.
- Determine the relevant unit, integration, API, UI, and end-to-end tests supported by the project.
- Test the required behavior without overextending the test suite.
- Validate edge cases, invalid inputs, and failure conditions.
- Report actual execution status honestly.

# Execution Instructions

1. Inspect the repo to identify the current testing framework, conventions, and supported commands.
2. Determine the minimum tests required for the changed behavior.
3. Cover key behavior such as:
   - unit logic
   - business rules
   - repository/data behavior
   - API or handler behavior
   - UI flows when supported
   - integration or end-to-end flows only if the repo already supports them
4. Validate edge cases, invalid input, status transitions, and error handling.
5. Run the repo-supported validation commands that are actually available.
6. Report any unavailable tooling instead of claiming success without evidence.

# Output / Handoff

Return a testing summary containing:

- tested behaviors
- test types used
- key edge cases covered
- validation commands run
- results and failures
- remaining gaps or risks

Pass the test results to final-quality-review and documentation.

# Rules and Constraints

- Do not test mock-only behavior.
- Do not add test-only code into production modules.
- Keep tests focused on actual behavior rather than implementation details.
- Do not claim a test passed unless it was executed and the result is known.
- Reuse the repo's existing test patterns and tooling before introducing anything new.
- Keep the test strategy generic and reusable across many use cases.
