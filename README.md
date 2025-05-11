# GCP Generative AI Scaffold (gen-bootstrap)

This project provides a scaffold and command-line interface (CLI) named `gen-bootstrap` (invoked via `poetry run gen-bootstrap`) to accelerate the development of generative AI projects using the **official Google Agent Development Kit (google-adk)** on Google Cloud Platform (GCP).

It aims to provide a well-structured project foundation, integrate `google-adk` for agent logic, and automate common tasks throughout the development lifecycle, from local development to deployment on Cloud Run.

## Core Technologies

* **Python 3.9+**
* **Poetry** for dependency management.
* **Google Agent Development Kit (`google-adk`)** for agent logic and orchestration.
* **FastAPI** for serving the agent via HTTP (integrated with `google-adk`).
* **Typer** for the CLI (`gen-bootstrap`).
* **Google Cloud Platform (GCP)** for deployment (Cloud Run) and services (Vertex AI, Secret Manager, etc.).

## Features (Current Implementation)

* Project structure designed for `google-adk` based applications.
* Core agent logic defined in `adk/agent.py` using `google.adk.agents.LlmAgent`.
* Example custom tool in `tools/example_tool.py` using `google.adk.tools.FunctionTool`.
* Functional CLI (`gen-bootstrap`) for:
    * `init`: Project and environment setup (guides on `google-adk` install).
    * `run`: Local execution of the FastAPI server (serving the ADK agent) OR direct launch of ADK Web UI.
    * `deploy`: Basic deployment of the ADK-powered FastAPI app to Cloud Run.
    * `setup-gcp`: Guidance for manual GCP resource setup.
    * `tools list`: Lists available agent tools found in the `tools/` directory.
    * `tools describe <tool_name>`: Shows detailed information about a specific agent tool.
    * `prompts list`: Lists available Prompts in Vertex AI Prompt Registry.
    * `prompts get <prompt_id>`: Displays details of a specific Prompt from Vertex AI Prompt Registry.
    * `prompts create --file <path.yaml>`: Creates a new Prompt (or new version) in Vertex AI from a local YAML definition file.
    * `secrets list`: Lists secrets in Google Secret Manager for the configured project.
    * `secrets get <secret_id> [--version <version_number|latest>]`: Retrieves and displays the payload of a specific secret version.
    * `secrets create <secret_id>`: Creates a new (empty) secret in Google Secret Manager.
    * `secrets add-version <secret_id> (--data <string> | --data-file <path>)`: Adds a new version to an existing secret.
* FastAPI server (`main.py`) integrated with `google-adk` to serve the agent, including ADK Web UI.
* Basic structured logging and configuration management (`.env`).
* Example Gradio test client (`test_client.py`) for interacting with the served agent.

## Getting Started

### Prerequisites

* Python 3.9 or higher.
* Poetry ([Installation Guide](https://python-poetry.org/docs/#installation)).
* Google Cloud SDK (`gcloud` CLI authenticated - see `docs/guides/manual_gcp_setup.md`).
* Docker (for Cloud Build, used by `gcloud run deploy --source .`).

### Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone YOUR_PROJECT_REPOSITORY_URL gen-bootstrap-project
    cd gen-bootstrap-project
    ```

2.  **Configure Project Settings (`.env` file):**
    Copy the template environment file and **edit it with your specific GCP Project ID** and other necessary values (like `DEFAULT_GEMINI_MODEL` if you wish to override the default in `config/settings.py`).
    ```bash
    cp template.env .env
    # Now EDIT the .env file in the project root with your details.
    ```

3.  **Initialize Project & Install Dependencies:**
    The `init` command will guide you. It's crucial that `google-adk` is installed.
    ```bash
    poetry run gen-bootstrap init
    ```
    This typically involves running `poetry add google-adk` (if not already in `pyproject.toml` from the scaffold base) and then `poetry install`.

4.  **Manual GCP Setup:**
    Carefully follow the instructions in `docs/guides/manual_gcp_setup.md` to configure your GCP project (enable APIs, set IAM permissions, etc.). This is essential for the agent to function and deploy correctly.

5.  **Set up Pre-commit Hooks (Optional but Recommended):**
    ```bash
    poetry run pre-commit install
    ```

## Development Workflow

1.  **Define/Modify Agents:** Edit `adk/agent.py`. Use `google-adk` classes like `LlmAgent`.
2.  **Define/Modify Tools:** Create/edit files in `tools/` using `FunctionTool` or `@tool`.
3.  **Link Tools to Agent:** In `adk/agent.py`, pass your tool instances to the `tools` parameter of your `LlmAgent`.
4.  **Run & Test Locally:**
    * **Primary Method (FastAPI Server + ADK Web UI):**
        ```bash
        poetry run gen-bootstrap run
        ```
        Access the FastAPI app at `http://localhost:8080`. The ADK Web UI is often available at `http://localhost:8080/adk_web`. You can also test API endpoints like `/custom_health` or the ADK `/run` endpoint.
    * **ADK Native Web UI Only:**
        ```bash
        poetry run gen-bootstrap run --adk-ui-only --agent-path adk.agent:root_agent
        ```
    * **ADK CLI Runner:**
        ```bash
        poetry run adk run adk.agent:root_agent --input "What time is it in London?"
        ```
    * **Gradio Test Client:**
        ```bash
        poetry run python test_client.py
        ```
        (Ensure the FastAPI server from `poetry run gen-bootstrap run` is running in another terminal).

5.  **Deploy to Cloud Run:**
    When ready, deploy your application:
    ```bash
    poetry run gen-bootstrap deploy
    ```
    You will be prompted for a Cloud Run service name and region.

## Project Structure Overview

* `adk/`: Core agent logic using `google-adk`.
* `cli/`: The `gen-bootstrap` CLI implementation.
* `config/`: Application configuration (`settings.py`).
* `tools/`: Custom tools for your ADK agents.
* `utils/`: Shared utilities (logging, etc.).
* `main.py`: FastAPI application serving the ADK agent.
* `test_client.py`: Gradio UI for testing the deployed/served agent.
* `docs/`: All project documentation (ADRs, guides, tutorials).
* `template.env`: Template for environment variables.
* `pyproject.toml`: Poetry project configuration and dependencies.
* `Procfile`: (To be created by user or `deploy` command) Defines how Cloud Run starts the app.

## Documentation

* `docs/plan/`: Project vision and phased plan.
* `docs/adrs/`: Architecture Decision Records.
* `docs/guides/manual_gcp_setup.md`: **Essential** for initial GCP configuration.
* `docs/tutorials/01-getting-started.md`: Initial setup tutorial.

## Roadmap

The project has made significant progress, with most Alpha phase deliverables complete and substantial advancement into the Beta phase. Some Gamma phase features (like `setup-gcp` automation and initial monitoring CLI commands) are also in progress.

**Progress and Next Steps:**
The project is actively in the Beta phase, with many core features implemented, and Gamma phase development has commenced.
Key areas currently in progress or planned next include:
*   Finalizing Cloud Trace integration (Beta phase).
*   Completing the `gen-bootstrap monitoring dashboard` and `gen-bootstrap monitoring alerts` commands (Gamma phase).
*   Developing the Evaluation Framework, including the `gen-bootstrap evaluate` command (Gamma phase).
*   Implementing Memory and State Management capabilities for stateful agents (Gamma phase).
*   Further expanding test coverage across all components.

For a comprehensive view of our development plan and progress, please see the [Detailed Project Plan](docs/plan/detailed_plan.md).

## Contributing

Please see the `CONTRIBUTING.md` file for guidelines.

## License

[Specify your license here]

---

*This scaffold is designed to provide a robust starting point for building production-ready AI agents with Google ADK on GCP.*
