# 11. Use FastAPI/Uvicorn for the Backend Server

## Status

Accepted (if applicable to ADK structure)

## Context

The generative AI ADK application, when deployed to Cloud Run, will likely need to expose an HTTP endpoint to receive requests (e.g., from a frontend, another service, or a webhook). We need a performant and easy-to-use Python web framework for this purpose.

## Decision

We will use FastAPI as the web framework and Uvicorn as the ASGI server for the backend component of the ADK application, if the ADK structure requires a web server to handle incoming requests.

## Consequences

*   **Benefits:**
    *   High performance due to being built on ASGI standards.
    *   Automatic generation of OpenAPI (Swagger) documentation.
    *   Easy data validation using Pydantic.
    *   Modern Python features (async/await, type hints).
    *   Good fit for building APIs.
*   **Drawbacks:**
    *   Adds dependencies (`fastapi`, `uvicorn`).
    *   Requires understanding of asynchronous programming if leveraging `async/await`.
*   **Impact on Plan:**
    *   `fastapi` and `uvicorn` will be included as core dependencies in `pyproject.toml`.
    *   The `main.py` or a file in `adk/` will contain the FastAPI application instance.
    *   The `Dockerfile` will include the command to run the FastAPI application using Uvicorn.
    *   The plan for Cloud Run deployment includes configuring the container to listen on the correct port (8080 by default for Cloud Run).
