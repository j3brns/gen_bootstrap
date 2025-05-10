# 20. Use Evaluation Framework

## Status

Accepted (Gamma Phase)

## Context

Evaluating the performance and quality of generative AI agents is crucial for iterative improvement and ensuring they meet desired criteria. We need a structured approach to run agents against test datasets and measure relevant metrics.

## Decision

We will include a basic evaluation framework within the project scaffold, consisting of an `evaluation/` directory for scripts and data, and a CLI command (`cli evaluate`) to trigger evaluation runs.

## Consequences

*   **Benefits:**
    *   Provides a dedicated place and process for evaluating agent performance.
    *   Enables running agents against consistent test datasets.
    *   Facilitates measuring and comparing metrics across different agent versions, models, or configurations.
    *   Supports offline A/B testing of prompts or models.
*   **Drawbacks:**
    *   Requires defining evaluation datasets and metrics.
    *   Implementing evaluation scripts can be time-consuming depending on complexity.
    *   Analyzing results requires dedicated effort.
*   **Impact on Plan:**
    *   An `evaluation/` directory will be added to the project structure (Gamma Phase).
    *   A `cli evaluate` command will be implemented (Gamma Phase).
    *   The `evaluation/` directory will contain subdirectories for configs, datasets, scripts, and results.
    *   The evaluation process will leverage logging (and optionally Weave) to record run details and results.
    *   Documentation will cover how to set up and run evaluations.
