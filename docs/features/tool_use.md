# Feature: Tool Use / Function Calling

## Status

Partially Implemented (Beta Phase)
* `gen-bootstrap tools list`: Implemented.
* `gen-bootstrap tools describe <tool_name>`: Implemented.

## Description

This feature provides a structured approach for defining and integrating external tools or functions that ADK agents can use to interact with the outside world (e.g., calling APIs, accessing databases). It leverages the Google Agent Development Kit's (ADK) robust tool framework.

## Goals

*   Enable agents to perform actions beyond generating text.
*   Provide a clear pattern for defining tool interfaces and implementations using ADK's tool classes.
*   Facilitate presenting tool capabilities to the generative model for function calling.
*   Support secure execution of tools, including accessing secrets and handling authentication via ADK's `ToolContext`.
*   Enable integration with Model Context Protocol (MCP) for using tools from external MCP servers.

## Components

*   **`tools/` Directory:** Houses the definitions and implementations of external tools.
*   **ADK Tool Classes:** Utilizes `google.adk.tools.FunctionTool`, `LongRunningFunctionTool`, and `AgentTool` for wrapping Python functions, generators, and other agents as tools.
*   **Built-in Tools:** Leverages built-in ADK tools (e.g., `google_search`, `vertex_ai_search_tool`) where appropriate.
*   **OpenAPI Tools:** Supports creating tools from OpenAPI specifications using `google.adk.tools.OpenAPIToolset`.
*   **Third-Party Tools:** Allows wrapping tools from other frameworks (e.g., LangChain, CrewAI) using ADK's tool wrappers.
*   **`utils/`:** Provides helper functions for tools (e.g., secret retrieval, making robust HTTP calls).
*   **`ToolContext`:** Provides access to session state, artifacts, authentication, and other contextual information within tool functions.
*   **MCP Integration:** Supports using tools from external MCP servers via `google.adk.tools.MCPToolset`.
*   **CLI Commands:** `cli tools list`, `cli tools describe` to manage and inspect tools.
*   **ADK Agents (`adk/`):** Agent logic to identify tool calls from the model, execute tools, and process results.

## Implementation Details

*   Define tools by creating Python files in the `tools/` directory.
*   Use `FunctionTool` to wrap standard synchronous/asynchronous functions. Ensure functions have clear names, docstrings, parameter type hints, and serializable return types.
*   Use `LongRunningFunctionTool` to wrap Python generator functions for non-blocking execution of long tasks.
*   Use `AgentTool` to treat other agents as callable tools, enabling complex agent orchestration.
*   Leverage built-in ADK tools where applicable.
*   Use `OpenAPIToolset` to automatically generate tools from OpenAPI specifications.
*   Wrap third-party tools using ADK's tool wrappers (`LangchainTool`, `CrewaiTool`).
*   Access secrets and other contextual information within tool functions using the `ToolContext` object.
*   Connect to external MCP servers using `MCPToolset.from_server`.
*   Agents will need to format tool descriptions/schemas in a way the generative model understands for function calling.
*   Agents will parse model responses to detect tool call requests.
*   Implement logic in agents to execute the requested tool, passing the correct parameters.
*   Ensure tools use `utils/secret_manager` for any necessary credentials.
*   Extend logging and tracing to cover tool calls and results, potentially using ADK's callback mechanism.
*   Develop CLI commands using Typer/Click to list and describe tools based on the code in `tools/`. (Listing implemented)

## Acceptance Criteria

*   A new tool can be defined by creating a Python file in the `tools/` directory using ADK's tool classes (`FunctionTool`, `LongRunningFunctionTool`, `AgentTool`).
*   The `gen-bootstrap tools list` command correctly lists the available tools by inspecting `FunctionTool` instances in the `tools/` directory. (Implemented)
*   The `gen-bootstrap tools describe <tool_name>` command shows the description, parameters (from type hints), and docstring of a specified tool. (Implemented)
*   An ADK agent can be configured to be aware of available tools.
*   An agent can successfully identify a tool call request from a generative model's response.
*   An agent can successfully execute a tool, passing the correct parameters.
*   The result of a tool execution is correctly processed by the agent.
*   Tool execution errors are handled gracefully and logged.
*   Tools can securely access secrets using `ToolContext` and `utils/secret_manager`.
*   The project can connect to and use tools from external MCP servers.
