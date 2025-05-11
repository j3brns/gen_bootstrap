# 3. Use Vertex AI Prompt Classes

## Status

Accepted

## Context

Managing prompt templates for generative AI models can become complex, especially with variations, versioning, and collaboration. We need a centralized, managed approach to store and retrieve prompts.

## Decision

We will use Vertex AI Prompt Classes as the primary mechanism for managing prompt templates.

## Consequences

*   **Benefits:**
    *   Centralized and managed prompt repository on GCP.
    *   Supports prompt versioning.
    *   Facilitates collaboration on prompt engineering.
    *   Integrates with Vertex AI models.
    *   Leverages ADK's `LlmAgent` by providing a flexible way to define the agent's instructions.
*   **Drawbacks:**
    *   Requires using the Vertex AI API for prompt management.
    *   Adds a dependency on Vertex AI for prompt storage.
*   **Impact on Plan:**
    *   `utils/` module will include wrappers for the Vertex AI Prompt Classes API.
    *   CLI will include commands (`cli prompts`) for managing Prompt Classes (create, list, get, update).
    *   ADK agents will fetch prompts dynamically from Vertex AI using the `utils/` wrappers. The `LlmAgent`'s `instruction` parameter will be a callable function from `utils/prompt_manager.py` that retrieves the prompt from Vertex AI Prompt Classes at runtime.
    *   Plan includes using Prompt Class versions for A/B testing.
