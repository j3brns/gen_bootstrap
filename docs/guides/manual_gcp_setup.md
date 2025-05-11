# Manual GCP Resource Setup Guide

This guide outlines the essential Google Cloud Platform (GCP) resources and configurations required to run and deploy the "gen-bootstrap" Generative AI ADK Scaffold. For the Alpha and early Beta phases of this project, these steps should be performed manually.

The `poetry run gen-bootstrap setup-gcp` command in the CLI will also direct you to this guide.

## Prerequisites

1.  **Google Cloud Account & Project:**
    * Ensure you have an active Google Cloud account.
    * Create a new GCP Project or select an existing one. Note your **Project ID**.
    * Ensure billing is enabled for your project.

2.  **`gcloud` CLI:**
    * Install the Google Cloud SDK (which includes `gcloud`): [Install gcloud CLI](https://cloud.google.com/sdk/docs/install)
    * Authenticate the `gcloud` CLI:
        ```bash
        gcloud auth login
        gcloud auth application-default login # Important for application default credentials
        ```
    * Set your default project:
        ```bash
        gcloud config set project YOUR_PROJECT_ID
        ```
        (Replace `YOUR_PROJECT_ID` with your actual Project ID)

3.  **Poetry and Project Dependencies:**
    * Ensure Poetry is installed.
    * Run `poetry add google-adk` and `poetry install` in the project root.

## Essential GCP Services & APIs

Enable the following APIs for your GCP project via the GCP Console (APIs & Services > Library) or `gcloud`:

```bash
gcloud services enable \
    run.googleapis.com \
    iam.googleapis.com \
    secretmanager.googleapis.com \
    aiplatform.googleapis.com \
    logging.googleapis.com \
    monitoring.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com # Recommended for storing container images
```
* **Cloud Run API (`run.googleapis.com`):** For deploying the application.
* **IAM API (`iam.googleapis.com`):** For managing permissions.
* **Secret Manager API (`secretmanager.googleapis.com`):** For storing API keys, etc.
* **Vertex AI API (`aiplatform.googleapis.com`):** For `google-adk` to access generative models.
* **Cloud Logging & Monitoring APIs:** For observability.
* **Cloud Build API & Artifact Registry API:** For building and storing container images for Cloud Run.

## Secret Manager Setup (Optional, if your agent needs secrets)

If your agent or its tools require API keys or other sensitive credentials:

1.  **Create a secret:**
    ```bash
    gcloud secrets create your-secret-name \
        --replication-policy="automatic" \
        --project="YOUR_PROJECT_ID"
    ```
2.  **Add a version with the secret value:**
    ```bash
    printf "your_actual_secret_value" | gcloud secrets versions add your-secret-name \
        --data-file=- \
        --project="YOUR_PROJECT_ID"
    ```
    Update `your-secret-name` and `your_actual_secret_value`.

## IAM Permissions for Cloud Run Service Identity

Your Cloud Run service runs with a service identity. This identity needs permissions to access other GCP services (like Vertex AI, Secret Manager).

1.  **Identify your Cloud Run service account:**
    * If using the default Compute Engine service account: `PROJECT_NUMBER-compute@developer.gserviceaccount.com`. Get `PROJECT_NUMBER` via `gcloud projects describe YOUR_PROJECT_ID --format="value(projectNumber)"`.
    * If you specify a custom service account during `gcloud run deploy`, use that.

2.  **Grant necessary roles to the service account (replace `SERVICE_ACCOUNT_EMAIL`):**
    * **Vertex AI User (essential for ADK agent to use models):**
        ```bash
        gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
            --member="serviceAccount:SERVICE_ACCOUNT_EMAIL" \
            --role="roles/aiplatform.user"
        ```
    * **Secret Manager Secret Accessor (if using secrets):**
        ```bash
        gcloud secrets add-iam-policy-binding your-secret-name \
            --member="serviceAccount:SERVICE_ACCOUNT_EMAIL" \
            --role="roles/secretmanager.secretAccessor" \
            --project="YOUR_PROJECT_ID"
        ```
    * **Cloud Logging Writer & Monitoring Metric Writer:** Usually granted by default to the Compute Engine service account. Verify if using a custom service account.

## Next Steps

* Update your project's `.env` file with your `GCP_PROJECT_ID` and any other configurations.
* You should now be able to use `poetry run gen-bootstrap deploy` to deploy.

This guide covers essential manual setup. Always refer to the latest project and `google-adk` documentation.
