---
mode: agent
description: "Perform final cross-checks for quality, completeness, and consistency"
tools: ["codebase", "search", "editFiles", "terminal"]
---

# Final quality review

Review the entire solution for `{{USE_CASE}}` before sign-off.

## Inputs

- Requirements: `{{REQUIREMENTS}}`
- Design summary: `{{DESIGN_SUMMARY}}`
- Implementation details: inspect before finalizing
- Constraints: `{{CONSTRAINTS}}`

## Review checklist

- Does the implementation match the requirement set?
- Is the architecture consistent with the repository's existing patterns?
- Are responsibilities cleanly separated?
- Did validation and error handling cover meaningful failure modes?
- Are tests covering the changed behavior?
- Are docs accurate and aligned with what was implemented?
- Did the work avoid unnecessary dependencies or broad scope changes?
- Are assumptions and unresolved gaps clearly noted?

## Output format

```text
Final status
- Ready / needs follow-up:
- Remaining risks:
- Open assumptions:

Review summary
- Requirements coverage:
- Architecture fit:
- Test confidence:
- Documentation confidence:
```

## Sign-off rule

Only mark the work as complete if the repo context, requirements, implementation, tests, and documentation all align.
