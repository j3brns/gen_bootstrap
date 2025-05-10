# Feature: Secret Management

## Status

Planned (Beta Phase)

## Description

This feature provides a secure way to store and retrieve sensitive information, such as API keys and credentials, using Google Secret Manager.

## Goals

*   Prevent hardcoding secrets in code or configuration files.
*   Provide a standardized and secure method for agents and tools to access secrets.
*   Enable management of secrets via the CLI.
*   Ensure deployed applications can securely access necessary secrets.

## Components

*   **Google Secret Manager:** The GCP service used to store secrets.
*   **`utils/secret_manager.py`:** Python module containing functions to interact with the Google Secret Manager API (get secret versions).
*   **`cli/commands/secrets.py`:** CLI commands (`cli secrets create`, `add-version`, `list`, `get`) to manage secrets.
*   **ADK Agents and Tools (`adk/`, `tools/`):** Code will call `utils.secret_manager` functions to retrieve secrets at runtime.
*   **Cloud Run Deployment:** Configuration to pass secret references as environment variables to the deployed service.
*   **IAM Permissions:** Configuration to grant the Cloud Run service identity permission to access secrets.

## Implementation Details

*   Use the `google-cloud-secret-manager` Python client library.
*   Implement functions in `utils/secret_manager.py` to retrieve specific secret versions.
*   Develop corresponding commands in the CLI using Typer/Click.
*   Document how to create secrets in Secret Manager and add versions using the CLI.
*   Document how to configure Cloud Run environment variables to reference secrets.
*   Document the necessary IAM roles for the Cloud Run service identity.

## Acceptance Criteria

*   Users can create a new secret in Secret Manager using the CLI.
*   Users can add a new version to an existing secret from a file using the CLI.
*   Users can list secrets using the CLI.
*   Users can retrieve the content of a specific secret version using the CLI.
*   An ADK agent or tool can successfully retrieve a secret value at runtime using the `utils` functions.
*   Secret retrieval logic handles potential errors (e.g., secret not found, permission denied).
*   Documentation clearly explains the secure workflow for managing and accessing secrets.
