# cli/monitoring_cli.py
import os
import shutil
import subprocess

import typer
from typing_extensions import Annotated

# Attempt to load project_settings from the main CLI's structure
try:
    from config.settings import settings as project_settings

    # A list of APIs expected to be enabled by setup_gcp, including monitoring
    EXPECTED_APIS_TO_ENABLE = [
        "run.googleapis.com",
        "iam.googleapis.com",
        "secretmanager.googleapis.com",
        "aiplatform.googleapis.com",
        "logging.googleapis.com",
        "monitoring.googleapis.com",  # Important one for this module
        "cloudbuild.googleapis.com",
        "artifactregistry.googleapis.com",
    ]
except ImportError:
    project_settings = None  # Fallback if settings cannot be loaded
    EXPECTED_APIS_TO_ENABLE = ["monitoring.googleapis.com"]  # Minimal fallback
    typer.secho(
        "Warning: Could not load project settings for monitoring_cli.py. "
        "GCP Project ID checks may be limited.",
        fg=typer.colors.YELLOW,
    )


app = typer.Typer(
    name="monitoring",
    help="Manage Cloud Monitoring setup, dashboards, and alerts for the project.",
    no_args_is_help=True,
)


def _get_effective_project_id(project_id_option: str | None) -> str | None:
    """Helper to determine the effective GCP Project ID."""
    if project_id_option:
        return project_id_option
    if (
        project_settings
        and hasattr(project_settings, "gcp_project_id")
        and project_settings.gcp_project_id
        and project_settings.gcp_project_id != "your-gcp-project-id"
    ):
        return project_settings.gcp_project_id
    env_project_id = os.getenv("GCP_PROJECT_ID")
    if env_project_id and env_project_id != "your-gcp-project-id":
        return env_project_id
    return None


def _check_api_enabled(project_id: str, api_name: str) -> bool:
    """Checks if a specific API is enabled for the project."""
    typer.echo(f"Checking if API '{api_name}' is enabled for project '{project_id}'...")
    cmd = [
        "gcloud",
        "services",
        "list",
        f"--project={project_id}",
        f"--filter=config.name={api_name}",
        "--format=value(config.name)",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return api_name in result.stdout
    except subprocess.CalledProcessError as e:
        typer.secho(
            f"Error checking API status for {api_name}: {e.stderr}", fg=typer.colors.RED
        )
        return False
    except FileNotFoundError:
        typer.secho(
            "ERROR: 'gcloud' CLI not found. Please install and configure it.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)


@app.command()
def setup(
    project_id: Annotated[
        str,
        typer.Option(
            "--project",
            "-p",
            help="GCP Project ID. If not provided, uses configured default or environment variable.",
        ),
    ] = None,
):
    """
    Verifies Cloud Monitoring setup and provides guidance.
    Ensures the 'monitoring.googleapis.com' API is enabled.
    """
    typer.echo("Verifying Cloud Monitoring setup...")

    if not shutil.which("gcloud"):
        typer.secho(
            "ERROR: 'gcloud' CLI not found. Please install and configure it.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    effective_project_id = _get_effective_project_id(project_id)
    if not effective_project_id:
        typer.secho(
            "GCP Project ID not determined. Please provide via --project, .env, or GCP_PROJECT_ID env var.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    typer.echo(f"Using project ID: {effective_project_id}")

    monitoring_api = "monitoring.googleapis.com"
    if _check_api_enabled(effective_project_id, monitoring_api):
        typer.secho(
            f"SUCCESS: API '{monitoring_api}' is enabled for project {effective_project_id}.",
            fg=typer.colors.GREEN,
        )
    else:
        typer.secho(
            f"WARNING: API '{monitoring_api}' is not enabled for project {effective_project_id}. "
            f"Please run 'gen-bootstrap setup-gcp --project {effective_project_id}' or enable it manually in the GCP console.",
            fg=typer.colors.YELLOW,
        )
        # Optionally, offer to enable it here, but setup-gcp is the primary tool for API enablement.

    typer.echo("\nGuidance for Cloud Monitoring:")
    typer.echo(
        "- Ensure you have a Cloud Monitoring Workspace associated with your GCP project."
    )
    typer.echo(
        "  This is often created automatically or can be set up via the GCP Console."
    )
    typer.echo(
        "- Use the 'dashboard' and 'alerts' subcommands (once implemented) to create project-specific resources."
    )
    typer.echo(f"- For more details, visit: https://cloud.google.com/monitoring/docs")


@app.command()
def dashboard():
    """
    (Not yet implemented) Creates or manages a basic monitoring dashboard.
    """
    typer.secho(
        "Command 'monitoring dashboard' is not yet implemented.", fg=typer.colors.YELLOW
    )
    typer.echo(
        "This command will be used to create/update a predefined Cloud Monitoring dashboard for key project metrics."
    )


@app.command()
def alerts():
    """
    (Not yet implemented) Creates or manages basic alert policies.
    """
    typer.secho(
        "Command 'monitoring alerts' is not yet implemented.", fg=typer.colors.YELLOW
    )
    typer.echo(
        "This command will be used to create/update predefined Cloud Monitoring alert policies for critical conditions."
    )


if __name__ == "__main__":
    app()
