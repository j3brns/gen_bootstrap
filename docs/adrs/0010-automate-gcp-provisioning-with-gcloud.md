# 10. Automate GCP Resource Provisioning using `gcloud`

## Status

Proposed (Gamma Phase)

## Context

Setting up the necessary GCP resources (Cloud Run service, Secret Manager secrets, Firestore database, IAM permissions) manually can be time-consuming and error-prone. Automating this process will streamline project setup.

## Decision

We will automate the provisioning of essential GCP resources using `gcloud` commands executed from the project's CLI.

## Consequences

*   **Benefits:**
    *   Simplifies and accelerates the initial project setup on GCP.
    *   Reduces the potential for manual configuration errors.
    *   Leverages the user's existing `gcloud` CLI installation and authentication.
    *   Relatively straightforward to implement within the Python CLI using subprocess calls.
*   **Drawbacks:**
    *   Requires the user to have the `gcloud` CLI installed and authenticated.
    *   Less declarative than Infrastructure as Code tools (like Terraform or Pulumi).
    *   Error handling for subprocess calls needs careful implementation.
*   **Impact on Plan:**
    *   This is planned for the Gamma phase.
    *   A new CLI command (`cli setup gcp`) will be implemented.
    *   The CLI code will use Python's `subprocess` module to execute `gcloud` commands.
    *   The command will be interactive, prompting the user for necessary information and confirming actions.
    *   Documentation will cover the prerequisites (`gcloud` installation) and usage of the provisioning command.
    *   The plan includes documenting the IAM permissions required for the user running the command and for the provisioned resources (e.g., Cloud Run service account).
