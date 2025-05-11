# Feature: Prompt Management

## Status

Partially Implemented (Beta Phase)
* `gen-bootstrap prompts list`: Implemented (interacts with Vertex AI Prompt Registry).
* `gen-bootstrap prompts get <prompt_id>`: Implemented (interacts with Vertex AI Prompt Registry).
* `gen-bootstrap prompts create --file <path_to_prompt_file>`: Implemented (interacts with Vertex AI Prompt Registry, handles updates by creating new versions).
* `gen-bootstrap prompts update`: Functionality covered by `create` (versioning).

## Description

This feature provides a centralized and managed way to define, store, version, and retrieve prompt templates for generative AI models using Vertex AI Prompt Classes, including associated safety settings.

## Goals

*   Enable prompt engineers and developers to manage prompts outside of the core agent code.
*   Support versioning of prompt templates.
*   Facilitate fetching specific prompt versions by agents at runtime.
*   Provide CLI commands for managing Prompt Classes in Vertex AI.
*   Leverage Vertex AI's built-in safety features associated with Prompt Classes.

## Components

*   **Vertex AI Prompt Classes:** The GCP service used to store and manage prompts, including safety settings.
*   **`utils/prompt_manager.py`:** Python module containing functions to interact with the Vertex AI Prompt Classes API (create, list, get, update).
*   **`cli/commands/prompts.py`:** CLI commands (`cli prompts create`, `list`, `get`, `update`) to manage Prompt Classes.
*   **ADK Agents (`adk/`):** Agent code will call `utils.prompt_manager` functions to fetch prompts.
*   **`prompts/` (Optional):** Local directory for storing prompt source files before uploading as Prompt Classes.

## Implementation Details

*   Use the `google-cloud-aiplatform` Python client library.
*   Implement functions in `utils/prompt_manager.py` to wrap Vertex AI Prompt Class operations.
*   Develop corresponding commands in the CLI using Typer/Click.
*   Agents will fetch prompts by name and optionally version.
*   When using prompts fetched from Vertex AI, leverage associated safety settings provided by the Vertex AI API.
*   Documentation will explain how to define prompts (including safety settings), use the CLI to manage them, and fetch and use them in agent code, highlighting the safety aspects.

## Acceptance Criteria

*   Users can create a new Prompt (or new version) in Vertex AI from a local YAML definition file using the CLI. (Implemented)
*   Users can list existing Prompts in Vertex AI Prompt Registry using the CLI. (Implemented)
*   Users can retrieve the content and details of a specific Prompt from Vertex AI Prompt Registry using the CLI. (Implemented)
*   Users can update an existing Prompt by submitting a modified definition file with the same `prompt_name` using the `create` command, which results in a new version. (Covered by `create`)
*   An ADK agent can successfully fetch a specified Prompt Class version at runtime using the `utils` functions.
*   Prompt fetching logic handles potential errors (e.g., prompt not found).
*   The application successfully applies safety settings defined in Vertex AI Prompt Classes when interacting with models.
*   Documentation clearly explains how safety policies are integrated via Prompt Classes.
