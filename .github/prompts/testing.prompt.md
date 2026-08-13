---
mode: agent
description: "Define and execute a reusable testing strategy"
tools: ["codebase", "search", "editFiles", "terminal"]
---

# Testing

Define and execute the testing strategy for `{{USE_CASE}}` while following the repository's existing test patterns.

## Inputs

- Requirements: `{{REQUIREMENTS}}`
- Constraints: `{{CONSTRAINTS}}`
- Current test framework and repository conventions: inspect before coding

## Goal

Verify correctness, edge cases, and regression safety with the smallest effective test set.

## Test strategy

- Write tests for the required behavior, not the implementation details.
- Cover happy paths, invalid input, edge conditions, and failure paths.
- Include validation checks, status transitions, and repository/service interactions as needed.
- Prefer repository-consistent test styles and realistic data.

## Checklist

- Unit tests for business logic or validation
- Integration tests for API or service boundaries
- UI tests only if the repo already has a pattern for them
- Edge cases and empty input handling
- Error handling and contract validation

## Output format

```text
Test plan
- Scope:
- Happy paths:
- Edge cases:
- Failure cases:

Validation steps
- Commands to run:
- Expected outcomes:
```

## Guardrails

- Do not test mock-only behavior.
- Do not add test-only code to production modules.
- Keep tests focused on real behavior and signal actual risk.
- Do not broaden the test suite unnecessarily.
