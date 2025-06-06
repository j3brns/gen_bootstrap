# Agent Development Kit (ADK)

https://github.com/google/adk-docs/blob/main/llms.txt

## High-Level Summary

The Agent Development Kit (ADK) is an open-source, code-first Python toolkit designed for developers building, evaluating, and deploying sophisticated AI agents, with a strong focus on integration with Google Cloud services and Gemini models. It emphasizes flexibility and fine-grained control over agent behavior, orchestration, and tool usage directly within Python code.

**Key Features:**

*   **Rich Tool Ecosystem:** Supports built-in tools (Google Search, Code Execution, Vertex AI Search), custom Python functions, OpenAPI spec integration, third-party libraries (LangChain, CrewAI), Google Cloud integrations (API Hub, Application Integration, MCP Toolbox for DBs), MCP standard tools, and using other agents as tools. Includes robust authentication handling.
*   **Code-First Development:** Define agent logic, workflows, and state management directly in Python, enabling testability, versioning, and debugging.
*   **Flexible Orchestration:** Build multi-agent systems using predefined workflow agents (`SequentialAgent`, `ParallelAgent`, `LoopAgent`) for structured processes or leverage `LlmAgent` for dynamic, LLM-driven routing and decision-making. Custom agents (`BaseAgent`) allow for arbitrary logic.
*   **Context & State Management:** Provides mechanisms for managing conversational context (`Session`), short-term state (`State` with session/user/app/temp scopes), long-term memory (`MemoryService`), and binary data (`ArtifactService`).
*   **Callbacks for Control:** Offers hooks (`before/after_agent`, `before/after_model`, `before/after_tool`) to observe, customize, or intercept agent execution flow for logging, validation, guardrails, caching, and more.
*   **Deployment Ready:** Facilitates deployment to various environments, including local testing, Google Cloud Run, and the scalable Vertex AI Agent Engine.
*   **Evaluation Framework:** Includes tools and patterns for evaluating agent performance based on trajectory (tool usage) and final response quality against predefined test cases.
*   **Responsible AI:** Provides guidance and mechanisms (guardrails, callbacks, identity management) for building safer and more secure agents.

The documentation covers getting started guides (installation, quickstarts, tutorial), core concepts (agents, tools, sessions, context, runtime, events), advanced topics (multi-agent systems, callbacks, custom agents, memory, artifacts, authentication), deployment strategies, evaluation methods, and responsible AI practices. Code examples and snippets illustrate key functionalities.

## Table of Contents
- [Agent Development Kit (ADK)](#agent-development-kit-adk)
  - [High-Level Summary](#high-level-summary)
  - [Table of Contents](#table-of-contents)
  - [Overview \& Core Concepts](#overview--core-concepts)
  - [Installation \& Setup](#installation--setup)
  - [Agents](#agents)
    - [BaseAgent](#baseagent)
    - [LlmAgent (`Agent`)](#llmagent-agent)
    - [Workflow Agents](#workflow-agents)
      - [SequentialAgent](#sequentialagent)
      - [ParallelAgent](#parallelagent)
      - [LoopAgent](#loopagent)
    - [Custom Agents](#custom-agents)
    - [Multi-Agent Systems](#multi-agent-systems)
    - [Models](#models)
  - [Tools](#tools)
    - [Tool Concepts](#tool-concepts)
    - [ToolContext](#toolcontext)
    - [Function Tools](#function-tools)
    - [Built-in Tools](#built-in-tools)
    - [OpenAPI Tools](#openapi-tools)
    - [Third-Party Tools (LangChain, CrewAI)](#third-party-tools-langchain-crewai)
    - [Google Cloud Tools](#google-cloud-tools)
    - [MCP Tools](#mcp-tools)
    - [Authentication](#authentication)
  - [Sessions, State \& Memory](#sessions-state--memory)
    - [Session](#session)
    - [SessionService](#sessionservice)
    - [State](#state)
    - [Memory \& MemoryService](#memory--memoryservice)
  - [Artifacts](#artifacts)
    - [Artifact Concepts](#artifact-concepts)
    - [ArtifactService](#artifactservice)
    - [Context Methods](#context-methods)
  - [Context Objects](#context-objects)
    - [InvocationContext](#invocationcontext)
    - [ReadonlyContext](#readonlycontext)
    - [CallbackContext](#callbackcontext)
    - [ToolContext (Recap)](#toolcontext-recap)
  - [Callbacks](#callbacks)
    - [Callback Mechanism](#callback-mechanism)
    - [Agent Lifecycle Callbacks](#agent-lifecycle-callbacks)
    - [LLM Interaction Callbacks](#llm-interaction-callbacks)
    - [Tool Execution Callbacks](#tool-execution-callbacks)
    - [Callback Patterns \& Best Practices](#callback-patterns--best-practices)
  - [Runtime \& Events](#runtime--events)
    - [Event Loop](#event-loop)
    - [Event Object](#event-object)
    - [Runtime Components](#runtime-components)
    - [Key Behaviors (State Timing, Streaming, Async)](#key-behaviors-state-timing-streaming-async)
  - [Evaluation](#evaluation)
    - [Concepts](#concepts)
    - [Methods (`adk web`, `pytest`, `adk eval`)](#methods-adk-web-pytest-adk-eval)
    - [Criteria](#criteria)
  - [Deployment](#deployment)
    - [Vertex AI Agent Engine](#vertex-ai-agent-engine)
    - [Cloud Run (`adk deploy`, `gcloud`)](#cloud-run-adk-deploy-gcloud)
  - [Safety \& Security](#safety--security)
  - [Development Tools (CLI)](#development-tools-cli)
  - [Contributing](#contributing)

## Overview & Core Concepts

*   **ADK (Agent Development Kit):** Open-source Python toolkit for building, evaluating, and deploying AI agents, integrated with Google Cloud and Gemini.
*   **Code-First:** Define agent logic, tools, and orchestration in Python.
*   **Key Primitives:** Agent, Tool, Callback, Session, State, Memory, Artifact, Event, Runner, Model.
*   **Focus:** Flexibility, control, Google ecosystem integration.
*   **Capabilities:** Multi-Agent Systems, Rich Tooling, Flexible Orchestration, Streaming, Evaluation, Deployment, Responsible AI features.

*(See: `README.md`, `docs/index.md`, `docs/get-started/about.md`)*

## Installation & Setup

1.  **Create Virtual Environment (Recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate # macOS/Linux
    # .venv\Scripts\activate.bat # Windows CMD
    # .venv\Scripts\Activate.ps1 # Windows PowerShell
    ```
2.  **Install ADK:**
    ```bash
    pip install google-adk
    ```
3.  **Model Setup (API Keys / ADC):**
    *   **Google AI Studio:** Set `GOOGLE_API_KEY` in `.env` or environment. Set `GOOGLE_GENAI_USE_VERTEXAI=FALSE`.
    *   **Vertex AI:** Authenticate (`gcloud auth application-default login`), set `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`. Set `GOOGLE_GENAI_USE_VERTEXAI=TRUE`.
    *   **LiteLLM (OpenAI, Anthropic, etc.):** Set provider-specific keys (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`).

*(See: `docs/get-started/installation.md`, `docs/get-started/quickstart.md`, `docs/agents/models.md`)*

## Agents

The fundamental execution units. All inherit from `BaseAgent`.

*(See: `docs/agents/index.md`)*

### BaseAgent

*   The foundation class for all agents.
*   Requires `name`.
*   Can have `parent_agent` and `sub_agents` list to define hierarchy.
*   Implements core `run_async` logic (often overridden).

*(See: `docs/agents/custom-agents.md`)*

### LlmAgent (`Agent`)

*   Uses an LLM for reasoning, generation, and tool/transfer decisions.
*   **Key Parameters:**
    *   `name` (str): Unique agent identifier.
    *   `model` (str | `BaseLlm`): LLM identifier (e.g., `"gemini-2.0-flash"`) or a wrapper instance (e.g., `LiteLlm(model="openai/gpt-4o")`).
    *   `instruction` (str | Callable): Guides the LLM's behavior, goals, persona, tool usage.
    *   `description` (str, Optional): Summary for delegation/discovery.
    *   `tools` (List[`BaseTool` | Callable], Optional): Tools available to the agent.
    *   `sub_agents` (List[`BaseAgent`], Optional): Child agents for hierarchy/delegation.
    *   `output_key` (str, Optional): Session state key to automatically save the agent's final text/structured response.
    *   `output_schema` (Pydantic BaseModel, Optional): Enforces JSON output matching the schema. **Disables tool use and transfer.**
    *   `input_schema` (Pydantic BaseModel, Optional): Requires input to match the schema.
    *   `generate_content_config` (`genai.types.GenerateContentConfig`, Optional): Controls LLM generation parameters (temp, max tokens, safety).
    *   `include_contents` (str, Optional, Default: `'default'`): `'none'` excludes conversation history from LLM context.
    *   Callbacks (`before_agent_callback`, etc.): Functions to hook into lifecycle.
*   **Behavior:** Non-deterministic, LLM-driven.

*(See: `docs/agents/llm-agents.md`)*

### Workflow Agents

*   Orchestrate sub-agent execution based on predefined logic (no LLM for flow control).
*   Deterministic execution patterns.

*(See: `docs/agents/workflow-agents/index.md`)*

#### SequentialAgent

*   Executes `sub_agents` one after another in the list order.
*   Passes the same `InvocationContext` sequentially (state is shared).
*   Use Case: Pipelines, ordered tasks.

*(See: `docs/agents/workflow-agents/sequential-agents.md`, `examples/python/snippets/agents/workflow-agents/sequential_agent_code_development_agent.py`)*

#### ParallelAgent

*   Executes `sub_agents` concurrently. Event order is not guaranteed.
*   Assigns distinct `branch` identifiers in context.
*   Sub-agents access the *same shared* `session.state` (requires careful key management).
*   Use Case: Independent tasks to reduce latency (e.g., parallel API calls).

*(See: `docs/agents/workflow-agents/parallel-agents.md`, `examples/python/snippets/agents/workflow-agents/parallel_agent_web_research.py`)*

#### LoopAgent

*   Executes `sub_agents` sequentially in a loop.
*   **Parameters:**
    *   `max_iterations` (int, Optional): Maximum number of loop cycles.
    *   `sub_agents` (List[`BaseAgent`]): Agents to run in each iteration.
*   **Termination:** Stops after `max_iterations` or when a sub-agent yields an `Event` with `actions.escalate=True`.
*   Passes the same `InvocationContext` (state persists across iterations).
*   Use Case: Iterative refinement, polling, processes repeating until a condition is met.

*(See: `docs/agents/workflow-agents/loop-agents.md`, `examples/python/snippets/agents/workflow-agents/loop_agent_doc_improv_agent.py`)*

### Custom Agents

*   Inherit directly from `BaseAgent`.
*   Implement custom orchestration logic in `async def _run_async_impl(self, ctx: InvocationContext)`.
*   Call sub-agents using `await self.sub_agent_instance.run_async(ctx)`.
*   Use `ctx.session.state` for data passing and control flow.
*   Register sub-agents via `super().__init__(sub_agents=[...])`.
*   Use Case: Complex conditional logic, unique workflows, deep external integrations within the control flow.

*(See: `docs/agents/custom-agents.md`, `examples/python/snippets/agents/custom-agent/storyflow_agent.py`)*

### Multi-Agent Systems

*   Compose agents into hierarchies (`parent_agent`, `sub_agents`).
*   **Communication/Coordination:**
    *   **Shared State (`session.state`):** Passive data exchange (e.g., via `output_key`).
    *   **LLM Delegation (Transfer):** `LlmAgent` uses LLM to call `transfer_to_agent(agent_name='...')` based on instructions/descriptions. Handled by `AutoFlow`.
    *   **Explicit Invocation (`AgentTool`):** Wrap an agent in `AgentTool` and add to parent's `tools` list. Parent LLM calls it like a function.
*   **Patterns:** Coordinator/Dispatcher, Sequential Pipeline, Parallel Fan-Out/Gather, Hierarchical Decomposition, Generator-Critic, Iterative Refinement, Human-in-the-Loop (via custom tools).

*(See: `docs/agents/multi-agents.md`)*

### Models

*   ADK supports various LLMs.
*   **Google Gemini:** Direct string IDs (`gemini-2.0-flash`, etc.). Set up via Google AI (`GOOGLE_API_KEY`) or Vertex AI (`GOOGLE_CLOUD_PROJECT`, `GOOGLE_GENAI_USE_VERTEXAI=TRUE`).
*   **LiteLLM Integration (`LiteLlm` wrapper):**
    *   Install `litellm`. Set provider API keys (e.g., `OPENAI_API_KEY`).
    *   Use `LlmAgent(model=LiteLlm(model="provider/model_name"), ...)`
    *   Supports OpenAI, Anthropic (non-Vertex), Cohere, Ollama (local), self-hosted endpoints (vLLM).
*   **Vertex AI Endpoints:**
    *   Use full resource string (`projects/.../endpoints/...`) as `model`.
    *   Requires Vertex AI setup (`GOOGLE_GENAI_USE_VERTEXAI=TRUE`).
    *   Works for Model Garden deployments and fine-tuned models.
*   **Third-Party on Vertex (e.g., Claude):**
    *   Requires Vertex AI setup.
    *   Install provider library (e.g., `anthropic[vertex]`).
    *   **Register** the model class with ADK: `LLMRegistry.register(Claude)`.
    *   Use direct model string (e.g., `"claude-3-sonnet@20240229"`) in `LlmAgent`.

*(See: `docs/agents/models.md`)*

## Tools

Capabilities provided to agents beyond core LLM functions.

*(See: `docs/tools/index.md`)*

### Tool Concepts

*   Action-oriented code components (functions, classes).
*   Extend agent abilities (API calls, search, code execution, DB query, RAG).
*   Used by `LlmAgent` via function calling based on instructions and tool descriptions/schemas.

### ToolContext

*   Special object injected into tool functions/callbacks if declared: `def my_tool(..., tool_context: ToolContext)`.
*   Inherits from `CallbackContext`.
*   **Key Capabilities:**
    *   `state`: Read/write session state.
    *   `actions`: Modify `EventActions` (e.g., `skip_summarization=True`, `transfer_to_agent`, `escalate`).
    *   `function_call_id`: ID of the LLM's request to call this tool.
    *   `agent_name`, `invocation_id`.
    *   `request_credential(auth_config)`: Initiate auth flow.
    *   `get_auth_response(auth_config)`: Retrieve credentials after auth flow.
    *   `list_artifacts()`: List available session artifacts.
    *   `load_artifact(filename, version=None)`: Load artifact content.
    *   `save_artifact(filename, artifact)`: Save artifact content.
    *   `search_memory(query)`: Query the long-term `MemoryService`.

*(See: `docs/tools/index.md#tool-context`, `docs/context/index.md`)*

### Function Tools

*   Wrap custom Python functions or methods.
*   **`FunctionTool(func=my_function)`:** Standard synchronous/asynchronous functions.
    *   Function **name**, **docstring**, **parameters** (with type hints), and **return type** (`dict` preferred, must be serializable) are critical for LLM usage.
    *   Use simple, JSON-serializable types for args/return.
    *   Keep tools focused; decompose complex tasks.
*   **`LongRunningFunctionTool(func=my_generator_func)`:** Wraps a Python *generator* function (`yield`).
    *   `yield` intermediate progress dicts (sent as `FunctionResponse`).
    *   `return` final result dict (sent as final `FunctionResponse`).
    *   Enables non-blocking execution for long tasks.
*   **`AgentTool(agent=other_agent_instance)`:** Treats another agent as a callable tool.
    *   Parent LLM calls it like a function.
    *   `AgentTool` runs the target agent, captures final response, and returns it.
    *   `skip_summarization` (bool): Option to bypass LLM summarization of the sub-agent's result.

*(See: `docs/tools/function-tools.md`, Example Snippets)*

### Built-in Tools

*   Ready-to-use tools provided by ADK. Require specific models (often Gemini).
*   `google_search`: Performs Google web search.
*   `built_in_code_execution`: Executes Python code sandboxed (via Gemini API).
*   `vertex_ai_search_tool(data_store_id)`: Searches a specific Vertex AI Search data store.
*   **Limitations (Current):** Generally, only one built-in tool per root/single agent is supported directly. Cannot be used directly in sub-agents (use delegation patterns).

*(See: `docs/tools/built-in-tools.md`, Example Snippets)*

### OpenAPI Tools

*   **`OpenAPIToolset`:** Automatically generates `RestApiTool` instances from an OpenAPI v3 spec (JSON/YAML string or dict).
*   **`RestApiTool`:** Represents a single API operation (e.g., GET /users). Handles request construction, execution, and response.
*   **Usage:**
    1.  Instantiate `OpenAPIToolset(spec_str=..., spec_str_type=..., auth_scheme=..., auth_credential=...)`.
    2.  Get tools: `api_tools = toolset.get_tools()`.
    3.  Add `api_tools` to `LlmAgent(tools=...)`.
*   Handles parameters (path, query, header, cookie), request bodies, and authentication schemes defined in the spec.

*(See: `docs/tools/openapi-tools.md`, `examples/python/snippets/tools/openapi_tool.py`)*

### Third-Party Tools (LangChain, CrewAI)

*   Wrappers to integrate tools from other frameworks.
*   **`LangchainTool(tool=langchain_tool_instance)`:** Wraps a LangChain tool.
    *   Requires `langchain_community`, etc.
*   **`CrewaiTool(name=..., description=..., tool=crewai_tool_instance)`:** Wraps a CrewAI tool.
    *   Requires `crewai-tools`.
    *   **Must** provide `name` and `description` for the ADK wrapper.
*   **Usage:** Instantiate provider tool, wrap with ADK tool, add wrapped tool to `LlmAgent`.

*(See: `docs/tools/third-party-tools.md`, Example Snippets)*

### Google Cloud Tools

*   Integrations with Google Cloud services.
*   **`ApiHubToolset`:** Creates tools from APIs documented in Apigee API Hub. Requires GCP auth (access token or service account) and API Hub resource name. Can configure API auth (API Key, SA, OIDC).
*   **`ApplicationIntegrationToolset`:** Creates tools from Application Integration workflows or Integration Connectors (e.g., Salesforce, SAP). Requires GCP project/location, integration/connection details, and GCP auth.
*   **MCP Toolbox for Databases:** Uses `ToolboxTool` from `google.adk.tools.toolbox_tool` to connect to a deployed MCP Toolbox server (separate open-source server). Requires `toolbox-langchain`. `toolbox = ToolboxTool("https://server-url")`, `tools = toolbox.get_toolset(...)`.

*(See: `docs/tools/google-cloud-tools.md`, `docs/tools/mcp-tools.md`)*

### MCP Tools

*   Model Context Protocol (MCP) integration.
*   **Using MCP Servers in ADK:**
    *   `MCPToolset.from_server(connection_params=...)`: Connects ADK agent to an external MCP server.
    *   `connection_params`: `StdioServerParameters(command='npx', args=[...], env={...})` for local servers, or `SseServerParams(url=...)` for remote.
    *   Returns `(tools, exit_stack)`. Tools are added to `LlmAgent`.
    *   **Crucial:** Call `await exit_stack.aclose()` for cleanup.
*   **Exposing ADK Tools via MCP:**
    *   Build a Python MCP server using `pip install mcp`.
    *   Use `adk_to_mcp_tool_type(adk_tool)` in `list_tools` handler.
    *   Call `adk_tool.run_async(...)` in `call_tool` handler.

*(See: `docs/tools/mcp-tools.md`)*

### Authentication

*   Handles secure access for tools calling external APIs.
*   **Core Concepts:**
    *   `AuthScheme`: *How* API expects credentials (e.g., `APIKey`, `HTTPBearer`, `OAuth2`, `OpenIdConnectWithConfig`). Defined by OpenAPI spec or specific classes.
    *   `AuthCredential`: *Initial* info to start auth (e.g., Client ID/Secret, API key value). `auth_type` indicates flow (e.g., `API_KEY`, `OAUTH2`, `SERVICE_ACCOUNT`, `OPEN_ID_CONNECT`).
*   **Configuration:** Passed during `OpenAPIToolset`, `APIHubToolset`, etc. initialization, or via specific methods like `GoogleApiToolSet.configure_auth(...)`.
*   **Interactive Flow (OAuth/OIDC):**
    1.  Tool call fails -> ADK yields `adk_request_credential` function call event.
    2.  Client app extracts `AuthConfig` (contains `auth_uri`) from event args.
    3.  Client app redirects user to `auth_uri` (appending `redirect_uri`).
    4.  User logs in, authorizes. IDP redirects back to `redirect_uri` with `code`.
    5.  Client app captures callback URL, updates `AuthConfig` (`auth_response_uri`, `redirect_uri`).
    6.  Client app sends `AuthConfig` back via `FunctionResponse` for `adk_request_credential`.
    7.  ADK performs token exchange, stores tokens, retries original tool call.
*   **Custom `FunctionTool` Auth:**
    1.  Check state for cached credentials. Refresh if needed.
    2.  If no valid creds, check `tool_context.get_auth_response()` for results from client flow.
    3.  If still no creds, call `tool_context.request_credential(AuthConfig(...))` to start the flow. Return pending status.
    4.  ADK handles token exchange after user interaction.
    5.  On retry, `get_auth_response()` provides creds. Cache them in state.
    6.  Make API call with creds.
    7.  Return result.
*   **Security:** Avoid storing sensitive tokens (esp. refresh tokens) directly in basic state. Use secure secret managers for production. Consider encrypting state if using persistent DBs.

*(See: `docs/tools/authentication.md`, `examples/python/snippets/tools/auth/`)*

## Sessions, State & Memory

Manage conversational context.

*(See: `docs/sessions/index.md`)*

### Session

*   Represents a single, ongoing conversation thread.
*   Container for `events` (history) and `state` (current context data).
*   Identified by `id`, `app_name`, `user_id`.
*   Managed by `SessionService`.

*(See: `docs/sessions/session.md`)*

### SessionService

*   Manages `Session` object lifecycle (create, get, update, delete).
*   Responsible for persisting session data (events, state).
*   **Implementations:**
    *   `InMemorySessionService`: Non-persistent, for local dev/testing.
    *   `DatabaseSessionService`: Persistent using SQLAlchemy-compatible DB (`pip install google-adk[database]`). Requires DB URL.
    *   `VertexAiSessionService`: Persistent using Vertex AI Agent Engine backend (`pip install google-adk[vertexai]`). Requires GCP setup, `app_name` is Reasoning Engine ID.

*(See: `docs/sessions/session.md`)*

### State

*   Dictionary (`session.state`) holding temporary data for the *current* conversation.
*   Keys are strings, values must be JSON-serializable (str, int, bool, float, list/dict of primitives).
*   **Prefixes (Define Scope):**
    *   **(None):** Session-specific.
    *   `user:`: User-specific across sessions (requires persistent service).
    *   `app:`: App-specific across users/sessions (requires persistent service).
    *   `temp:`: Temporary for current invocation turn (never persisted).
*   **Updates:**
    *   **Recommended:** Via `append_event` flow using:
        *   `LlmAgent(output_key="state_key")`: Saves final agent response text/structure.
        *   `Event(actions=EventActions(state_delta={...}))`: Manually specify changes in an event.
    *   **Discouraged:** Direct modification (`retrieved_session.state['key'] = value`) bypasses history, persistence, safety. Use context objects (`tool_context.state`, `callback_context.state`) within tools/callbacks.

*(See: `docs/sessions/state.md`)*

### Memory & MemoryService

*   Manages long-term, searchable knowledge potentially spanning multiple sessions.
*   `BaseMemoryService` interface.
*   **Responsibilities:**
    *   `add_session_to_memory(session)`: Ingest relevant info from a session.
    *   `search_memory(app_name, user_id, query)`: Search the store.
*   **Implementations:**
    *   `InMemoryMemoryService`: Non-persistent, basic keyword search.
    *   `VertexAiRagMemoryService`: Persistent, uses Vertex AI RAG Corpus for semantic search (`pip install google-adk[vertexai]`). Requires GCP setup, Corpus ID.
*   **Usage:** Agents use tools (e.g., `load_memory`) that call `memory_service.search_memory`.

*(See: `docs/sessions/memory.md`)*

## Artifacts

Manage named, versioned binary data (files) associated with sessions or users.

*(See: `docs/artifacts/index.md`)*

### Artifact Concepts

*   Represents binary data (e.g., image, PDF) identified by a `filename` string.
*   Stored/retrieved via `ArtifactService`.
*   Data represented as `google.genai.types.Part` (usually `inline_data` with `data: bytes` and `mime_type: str`).
*   Automatically versioned on save.
*   **Namespacing:**
    *   `"report.pdf"`: Session-scoped (app/user/session).
    *   `"user:profile.png"`: User-scoped (app/user), accessible across sessions.

### ArtifactService

*   Manages artifact storage and retrieval. Configured on the `Runner`.
*   **Implementations:**
    *   `InMemoryArtifactService`: Non-persistent, stores in Python dict.
    *   `GcsArtifactService`: Persistent, stores versions as objects in Google Cloud Storage bucket. Requires GCS bucket name and permissions.

### Context Methods

*   Available on `CallbackContext` and `ToolContext`. Require `ArtifactService` configured on `Runner`.
*   `save_artifact(filename: str, artifact: types.Part) -> int`: Saves data, returns version number. Records action in `event.actions.artifact_delta`.
*   `load_artifact(filename: str, version: Optional[int] = None) -> Optional[types.Part]`: Retrieves artifact. Loads latest if `version` is None.
*   `list_artifacts() -> list[str]` (`ToolContext` only): Lists available artifact filenames in scope.

*(See: `docs/artifacts/index.md`)*

## Context Objects

Bundles of information available during execution. Passed automatically by the framework.

*(See: `docs/context/index.md`)*

### InvocationContext

*   Most comprehensive context. Passed to agent `_run_async_impl`.
*   Contains: `session` (with `state`, `events`), `agent`, `invocation_id`, `user_content`, configured services (`session_service`, `artifact_service`, `memory_service`), `end_invocation` flag.

### ReadonlyContext

*   Base class, provides read-only view. Used in `InstructionProvider`.
*   Contains: `invocation_id`, `agent_name`, read-only `state`.

### CallbackContext

*   Used in agent/model callbacks (`before/after_agent`, `before/after_model`).
*   Adds to `ReadonlyContext`:
    *   **Mutable `state` property:** Allows read/write. Changes tracked.
    *   `save_artifact`, `load_artifact` methods.
    *   `user_content`.

### ToolContext (Recap)

*   Used in tool functions/callbacks (`before/after_tool`).
*   Inherits from `CallbackContext`.
*   Adds:
    *   `request_credential`, `get_auth_response`.
    *   `list_artifacts`.
    *   `search_memory`.
    *   `function_call_id`: ID of the originating function call request.
    *   `actions`: Direct access to `EventActions` for the current step.

## Callbacks

Functions to hook into agent lifecycle points. Registered on `Agent` initialization.

*(See: `docs/callbacks/index.md`)*

### Callback Mechanism

*   Framework calls registered functions at specific points.
*   Receive context objects (`CallbackContext` or `ToolContext`).
*   **Control Flow:**
    *   `return None`: Allows default behavior to proceed.
    *   `return <Specific Object>`: **Overrides** default behavior / **skips** next step.
        *   `before_agent_callback` -> `types.Content`: Skips agent run, uses Content as result.
        *   `before_model_callback` -> `LlmResponse`: Skips LLM call, uses LlmResponse.
        *   `before_tool_callback` -> `dict`: Skips tool execution, uses dict as result.
        *   `after_agent_callback` -> `types.Content`: Replaces agent result.
        *   `after_model_callback` -> `LlmResponse`: Replaces LLM response.
        *   `after_tool_callback` -> `dict`: Replaces tool result.

### Agent Lifecycle Callbacks

*   Apply to any `BaseAgent`.
*   `before_agent_callback(callback_context: CallbackContext)`: Runs before `_run_async_impl`. Return `Content` to skip.
*   `after_agent_callback(callback_context: CallbackContext)`: Runs after successful `_run_async_impl`. Return `Content` to replace result.

*(See: `docs/callbacks/types-of-callbacks.md`)*

### LLM Interaction Callbacks

*   Specific to `LlmAgent`.
*   `before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest)`: Runs before LLM call. Return `LlmResponse` to skip. Can modify `llm_request`.
*   `after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse)`: Runs after LLM response. Return `LlmResponse` to replace.

*(See: `docs/callbacks/types-of-callbacks.md`, Example Snippets)*

### Tool Execution Callbacks

*   Specific to `LlmAgent` when calling tools.
*   `before_tool_callback(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext)`: Runs before tool `run_async`. Return `dict` to skip tool and use dict as result. Can modify `args`.
*   `after_tool_callback(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict)`: Runs after tool `run_async`. Return `dict` to replace `tool_response`.

*(See: `docs/callbacks/types-of-callbacks.md`, Example Snippets)*

### Callback Patterns & Best Practices

*   **Patterns:** Guardrails, State Management, Logging, Caching, Request/Response Modification, Conditional Skipping, Tool Actions (Auth, Skip Summarization), Artifact Handling.
*   **Best Practices:** Keep focused, mind performance (avoid blocking), handle errors, manage state carefully, consider idempotency, test thoroughly, use clear names/docs, use correct context type.

*(See: `docs/callbacks/design-patterns-and-best-practices.md`)*

## Runtime & Events

The execution engine and communication mechanism.

*(See: `docs/runtime/index.md`)*

### Event Loop

*   Core operational pattern: `Runner` orchestrates, `Execution Logic` (Agents, Tools, Callbacks) yields `Event` objects.
*   **Cycle:**
    1.  Runner starts Agent.
    2.  Agent logic runs, yields `Event`, pauses.
    3.  Runner receives Event, processes `actions` (commits state/artifact changes via Services), yields event upstream.
    4.  Agent logic resumes, sees committed state. Repeats.

### Event Object

*   (`google.adk.events.Event`) Immutable record of an occurrence.
*   Contains: `author` ('user' or agent name), `content` (`types.Content` with text, function call/response, etc.), `actions` (`EventActions` payload), `invocation_id`, `id`, `timestamp`, `partial` flag, etc.
*   `event.actions`: Carries `state_delta`, `artifact_delta`, `transfer_to_agent`, `escalate`, `skip_summarization`, etc.
*   `event.is_final_response()`: Helper to identify user-facing final output for a turn.

*(See: `docs/events/index.md`)*

### Runtime Components

*   `Runner`: Orchestrates the Event Loop for an invocation.
*   Execution Logic: Agents, Tools, Callbacks that yield Events.
*   `Event`: Communication unit.
*   `Services`: Persistence layers (`SessionService`, `ArtifactService`, `MemoryService`).
*   `Session`: Container for one conversation's state and events.
*   `Invocation`: A single user-query-to-final-response cycle.

### Key Behaviors (State Timing, Streaming, Async)

*   **State Commitment:** Changes (`state_delta`) are committed by `SessionService` *after* the event carrying them is yielded and processed by the Runner.
*   **Dirty Reads:** Code *within* the same invocation step might see local, uncommitted state changes made earlier in that step.
*   **Streaming (`partial=True`):** Events marked `partial` are yielded upstream immediately (for UI) but their `actions` are processed only when the final (non-partial) event arrives.
*   **Async Primary:** Runtime is built on `asyncio`. `Runner.run_async` is the core method. Synchronous tools/callbacks may run in threads.

*(See: `docs/runtime/index.md`)*

## Evaluation

Assessing agent performance.

*(See: `docs/evaluate/index.md`)*

### Concepts

*   Evaluates **Trajectory** (tool usage steps) and **Final Response**.
*   Uses predefined datasets (`.test.json` files or `.evalset.json` files).
*   **Test Files:** Simpler, single session per file, good for unit tests during dev. Fields: `query`, `expected_tool_use`, `expected_intermediate_agent_responses`, `reference`.
*   **Evalsets:** Multiple sessions ("evals"), can represent complex multi-turn conversations, good for integration tests. Fields per turn same as test files, plus `name` and `initial_session` per eval.

### Methods (`adk web`, `pytest`, `adk eval`)

*   **`adk web`:** Interactive evaluation via "Eval" tab in the dev UI. Can create evalsets from sessions.
*   **`pytest`:** Programmatic evaluation using `AgentEvaluator.evaluate(agent_module=..., eval_dataset=...)`. Good for CI/CD.
*   **`adk eval <AGENT_MODULE> <EVAL_SET_FILE(S)>`:** CLI command to run evaluations on evalsets.

### Criteria

*   Specified in `test_config.json` (optional, uses defaults if absent).
*   `tool_trajectory_avg_score` (float, default 1.0): Accuracy of tool usage steps vs. `expected_tool_use`.
*   `response_match_score` (float, default 0.8): ROUGE score comparing final agent response vs. `reference`.

## Deployment

Moving agents to scalable environments.

*(See: `docs/deploy/index.md`)*

### Vertex AI Agent Engine

*   Fully managed, auto-scaling Google Cloud service.
*   **Steps:**
    1.  Install `google-cloud-aiplatform[adk,agent_engines]`.
    2.  Initialize Vertex AI SDK (`vertexai.init(...)`).
    3.  Wrap agent: `app = reasoning_engines.AdkApp(agent=root_agent, ...)`.
    4.  Deploy: `remote_app = agent_engines.create(agent_engine=root_agent, requirements=[...])`. (Takes time).
    5.  **Grant Permissions:** Assign `roles/aiplatform.user` to the `service-...@gcp-sa-aiplatform-re.iam.gserviceaccount.com` service agent for managed sessions.
    6.  Interact: `remote_app.create_session()`, `remote_app.stream_query()`.
    7.  Cleanup: `remote_app.delete(force=True)`.

*(See: `docs/deploy/agent-engine.md`)*

### Cloud Run (`adk deploy`, `gcloud`)

*   Deploy as a container on Google Cloud's serverless platform.
*   **Method 1: `adk deploy cloud_run` CLI:**
    *   `adk deploy cloud_run --project <...> --region <...> [options] <AGENT_DIR_PATH>`
    *   Options: `--service_name`, `--app_name`, `--with_ui`, `--port`, etc.
    *   Handles Dockerfile creation and deployment.
*   **Method 2: `gcloud run deploy` (Manual):**
    1.  Create `Dockerfile` (Python base, copy code, install requirements, set user, CMD `uvicorn`).
    2.  Create `requirements.txt` (`google-adk`, other deps).
    3.  Create `main.py` using FastAPI and `get_fast_api_app` from ADK.
    4.  Run `gcloud run deploy <service_name> --source . --region <...> --project <...> [flags]`.
        *   Flags: `--allow-unauthenticated`, `--set-env-vars`.
*   **Testing:** Use deployed UI (if `--with_ui` or `SERVE_WEB_INTERFACE=True`) or `curl` against API endpoints (`/list-apps`, `/apps/.../sessions/...`, `/run`, `/run_sse`). Use `gcloud auth print-identity-token` for authenticated services.

*(See: `docs/deploy/cloud-run.md`, `docs/get-started/testing.md`)*

## Safety & Security

Building trustworthy agents.

*   **Risks:** Misalignment, harmful content, brand safety issues, unsafe actions (data leaks, unauthorized actions), prompt injection.
*   **Mitigation Strategies:**
    *   **Identity/Authorization:** Configure tools to use Agent-Auth (service account) or User-Auth (OAuth).
    *   **Guardrails:**
        *   *In-Tool:* Design tools defensively, check `tool_context` state/policy.
        *   *Gemini Built-in:* Use content filters and safety system instructions.
        *   *Callbacks:* Use `before_model_callback` / `before_tool_callback` to inspect/block inputs or args.
        *   *LLM as Filter:* Use a fast LLM (e.g., Gemini Flash Lite) via callbacks to screen inputs/outputs.
    *   **Sandboxed Code Execution:** Use Vertex Code Interpreter extension or Gemini API's tool (`built_in_code_execution`), or build custom sandboxed environments.
    *   **Evaluation & Tracing:** Assess safety via evaluations; use tracing for observability.
    *   **Network Controls:** Use VPC Service Controls to limit external access.
    *   **UI Escaping:** Always escape model-generated content in UIs to prevent XSS.

*(See: `docs/guides/responsible-agents.md`)*

## Development Tools (CLI)

*   `adk web [AGENTS_DIR]`: Starts local FastAPI server with Dev UI. Options: `--port`, `--session_db_url`, `--log_level`, `--allow_origins`.
*   `adk run <AGENT_DIR>`: Runs interactive CLI session with one agent. Option: `--save_session`.
*   `adk eval <AGENT_MODULE> <EVAL_SET_FILE(S)>`: Runs evaluations. Options: `--config_file_path`, `--print_detailed_results`.
*   `adk api_server [AGENTS_DIR]`: Starts local FastAPI server (API only, no UI). Similar options to `adk web`.
*   `adk deploy cloud_run <AGENT_DIR>`: Deploys agent to Cloud Run. Options: `--project`, `--region`, `--service_name`, `--with_ui`.

*(See: `docs/get-started/local-dev.md`)*

## Contributing

*   Requires signing Google CLA.
*   Follows Google Open Source Community Guidelines.
*   Use GitHub Discussions for questions/ideas.
*   Report framework bugs in `google/adk-python`.
*   Report doc errors/suggest enhancements in `google/adk-docs`.
*   Submit PRs to the relevant repository. Code reviews required.
*   Contributions licensed under Apache 2.0.

*(See: `docs/contributing-guide.md`)*