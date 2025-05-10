# 19. Group Features into Alpha, Beta, and Gamma Phases

## Status

Accepted

## Context

The project to build the GCP Generative AI ADK Scaffold and CLI involves a significant number of features and integrations. Attempting to deliver all features at once could increase complexity, extend the initial delivery timeline, and delay getting a usable version into users' hands. We need a strategy to manage development, deliver value incrementally, and gather feedback.

## Decision

We will group the project's features and deliverables into three distinct phases: Alpha, Beta, and Gamma. Each phase will have a defined set of goals and deliverables, building upon the previous phase.

## Consequences

*   **Benefits:**
    *   Provides a clear roadmap for development.
    *   Allows for incremental delivery of value, enabling users to benefit from core features sooner (Alpha).
    *   Helps manage complexity by focusing on a subset of features in each phase.
    *   Facilitates gathering feedback on core functionality before developing advanced features.
    *   Clearer scope for each development iteration.
*   **Drawbacks:**
    *   Users may have to wait for later phases to access certain advanced features.
    *   Dependencies between features across phases need careful management.
*   **Impact on Plan:**
    *   The detailed plan is structured around these three phases, outlining the specific features and deliverables for each.
    *   Development efforts will be prioritized according to the features assigned to the current phase.
    *   Documentation will reflect the phased availability of features.
    *   The ADRs for specific features (e.g., Memory/State Management, Monitoring/Alerting, GCP Provisioning, Weave) reference the Gamma phase as their target.
