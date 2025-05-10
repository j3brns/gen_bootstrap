import os
import shutil
import subprocess

import typer
from dotenv import load_dotenv
from typing_extensions import Annotated

from . import prompts_cli  # Import the new prompts subcommand module
from . import tools_cli  # Import the tools subcommand module

app = typer.Typer(name="gen-bootstrap")  # Set CLI name here

# Add new subcommand groups
app.add_typer(tools_cli.app, name="tools", help="Manage and inspect agent tools.")
app.add_typer(prompts_cli.app, name="prompts", help="Manage Vertex AI Prompt Classes.")

# Load .env variables for CLI execution context
# This ensures project_settings can pick them up if CLI is run before app server
load_dotenv()
try:
    from config.settings import settings as project_settings
except ImportError:

    class MockSettings:  # Basic fallback
        gcp_project_id: str = "your-gcp-project-id"
        default_gemini_model: str = "gemini-1.5-pro-latest"

    project_settings = MockSettings()
    typer.secho(
        "Warning: Could not load project settings from config. Fallback used.",
        fg=typer.colors.YELLOW,
    )


@app.command()
def init():
    """Initializes the project: .env setup, guides on dependencies and pre-commit."""
    typer.echo("Initializing GCP Generative AI ADK Scaffold project (gen-bootstrap)...")

    typer.echo("\nKey Dependencies:")
    typer.echo(
        "  - This scaffold uses 'google-adk'. If not yet added via Phase 0, run:"
    )
    typer.echo("    `poetry add google-adk`")
    typer.echo("  - Ensure all dependencies are installed:")
    typer.echo("    `poetry install`")

    typer.echo("\nSetting up project configuration (.env file)...")
    if not os.path.exists(".env"):
        if os.path.exists("template.env"):
            shutil.copy("template.env", ".env")
            typer.echo("SUCCESS: '.env' file created from 'template.env'.")
            typer.secho(
                "ACTION REQUIRED: Please review and update '.env' "
                "with your GCP_PROJECT_ID.",
                fg=typer.colors.YELLOW,
            )
        else:
            typer.secho(
                "WARNING: 'template.env' not found. Create '.env' "
                "manually with GCP_PROJECT_ID.",
                fg=typer.colors.YELLOW,
            )
    else:
        typer.echo(
            "INFO: '.env' file already exists. Ensure GCP_PROJECT_ID is correctly set."
        )

    typer.echo("\nSetting up pre-commit hooks (optional but recommended)...")
    typer.echo("  If you want to use pre-commit hooks, run:")
    typer.echo("    `poetry run pre-commit install`")

    typer.echo("\nProject initialization guidance complete.")
    typer.echo('Ensure \'pyproject.toml\' has: "gen-bootstrap" = "cli.main:app"')


@app.command()
def run(
    host: Annotated[str, typer.Option(help="Host for FastAPI server.")] = "0.0.0.0",
    port: Annotated[int, typer.Option(help="Port for FastAPI server.")] = 8080,
    adk_ui_only: Annotated[
        bool, typer.Option("--adk-ui-only", help="Run only Google ADK Web UI directly.")
    ] = False,
    agent_path: Annotated[
        str,
        typer.Option(help="Agent module path for ADK UI (e.g. adk.agent:root_agent)."),
    ] = "adk.agent:root_agent",
):
    """
    Runs the application: FastAPI server by default, or ADK Web UI with --adk-ui-only.
    """
    if adk_ui_only:
        typer.echo(f"Attempting to run Google ADK Web UI for agent: {agent_path}...")
        adk_command = ["poetry", "run", "adk", "web", agent_path]
        typer.echo(f"Executing: {' '.join(adk_command)}")
        try:
            process = subprocess.Popen(adk_command)
            process.wait()
        except FileNotFoundError:
            typer.secho(
                "ERROR: 'poetry' or 'adk' (from google-adk) not found.",
                fg=typer.colors.RED,
            )
            raise typer.Exit(code=1)
        except Exception as e:
            typer.secho(f"ERROR running ADK Web UI: {e}", fg=typer.colors.RED)
            raise typer.Exit(code=1)
    else:
        typer.echo(
            f"Attempting to run FastAPI app (serving ADK agent) on {host}:{port}..."
        )
        if not os.path.exists("main.py"):
            typer.secho("ERROR: main.py not found.", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        uvicorn_command = [
            "poetry",
            "run",
            "uvicorn",
            "main:app",
            "--host",
            host,
            "--port",
            str(port),
            "--reload",
            "--reload-dir",
            ".",
        ]
        typer.echo(f"Executing: {' '.join(uvicorn_command)}")
        try:
            process = subprocess.Popen(uvicorn_command)
            process.wait()
        except FileNotFoundError:
            typer.secho("ERROR: 'poetry' or 'uvicorn' not found.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        except Exception as e:
            typer.secho(f"ERROR running FastAPI app: {e}", fg=typer.colors.RED)
            raise typer.Exit(code=1)


@app.command()
def deploy(
    service_name: Annotated[
        str,
        typer.Option(
            prompt="Cloud Run service name", help="Name for the Cloud Run service."
        ),
    ] = "",
    region: Annotated[
        str, typer.Option(prompt="GCP region", help="GCP region (e.g. us-central1).")
    ] = "",
    project_id: Annotated[
        str, typer.Option(help="GCP Project ID (overrides .env if provided).")
    ] = "",
):
    """Builds and deploys the ADK application (FastAPI server) to Cloud Run."""
    typer.echo("Attempting to deploy application to Cloud Run...")

    if not shutil.which("gcloud"):
        typer.secho(
            "ERROR: 'gcloud' CLI not found. Please install and configure it.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    effective_project_id = (
        project_id or os.getenv("GCP_PROJECT_ID") or project_settings.gcp_project_id
    )
    if not service_name or not region or effective_project_id == "your-gcp-project-id":
        typer.secho(
            "ERROR: Service name, region, and valid GCP Project ID are required.",
            fg=typer.colors.RED,
        )
        typer.secho(
            "Ensure GCP_PROJECT_ID is set in .env, passed as option, or loaded by config.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    procfile_path = "Procfile"
    if not os.path.exists(procfile_path):
        default_procfile_content = (
            "web: poetry run uvicorn main:app "
            "--host 0.0.0.0 --port $PORT --workers 1"
        )
        typer.secho(f"WARNING: '{procfile_path}' not found.", fg=typer.colors.YELLOW)
        if typer.confirm(
            f"Create default '{procfile_path}' with: '{default_procfile_content}'?"
        ):
            try:
                with open(procfile_path, "w") as pf:
                    pf.write(default_procfile_content)
                typer.echo(f"SUCCESS: '{procfile_path}' created.")
            except IOError as e:
                typer.secho(
                    f"ERROR: Could not create '{procfile_path}': {e}",
                    fg=typer.colors.RED,
                )
                raise typer.Exit(code=1)
        elif not typer.confirm(
            "Continue deployment without Procfile (highly not recommended)?"
        ):
            raise typer.Exit()

    deploy_command = [
        "gcloud",
        "run",
        "deploy",
        service_name,
        "--source",
        ".",
        "--region",
        region,
        "--project",
        effective_project_id,
        "--allow-unauthenticated",  # Common for testing; review for production
        "--platform",
        "managed",
        # Consider adding more flags as needed, e.g., --memory, --cpu, --set-env-vars
    ]
    typer.echo(f"Executing: {' '.join(deploy_command)}")
    try:
        result = subprocess.run(
            deploy_command, check=True, capture_output=True, text=True
        )
        typer.secho("SUCCESS: Deployment successful!", fg=typer.colors.GREEN)
        if result.stdout:
            typer.echo(f"Output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        typer.secho(
            f"ERROR: Deployment failed. Return code: {e.returncode}",
            fg=typer.colors.RED,
        )
        if e.stdout:
            typer.echo(f"Stdout:\n{e.stdout}")
        if e.stderr:
            typer.secho(f"Stderr:\n{e.stderr}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.secho(
            f"ERROR: An unexpected error occurred during deployment: {e}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)


@app.command()
def setup_gcp():
    """Provides guidance for manually setting up essential GCP resources."""
    typer.echo("GCP Resource Setup Guidance (Manual Steps for Alpha/Beta):")
    typer.echo("-----------------------------------------------------------")
    typer.echo("A comprehensive guide is available at: docs/guides/manual_gcp_setup.md")
    typer.echo("\nKey requirements:")
    typer.echo("1. Active GCP Project with Billing enabled.")
    typer.echo("2. `gcloud` CLI installed, authenticated, and project configured.")
    typer.echo(
        "3. Essential APIs enabled (Cloud Run, Secret Manager, Vertex AI, etc. - see guide)."
    )
    typer.echo("4. Secrets (if any) created in Secret Manager.")
    typer.echo("5. Cloud Run service identity granted IAM permissions (see guide).")
    typer.echo(
        "\nPlease refer to the full guide for detailed commands and instructions."
    )


if __name__ == "__main__":
    app()
