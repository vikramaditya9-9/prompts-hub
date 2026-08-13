---
mode: agent
description: "Update repo documentation to reflect the actual implementation"
tools: ["codebase", "search", "editFiles"]
---

# Purpose

Update the repository documentation so it reflects the actual behavior, structure, usage, and validation status for `{{USE_CASE}}`.

# Inputs

- `{{REQUIREMENTS}}`
- `{{ARCHITECTURE_CONTEXT}}`
- `{{CONSTRAINTS}}`
- implementation summary and validation results

# Responsibilities

- Review the existing documentation and identify what is missing or inaccurate.
- Update README, setup instructions, configuration guidance, usage notes, and architecture notes where appropriate.
- Describe actual behavior, constraints, and verification steps.
- Keep the documentation consistent with the implementation and repo conventions.

# Execution Instructions

1. Inspect the repo's existing documentation and current conventions.
2. Update only the documentation needed for the implemented behavior.
3. Include setup, configuration, usage, testing, and architectural notes where those are relevant.
4. Document actual behavior, assumptions, and known limitations clearly.
5. Keep the content concise and aligned with the repository's existing style.

# Output / Handoff

Return documentation updates covering:

- overview and purpose
- architecture or component summary
- setup and configuration notes
- usage instructions
- testing notes
- limitations and assumptions

Pass the documentation state to final-quality-review.

# Rules and Constraints

- Do not invent features, workflows, or configuration that are not present.
- Keep documentation generic and reusable, not tied to a single business domain.
- Reflect actual behavior only.
- Avoid repeating large parts of the code in prose; summarize clearly and practically.
- Update the minimum necessary documentation to keep the repo honest and usable.
