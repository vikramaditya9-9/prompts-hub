# Build an Insurance Claim Workflow

Build a complete insurance-claim workflow that lets a user capture claim information, review it, and prepare it for submission.

## Instructions

1. Inspect the repository before making changes. Identify the language, framework, package manager, application entry point, API conventions, UI framework, persistence approach, test tools, and existing project structure.
2. Follow the repository's existing architecture and conventions. Reuse existing dependencies and components. Do not introduce a new framework or database unless the current project has no suitable option.
3. Define a claim data model that supports policy details, incident details, affected people or property, losses and expenses, supporting documents, status, and audit timestamps when consistent with the project.
4. Implement APIs using the project's routing and serialization conventions. At minimum provide:
   - `POST /api/claims` to create a claim draft;
   - `GET /api/claims/{id}` to retrieve a claim;
   - `PUT` or `PATCH /api/claims/{id}` to update a draft;
   - `POST /api/claims/{id}/submit` to validate and mark a claim ready for submission;
   - an endpoint for supported insurance types or claim-form metadata when the UI needs it.
5. Validate required fields, dates, amounts, currency, enum values, and claim state transitions at the API boundary. Return consistent success and error response shapes with appropriate HTTP status codes.
6. Implement a service layer containing claim rules and orchestration. Keep HTTP concerns out of services and persistence concerns out of route handlers or controllers.
7. Implement a repository layer behind an interface or project-equivalent abstraction. Provide a deterministic mock or in-memory repository with seeded data so the feature runs locally without external services.
8. Build a responsive UI using the repository's existing UI framework. Include a multi-section claim form, accessible validation, repeatable loss and document fields, draft-save behavior, loading and error states, a review screen, and a final verification step before submission.
9. Use mock data in development and tests only. Clearly label seeded records as mock data and never use fabricated data in a real claim submission.
10. Ask only for information needed to prepare the claim. Never request passwords, payment-card PINs, authentication codes, or unnecessary sensitive personal data.
11. Clearly separate confirmed facts from estimates, assumptions, and missing information. Never invent incident details, losses, medical information, receipts, witnesses, or policy coverage.
12. Help the user create a factual claim statement that includes:
   - what happened and when;
   - people, property, vehicles, or services affected;
   - immediate steps taken to prevent further loss;
   - injuries or damage, described only from the user's information;
   - police, emergency, repair, medical, or other report references;
   - the amount being claimed, with a breakdown and supporting evidence.
13. Create a checklist of supporting documents relevant to the claim, such as the policy schedule, identification, invoices, receipts, photographs, repair estimates, medical records, proof of ownership, travel records, police reports, or witness details. Mark each item as provided, missing, or not applicable.
14. Identify policy deadlines, notice requirements, deductibles, exclusions, limits, and required forms only when they are present in the policy or supplied by the user. Tell the user to confirm uncertain requirements with the insurer.
15. Produce a submission-ready claim package containing:
   - a claim summary;
   - the claim statement;
   - loss or expense table;
   - document checklist;
   - questions for the insurer;
   - suggested next actions and deadlines.
16. Do not provide a guaranteed outcome, legal conclusion, medical diagnosis, or advice to misrepresent facts. Encourage the user to consult a licensed professional for legal, financial, or medical questions.
17. Before submission, ask the user to verify names, dates, policy details, amounts, attachments, and contact information. Do not submit a claim or contact the insurer unless the user explicitly requests that action and the required integration is available.
18. Recommend keeping copies of the complete submission, confirmation number, correspondence, receipts, and a timeline of communications.
19. Add focused tests for API validation and status codes, service rules and state transitions, repository CRUD behavior, deterministic mock data, UI rendering and validation, draft saving, API failures, and successful submission. Add integration or end-to-end tests for the primary create, edit, review, and submit flow when supported.
20. Update OpenAPI, UI documentation, README usage instructions, environment configuration, and seed instructions when those conventions already exist.
21. Run the repository's formatter, linter, type checker, build command, unit tests, and focused integration or UI tests when configured. Report unavailable tools instead of adding unrelated tooling.

## Output

Report the implementation first:

### Implementation Summary

- files created or updated;
- detected language, framework, package manager, and persistence approach;
- API routes, request and response shapes, validation rules, and status codes;
- services and business rules;
- repository interface and mock-data strategy;
- UI screens, form sections, states, accessibility behavior, and API integration;
- tests added or updated;
- commands run and their results;
- assumptions, unavailable tools, and remaining production integration work.

Then provide the claim workflow artifacts:

Use this structure:

### Claim Overview

- Insurance type:
- Insurer:
- Policy or claim reference:
- Incident date and location:
- Current claim status:

### Claim Statement

Write a concise, factual statement using only confirmed information. Clearly label any missing details with `[NEEDS INFORMATION]`.

### Loss or Expense Table

| Item | Description | Date | Amount | Evidence | Status |
|---|---|---|---:|---|---|

### Document Checklist

| Document | Required or optional | Status | Notes |
|---|---|---|---|

### Questions for the Insurer

List questions about coverage, deductibles, deadlines, required forms, assessment, settlement, and next steps.

### Next Actions

List the actions in priority order, including any deadline supplied by the user or policy. Mark unknown deadlines as `CONFIRM WITH INSURER`.

### Verification Before Submission

Remind the user to verify all facts, amounts, attachments, and contact details before submitting.
