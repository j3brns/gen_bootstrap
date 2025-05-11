# Feature: Evaluation Framework

## Status

Planned (Gamma Phase)

## Description

This feature provides a structured framework for evaluating the performance and quality of generative AI agents against predefined datasets and metrics, leveraging the Google Agent Development Kit's (ADK) built-in evaluation capabilities.

## Goals

*   Enable systematic evaluation of agent performance using ADK's evaluation tools.
*   Support running agents against consistent test datasets (in ADK's `.test.json` or `.evalset.json` format).
*   Facilitate measuring and comparing metrics across different agent versions, models, or configurations using ADK's evaluation criteria.
*   Provide a CLI command to trigger evaluation runs using ADK's evaluation methods.
*   Integrate with logging and optional Weave for recording and visualizing evaluation results.

## Components

*   **ADK Evaluation Framework:** Leverages ADK's `AgentEvaluator`, dataset formats (`.test.json`, `.evalset.json`), and evaluation methods.
*   **`evaluation/` Directory:** Houses project-specific evaluation datasets (in ADK's format) and configurations.
*   **`evaluation/configs/`:** Stores configuration files for evaluation runs (e.g., `test_config.json` to override default evaluation criteria).
*   **`evaluation/datasets/`:** Stores test datasets in ADK's `.test.json` or `.evalset.json` format.
*   **`evaluation/scripts/`:** (Optional) Contains Python scripts that *use* ADK's `AgentEvaluator` for programmatic evaluation within `pytest` or other testing harnesses.
*   **`evaluation/results/`:** (Often excluded from version control) Stores evaluation output and reports.
*   **`cli/commands/evaluate.py`:** Implements the `cli evaluate` command, which either wraps ADK's `adk eval` CLI or integrates with `pytest` using ADK's evaluation capabilities.
*   **ADK Agents (`adk/`):** The agents being evaluated.
*   **Logging and Tracing:** Used to record details of evaluation runs.
*   **Optional Weave Integration:** For enhanced visualization and tracking of evaluation results.

## Implementation Details

*   Use ADK's dataset formats (`.test.json`, `.evalset.json`) for defining evaluation datasets.
*   Implement the `cli evaluate` command to either:
    *   Wrap ADK's `adk eval <AGENT_MODULE> <EVAL_SET_FILE(S)>` command, passing appropriate project-specific paths.
    *   Integrate with `pytest` and use ADK's `AgentEvaluator.evaluate()` for programmatic evaluation.
*   Develop example evaluation scripts (if needed) that load datasets, run agents using ADK's framework, and calculate metrics.
*   Ensure evaluation scripts use the logging utilities (and optionally Weave) to record run details, inputs, outputs, and metrics.
*   Document how to set up evaluation configurations, create datasets, write evaluation scripts (if needed), and run evaluations using the CLI, highlighting the use of ADK's evaluation features.
*   Document how to interpret evaluation results in logs, Cloud Monitoring (if metrics are emitted), and optionally Weave.

## Acceptance Criteria

*   Users can define an evaluation run using ADK's dataset formats and a configuration file (if needed to override defaults).
*   Users can trigger an evaluation run using the `cli evaluate` command, leveraging ADK's evaluation methods.
*   The evaluation process successfully runs the specified agent against the dataset using ADK's framework.
*   Relevant metrics are calculated and logged for each evaluation run.
*   Evaluation results are saved to the `evaluation/results/` directory (or configured location).
*   Evaluation runs and their results are visible in Cloud Logging (and optionally Weave).
*   Documentation clearly explains how to use the evaluation framework, emphasizing ADK's built-in features and how to extend them.
