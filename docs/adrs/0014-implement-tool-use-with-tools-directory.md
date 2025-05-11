# 14. Implement Tool Use with a Dedicated `tools/` Directory

## Status

Accepted (Leveraging ADK's Tool Framework)

## Context

Modern generative AI agents often need to interact with external systems and data sources to perform tasks beyond text generation. This requires a mechanism for the agent to call external functions or tools. We need a structured way to define, implement, and manage these tools within the project, leveraging the Google Agent Development Kit's (ADK) tool framework.

## Decision

We will implement external tools that ADK agents can use within a dedicated `tools/` directory, utilizing ADK's tool classes (`FunctionTool`, `LongRunningFunctionTool`, `AgentTool`) and related features.

## Consequences

*   **Benefits:**
    *   Provides a clear, organized location for all external tool code.
    *   Promotes reusability of tools across different agents.
    *   Enforces a standard approach for tools using ADK's tool classes, making them easier to integrate with agents and test.
    *   Separates tool logic from core agent logic.
    *   Leverages ADK's `ToolContext` for secure secret retrieval, artifact management, and authentication.
    *   Supports integration with external MCP servers via ADK's `MCPToolset`.
*   **Drawbacks:**
    *   Requires understanding and utilizing ADK's tool framework.
    *   Agents need logic to understand tool calls from the model and execute the corresponding tool implementation, following ADK's patterns.
*   **Impact on Plan:**
    *   A `tools/` directory will be added to the project structure.
    *   Tools will be implemented using ADK's `FunctionTool`, `LongRunningFunctionTool`, and `AgentTool` classes.
    *   ADK agents in `adk/` will include logic to work with tools from the `tools/` directory, following ADK's tool invocation patterns.
    *   The `utils/` module will provide helper functions for tools (e.g., secret retrieval using ADK's `ToolContext`).
    *   CLI commands (`cli tools`) will be implemented to list and describe tools based on the contents of the `tools/` directory, potentially leveraging ADK's tool introspection capabilities.
    *   Testing plan includes testing individual tools and agents using tools, leveraging ADK's testing framework.
    *   MCP integration will be achieved using ADK's `MCPToolset` to connect to external MCP servers.
