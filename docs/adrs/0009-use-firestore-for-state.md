# 9. Use Firestore for Memory and State Management

## Status

Proposed (Gamma Phase - Requires careful alignment with ADK's state management)

## Context

Generative AI agents, especially conversational ones, need to maintain state or memory across interactions. Since the planned deployment platform (Cloud Run) is stateless, this state must be stored externally. We need a scalable and suitable external storage solution on GCP.

## Decision

We propose exploring the use of Firestore as a potential backend for ADK's `SessionService` and `MemoryService` to provide persistent storage for agent state and memory. This will involve creating custom implementations of these ADK services that leverage Firestore for data persistence.

## Consequences

*   **Benefits:**
    *   Serverless NoSQL database, scales automatically.
    *   Suitable for storing structured conversation history or agent state objects.
    *   Integrates well with other GCP services.
    *   Flexible data model.
    *   Leverages ADK's built-in abstractions for session and memory management.
*   **Drawbacks:**
    *   Requires integrating the Firestore client library within custom ADK service implementations.
    *   Adds a dependency on GCP.
    *   Requires configuring IAM permissions for services accessing Firestore.
    *   May have higher latency compared to in-memory stores like Memorystore for very frequent, low-latency state access.
*   **Impact on Plan:**
    *   This is planned for the Gamma phase.
    *   `utils/` module may include helper functions to facilitate Firestore interaction *within the custom ADK service implementations*.
    *   ADK agents requiring state will use the custom Firestore-backed `SessionService` and `MemoryService`.
    *   CLI `setup gcp` command (Gamma) can optionally provision a Firestore database.
    *   Cloud Run deployment plan (Gamma) will include configuring access to Firestore for the custom ADK services.
    *   Documentation will cover Firestore setup and usage for state management, emphasizing the use of ADK's `SessionService` and `MemoryService` interfaces.
    *   The plan can mention other options like Memorystore as alternatives depending on specific latency/cost requirements, and how they could be implemented as other custom ADK service implementations.
