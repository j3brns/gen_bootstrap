# 2. Deploy on Cloud Run

## Status

Accepted

## Context

We need a scalable, serverless platform on GCP to host the generative AI ADK application. The platform should handle request serving, scaling, and provide integration with other GCP services.

## Decision

We will deploy the generative AI ADK application on Google Cloud Run.

## Consequences

*   **Benefits:**
    *   Serverless and fully managed.
    *   Automatic scaling based on request load.
    *   Pay-per-use pricing.
    *   Easy integration with other GCP services (Logging, Trace, Secret Manager, Vertex AI) via IAM permissions and environment variables.
    *   Supports containerized applications.
*   **Drawbacks:**
    *   Stateless nature requires external services for persistent state (addressed by Memory/State Management plan).
    *   Cold starts can occur with infrequent traffic (can be mitigated with min instances).
*   **Impact on Plan:**
    *   `deployment/Dockerfile` is required to containerize the application.
    *   CLI `deploy` command will use `gcloud run deploy`.
    *   Plan includes details on configuring environment variables and IAM permissions for Cloud Run service identity.
    *   Memory and State Management plan relies on external storage accessible from Cloud Run.
