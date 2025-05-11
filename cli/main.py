import os
import shutil
import subprocess

import typer
from dotenv import load_dotenv
from typing_extensions import Annotated

from . import prompts_cli  # Import the new prompts subcommand module
from . import tools_cli  # Import the tools subcommand module
from . import secrets_cli # Import the new secrets subcommand module

app = typer.Typer(name="gen-bootstrap")  # Set CLI name here

# Add new subcommand groups
app.add_typer(tools_cli.app, name="tools", help="Manage and inspect agent tools.")
app.add_typer(prompts_cli.app, name="prompts", help="Manage Vertex AI Prompts using vertexai.preview.prompts.")
app.add_typer(secrets_cli.app, name="secrets", help="Manage secrets in Google Secret Manager.")

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


EXPECTED_APIS_TO_ENABLE = [ # Copied from test for consistency
    "run.googleapis.com",
    "iam.googleapis.com",
    "secretmanager.googleapis.com",
    "aiplatform.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    "cloudbuild.googleapis.com",
    "artifactregistry.googleapis.com",
]

@app.command()
def test(
    path: Annotated[str, typer.Option("--path", "-p", help="Path to test file or directory.")] = "tests",
    coverage: Annotated[bool, typer.Option("--coverage", "-c", help="Enable coverage reporting.")] = False,
    html: Annotated[bool, typer.Option("--html", help="Generate HTML coverage report.")] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Enable verbose output.")] = False,
    junit: Annotated[bool, typer.Option("--junit", help="Generate JUnit XML report.")] = False,
    output_dir: Annotated[str, typer.Option("--output-dir", help="Directory for coverage reports.")] = ".coverage",
    clean: Annotated[bool, typer.Option("--clean", help="Clean coverage data before running tests.")] = False,
):
    """
    Run tests using pytest with optional coverage reporting.
    """
    typer.echo("Running tests...")
    
    # Create coverage data directory
    coverage_data_dir = ".coverage_data"
    if coverage:
        try:
            os.makedirs(coverage_data_dir, exist_ok=True)
            
            # Clean coverage data if requested
            if clean:
                typer.echo("Cleaning coverage data...")
                coverage_data_file = os.path.join(coverage_data_dir, ".coverage")
                if os.path.exists(coverage_data_file):
                    try:
                        os.remove(coverage_data_file)
                        typer.echo("Coverage data file removed.")
                    except PermissionError:
                        typer.secho(
                            f"WARNING: Could not remove coverage data file: Permission denied. "
                            f"Try closing any processes that might be using it.",
                            fg=typer.colors.YELLOW,
                        )
                    except Exception as e:
                        typer.secho(
                            f"WARNING: Could not remove coverage data file: {e}",
                            fg=typer.colors.YELLOW,
                        )
        except Exception as e:
            typer.secho(
                f"WARNING: Could not create coverage data directory: {e}",
                fg=typer.colors.YELLOW,
            )
    
    # Ensure the output directory exists if coverage is enabled
    if coverage and (html or junit):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            typer.secho(
                f"WARNING: Could not create output directory: {e}",
                fg=typer.colors.YELLOW,
            )
    
    # Build the pytest command
    pytest_cmd = ["poetry", "run", "pytest"]
    
    # Add path
    pytest_cmd.append(path)
    
    # Add verbosity
    if verbose:
        pytest_cmd.append("-v")
    
    # Add coverage options
    if coverage:
        pytest_cmd.append("--cov=.")
        
        # Add coverage report formats
        if html:
            pytest_cmd.append(f"--cov-report=html:{output_dir}/html")
        
        if junit:
            pytest_cmd.append(f"--junitxml={output_dir}/junit.xml")
            
        # Always add terminal report
        pytest_cmd.append("--cov-report=term")
    
    # Execute the command
    typer.echo(f"Executing: {' '.join(pytest_cmd)}")
    try:
        result = subprocess.run(pytest_cmd, check=False, capture_output=True, text=True)
        
        # Print stdout and stderr
        if result.stdout:
            typer.echo(result.stdout)
        if result.stderr:
            typer.secho(result.stderr, fg=typer.colors.YELLOW)
        
        if result.returncode == 0:
            typer.secho("All tests passed successfully!", fg=typer.colors.GREEN)
            
            if coverage and html:
                typer.echo(f"HTML coverage report generated in {output_dir}/html")
                typer.echo(f"Open {output_dir}/html/index.html to view the report")
                
            return result.returncode
        else:
            # Check for permission errors
            if "PermissionError" in result.stderr and ".coverage" in result.stderr:
                typer.secho(
                    "Permission error accessing coverage data file. "
                    "Try running with --clean flag or manually delete the .coverage_data directory.",
                    fg=typer.colors.RED,
                )
            
            typer.secho(f"Tests failed with return code: {result.returncode}", fg=typer.colors.RED)
            return result.returncode
            
    except FileNotFoundError:
        typer.secho("ERROR: 'poetry' or 'pytest' not found.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.secho(f"ERROR running tests: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command()
def setup_gcp(
    project_id: Annotated[str, typer.Option("--project", "-p", help="GCP Project ID. If not provided, uses configured default.")] = None,
    interactive: Annotated[bool, typer.Option(help="Enable interactive mode for confirmations.")] = False # Not used yet
):
    """
    Automates parts of GCP setup: enables APIs. (IAM and other resources TBD).
    Refers to docs/guides/manual_gcp_setup.md for full details.
    """
    typer.echo("Starting GCP setup process...")

    if not shutil.which("gcloud"):
        typer.secho(
            "ERROR: 'gcloud' CLI not found. Please install and configure it, then ensure it's in your PATH.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    effective_project_id = project_id
    if not effective_project_id:
        if hasattr(project_settings, 'gcp_project_id') and project_settings.gcp_project_id and project_settings.gcp_project_id != "your-gcp-project-id":
            effective_project_id = project_settings.gcp_project_id
        else:
            typer.secho(
                "GCP Project ID not provided via --project option and not found or not configured in project settings.",
                fg=typer.colors.RED,
            )
            typer.secho("Please provide a valid project ID using the --project option or configure it in your .env file.", fg=typer.colors.RED)
            raise typer.Exit(code=1)

    typer.echo(f"Target GCP Project ID: {effective_project_id}")

    # 1. Enable APIs
    typer.echo(f"\nAttempting to enable necessary APIs for project {effective_project_id}...")
    apis_to_enable_str = " ".join(EXPECTED_APIS_TO_ENABLE)
    enable_cmd = [
        "gcloud", "services", "enable",
        *EXPECTED_APIS_TO_ENABLE, # Unpack the list of APIs
        f"--project={effective_project_id}"
    ]
    
    typer.echo(f"Executing: {' '.join(enable_cmd)}")
    try:
        # Using check=False to handle errors manually for better output
        result = subprocess.run(enable_cmd, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            typer.secho(f"Successfully enabled/verified APIs: {apis_to_enable_str}", fg=typer.colors.GREEN)
            if result.stdout:
                typer.echo("gcloud output:\n" + result.stdout)
        else:
            typer.secho(f"Error enabling APIs. 'gcloud' exited with code {result.returncode}.", fg=typer.colors.RED)
            if result.stderr:
                typer.secho("gcloud error output:\n" + result.stderr, fg=typer.colors.RED)
            if result.stdout: # Sometimes gcloud puts error details in stdout
                 typer.secho("gcloud output:\n" + result.stdout, fg=typer.colors.RED)
            raise typer.Exit(code=1)
    except FileNotFoundError: # Should be caught by shutil.which earlier, but as a safeguard
        typer.secho("ERROR: 'gcloud' command not found during subprocess execution.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.secho(f"An unexpected error occurred while enabling APIs: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1) # Corrected indentation

    typer.echo("\nAPI enabling step complete.")

    # 2. Grant IAM role: roles/aiplatform.user to default Compute Engine SA
    typer.echo(f"\nAttempting to grant 'roles/aiplatform.user' to default Compute SA for project {effective_project_id}...")
    
    # Get project number
    get_proj_num_cmd = [
        "gcloud", "projects", "describe", effective_project_id,
        "--format=value(projectNumber)"
    ]
    typer.echo(f"Executing: {' '.join(get_proj_num_cmd)}")
    try:
        proj_num_result = subprocess.run(get_proj_num_cmd, capture_output=True, text=True, check=True)
        project_number = proj_num_result.stdout.strip()
        if not project_number:
            typer.secho("Error: Could not retrieve project number.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        
        default_sa_email = f"{project_number}-compute@developer.gserviceaccount.com"
        typer.echo(f"Default Compute SA identified: {default_sa_email}")

        # Grant roles/aiplatform.user
        grant_aiplatform_cmd = [
            "gcloud", "projects", "add-iam-policy-binding", effective_project_id,
            f"--member=serviceAccount:{default_sa_email}",
            "--role=roles/aiplatform.user",
            "--condition=None" # Explicitly set no condition
        ]
        typer.echo(f"Executing: {' '.join(grant_aiplatform_cmd)}")
        # Using check=False to handle errors manually, as add-iam-policy-binding can be noisy
        # or fail if binding already exists (though it should be idempotent).
        iam_result = subprocess.run(grant_aiplatform_cmd, capture_output=True, text=True, check=False)

        if iam_result.returncode == 0:
            typer.secho(f"Successfully granted/verified 'roles/aiplatform.user' to {default_sa_email}.", fg=typer.colors.GREEN)
            if iam_result.stdout:
                 typer.echo("gcloud output:\n" + iam_result.stdout)
        else:
            # Check if it's because the binding already exists (which is not an error for us)
            # Common message: "WARNING: Binding already exists for..." or "ERROR: (gcloud.projects.add-iam-policy-binding) User [X] does not have permission to actualize role [Y] on project [Z] or it may not exist."
            # Or "ERROR: (gcloud.projects.add-iam-policy-binding) PERMISSION_DENIED: User ... does not have resourcemanager.projects.setIamPolicy permission for project ..."
            # For now, just print warning/error. A more robust solution would parse stderr.
            if "already exists" in iam_result.stderr.lower() or "already exists" in iam_result.stdout.lower() :
                 typer.secho(f"Note: IAM binding for 'roles/aiplatform.user' to {default_sa_email} likely already exists.", fg=typer.colors.YELLOW)
                 if iam_result.stdout: typer.echo("gcloud output:\n" + iam_result.stdout)
                 if iam_result.stderr: typer.echo("gcloud stderr:\n" + iam_result.stderr)
            else:
                typer.secho(f"Error granting 'roles/aiplatform.user'. 'gcloud' exited with code {iam_result.returncode}.", fg=typer.colors.RED)
                if iam_result.stderr:
                    typer.secho("gcloud error output:\n" + iam_result.stderr, fg=typer.colors.RED)
                if iam_result.stdout:
                     typer.secho("gcloud output:\n" + iam_result.stdout, fg=typer.colors.RED)
                # We might not want to exit here if other steps can proceed, or make it conditional.
                # For now, let's treat it as a significant warning/error.
                # raise typer.Exit(code=1) 
                typer.secho("Continuing with other setup steps despite potential IAM issue.", fg=typer.colors.YELLOW)


    except subprocess.CalledProcessError as e:
        typer.secho(f"A gcloud command failed: {e.cmd}", fg=typer.colors.RED)
        if e.stderr:
            typer.secho("Error output:\n" + e.stderr, fg=typer.colors.RED)
        if e.stdout:
             typer.secho("Output:\n" + e.stdout, fg=typer.colors.RED)
        raise typer.Exit(code=1)
    except FileNotFoundError:
        typer.secho("ERROR: 'gcloud' command not found during subprocess execution.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.secho(f"An unexpected error occurred during IAM setup: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.echo("\nIAM setup for Vertex AI User role complete (or verified).")
    typer.echo("Further setup steps (Secret Manager IAM, etc.) are TBD for automation.")
    typer.echo(f"Please also consult the manual guide: docs/guides/manual_gcp_setup.md")


if __name__ == "__main__":
    app()
