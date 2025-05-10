# ADR 0028: Set CLI Script Alias to `gen-bootstrap`

**Status:** Accepted

**Date:** 2025-05-10 <!-- Please update with the actual decision date -->

**Context:**

The project's command-line interface (CLI) was previously aliased as `lunagen` (see ADR 0024). As part of a broader project refactoring to align with the "gen-bootstrap" identity and integrate the Google Agent Development Kit (`google-adk`), a new, consistent CLI alias was required. The previous alias `lunagen` no longer reflected the project's new name and focus.

**Decision:**

We decided to change the script alias for the project's CLI, defined in `pyproject.toml` under `[tool.poetry.scripts]`, from `lunagen` to `"gen-bootstrap"`.

The relevant section in `pyproject.toml` is now:
```toml
[tool.poetry.scripts]
"gen-bootstrap" = "sparc.cli.main:app"
```
This allows the CLI to be invoked via `poetry run gen-bootstrap ...` within the project's environment after running `poetry install`. The entry point `sparc.cli.main:app` assumes the Typer application object `app` is located in `sparc/cli/main.py`.

This decision supersedes ADR 0024.

**Consequences:**

*   **Positive:**
    *   Provides a CLI alias (`gen-bootstrap`) that is consistent with the refactored project name and identity.
    *   Improves clarity and developer experience by aligning the command with the project's branding.
    *   Follows standard Python packaging practices for defining script entry points.
*   **Neutral:**
    *   Requires users to run `poetry install` to update the script wrapper to use the new alias.
    *   Global access (invoking `gen-bootstrap` directly without `poetry run`) still requires manual PATH configuration by the user for the Poetry scripts directory.
*   **Negative:**
    *   Users accustomed to the previous `lunagen` alias will need to adapt to the new command.

**Further Considerations:**
<!-- [TODO: User to elaborate on any further considerations, alternatives discussed, or detailed rationale if necessary.] -->
