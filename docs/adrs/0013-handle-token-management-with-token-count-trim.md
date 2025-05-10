# 13. Handle Token Management with `token_count_trim`

## Status

Accepted

## Context

Generative AI models have context window limits, and exceeding these limits results in errors. Efficiently managing the number of tokens in prompts and conversation history is necessary for both technical feasibility and cost optimization. We need a reliable way to count tokens and truncate text when necessary.

## Decision

We will use the `token_count_trim` Python package to handle token counting and text truncation.

## Consequences

*   **Benefits:**
    *   Provides a dedicated and potentially model-agnostic library for token handling.
    *   Offers functions for both counting tokens and trimming text based on a target token limit.
    *   Leverages an existing, maintained library rather than building custom logic from scratch.
*   **Drawbacks:**
    *   Adds an external dependency to the project.
    *   Accuracy may vary slightly depending on the specific model and the package's implementation for that model.
*   **Impact on Plan:**
    *   `token_count_trim` will be included as a core dependency in `pyproject.toml`.
    *   The `utils/` module will contain wrapper functions that utilize `token_count_trim` for token counting and truncation.
    *   ADK agents and potentially tools will call these `utils/` functions before sending requests to generative models.
    *   The plan for direct inference access reinforces the need for client-side token management handled by this package.
