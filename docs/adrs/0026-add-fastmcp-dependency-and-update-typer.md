# ADR 0026: Add `fastmcp` Dependency and Update `typer`

**Status:** Superseded
**Reason:** MCP interactions and tool context management will primarily be handled via `google-adk`. If `fastmcp` is to be used later, its role must be defined as complementary to `google-adk`.

**Date:** 2025-04-22

**Context:**

The project uses FastAPI for its backend component (ADR-0011) and aims to implement tool-use capabilities (ADR-0014), potentially aligning with Model Context Protocol (MCP) principles. The `fastmcp` library (`https://pypi.org/project/fastmcp/`) was identified as a potential accelerator for integrating MCP patterns within a FastAPI application.

An initial attempt to add `fastmcp` using `poetry add fastmcp` failed due to a dependency conflict. The required version of `fastmcp` (`^2.2.1`) depended on `typer` version `>=0.15.2`, whereas the project was constrained to `typer` `^0.12.0`.

**Decision:**

1.  We decided to resolve the conflict by updating the `typer` dependency constraint in `pyproject.toml` from `{extras = ["all"], version = "^0.12.0"}` to `{extras = ["all"], version = "^0.15.2"}`.
2.  Following the update to `typer`, we successfully added the `fastmcp` package using `poetry add fastmcp`. This installed `fastmcp` (`^2.2.1`) and its required dependencies (including `mcp`), updated `typer` to `0.15.2`, and updated the `poetry.lock` file.

**Consequences:**

*   **Positive:**
    *   Adds the `fastmcp` library, potentially simplifying the implementation of MCP-related features within the FastAPI backend.
    *   Adds the core `mcp` library as a dependency.
    *   Keeps dependencies managed consistently via Poetry.
    *   Resolves the version conflict by updating `typer`.
*   **Neutral:**
    *   Adds several new dependencies (`fastmcp`, `mcp`, `httpx-sse`, `pydantic-settings`, `sse-starlette`, `exceptiongroup`, `openapi-pydantic`).
    *   Updates the `typer` version, which might require minor code adjustments if deprecated features were used (though unlikely between these versions).
*   **Negative:**
    *   Increases the overall dependency footprint of the project.
