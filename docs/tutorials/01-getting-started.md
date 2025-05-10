# Tutorial 1: Getting Started with the `gen-bootstrap` ADK Scaffold

This tutorial guides you through setting up a new project using the `gen-bootstrap` scaffold, which is now designed to work with the **official Google Agent Development Kit (`google-adk`)**. You will set up the environment, understand the core structure, and run the example agent locally.

## Prerequisites

* Python 3.9 or higher (recommended for `google-adk`).
* Poetry installed ([Poetry Installation Guide](https://python-poetry.org/docs/#installation)).
* Google Cloud SDK (`gcloud` CLI) installed and authenticated. You must have logged in (`gcloud auth login`, `gcloud auth application-default login`) and set your default project (`gcloud config set project YOUR_PROJECT_ID`). See `docs/guides/manual_gcp_setup.md` for details.
* Docker installed (used by Cloud Build when deploying to Cloud Run from source).

## Steps

1.  **Clone the Scaffold Repository:**
    Obtain the scaffold code and navigate into the project directory.
    ```bash
    git clone YOUR_PROJECT_REPOSITORY_URL gen-bootstrap-project
    cd gen-bootstrap-project
    ```

2.  **Configure Project Settings (`.env` file):**
    This is a **critical step**. Copy the template environment file and edit it with your specific GCP Project ID. The agent also uses a default Gemini model which can be configured here or in `config/settings.py`.
    ```bash
    cp template.env .env
    ```
    Now, **open the `.env` file (in the project root) with a text editor and replace `YOUR_GCP_PROJECT_ID_HERE` with your actual GCP Project ID.** You can also set `DEFAULT_GEMINI_MODEL` if desired.

3.  **Initialize the Project & Install Dependencies:**
    The `gen-bootstrap init` command will guide you on ensuring dependencies like `google-adk` are set up.
    ```bash
    poetry run gen-bootstrap init
    ```
    This typically involves:
    * Ensuring `google-adk` is added to your `pyproject.toml` (run `poetry add google-adk` if the `init` script indicates it's missing or if you're setting up from an older base).
    * Running `poetry install` to install all defined dependencies, including `google-adk`, `fastapi`, `uvicorn`, etc.

4.  **Set up Pre-commit Hooks (Optional but Recommended):**
    For consistent code quality:
    ```bash
    poetry run pre-commit install
    ```

5.  **Perform Manual GCP Setup:**
    Before running or deploying, you **must** configure your GCP environment. This includes enabling necessary APIs and setting IAM permissions for the Cloud Run service identity.
    **Carefully follow all instructions in:** `docs/guides/manual_gcp_setup.md`

6.  **Understand the Core Project Structure for ADK Development:**
    * **Agent Logic:** Your primary agent(s) are defined in `adk/agent.py` using `google-adk` classes like `LlmAgent`.
    * **Tools:** Custom tools for your agent(s) are created in the `tools/` directory (e.g., `example_tool.py`) using `google-adk`'s `FunctionTool` or `@tool` decorator.
    * **Serving:** The FastAPI application in `main.py` is configured to serve your ADK agent (defined in `adk/agent.py`) using `google.adk.cli.fast_api.get_fast_api_app`. This typically exposes endpoints like `/run` and the ADK Web UI at `/adk_web`.

7.  **Run the Example Agent Locally:**
    You have several ways to run and test your agent:

    * **A) Run the FastAPI Service (Recommended for general development & API testing):**
        This starts the Uvicorn server for `main.py`.
        ```bash
        poetry run gen-bootstrap run
        ```
        * Access the FastAPI app in your browser at `http://localhost:8080`.
        * The ADK Web UI should be available at `http://localhost:8080/adk_web` for interacting with your agent.
        * You can also send POST requests to the `/run` endpoint (e.g., using `curl` or Postman) with a payload like:
            ```json
            {
                "messages": [{"content": {"text": "What time is it in UTC?"}, "role": "user"}],
                "session_id": "tutorial-session-123"
            }
            ```

    * **B) Run ADK's Native Web UI Directly (Good for focused ADK debugging):**
        ```bash
        poetry run gen-bootstrap run --adk-ui-only --agent-path adk.agent:root_agent
        ```
        (This runs `adk web adk.agent:root_agent` internally.)

    * **C) Run via ADK CLI (For quick command-line tests):**
        ```bash
        poetry run adk run adk.agent:root_agent --input "What is the weather like?"
        ```
        *(Note: The example agent doesn't have a weather tool yet, so it will respond based on its instructions.)*

    * **D) Use the Gradio Test Client:**
        First, ensure the FastAPI server is running (using Option A in a separate terminal). Then, run:
        ```bash
        poetry run python test_client.py
        ```
        This will launch a Gradio interface in your browser to interact with the agent via its API.

8.  **Explore and Modify:**
    * Open `adk/agent.py` to see how `root_agent` is defined with instructions and tools.
    * Open `tools/example_tool.py` to see how `get_current_time_tool` is defined.
    * Try modifying the agent's instructions or adding a new simple tool. Re-run to see your changes.

## Next Steps

* Dive deep into the official **`google-adk` documentation** ([https://google.github.io/adk-docs/](https://google.github.io/adk-docs/)) to learn about advanced agent types, tool creation, state management, orchestration, and evaluation.
* Implement more sophisticated tools relevant to your use case in the `tools/` directory.
* Refine your agent's instructions and capabilities in `adk/agent.py`.
* Once you are satisfied with local development, proceed to deploy your application to Cloud Run using `poetry run gen-bootstrap deploy`.
