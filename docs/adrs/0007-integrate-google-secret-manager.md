# 7. Integrate Google Secret Manager for Secrets

## Status

Accepted

## Context

Generative AI applications and their tools often require access to sensitive credentials like API keys for external services. Storing these secrets securely is paramount, especially in a cloud environment.

## Decision

We will use Google Secret Manager as the secure storage solution for application secrets.

## Consequences

*   **Benefits:**
    *   Centralized and managed secret storage on GCP.
    *   Secrets are encrypted at rest and in transit.
    *   Access control via IAM permissions.
    *   Supports secret versioning.
    *   Avoids hardcoding secrets in code or configuration.
*   **Drawbacks:**
    *   Requires integrating the Google Secret Manager client library.
    *   Adds a dependency on GCP for secret storage.
    *   Requires configuring IAM permissions for services accessing secrets.
*   **Impact on Plan:**
    *   `utils/` module will include functions to retrieve secrets from Secret Manager.
    *   CLI will include commands (`cli secrets`) for managing secrets.
    *   ADK agents and tools will retrieve necessary secrets via the `utils/` functions.
    *   Cloud Run deployment plan includes configuring environment variables to reference secrets and documenting required IAM permissions.
