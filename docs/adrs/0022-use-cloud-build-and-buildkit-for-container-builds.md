# 22. Use Cloud Build and BuildKit for Container Builds

## Status

Accepted

## Context

Deploying the application to Cloud Run requires building a container image. We need an efficient, reliable, and scalable method for building these images, ideally integrated with GCP and leveraging modern container build capabilities.

## Decision

We will use Google Cloud Build, which supports BuildKit, as the primary service for building container images for deployment to Cloud Run. The project's CLI will orchestrate builds via Cloud Build.

## Consequences

*   **Benefits:**
    *   **Managed Service:** Cloud Build is fully managed, eliminating the need to manage build infrastructure.
    *   **Scalability and Reliability:** Scales automatically and provides a reliable build environment.
    *   **BuildKit Advantages:** Leverages BuildKit for faster builds, improved caching, enhanced security, and support for modern Dockerfile features.
    *   **GCP Integration:** Seamless integration with Google Container Registry/Artifact Registry and Cloud Run.
    *   **CI/CD Friendly:** Easily integrates into automated CI/CD pipelines.
*   **Drawbacks:**
    *   Requires using Cloud Build, which incurs costs based on build time.
    *   Requires the user's GCP project to have the Cloud Build API enabled.
    *   Debugging builds can sometimes be slightly different than local Docker builds.
*   **Impact on Plan:**
    *   The `cli deploy` command will primarily use `gcloud builds submit` to trigger builds on Cloud Build.
    *   The `deployment/Dockerfile` will be designed to be compatible with BuildKit.
    *   Documentation will explain the build process using Cloud Build and mention the benefits of BuildKit.
    *   The plan for GCP Resource Provisioning (Gamma) can include enabling the Cloud Build API.
