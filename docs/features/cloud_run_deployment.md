# Feature: Cloud Run Deployment

## Status

Planned (Alpha Phase - Basic, Beta/Gamma Phases - Enhanced)

## Description

This feature provides an automated process via the CLI to containerize the ADK application and deploy it to Google Cloud Run.

## Goals

*   Simplify the process of deploying the application to a scalable production environment.
*   Automate Docker image building and pushing.
*   Automate Cloud Run service creation or update.
*   Provide a mechanism to configure the deployed application (environment variables, secrets).
*   Guide users on necessary IAM permissions.

## Components

*   **`deployment/Dockerfile`:** Defines how to build the container image.
*   **`cli/commands/deploy.py`:** Implements the `cli deploy` command logic.
*   **Google Cloud SDK (`gcloud`):** Used by the CLI to interact with Google Container Registry/Artifact Registry and Cloud Run.
*   **Docker:** Required in the user's environment (or rely on Cloud Build).
*   **Configuration:** Project and deployment settings in `config/`.
*   **Google Secret Manager:** Integrated for securely providing secrets to the deployed service via environment variables.
*   **IAM Permissions:** Required for the Cloud Run service identity.

## Implementation Details

*   The `cli deploy` command will orchestrate the steps: build image, tag image, push image, deploy to Cloud Run.
*   Use `subprocess` to execute `gcloud` or `docker` commands, or use `gcloud builds submit` for remote building.
*   The `Dockerfile` will install production dependencies using Poetry.
*   The `gcloud run deploy` command will be constructed with parameters for image, service name, region, and configuration (environment variables, memory, CPU, concurrency).
*   Environment variables will be used to pass configuration and secret references (`--set-env-vars`).
*   Documentation and CLI output will guide the user on setting up the required IAM permissions for the Cloud Run service account to access Secret Manager and other GCP services.
*   Consider adding optional pre-deployment test execution.

## Acceptance Criteria

*   Users can successfully build a Docker image for the application using the provided `Dockerfile`.
*   Users can successfully deploy the application to Cloud Run using the `cli deploy` command.
*   The deployed Cloud Run service runs the application correctly.
*   Configuration values and secrets are correctly passed to the deployed application via environment variables.
*   The `cli deploy` command provides clear output on the deployment process.
*   Documentation clearly explains the deployment process, configuration options, and IAM requirements.
*   (Beta/Gamma) Optional pre-deployment tests can be configured and executed by the `cli deploy` command.
