# 9. Use Firestore for Memory and State Management

## Status

Proposed (Gamma Phase)

## Context

Generative AI agents, especially conversational ones, need to maintain state or memory across interactions. Since the planned deployment platform (Cloud Run) is stateless, this state must be stored externally. We need a scalable and suitable external storage solution on GCP.

## Decision

We propose using Firestore as the primary external storage solution for agent memory and state.

## Consequences

*   **Benefits:**
    *   Serverless NoSQL database, scales automatically.
    *   Suitable for storing structured conversation history or agent state objects.
    *   Integrates well with other GCP services.
    *   Flexible data model.
*   **Drawbacks:**
    *   Requires integrating the Firestore client library.
    *   Adds a dependency on GCP.
    *   Requires configuring IAM permissions for services accessing Firestore.
    *   May have higher latency compared to in-memory stores like Memorystore for very frequent, low-latency state access.
*   **Impact on Plan:**
    *   This is planned for the Gamma phase.
    *   `utils/` module will include functions to interact with Firestore.
    *   ADK agents requiring state will use these `utils/` functions.
    *   CLI `setup gcp` command (Gamma) can optionally provision a Firestore database.
    *   Cloud Run deployment plan (Gamma) will include configuring access to Firestore.
    *   Documentation will cover Firestore setup and usage for state management.
    *   The plan can mention other options like Memorystore as alternatives depending on specific latency/cost requirements.
