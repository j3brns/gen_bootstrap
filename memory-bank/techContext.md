# Technical Context

This document details the technologies used, development setup, technical constraints, dependencies, and tool usage patterns.

## Technologies Used:
- Python 3.9+
- Poetry
- Google Agent Development Kit (google-adk)
- FastAPI
- Typer
- Google Cloud Platform (GCP)
- Cloud Run
- Vertex AI
- Secret Manager
- Uvicorn (implied by FastAPI serving)
- pytest (from file structure and README mentions of testing)
- Gradio (for the test client)
- `ttok` (for token counting and trimming, via `subprocess`)
- `subprocess` module (for executing external commands within the CLI and `ttok`)
- `dotenv` library (for loading environment variables)
- `shutil` module (for file operations in the CLI, e.g., copying `.env`)
- `os` module (for interacting with the operating system, e.g., checking file existence)
- `zoneinfo` (for timezone support in tools)
- Cloud Logging library (e.g., `google-cloud-logging`)
- Cloud Trace library (e.g., `google-cloud-trace`)

## Development Setup:
- Requires Python 3.9+ and Poetry installed.
- Google Cloud SDK (`gcloud`) authenticated.
- Docker required for Cloud Build (used by `gcloud run deploy`).
- Project configuration via `.env` file, loaded using `dotenv`.
- Dependencies managed by `poetry install`.
- Pre-commit hooks for code quality.

## Technical Constraints:
- Deployment primarily targeting Cloud Run.
- Reliance on GCP services (Vertex AI, Secret Manager, Cloud Logging, Cloud Trace, Cloud Monitoring, potentially Firestore).
- Compatibility with google-adk requirements.
- Execution of external commands via `subprocess` in the CLI requires the commands (`gcloud`, `uvicorn`, `adk`, `pytest`) to be available in the environment's PATH or via `poetry run`.

## Dependencies:
- Managed by Poetry (`pyproject.toml`, `poetry.lock`). Key dependencies include `google-adk`, `fastapi`, `typer`, GCP client libraries, `pytest`, `gradio`, `python-dotenv`, `uvicorn`, `ttok` (installed from Git repository).

## Tool Usage Patterns:
- `poetry run gen-bootstrap <command>`: This is the primary way to invoke the CLI. The `gen-bootstrap` script (aliased to `cli.main:app` via `pyproject.toml`) uses Typer for command structure and argument parsing.
- **CLI Command Execution via `subprocess`:** The `gen-bootstrap` CLI commands (`cli/main.py`) frequently use Python's `subprocess` module to execute other commands within the project's Poetry environment (`poetry run`) or system commands (`gcloud`).
    - `gen-bootstrap init`: Uses `shutil.copy` and `os.path.exists` for `.env` file management. Guides the user on `poetry add google-adk` and `poetry install`.
    - `gen-bootstrap run`: Executes either `poetry run adk web <agent_path>` (if `--adk-ui-only` is used) or `poetry run uvicorn main:app --host ... --port ... --reload ...` via `subprocess`.
    - `gen-bootstrap deploy`: Orchestrates deployment by executing `gcloud run deploy --source . --region ... --project ...` via `subprocess`. It also conditionally executes `poetry run pytest ...` via `subprocess` if the `--run-tests` flag is used. It uses `shutil.which` to check for `gcloud`. Includes logic to create a default `Procfile` using standard file operations if one is missing.
    - `gen-bootstrap test`: Executes `poetry run pytest <path> ...` via `subprocess`, supporting various pytest and coverage flags. Uses `os` and `shutil` for managing coverage data files and directories.
    - `gen-bootstrap setup-gcp`: Automates enabling required GCP APIs and granting essential IAM roles (`roles/aiplatform.user`, `roles/secretmanager.secretAccessor`) to the default Compute Engine service account using `gcloud` commands via `subprocess`. Uses `shutil.which` to check for `gcloud`.
- `poetry run python test_client.py`: Executes the Gradio test client script.
- Custom tools are implemented as asynchronous Python functions wrapped by `google.adk.tools.FunctionTool`.
- `utils/token_utils.py` uses `subprocess` to execute the `ttok` command-line tool for counting and trimming tokens.
