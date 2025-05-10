# ADR 0024: Set CLI Script Alias to `lunagen`

**Status:** Superseded
**Superseded by:** Decision to use "gen-bootstrap" as the CLI alias (see ADR 0028 or project documentation).

**Date:** 2025-04-22

**Context:**

The project includes a command-line interface (CLI) implemented using Typer/Click (ADR-0004), with the main entry point at `cli/main.py`. Initially, the script alias defined in `pyproject.toml` under `[tool.poetry.scripts]` was `cli`, later briefly changed to `sparc`. Running the CLI required typing `poetry run python cli/main.py ...` or `poetry run cli ...`. These commands are functional but not particularly memorable or user-friendly for frequent use. A more descriptive and accessible alias was desired.

**Decision:**

We decided to change the script alias defined in `pyproject.toml` to `lunagen`.

The relevant section in `pyproject.toml` is now:
```toml
[tool.poetry.scripts]
lunagen = "cli.main:app"
```
This allows the CLI to be invoked via `poetry run lunagen ...` within the project's environment after running `poetry install`.

Instructions were also provided on how to add the Poetry scripts directory to the system PATH to enable global invocation via just `lunagen ...`.

**Consequences:**

*   **Positive:**
    *   Provides a more memorable and distinct command (`lunagen`) for invoking the CLI.
    *   Improves developer experience.
    *   Follows standard Python packaging practices for defining entry points.
*   **Neutral:**
    *   Requires users to run `poetry install` to update the script wrapper.
    *   Global access requires a manual PATH configuration step by the user.
*   **Negative:**
    *   None anticipated.
