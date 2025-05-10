# 8. Use Pre-commit Hooks for Code Quality

## Status

Accepted

## Context

Maintaining consistent code style, formatting, and preventing common issues before code is committed to the repository is crucial for collaboration and project health.

## Decision

We will integrate `pre-commit` hooks to automatically run code formatting, linting, and other checks before commits are finalized.

## Consequences

*   **Benefits:**
    *   Enforces consistent code style and formatting across the team.
    *   Catches common errors early in the development cycle.
    *   Reduces time spent on manual code reviews for style issues.
    *   Automates tasks like sorting imports and stripping notebook outputs.
*   **Drawbacks:**
    *   Requires developers to install `pre-commit` and set up the hooks initially.
    *   Commits might be slightly slower due to hook execution.
*   **Impact on Plan:**
    *   `.pre-commit-config.yaml` will be a core project file.
    *   `pre-commit` and chosen linters/formatters (`black`, `isort`, `flake8`, `nbstripout`) will be included as development dependencies in `pyproject.toml`.
    *   CLI `init` command will guide users to install and set up pre-commit hooks.
    *   Documentation will explain how to use and configure pre-commit.
