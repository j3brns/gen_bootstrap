# Feature: Token Management

## Status

Planned (Alpha Phase - Basic, Gamma Phase - Advanced)

## Description

This feature provides utilities for counting tokens in text and truncating text to fit within a specified token limit, which is essential for interacting with generative AI models that have context window constraints.

## Goals

*   Accurately count tokens for supported generative models.
*   Provide basic text truncation capabilities.
*   (Gamma) Implement more sophisticated truncation strategies (e.g., summarization).
*   Enable ADK agents to manage context window usage effectively.

## Components

*   **`ttok`:** The primary tool used for token counting and basic truncation, accessed via the `subprocess` module.
*   **`utils/token_utils.py`:** Python module containing wrapper functions for executing the `ttok` command and potentially implementing more advanced truncation logic.
*   **ADK Agents (`adk/`):** Agent code will call `utils.token_utils` functions to check token counts and truncate input/history before making model calls.
*   **Configuration:** Potentially store model-specific context window sizes in `config/`.

## Implementation Details

*   Include `ttok` as a core dependency in `pyproject.toml` (installed from Git repository).
*   Implement functions in `utils/token_utils.py` to execute the `ttok` command via `subprocess` for counting and trimming.
*   Design agent logic to use these utilities to manage the context window.
*   (Gamma Phase) Research and implement more advanced truncation strategies (e.g., using a separate model for summarization) in `utils/token_utils.py`.
*   Document how to use the token management utilities in agent code and notebooks.

## Acceptance Criteria

*   Users can count tokens for a given text using the provided utilities.
*   Users can truncate text to a specified token limit using the basic truncation utility.
*   ADK agents can use the token management utilities to stay within model context window limits.
*   (Gamma) More sophisticated truncation strategies are available and documented.
*   Token counting and truncation logic handles different text inputs correctly.
