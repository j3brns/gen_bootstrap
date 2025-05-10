# Troubleshooting Guide

This guide provides solutions to common issues you might encounter while using the GCP Generative AI ADK Scaffold and CLI.

## General Issues

**Issue:** `command not found: cli`

*   **Cause:** The project's CLI entry point is not accessible in your environment's PATH, or you are not running the command within the Poetry virtual environment.
*   **Solution:** Ensure you have activated the Poetry virtual environment (`poetry shell`) before running CLI commands. Alternatively, you can run commands using `poetry run cli <command>`.

**Issue:** Dependency installation fails with Poetry.

*   **Cause:** Network issues, incompatible package versions, or issues with the Poetry configuration.
*   **Solution:**
    *   Check your internet connection.
    *   Ensure you have the correct Python version installed as specified in `pyproject.toml`.
    *   Try clearing Poetry's cache (`poetry cache clear --all`).
    *   If a specific package is causing issues, try updating it individually (`poetry add <package>@latest`) or check its documentation for compatibility requirements.
    *   Ensure `poetry.lock` is not corrupted (though Poetry usually handles this).

**Issue:** Pre-commit hooks are not running.

*   **Cause:** Pre-commit hooks were not installed in your Git repository.
*   **Solution:** Run `pre-commit install` in the project's root directory to set up the git hooks.

## GCP-Related Issues

**Issue:** `gcloud` command not found or authentication errors.

*   **Cause:** The Google Cloud SDK is not installed, not in your PATH, or you are not authenticated.
*   **Solution:**
    *   Install the Google Cloud SDK: [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)
    *   Ensure the `gcloud` command is in your system's PATH.
    *   Authenticate with GCP: `gcloud auth login`
    *   Set your active project: `gcloud config set project YOUR_PROJECT_ID`

**Issue:** Permission denied when the application (e.g., on Cloud Run) tries to access GCP services (Secret Manager, Vertex AI, Firestore).

*   **Cause:** The service account used by your Cloud Run revision does not have the necessary IAM permissions to access the required GCP resources.
*   **Solution:**
    *   Identify the service account used by your Cloud Run service (usually `PROJECT_NUMBER-compute@developer.gserviceaccount.com` unless you specified a custom one).
    *   Go to the IAM section in the GCP console.
    *   Find the service account and grant it the necessary roles (e.g., `roles/secretmanager.secretAccessor`, `roles/aiplatform.user`, `roles/datastore.user` for Firestore).
    *   Refer to the documentation for specific IAM role requirements for each service.

**Issue:** Cloud Run deployment fails.

*   **Cause:** Issues with the Dockerfile, container build errors, insufficient permissions, or Cloud Run configuration problems.
*   **Solution:**
    *   Check the build logs in Cloud Build (if using `gcloud builds submit`) or your local Docker build output for errors.
    *   Ensure the `Dockerfile` correctly copies all necessary files and installs dependencies.
    *   Verify that the entrypoint command in the Dockerfile is correct.
    *   Check the Cloud Run deployment logs in the GCP console for specific error messages.
    *   Ensure the user account performing the deployment has sufficient permissions to build images, push to the container registry, and deploy to Cloud Run.

**Issue:** Application logs are not appearing in Cloud Logging.

*   **Cause:** Application is not writing logs to standard output/error, or the Cloud Run service identity lacks logging permissions.
*   **Solution:**
    *   Ensure your application code is using the provided logging utilities (`utils/logging_utils.py`) which are configured to write to standard output/error.
    *   Verify the Cloud Run service account has the `roles/logging.logWriter` IAM role.

## Generative AI Specific Issues

**Issue:** Model requests fail due to token limits.

*   **Cause:** The input prompt or conversation history exceeds the model's context window.
*   **Solution:**
    *   Implement or verify the use of the token management utilities (`utils/token_utils.py`) to count tokens and truncate input/history before sending requests to the model.
    *   Review the model's documentation for its specific context window size.

**Issue:** Model responses are unexpected or low quality.

*   **Cause:** Issues with the prompt design, model parameters, or insufficient context.
*   **Solution:**
    *   Refine your prompt templates, potentially using Vertex AI Prompt Classes and their versioning to experiment.
    *   Adjust model parameters (temperature, top-k, top-p).
    *   Ensure sufficient and relevant conversation history or context is provided to the model (consider Memory/State Management if applicable).
    *   Use the evaluation framework and optional Weave integration to analyze model behavior with different prompts and parameters.

**Issue:** Tool calls from the model are incorrect or fail.

*   **Cause:** Issues with the tool description provided to the model, errors in the tool's implementation, or incorrect parsing of the model's tool call request.
*   **Solution:**
    *   Review and refine the description and schema provided for the tool to the generative model.
    *   Debug the tool's implementation in the `tools/` directory.
    *   Verify the agent's logic for parsing the model's response and executing the tool.
    *   Check logs and traces for details on the tool call and any errors.

This troubleshooting guide covers common areas and provides initial steps for diagnosing and resolving issues.
