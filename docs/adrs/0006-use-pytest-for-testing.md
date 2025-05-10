# 6. Use pytest for the Testing Framework

## Status

Accepted

## Context

Automated testing is essential for ensuring the correctness and reliability of the project's code, including utilities, CLI commands, and ADK agent components. We need a flexible and widely adopted testing framework for Python.

## Decision

We will use pytest as the primary testing framework for unit and integration tests.

## Consequences

*   **Benefits:**
    *   Easy to write and run tests.
    *   Supports simple `assert` statements.
    *   Extensive plugin ecosystem (e.g., `pytest-mock`).
    *   Good support for parameterization and fixtures.
    *   Widely adopted in the Python community.
*   **Drawbacks:**
    *   Requires developers to learn the pytest conventions.
*   **Impact on Plan:**
    *   `tests/` directory will be structured to work with pytest.
    *   Tests will be written as functions or methods within classes following pytest conventions.
    *   `pytest` and necessary plugins (`pytest-mock`) will be included as development dependencies in `pyproject.toml`.
    *   CLI `test` command will execute `pytest`.
    *   Pre-commit hooks can integrate with pytest for checks.
