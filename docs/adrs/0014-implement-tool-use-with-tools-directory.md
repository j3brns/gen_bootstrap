# 14. Implement Tool Use with a Dedicated `tools/` Directory

## Status

Accepted

## Context

Modern generative AI agents often need to interact with external systems and data sources to perform tasks beyond text generation. This requires a mechanism for the agent to call external functions or tools. We need a structured way to define, implement, and manage these tools within the project.

## Decision

We will implement external tools that ADK agents can use within a dedicated `tools/` directory. Tools will follow a standard interface, and the `tools/` directory will house their definitions and implementations.

## Consequences

*   **Benefits:**
    *   Provides a clear, organized location for all external tool code.
    *   Promotes reusability of tools across different agents.
    *   Enforces a standard interface for tools, making them easier to integrate with agents and test.
    *   Separates tool logic from core agent logic.
*   **Drawbacks:**
    *   Requires defining and adhering to a standard tool interface.
    *   Agents need logic to understand tool calls from the model and execute the corresponding tool implementation.
*   **Impact on Plan:**
    *   A new `tools/` directory will be added to the project structure.
    *   A standard tool interface or base class will be defined (likely in `tools/`).
    *   Individual tool implementations will reside in `tools/`.
    *   ADK agents in `adk/` will include logic to work with tools from the `tools/` directory.
    *   The `utils/` module will provide helper functions for tools (e.g., secret retrieval).
    *   CLI commands (`cli tools`) will be implemented to list and describe tools based on the contents of the `tools/` directory.
    *   Testing plan includes testing individual tools and agents using tools.
