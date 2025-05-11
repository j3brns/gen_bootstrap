# Feature: Cloud Run Deployment

## Status

Planned (Alpha Phase - Basic, Beta/Gamma Phases - Enhanced)

## Description

This feature provides an automated process via the CLI to containerize the ADK application and deploy it to Google Cloud Run, leveraging BuildKit for enhanced build capabilities.

## Goals

*   Simplify the process of deploying the application to a scalable production environment.
*   Automate Docker image building and pushing using Cloud Build with BuildKit.
*   Automate Cloud Run service creation or update.
*   Provide a mechanism to configure the deployed application (environment variables, secrets).
*   Guide users on necessary IAM permissions.

## Components

*   **`deployment/Dockerfile`:** Defines how to build the container image.
*   **`deployment/cloudbuild.yaml`:** Configures Cloud Build to use BuildKit.
*   **`cli/commands/deploy.py`:** Implements the `cli deploy` command logic.
*   **Google Cloud SDK (`gcloud`):** Used by the CLI to interact with Google Container Registry/Artifact Registry and Cloud Run.
*   **Cloud Build:** Used for building the container image with BuildKit.
*   **Container Registry/Artifact Registry:** Stores the built Docker images.
*   **Configuration:** Project and deployment settings in `config/`.
*   **Google Secret Manager:** Integrated for securely providing secrets to the deployed service via environment variables.
*   **IAM Permissions:** Required for the Cloud Run service identity and Cloud Build service account.

## Implementation Details

*   The `cli deploy` command will orchestrate the steps: build image using Cloud Build with BuildKit, tag image, push image, deploy to Cloud Run.
*   Use `gcloud builds submit --config deployment/cloudbuild.yaml --tag <image_name>` for remote building using Cloud Build with BuildKit enabled.
*   The `deployment/cloudbuild.yaml` file will configure the build environment to use BuildKit, enabling features like improved caching and parallel builds.
*   The `Dockerfile` will install production dependencies using Poetry.
*   The `gcloud run deploy` command will be constructed with parameters for image, service name, region, and configuration (environment variables, memory, CPU, concurrency).
*   Environment variables will be used to pass configuration and secret references (`--set-env-vars`).
*   Documentation and CLI output will guide the user on setting up the required IAM permissions for the Cloud Run service account to access Secret Manager and other GCP services, and for the Cloud Build service account to push images.
*   Consider adding optional pre-deployment test execution.

## Acceptance Criteria

*   Users can successfully build a Docker image for the application using Cloud Build with BuildKit, configured by `deployment/cloudbuild.yaml`.
*   Users can successfully deploy the application to Cloud Run using the `cli deploy` command.
*   The deployed Cloud Run service runs the application correctly.
*   Configuration values and secrets are correctly passed to the deployed application via environment variables.
*   The `cli deploy` command provides clear output on the deployment process.
*   Documentation clearly explains the deployment process, configuration options, and IAM requirements, including BuildKit configuration.
*   (Beta/Gamma) Optional pre-deployment tests can be configured and executed by the `cli deploy` command.
