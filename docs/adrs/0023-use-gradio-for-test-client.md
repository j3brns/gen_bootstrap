# 0023 - Use Gradio for Test Client

## Status

Accepted

## Context

We need a simple way to test the core functionality of the ADK agent without integrating it into a larger application or CLI. A web-based test client would allow for easy interaction and demonstration.

## Decision

We will use Gradio to create a low-fidelity GUI for testing and Proof of Concept (PoC) purposes.

## Consequences

*   **Pros:**
    *   Rapid development of a simple interactive interface.
    *   Easy to use and integrate with existing Python functions.
    *   Good for quick demos and testing.

*   **Cons:**
    *   Limited customization options compared to full web frameworks.
    *   Primarily designed for demos, not complex applications.
    *   Less control over underlying web server behavior.

This decision is specifically for a simple test client and does not preclude the use of other frameworks for more complex future web interfaces.
