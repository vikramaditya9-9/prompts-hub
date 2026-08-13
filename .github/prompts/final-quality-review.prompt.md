---
mode: agent
description: "Review the final implementation against requirements, quality, and repo standards"
tools: ["codebase", "search", "editFiles", "terminal"]
---

# Purpose

Perform a final quality review for `{{USE_CASE}}` and determine whether the implementation is ready, incomplete, or blocked by risk.

# Inputs

- `{{REQUIREMENTS}}`
- `{{ARCHITECTURE_CONTEXT}}`
- `{{CONSTRAINTS}}`
- all prior implementation outputs

# Responsibilities

- Review the implementation against the requirements.
- Check architecture consistency and separation of concerns.
- Review API, repository, UI, and testing quality.
- Inspect error handling, edge cases, and security-relevant assumptions.
- Run available quality checks and report actual status.
- Flag remaining risks and unresolved issues.

# Execution Instructions

1. Review the implementation against the requirements and constraints.
2. Check whether the architecture remains consistent with the repo's patterns.
3. Inspect backend, repository, UI, and documentation outputs for alignment and gaps.
4. Review test coverage and validation results.
5. Check error handling, validation, edge cases, and assumptions.
6. Run repo-supported quality checks when available.
7. Report the outcome clearly as PASS, FAIL, NOT AVAILABLE, or REMAINING RISK.
8. Provide a final confidence rating and any follow-up recommendations.

# Output / Handoff

Return a final quality report containing:

- requirements coverage
- architecture fit
- API quality
- persistence quality
- UI quality
- test status
- documentation status
- security and error-handling review
- remaining gaps and risk
- final PASS / FAIL / NOT AVAILABLE / REMAINING RISK status

# Rules and Constraints

- Do not mark the work complete without available evidence.
- Clearly distinguish between PASS, FAIL, NOT AVAILABLE, and REMAINING RISK.
- Report unavailable validation tools honestly.
- Keep review domain-independent and repo-aware.
- Flag unresolved assumptions and hidden risk rather than suppressing them.
