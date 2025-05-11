# cli/prompts_cli.py
import typer
import os # Re-add os import
from google.cloud import aiplatform # For aiplatform.init
from vertexai.preview import prompts
from vertexai.preview.prompts import Prompt as LocalPrompt # Moved to top level

app = typer.Typer(
    name="prompts",
    help="Manage Vertex AI Prompts using vertexai.preview.prompts.",
    no_args_is_help=True
)

# Default location, can be overridden by option
DEFAULT_LOCATION = "us-central1"

def _initialize_vertexai(project_id: str | None, location: str | None):
    """Initializes Vertex AI with project and location, loading from config if necessary."""
    final_project_id = project_id
    final_location = location or DEFAULT_LOCATION

    if not final_project_id:
        try:
            from config.settings import settings as project_settings
            final_project_id = project_settings.gcp_project_id
        except ImportError:
            typer.secho("Project ID not provided and could not load from config.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
    
    if not final_project_id or final_project_id == "your-gcp-project-id":
        typer.secho(
            "Project ID is not configured. Please provide via --project-id or set in .env/config.",
            fg=typer.colors.RED
        )
        raise typer.Exit(code=1)
    
    try:
        aiplatform.init(project=final_project_id, location=final_location)
        typer.echo(f"Initialized Vertex AI for project: {final_project_id}, location: {final_location}")
        return final_project_id, final_location
    except Exception as e:
        typer.secho(f"Error initializing Vertex AI: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command("list")
def list_prompts_from_vertex(
    project_id: str = typer.Option(None, "--project-id", "-p", help="GCP Project ID. If not provided, uses configured default."),
    location: str = typer.Option(DEFAULT_LOCATION, "--location", "-l", help="GCP Location/Region for Vertex AI.")
):
    """Lists available Prompts in Vertex AI Prompt Registry."""
    effective_project_id, effective_location = _initialize_vertexai(project_id, location)

    try:
        retrieved_prompts = prompts.list() # Uses the initialized project/location
        
        if not retrieved_prompts:
            typer.echo(f"No prompts found in project {effective_project_id} (location: {effective_location}).")
        else:
            typer.echo(typer.style(f"Prompts in project {effective_project_id} (location: {effective_location}):", bold=True))
            # The 'prompts.list()' returns a list of 'Prompt' objects from vertexai.preview.prompts
            # Each object should have attributes like 'prompt_name', 'id', 'version_id', etc.
            for p in sorted(retrieved_prompts, key=lambda x: x.prompt_name if hasattr(x, 'prompt_name') else str(x.id)):
                name_to_display = p.prompt_name if hasattr(p, 'prompt_name') and p.prompt_name else f"ID: {p.id}"
                version_info = f"(Version: {p.version_id})" if hasattr(p, 'version_id') and p.version_id else ""
                typer.echo(f"- {name_to_display} {version_info}")
    except Exception as e:
        typer.secho(f"Error listing prompts from Vertex AI: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command("get")
def get_prompt_from_vertex(
    prompt_id: str = typer.Argument(..., help="The ID of the Prompt to retrieve from Vertex AI."),
    version_id: str = typer.Option(None, "--version", "-v", help="Specific version ID of the prompt. If None, retrieves the default version."),
    project_id: str = typer.Option(None, "--project-id", "-p", help="GCP Project ID. If not provided, uses configured default."),
    location: str = typer.Option(DEFAULT_LOCATION, "--location", "-l", help="GCP Location/Region for Vertex AI.")
):
    """Displays the details of a specific Prompt from Vertex AI Prompt Registry."""
    effective_project_id, effective_location = _initialize_vertexai(project_id, location)
    
    try:
        # The prompts.get() function takes prompt_id (which is the resource name or numeric ID)
        # and optionally version_id.
        # Example from notebook: prompts.get("8464170802747539456")
        # Example with version: prompts.get(prompt_id=..., version_id=...)
        
        retrieved_prompt = prompts.get(prompt_id=prompt_id, version_id=version_id) # Uses initialized project/location
        
        if not retrieved_prompt: # Should raise an error if not found, but good to check
            typer.secho(f"Error: Prompt ID '{prompt_id}' not found.", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        typer.echo(typer.style(f"Prompt Details (ID: {retrieved_prompt.id}):", bold=True))
        if hasattr(retrieved_prompt, 'prompt_name') and retrieved_prompt.prompt_name:
            typer.echo(f"  Name: {retrieved_prompt.prompt_name}")
        if hasattr(retrieved_prompt, 'version_id') and retrieved_prompt.version_id:
            typer.echo(f"  Version ID: {retrieved_prompt.version_id}")
        
        # Displaying the prompt data (template)
        if hasattr(retrieved_prompt, 'prompt_data') and retrieved_prompt.prompt_data:
            typer.echo(typer.style("  Prompt Template:", bold=True))
            typer.echo(retrieved_prompt.prompt_data)
        
        # Displaying system instruction
        if hasattr(retrieved_prompt, 'system_instruction') and retrieved_prompt.system_instruction:
            typer.echo(typer.style("  System Instruction:", bold=True))
            typer.echo(retrieved_prompt.system_instruction)
            
        # Displaying variables
        if hasattr(retrieved_prompt, 'variables') and retrieved_prompt.variables:
            typer.echo(typer.style("  Variables:", bold=True))
            for var_info in retrieved_prompt.variables:
                 # var_info is typically a dict like {"artist": "acdc"} or just a string key
                if isinstance(var_info, dict):
                    for k, v_example in var_info.items():
                        typer.echo(f"    - {k} (Example: {v_example})")
                else: # Assuming it's just a string key
                    typer.echo(f"    - {var_info}")
        
        # Displaying model name
        if hasattr(retrieved_prompt, 'model_name') and retrieved_prompt.model_name:
            typer.echo(f"  Model: {retrieved_prompt.model_name}")

    except Exception as e: # Catching google.api_core.exceptions.NotFound or similar
        typer.secho(f"Error retrieving prompt '{prompt_id}': {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command("create")
def create_prompt_in_vertex(
    file: str = typer.Option(..., "--file", "-f", help="Path to the local prompt definition YAML file."),
    project_id: str = typer.Option(None, "--project-id", "-p", help="GCP Project ID. If not provided, uses configured default."),
    location: str = typer.Option(DEFAULT_LOCATION, "--location", "-l", help="GCP Location/Region for Vertex AI.")
):
    """
    Creates a new Prompt in Vertex AI Prompt Registry from a local YAML definition file.
    If a prompt with the same 'prompt_name' exists, this will create a new version.
    """
    if not os.path.exists(file) or not os.path.isfile(file):
        typer.secho(f"Error: Prompt definition file '{file}' not found.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    try:
        import yaml # PyYAML
        # LocalPrompt is now imported at module level

        with open(file, "r", encoding="utf-8") as f:
            prompt_def_data = yaml.safe_load(f)

        if not isinstance(prompt_def_data, dict):
            typer.secho(f"Error: Invalid format in '{file}'. Expected a YAML dictionary.", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        # Validate required fields (based on notebook example)
        required_fields = ["prompt_name", "prompt_data", "model_name"] # system_instruction and variables are optional
        for field in required_fields:
            if field not in prompt_def_data:
                typer.secho(f"Error: Missing required field '{field}' in prompt definition file '{file}'.", fg=typer.colors.RED)
                raise typer.Exit(code=1)
        
        # Construct the local Prompt object
        # The LocalPrompt constructor takes keyword arguments matching its attributes
        
        # Initialize Vertex AI only after file parsing and validation are successful
        effective_project_id, effective_location = _initialize_vertexai(project_id, location)

        local_prompt = LocalPrompt(
            prompt_name=prompt_def_data.get("prompt_name"),
            prompt_data=prompt_def_data.get("prompt_data"),
            model_name=prompt_def_data.get("model_name"),
            system_instruction=prompt_def_data.get("system_instruction"), # Optional
            variables=prompt_def_data.get("variables") # Optional
        )
        
        typer.echo(f"Attempting to create/update prompt '{local_prompt.prompt_name}' in Vertex AI...")
        saved_prompt = prompts.create_version(prompt=local_prompt) # Uses initialized project/location

        typer.secho(
            f"Successfully created/updated prompt: {saved_prompt.prompt_name} "
            f"(ID: {saved_prompt.id}, Version: {saved_prompt.version_id})",
            fg=typer.colors.GREEN
        )

    except yaml.YAMLError as e:
        typer.secho(f"Error parsing YAML from file '{file}': {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    # Let typer.Exit from validation propagate without being caught by the generic Exception
    except typer.Exit:
        raise
    except ImportError: # Should not happen if PyYAML is installed
        typer.secho("Error: PyYAML library is not installed. Please install it.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    except Exception as e: # Catch other potential errors, e.g., from prompts.create_version()
        typer.secho(f"Error creating prompt in Vertex AI: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

# Placeholder for update command (which might be similar to create if create_version handles updates)

if __name__ == "__main__":
    app()
