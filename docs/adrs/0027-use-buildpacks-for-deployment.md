# ADR 0027: Use Google Cloud Buildpacks for Deployment

**Status:** Accepted

**Date:** 2025-04-22

**Context:**

The project targets Google Cloud Run for deployment (ADR-0002) and uses Google Cloud Build (ADR-0022). Initially, a `deployment/Dockerfile` was present to define the container image build process. While functional (pending corrections), maintaining a `Dockerfile` requires manual effort to ensure base images are updated, dependencies are layered correctly for caching, and the startup command aligns with the application structure (FastAPI/Uvicorn - ADR-0011).

Google Cloud Buildpacks offer an alternative, automated approach to building container images directly from source code for supported languages like Python, especially when using standard dependency managers like Poetry (ADR-0001).

**Decision:**

We decided to switch from using a custom `Dockerfile` to leveraging Google Cloud Buildpacks for building the container image for Cloud Run deployment.

This involved:
1.  Creating a `Procfile` in the project root to explicitly define the web process startup command:
    ```
    web: poetry run uvicorn main:app --host 0.0.0.0 --port $PORT
    ```
2.  Deleting the now redundant `deployment/Dockerfile`.

Deployments can now be initiated directly from source using commands like `gcloud run deploy --source .` or `gcloud builds submit --pack image=[IMAGE_NAME]`. Cloud Build will automatically use Buildpacks to detect the Python/Poetry/FastAPI setup, install dependencies, and configure the container image based on the `Procfile`.

**Consequences:**

*   **Positive:**
    *   Simplifies the deployment workflow by removing the need to maintain a `Dockerfile`.
    *   Leverages Google-managed base images and build steps, potentially improving security and build optimizations.
    *   Reduces boilerplate configuration in the repository.
*   **Neutral:**
    *   Relies on Buildpacks' conventions for detection and building. Explicit control via `Dockerfile` is relinquished.
    *   Requires a `Procfile` for explicit startup command definition (good practice).
*   **Negative:**
    *   Less control over fine-grained aspects of the container image build compared to using a `Dockerfile`, which might be a limitation for highly complex or non-standard setups (not applicable here).
