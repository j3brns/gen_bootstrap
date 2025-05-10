# Feature: Optional Weave Integration

## Status

Planned (Gamma Phase)

## Description

This feature provides optional integration with Weave (`weave-lang`) for enhanced logging, tracing visualization, and dedicated experiment tracking, complementing the standard Cloud Logging and Cloud Trace integration.

## Goals

*   Offer advanced visualization of LLM application traces and logs.
*   Provide dedicated support for tracking and comparing experimental runs.
*   Enable detailed analysis of agent behavior and performance during development and evaluation.
*   Maintain Cloud Logging and Cloud Trace as the default observability tools.

## Components

*   **Weave (`weave-lang`):** The optional external library for observability and experiment tracking.
*   **`utils/logging_utils.py` / `utils/tracing_utils.py`:** Modified to include conditional logic for logging/tracing to Weave if enabled.
*   **ADK Agents and Tools (`adk/`, `tools/`):** Code will use the updated logging/tracing utilities.
*   **CLI Commands (`cli run`, `cli evaluate`):** Include options/flags to enable Weave logging for specific runs.
*   **Evaluation Framework:** Can be configured to log evaluation runs to Weave.
*   **Documentation:** Explains how to install, configure, and use Weave, highlighting its optional and premium nature compared to standard GCP tools.

## Implementation Details

*   List `weave-lang` as an optional dependency in `pyproject.toml`.
*   Implement conditional logic in logging and tracing utilities to send data to Weave based on configuration (e.g., environment variable).
*   Add options to relevant CLI commands to enable Weave logging.
*   Provide guidance on setting up a Weave server (local or remote).
*   Document the benefits and potential costs of using Weave.

## Acceptance Criteria

*   Users can optionally install `weave-lang`.
*   When Weave is installed and configured, application logs and traces are sent to Weave in addition to (or selectively instead of) Cloud Logging/Trace.
*   Users can view and analyze application runs and experiments in the Weave UI.
*   CLI commands can successfully enable/disable Weave logging for runs.
*   Evaluation runs can be logged and visualized in Weave.
*   Documentation clearly explains the optional nature and usage of Weave.
