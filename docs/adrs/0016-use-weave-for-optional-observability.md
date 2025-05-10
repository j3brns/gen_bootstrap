# 16. Use Weave for Optional Premium Observability and Experiment Tracking

## Status

Proposed (Gamma Phase)

## Context

Cloud Logging and Cloud Trace provide essential, standard observability for GCP applications. However, for users requiring more advanced visualization of LLM application runs, detailed experiment tracking, and richer analysis capabilities, a dedicated tool can be beneficial. We want to offer this enhanced functionality as an optional layer.

## Decision

We will offer optional integration with Weave (`weave-lang`) as a premium layer for enhanced logging, tracing visualization, and dedicated experiment tracking, complementing the standard Cloud Logging and Cloud Trace integration.

## Consequences

*   **Benefits:**
    *   Provides a rich UI for visualizing LLM application traces and logs, offering insights beyond standard log viewers.
    *   Excellent support for tracking and comparing experimental runs with detailed metadata and results.
    *   Can help analyze agent behavior and performance in detail, especially during development and evaluation.
    *   Complements Cloud Logging and Trace with a different, potentially more LLM-centric, perspective.
*   **Drawbacks:**
    *   Adds an optional external dependency (`weave-lang`).
    *   Requires users to set up and potentially manage a Weave server (local or remote), which may involve additional infrastructure or service costs ("premium").
    *   Adds some complexity to the logging and tracing implementation to support conditional Weave logging alongside standard GCP logging.
    *   Users need to understand when to use Weave versus Cloud Logging/Trace based on their needs.
*   **Impact on Plan:**
    *   This is planned for the Gamma phase.
    *   `weave-lang` will be listed as an optional dependency in `pyproject.toml`.
    *   The logging and tracing utilities in `utils/` will include conditional logic to log to Weave *in addition to* or *selectively instead of* standard GCP logging/tracing if Weave is configured and enabled. Cloud Logging and Trace remain the default.
    *   CLI commands (`cli run`, `cli evaluate`) can include options/flags to enable Weave logging for specific runs.
    *   The evaluation framework can be configured to log runs to Weave.
    *   Documentation will clearly explain that Cloud Logging and Trace are the standard observability tools and that Weave is an optional add-on for advanced use cases, detailing installation, configuration, and potential costs.
