# Detailed Project Plan: GCP Generative AI ADK Scaffold and CLI

This document outlines the detailed plan for creating a scaffold and command-line interface (CLI) to accelerate the development of generative AI projects using the Google Agent Development Kit (ADK) on Google Cloud Platform (GCP).

## Current Status (May 2025)

The project has made significant progress, with most Alpha phase deliverables complete and substantial advancement into the Beta phase. Some Gamma phase features (like `setup-gcp` automation) are also in progress. Here's a high-level overview:

* **Alpha Phase**: [DONE] - Core scaffold, basic CLI commands, and project structure are in place.
* **Beta Phase**: [IN PROGRESS] - Most CLI commands for resource management (tools, prompts, secrets, test execution) are implemented. Some integration with GCP services is complete.
* **Gamma Phase**: [IN PROGRESS] - Key features like `setup-gcp` automation, `cli deploy` test integration, and initial `monitoring` CLI commands are now complete or in progress. Other areas like full monitoring, evaluation, and state management are still planned.

The following sections include status markers ([DONE], [IN PROGRESS], [TODO]) to provide a more detailed view of progress against the plan.

## Project Goals

1.  Provide a structured scaffold for generative AI projects built using the Google ADK.
2.  Develop a CLI for managing the ADK project lifecycle (setup, deployment, prompt management, secret management, testing, tool management, optional Weave integration, etc.).
3.  Integrate key GCP services for AI (specifically leveraging Vertex AI Prompt Classes), logging, tracing, deployment, and secret management, making them accessible within the ADK framework.
4.  Include features for token handling using `token_count_trim`, retries, and safety, designed to work with ADK agents, tools, Vertex AI Prompt Classes, and securely retrieved secrets.
5.  Establish a clear testing strategy and structure within the scaffold.
6.  Provide a clear structure and mechanism for defining and using external tools/functions within ADK agents.
7.  Offer optional integration with Weave for enhanced logging, tracing, and visualization.
8.  Provide guidance on organizing notebooks and integrate pre-commit hooks for code quality.
9.  Automate the provisioning of essential GCP resources (Gamma phase).
10. Support Memory and State Management for stateful agents using external storage (Gamma phase).
11. Include basic Monitoring and Alerting setup via the CLI (Gamma phase).

## Proposed Project Structure

The project will follow a modular structure to separate concerns and facilitate development.

```mermaid
graph TD
    A[Project Root] --> B[adk/]
    A --> C[tools/]
    A --> D[cli/]
    A --> E[config/]
    A --> F[utils/]
    A --> G[deployment/]
    A --> H[prompts/ (Optional)]
    A --> I[evaluation/ (Optional)]
    A --> J[tests/]
    A --> K[notebooks/]
    A --> L[README.md]
    A --> M[pyproject.toml]
    A --> N[poetry.lock]
    A --> O[main.py (or equivalent)]
    A --> P[.pre-commit-config.yaml]
    A --> Q[docs/]
    Q --> Q1[plan/]
    Q --> Q2[adrs/]
    Q --> Q3[features/]
```

*   `adk/`: Contains the core Google ADK agents, flows, and components.
*   `tools/`: Houses definitions and implementations of external tools used by agents.
*   `cli/`: Source code for the command-line interface.
*   `config/`: Configuration files for the project and GCP settings.
*   `utils/`: Shared utility functions and modules (GCP client wrappers, logging, token handling, retries, secret management, state management).
*   `deployment/`: Contains deployment-specific files like the `Dockerfile`.
*   `prompts/`: (Optional) Directory for local prompt development or versioning before uploading to Vertex AI Prompt Classes.
*   `evaluation/`: (Optional) Directory for evaluation scripts, datasets, and results.
*   `tests/`: Contains unit and integration tests.
*   `notebooks/`: Jupyter notebooks for experimentation and prototyping.
*   `docs/`: Project documentation (plan, ADRs, feature cards).
*   `README.md`: Project overview, setup, and usage instructions.
*   `pyproject.toml`: Poetry configuration and project dependencies.
*   `poetry.lock`: Poetry lock file for reproducible dependencies.
*   `main.py`: The main entry point for the ADK application.
*   `.pre-commit-config.yaml`: Configuration for pre-commit hooks.

## Technology Stack

*   **Language:** Python
*   **Package Manager:** Poetry
*   **CLI Framework:** Typer/Click
*   **Web Framework (if needed for ADK app):** FastAPI/Uvicorn
*   **Testing Framework:** pytest
*   **Mocking:** unittest.mock or pytest-mock
*   **Token Management:** `token_count_trim` package
*   **GCP Client Libraries:** `google-cloud-aiplatform`, `google-cloud-logging`, `google-cloud-trace`, `google-cloud-secret-manager`, `google-cloud-monitoring` (for CLI/setup), client libraries for chosen state storage (e.g., `google-cloud-firestore`).
*   **External API Interaction:** `requests` or `httpx`.
*   **Optional Observability:** `weave-lang`
*   **Development Tools:** `jupyterlab` or `notebook`, `pre-commit`, `black`, `isort`, `flake8`, `nbstripout`.
*   **GCP CLI:** `gcloud` (required in user environment for deployment and provisioning).
*   **Containerization:** Docker (required in user environment for building images, or rely on Cloud Build).

## Phased Development Plan

The project will be developed iteratively in three phases: Alpha, Beta, and Gamma.

### Alpha Phase (Core Scaffold and Basic Functionality)

*   **Focus:** Establish the fundamental project structure, core technologies, basic GCP integration, and essential CLI commands to get a simple ADK agent running locally and deployed to Cloud Run with basic logging and token management.
*   **Deliverables:**
    *   [DONE] Basic directory structure (`adk/`, `cli/`, `config/`, `utils/`, `deployment/`, `tests/`, `notebooks/`, `docs/`, `README.md`, `pyproject.toml`, `.pre-commit-config.yaml`).
    *   [DONE] Initial `pyproject.toml` with core dependencies (Poetry, Typer, FastAPI/Uvicorn, basic GCP libs, `token_count_trim`, dev dependencies like `pytest`, `pre-commit`, formatters/linters, `jupyterlab`).
    *   [DONE] Initial `.pre-commit-config.yaml` with basic hooks (formatting, linting, notebook output stripping).
    *   [DONE] Basic GCP Client Setup and SDK Wrapping in `utils/`.
    *   [DONE] A simple "Hello World" style example ADK agent in `adk/`.
    *   [DONE] Basic Structured Logging integration with Cloud Logging in `utils/`.
    *   [DONE] Basic Token Management using `token_count_trim` in `utils/`.
    *   [DONE] Basic Cloud Run Packaging (`Dockerfile`) for the simple agent.
    *   **CLI Commands:**
        *   [DONE] `gen-bootstrap init`: Project and environment setup.
        *   [DONE] `gen-bootstrap run`: Local execution of FastAPI server or ADK Web UI.
        *   [DONE] `gen-bootstrap deploy`: Basic deployment to Cloud Run.
    *   [DONE] Initial `tests/` structure and basic unit tests for `utils/`.
    *   [DONE] Initial `notebooks/` structure and a basic example notebook.
    *   [DONE] Initial `docs/` structure with placeholder files.

### Beta Phase (Enhanced GCP Integration, Core Agent Features, Basic Testing)

*   **Focus:** Build upon the Alpha foundation by integrating more key GCP services, adding core agent capabilities like prompt management and secret handling, and establishing a more robust testing framework.
*   **Deliverables:**
    *   [DONE] Full integration with **Vertex AI Prompt Classes** for fetching and listing prompts via `utils/`.
    *   [DONE] Integration with **Google Secret Manager** for securely retrieving secrets via `utils/`.
    *   [DONE] Initial implementation of **Tool Use / Function Calling**: `tools/` directory, tool interface, simple example tools, agent logic to use tools.
    *   [IN PROGRESS] Integration with **Cloud Trace** in `utils/`.
    *   [IN PROGRESS] Enhanced logging to include detailed request/response logging for model and tool interactions, correlated with trace IDs.
    *   **CLI Commands:**
        *   `gen-bootstrap prompts`:
            *   [DONE] `prompts list`: Lists available Prompts in Vertex AI Prompt Registry.
            *   [DONE] `prompts get <prompt_id>`: Displays details of a specific Prompt.
            *   [DONE] `prompts create --file <path.yaml>`: Creates a new Prompt (or new version) in Vertex AI.
        *   `gen-bootstrap secrets`:
            *   [DONE] `secrets list`: Lists secrets in Google Secret Manager.
            *   [DONE] `secrets get <secret_id>`: Retrieves secret payload.
            *   [DONE] `secrets create <secret_id>`: Creates a new (empty) secret.
            *   [DONE] `secrets add-version <secret_id>`: Adds a new secret version.
        *   `gen-bootstrap tools`:
            *   [DONE] `tools list`: Lists available agent tools.
            *   [DONE] `tools describe <tool_name>`: Shows detailed information about a specific tool.
        *   [DONE] `gen-bootstrap test`: Command to run tests (core functionality and initial tests implemented).
    *   [IN PROGRESS] More comprehensive unit tests and initial integration tests (recent additions for `cli test`, `get_current_time_async`, and `adk.agent` configuration).
    *   [DONE] Guidance on setting up IAM permissions for Cloud Run service identity.

### Gamma Phase (Advanced Features, Observability, Evaluation, Refinement)

*   **Focus:** Add more advanced features, enhance observability and evaluation capabilities, and refine the overall scaffold and CLI based on feedback and more complex use cases.
*   **Deliverables:**
    *   [TODO] **Optional Weave Integration:** Implement conditional logging and tracing to Weave in `utils/`.
    *   [TODO] Implement more sophisticated **Token Management** strategies (e.g., summarization) in `utils/`.
    *   [TODO] Implement basic **Memory and State Management** patterns or examples within `adk/` using an external store (e.g., Firestore).
    *   [TODO] Provide examples or patterns for building more **Complex Orchestration / Agent Flows** in `adk/`.
    *   [TODO] Refine Tool Use implementation.
    *   [TODO] **Evaluation Framework:** `evaluation/` directory, `cli evaluate` command, structure for evaluation scripts and data.
    *   **GCP Resource Provisioning Automation:**
        *   [IN PROGRESS] `gen-bootstrap setup-gcp`: Command to automate creation of key GCP resources using `gcloud`. Currently implements API enablement and IAM policy configuration.
    *   **Monitoring and Alerting:**
        *   [IN PROGRESS] `gen-bootstrap monitoring setup/dashboard/alerts`: Commands to configure Cloud Monitoring. Initial `setup` command implemented; `dashboard` and `alerts` are stubs.
    *   [IN PROGRESS] More comprehensive integration tests.
    *   [TODO] Set up the structure and initial scripts for Evaluation Tests.
    *   [DONE] Integrate test execution into the `cli deploy` command (optional).
    *   [TODO] Provide guidance or templates for **CI/CD pipeline integration**.
    *   [IN PROGRESS] Comprehensive `README.md` and detailed documentation in `docs/`.

## Key Components and Implementation Details

### CLI (`cli/`)

*   Built with Typer/Click.
*   Orchestrates project tasks by calling functions in `utils/` and executing `gcloud`/`docker` commands.
*   Commands for initialization, running, deployment, prompt management, secret management, tool management, testing, evaluation, monitoring setup, and GCP provisioning.

### Utilities (`utils/`)

*   Houses shared, reusable code.
*   **GCP Client Wrappers:** Functions to initialize and interact with Google Cloud SDKs (Vertex AI, Logging, Trace, Secret Manager, State Storage). Handles authentication.
*   **Logging:** Structured logging to Cloud Logging, including request/response details and trace correlation. Optional Weave logging.
*   **Tracing:** Integration with Cloud Trace and optionally Weave for end-to-end request tracing.
*   **Token Management:** Uses `token_count_trim` for counting and truncation. Provides functions for agents to check token usage and trim input/history.
*   **Retries:** Implements retry logic for unreliable external calls (GCP APIs, external tools).
*   **Secret Management:** Functions to retrieve secrets from Google Secret Manager.
*   **State Management:** Functions to load and save agent state/conversation history to an external store (e.g., Firestore).

### ADK Agents (`adk/`)

*   Implement the core agent logic using the Google ADK framework.
*   Utilize functions from `utils/` for interacting with GCP services, managing state, handling tokens, and logging.
*   Integrate with tools defined in `tools/`.

### Tools (`tools/`)

*   Directory for defining and implementing external tools.
*   Tools follow a standard interface.
*   Tool implementations use `utils/` for secure secret retrieval and robust external calls.
*   Tools provide descriptions and schemas for the generative model.

### Prompt Management (Vertex AI Prompt Classes)

*   Vertex AI Prompt Classes are the central repository for prompts.
*   `utils/` provides functions to fetch Prompt Classes by name and version.
*   CLI commands manage Prompt Classes in Vertex AI.
*   Agents fetch prompts dynamically using `utils/`.

### Secret Management (Google Secret Manager)

*   Google Secret Manager stores sensitive information.
*   `utils/` provides functions to retrieve secret versions.
*   CLI commands manage secrets in Secret Manager.
*   Cloud Run service identity requires IAM permissions to access secrets.

### Token Management (`token_count_trim`)

*   Uses the `token_count_trim` package for accurate token counting and text truncation.
*   Utilities in `utils/` wrap `token_count_trim` functions for easy use by agents.

### Testing (`tests/`)

*   Uses `pytest` as the framework.
*   Structure for unit (`tests/unit/`) and integration (`tests/integration/`) tests.
*   Uses mocking (`unittest.mock`/`pytest-mock`) for external dependencies.
*   CLI command `cli test` to run tests.
*   Pre-commit hooks include linting and formatting.

### Notebooks (`notebooks/`)

*   Directory for Jupyter notebooks for experimentation and prototyping.
*   Suggested organization into subdirectories (e.g., `exploration/`, `prototyping/`).
*   Run within the project's Poetry environment.
*   Pre-commit hook (`nbstripout`) to remove outputs.

### Evaluation (`evaluation/`)

*   (Optional) Directory for evaluation scripts, datasets, and results.
*   `cli evaluate` command to trigger evaluation runs.
*   Leverages logging (and optionally Weave) to record evaluation details and results.

### Deployment (`deployment/`)

*   Contains the `Dockerfile` for containerizing the ADK application.
*   `cli deploy` command orchestrates building the Docker image, pushing to a registry, and deploying to Cloud Run.
*   Configures environment variables (including secret references) and guides on IAM permissions.

### Memory and State Management

*   (Gamma Phase)
*   Integrates with external GCP state storage (e.g., Firestore).
*   `utils/` module for loading and saving state.
*   Agents use `utils/` to manage state across requests.

### Monitoring and Alerting

*   (Gamma Phase)
*   Leverages Cloud Run built-in metrics and log-based metrics from Cloud Logging.
*   `cli monitoring setup` command to configure basic dashboards and alerting policies in Cloud Monitoring.

### GCP Resource Provisioning Automation

*   (Gamma Phase)
*   `cli setup gcp` command to automate creation of key GCP resources using `gcloud`.
*   Interactive process with user confirmation.

## Experimentation Support

*   **Notebooks:** Primary environment for interactive prototyping.
*   **Modular Utilities:** Easy to swap models, test functions.
*   **Vertex AI Prompt Classes:** Versioning for prompt A/B testing.
*   **Tool Definitions:** Easy to prototype and swap tools.
*   **CLI `run`:** Quick local testing.
*   **Evaluation Framework:** Offline A/B testing and performance comparison.
*   **Optional Weave:** Experiment tracking and visualization.
*   **Configuration Files:** Parameterize experiments.
*   **Code Organization:** Suggested patterns for notebooks and evaluation code.

## A/B Testing Support

*   **Prompt A/B Testing:** Use Vertex AI Prompt Class versions and conditional fetching in agent code based on configuration or runtime parameters.
*   **Model A/B Testing:** Pass model identifiers to `utils/` wrappers and conditionally select models in agent code or deployment configurations.
*   **Evaluation Framework:** Compare performance of different configurations offline.
*   **Optional Weave:** Track and visualize A/B test runs and compare results.

## Code Quality

*   **Pre-commit Hooks:** Configured via `.pre-commit-config.yaml` for automatic formatting (`black`), sorting imports (`isort`), linting (`flake8`), and notebook output stripping (`nbstripout`).
*   **Testing:** Comprehensive unit and integration tests.

## Documentation (`docs/`)

*   Houses project documentation.
*   `plan/`: Detailed plan and executive overview.
*   `adrs/`: Architecture Decision Records for key decisions.
*   `features/`: Feature cards outlining specific functionalities.

This detailed plan provides a roadmap for building the GCP Generative AI ADK Scaffold and CLI, incorporating the features and considerations we discussed.
