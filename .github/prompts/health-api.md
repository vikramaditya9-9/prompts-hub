# Generate Application Health APIs

Design and implement health-check APIs for this application.

## Instructions

1. Inspect the repository before making changes. Identify the language, framework, package manager, application entry point, routing conventions, configuration system, logging approach, and existing test setup.
2. Follow the repository's existing architecture and naming conventions. Do not introduce a new framework or dependency unless the current stack has no suitable HTTP or health-check support.
3. Implement these endpoints, using the repository's standard API versioning conventions when they exist:
   - `GET /health/live`: process liveness. Return HTTP `200` when the application process is running. Do not call external services from this endpoint.
   - `GET /health/ready`: readiness for traffic. Check only dependencies required to serve requests, such as databases, queues, caches, or essential configuration. Return HTTP `200` when ready and HTTP `503` when not ready.
   - `GET /health`: return a concise aggregate health response when the application already exposes a general health route. Avoid creating a duplicate route if an equivalent endpoint exists.
4. Use a consistent JSON response shape containing at least `status` and `checks`. Each check should include a stable name and status. Include latency or error details only when they are safe for the deployment environment.
5. Apply strict timeouts to dependency checks. Run independent checks concurrently when that matches the framework's execution model, and ensure one failing dependency does not hide the status of the others.
6. Never expose secrets, credentials, connection strings, stack traces, internal hostnames, or sensitive query details in responses. Log diagnostic details through the existing structured logging system at an appropriate level.
7. Respect the application's authentication, middleware, tracing, and rate-limiting conventions. Health endpoints must remain usable by the configured load balancer or orchestrator, with authentication bypassed only when the repository's deployment model requires it.
8. Make dependency checks easy to replace or mock. Do not perform network calls at module import time, and do not make the liveness endpoint depend on readiness checks.
9. Add focused tests for:
   - liveness success without dependency calls;
   - readiness success when all required checks pass;
   - readiness returning `503` when a required check fails or times out;
   - partial check failures being represented without leaking sensitive details;
   - the response schema and content type.
10. Add or update OpenAPI documentation, route documentation, or README usage instructions when the repository already maintains them.
11. Run the repository's formatter, linter, type checker, build command, and focused tests when those tools are configured. Report commands that are unavailable instead of adding unrelated tooling.

## Configuration

Use existing configuration conventions for:

- dependency-check timeouts;
- required versus optional dependencies;
- environment-specific detail visibility;
- endpoint paths and API versioning.

If these settings do not exist, introduce the smallest configuration surface needed and document its defaults.

## Output

Report:

- files created or updated;
- detected language, framework, and package manager;
- endpoint paths, status codes, and response schema;
- dependencies checked and their required or optional classification;
- tests added or updated;
- validation commands run and their results;
- assumptions, unavailable tools, and remaining deployment steps.
