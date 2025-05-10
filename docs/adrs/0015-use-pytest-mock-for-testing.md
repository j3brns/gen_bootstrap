# 15. Use pytest-mock for Mocking in Tests

## Status

Accepted

## Context

When writing unit and integration tests, particularly for code that interacts with external services (like GCP APIs, external tools, or generative models), it is necessary to isolate the code under test by simulating the behavior of these dependencies. Mocking allows us to control the output of these dependencies and verify that our code interacts with them correctly without making actual external calls.

## Decision

We will use the `pytest-mock` plugin for pytest to facilitate mocking in our tests. This plugin provides a convenient fixture (`mocker`) that wraps Python's built-in `unittest.mock` library.

## Consequences

*   **Benefits:**
    *   Provides a clean and easy-to-use interface for mocking within pytest tests.
    *   Leverages the power of Python's standard `unittest.mock` library.
    *   Simplifies patching objects and controlling return values or side effects.
    *   Integrates seamlessly with the pytest framework and fixtures.
*   **Drawbacks:**
    *   Adds a development dependency (`pytest-mock`).
    *   Requires understanding of mocking concepts and the `unittest.mock` API.
*   **Impact on Plan:**
    *   `pytest-mock` will be included as a development dependency in `pyproject.toml`.
    *   Tests in the `tests/` directory will utilize the `mocker` fixture provided by `pytest-mock` to mock external dependencies, including GCP client library calls, tool executions, etc.
    *   Documentation will include examples of how to use `pytest-mock` in tests.
