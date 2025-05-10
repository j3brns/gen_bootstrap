# 17. Use Cloud Monitoring and Alerting

## Status

Proposed (Gamma Phase)

## Context

Operating generative AI applications in production requires proactive monitoring of their health, performance, and resource utilization. We need a system to visualize key metrics and receive notifications when predefined thresholds are breached.

## Decision

We propose using Google Cloud Monitoring for collecting and visualizing metrics and Google Cloud Alerting for defining alerting policies and notification channels.

## Consequences

*   **Benefits:**
    *   Provides dashboards to visualize key application and infrastructure metrics (from Cloud Run, log-based metrics).
    *   Enables setting up alerts based on metrics (e.g., error rate, latency, resource utilization).
    *   Integrates with various notification channels (email, Slack, PagerDuty, etc.).
    *   Leverages managed GCP services, reducing operational overhead.
    *   Complements Cloud Logging and Trace for comprehensive observability.
*   **Drawbacks:**
    *   Requires understanding Cloud Monitoring and Alerting concepts.
    *   Configuration can become complex for advanced scenarios.
    *   May incur costs depending on the volume of metrics and alerts.
*   **Impact on Plan:**
    *   This is planned for the Gamma phase.
    *   The plan includes leveraging built-in Cloud Run metrics and creating custom log-based metrics from Cloud Logging data.
    *   A new CLI command (`cli monitoring setup`) will be implemented to automate the creation of basic dashboards and alerting policies using `gcloud` or the Cloud Monitoring API.
    *   CLI commands to open monitoring dashboards and alerts pages will be included.
    *   Documentation will cover how to use the monitoring features and interpret metrics and alerts.
    *   Cloud Run service identity requires IAM permissions for Cloud Monitoring.
