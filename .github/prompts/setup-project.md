# Set Up Project File

Create the project setup file for this repository.

## Instructions

1. Inspect the repository before making changes. Identify the application type, language, framework, package manager, and existing configuration files.
2. Determine which project setup file is appropriate for the detected stack. Examples include `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or an equivalent project manifest.
3. Create the file only if it does not already exist. If it exists, preserve its current structure and make only the changes required to complete setup.
4. Include the minimum required metadata and configuration for the project to install dependencies, run locally, build, and test.
5. Follow the conventions already used by the repository. Do not add dependencies, scripts, or settings that are not needed for the detected stack.
6. Add or update documentation only when the setup file introduces a command or prerequisite that a contributor needs to know about.
7. Validate the result with the repository's available package-manager, build, lint, or test command. Report any missing tools or unresolved errors.
8. Do not delete, reset, or overwrite unrelated user changes.

## Output

Report:

- The setup file created or updated.
- The project type and package manager detected.
- The commands available for install, development, build, lint, and test.
- The validation command that was run and its result.
- Any decisions, assumptions, or remaining setup steps.
