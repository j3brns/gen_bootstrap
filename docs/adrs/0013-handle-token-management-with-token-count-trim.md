# 13. Handle Token Management with `token_count_trim`

## Status

Accepted

## Context

Generative AI models have context window limits, and exceeding these limits results in errors. Efficiently managing the number of tokens in prompts and conversation history is necessary for both technical feasibility and cost optimization. We need a reliable way to count tokens and truncate text when necessary.

## Decision

We will use the `ttok` command-line tool, accessed via the `subprocess` module, to handle token counting and text truncation, primarily for pre-processing inputs to ADK agents or within custom tools.

## Consequences

*   **Benefits:**
*   Provides a dedicated tool for token handling.
    *   Offers functions for both counting tokens and trimming text based on a target token limit.
    *   Leverages an existing, maintained tool rather than building custom logic from scratch.
*   **Drawbacks:**
    *   Requires executing an external command via `subprocess`, which can be less efficient than a native Python library.
    *   Accuracy may vary slightly depending on the specific model and the tool's implementation for that model.
*   **Impact on Plan:**
    *   `ttok` will be included as a core dependency in `pyproject.toml` (installed from Git repository).
    *   The `utils/` module will contain wrapper functions that execute the `ttok` command via `subprocess` for token counting and truncation.
    *   ADK agents and potentially tools will call these `utils/` functions, primarily for managing the size of *inputs* to the agent or data processed by tools, rather than directly manipulating the agent's internal conversation history (which is managed by ADK).
    *   The plan for direct inference access reinforces the need for client-side token management handled by this tool for pre-processing data.
