# Feature: Tool Use / Function Calling

## Status

Partially Implemented (Beta Phase)
* `gen-bootstrap tools list`: Implemented.
* `gen-bootstrap tools describe <tool_name>`: Implemented.

## Description

This feature provides a structured approach for defining and integrating external tools or functions that ADK agents can use to interact with the outside world (e.g., calling APIs, accessing databases).

## Goals

*   Enable agents to perform actions beyond generating text.
*   Provide a clear pattern for defining tool interfaces and implementations.
*   Facilitate presenting tool capabilities to the generative model for function calling.
*   Support secure execution of tools, including accessing secrets.

## Components

*   **`tools/` Directory:** Houses the definitions and implementations of external tools.
*   **Tool Interface/Base Class:** A standard Python interface or base class for tools.
*   **Individual Tool Implementations:** Python classes/functions in `tools/` that implement the logic for specific tools.
*   **ADK Agents (`adk/`):** Agent logic to identify tool calls from the model, execute tools, and process results.
*   **`utils/`:** Provides helper functions for tools (e.g., secret retrieval, making robust HTTP calls).
*   **CLI Commands:** `cli tools list`, `cli tools describe` to manage and inspect tools.

## Implementation Details

*   Define a simple, consistent interface for tools (e.g., a `run` method that accepts parameters and returns a result).
*   Implement example tools in the `tools/` directory (e.g., a mock weather tool, a simple calculator tool).
*   Agents will need to format tool descriptions/schemas in a way the generative model understands for function calling.
*   Agents will parse model responses to detect tool call requests.
*   Implement logic in agents to execute the requested tool, passing the correct parameters.
*   Ensure tools use `utils/secret_manager` for any necessary credentials.
*   Extend logging and tracing to cover tool calls and results.
*   Develop CLI commands using Typer/Click to list and describe tools based on the code in `tools/`. (Listing implemented)

## Acceptance Criteria

*   A new tool can be defined by creating a Python file in the `tools/` directory following the standard interface.
*   The `gen-bootstrap tools list` command correctly lists the available tools by inspecting `FunctionTool` instances in the `tools/` directory. (Implemented)
*   The `gen-bootstrap tools describe <tool_name>` command shows the description, parameters (from type hints), and docstring of a specified tool. (Implemented)
*   An ADK agent can be configured to be aware of available tools.
*   An agent can successfully identify a tool call request from a generative model's response.
*   An agent can successfully execute a tool, passing the correct parameters.
*   The result of a tool execution is correctly processed by the agent.
*   Tool execution errors are handled gracefully and logged.
