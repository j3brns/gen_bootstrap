# cli/secrets_cli.py
import typer
import os # Ensure os is imported
from google.cloud import secretmanager
from config.settings import settings as project_settings # Import at module level
# For typing, if needed: from google.cloud.secretmanager_v1.types import Secret

app = typer.Typer(
    name="secrets",
    help="Manage secrets in Google Secret Manager.",
    no_args_is_help=True
)

def _get_secret_manager_client():
    """Initializes and returns a Secret Manager client."""
    try:
        client = secretmanager.SecretManagerServiceClient()
        return client
    except Exception as e:
        typer.secho(f"Error initializing Secret Manager client: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command("list")
def list_secrets(
    project_id: str = typer.Option(None, "--project-id", "-p", help="GCP Project ID. If not provided, uses configured default.")
):
    """Lists secrets in Google Secret Manager for the specified project."""
    effective_project_id = project_id
    if not effective_project_id:
        if hasattr(project_settings, 'gcp_project_id'):
            effective_project_id = project_settings.gcp_project_id
        else: 
            typer.secho("Project ID not provided and gcp_project_id not found in settings.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        if not effective_project_id or effective_project_id == "your-gcp-project-id":
            typer.secho(
                "Project ID is not configured. Please provide via --project-id or set in .env/config.",
                fg=typer.colors.RED
            )
            raise typer.Exit(code=1)
            
    client = _get_secret_manager_client()
    parent = f"projects/{effective_project_id}"

    try:
        secrets_iterable = client.list_secrets(request={"parent": parent})
        secrets_list = list(secrets_iterable)

        if not secrets_list:
            typer.echo(f"No secrets found in project {effective_project_id}.")
        else:
            typer.echo(typer.style(f"Secrets in project {effective_project_id}:", bold=True))
            for secret in secrets_list:
                secret_id_only = secret.name.split("/")[-1]
                typer.echo(f"- {secret_id_only}")
    except Exception as e:
        typer.secho(f"Error listing secrets: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command("get")
def get_secret_version(
    secret_id: str = typer.Argument(..., help="The ID of the secret (e.g., 'my-api-key')."),
    version: str = typer.Option("latest", "--version", "-v", help="The version of the secret (e.g., '3' or 'latest')."),
    project_id: str = typer.Option(None, "--project-id", "-p", help="GCP Project ID. If not provided, uses configured default.")
):
    """Retrieves and displays the payload of a specific secret version."""
    effective_project_id = project_id
    if not effective_project_id:
        if hasattr(project_settings, 'gcp_project_id'):
            effective_project_id = project_settings.gcp_project_id
        else:
            typer.secho("Project ID not provided and gcp_project_id not found in settings.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        if not effective_project_id or effective_project_id == "your-gcp-project-id":
            typer.secho(
                "Project ID is not configured. Please provide via --project-id or set in .env/config.",
                fg=typer.colors.RED
            )
            raise typer.Exit(code=1)

    client = _get_secret_manager_client()
    secret_version_name = f"projects/{effective_project_id}/secrets/{secret_id}/versions/{version}"

    try:
        response = client.access_secret_version(name=secret_version_name)
        payload = response.payload.data.decode("UTF-8")
        typer.echo(f"Value for secret '{secret_id}' (version: {version}, project: {effective_project_id}):")
        typer.echo(payload)
    except Exception as e: 
        typer.secho(f"Error accessing secret '{secret_id}' (version {version}): {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command("create")
def create_secret(
    secret_id: str = typer.Argument(..., help="The ID for the new secret (e.g., 'my-new-api-key')."),
    project_id: str = typer.Option(None, "--project-id", "-p", help="GCP Project ID. If not provided, uses configured default."),
):
    """Creates a new (empty) secret in Google Secret Manager with automatic replication."""
    effective_project_id = project_id
    if not effective_project_id:
        if hasattr(project_settings, 'gcp_project_id'):
            effective_project_id = project_settings.gcp_project_id
        else:
            typer.secho("Project ID not provided and gcp_project_id not found in settings.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        if not effective_project_id or effective_project_id == "your-gcp-project-id":
            typer.secho(
                "Project ID is not configured. Please provide via --project-id or set in .env/config.",
                fg=typer.colors.RED
            )
            raise typer.Exit(code=1)

    client = _get_secret_manager_client()
    parent = f"projects/{effective_project_id}"
    
    secret_config = {"replication": {"automatic": {}}} 

    try:
        created_secret_obj = client.create_secret(
            request={
                "parent": parent,
                "secret_id": secret_id,
                "secret": secret_config,
            }
        )
        short_id = created_secret_obj.name.split("/")[-1]
        typer.secho(
            f"Secret '{short_id}' created successfully in project {effective_project_id}.",
            fg=typer.colors.GREEN
        )
    except Exception as e: 
        typer.secho(f"Error creating secret '{secret_id}': {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command("add-version")
def add_secret_version_cmd( # Renamed function to avoid conflict with SDK
    secret_id: str = typer.Argument(..., help="The ID of the secret to add a version to."),
    data: str = typer.Option(None, "--data", help="The secret data as a string. Mutually exclusive with --data-file."),
    data_file: str = typer.Option(None, "--data-file", help="Path to a file containing the secret data. Mutually exclusive with --data."),
    project_id: str = typer.Option(None, "--project-id", "-p", help="GCP Project ID. If not provided, uses configured default.")
):
    """Adds a new version to an existing secret in Google Secret Manager."""
    if data and data_file:
        typer.secho("Error: --data and --data-file are mutually exclusive.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    if not data and not data_file:
        typer.secho("Error: Either --data or --data-file must be provided.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    secret_payload_bytes: bytes
    if data:
        secret_payload_bytes = data.encode("UTF-8")
    elif data_file: # data_file is not None
        if not os.path.exists(data_file) or not os.path.isfile(data_file):
            typer.secho(f"Error: Data file '{data_file}' not found.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        try:
            with open(data_file, "rb") as f: 
                secret_payload_bytes = f.read()
        except Exception as e:
            typer.secho(f"Error reading data file '{data_file}': {e}", fg=typer.colors.RED)
            raise typer.Exit(code=1)
    
    effective_project_id = project_id
    if not effective_project_id:
        if hasattr(project_settings, 'gcp_project_id'):
            effective_project_id = project_settings.gcp_project_id
        else:
            typer.secho("Project ID not provided and gcp_project_id not found in settings.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        if not effective_project_id or effective_project_id == "your-gcp-project-id":
            typer.secho(
                "Project ID is not configured. Please provide via --project-id or set in .env/config.",
                fg=typer.colors.RED
            )
            raise typer.Exit(code=1)

    client = _get_secret_manager_client()
    parent_secret_name = f"projects/{effective_project_id}/secrets/{secret_id}"
    payload_proto = {"data": secret_payload_bytes}

    try:
        response = client.add_secret_version(
            request={"parent": parent_secret_name, "payload": payload_proto}
        )
        new_version_id = response.name.split("/")[-1]
        typer.secho(
            f"Added new version '{new_version_id}' to secret '{secret_id}' in project {effective_project_id}.",
            fg=typer.colors.GREEN
        )
    except Exception as e: 
        typer.secho(f"Error adding version to secret '{secret_id}': {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
