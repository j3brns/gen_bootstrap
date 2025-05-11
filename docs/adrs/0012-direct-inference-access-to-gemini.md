# 12. Direct Inference Access to Gemini Models

## Status

Accepted

## Context

The core function of the generative AI ADK application is to interact with Gemini models for inference. We need an efficient and direct method to access these models to minimize latency and ensure access to the latest model features without intermediaries.

## Decision

We will access Gemini models directly for inference using the Google Cloud SDK (`google-cloud-aiplatform` library) within the application code, leveraging the ADK's `LlmAgent` for model interaction.

## Consequences

*   **Benefits:**
    *   **No Gateway Overhead:** Direct API calls reduce latency compared to routing through an additional service layer.
    *   **No Feature Lag:** Access to the latest model features and parameters as soon as they are available in the SDK/API.
    *   **Client-Side Token Management:** Token counting and truncation logic can be implemented directly in the application (`utils/`) using tools like `token_count_trim`, giving fine-grained control.
    *   **Avoids Propagating REST Flaws:** The application interacts directly with the model API, avoiding potential limitations or design choices of an intermediate REST gateway if one were introduced.
    *   **No Provisioning Overhead:** No need to deploy and manage an additional intermediate service just for model access.
*   **Drawbacks:**
    *   The application code has a direct dependency on the Google Cloud SDK for model interaction, which is managed by the ADK's `LlmAgent`.
    *   Managing different model versions or endpoints might require explicit handling in the application code or configuration, which can be configured via the `LlmAgent`.
*   **Impact on Plan:**
    *   The `utils/` module may contain wrapper functions that *support* the `LlmAgent` by providing model configuration or selection, but the `LlmAgent` itself is the primary interface for model interaction.
    *   The Token Management plan (using `token_count_trim`) is reinforced, as truncation can happen client-side before the direct API call.
    *   ADK agents will interact with models via the `LlmAgent`, which handles the underlying SDK calls.
    *   The deployment plan needs to ensure the Cloud Run service identity has IAM permissions to invoke Gemini models.
