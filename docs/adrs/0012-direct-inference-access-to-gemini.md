# 12. Direct Inference Access to Gemini Models

## Status

Accepted

## Context

The core function of the generative AI ADK application is to interact with Gemini models for inference. We need an efficient and direct method to access these models to minimize latency and ensure access to the latest model features without intermediaries.

## Decision

We will access Gemini models directly for inference using the Google Cloud SDK (`google-cloud-aiplatform` library) within the application code, rather than relying on an intermediate gateway or service layer that is not part of the core GCP offering.

## Consequences

*   **Benefits:**
    *   **No Gateway Overhead:** Direct API calls reduce latency compared to routing through an additional service layer.
    *   **No Feature Lag:** Access to the latest model features and parameters as soon as they are available in the SDK/API.
    *   **Client-Side Token Management:** Token counting and truncation logic can be implemented directly in the application (`utils/`) using tools like `token_count_trim`, giving fine-grained control.
    *   **Avoids Propagating REST Flaws:** The application interacts directly with the model API, avoiding potential limitations or design choices of an intermediate REST gateway if one were introduced.
    *   **No Provisioning Overhead:** No need to deploy and manage an additional intermediate service just for model access.
*   **Drawbacks:**
    *   The application code has a direct dependency on the Google Cloud SDK for model interaction.
    *   Managing different model versions or endpoints might require explicit handling in the application code or configuration.
*   **Impact on Plan:**
    *   The `utils/` module will contain wrapper functions that directly use the `google-cloud-aiplatform` library to call Gemini models.
    *   The Token Management plan (using `token_count_trim`) is reinforced, as truncation will happen client-side before the direct API call.
    *   ADK agents will interact with models via these direct `utils/` wrappers.
    *   The deployment plan needs to ensure the Cloud Run service identity has IAM permissions to invoke Gemini models.
