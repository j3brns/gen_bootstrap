# cli/prompts_cli.py
import os

import typer

# NOTE: Vertex AI Prompt Registry SDK integration is deferred due to import issues
# with the current google-cloud-aiplatform version.
# This implementation temporarily lists prompts from a local 'prompts/' directory.

app = typer.Typer(
    name="prompts",
    help="Manage local prompt definition files (Vertex AI integration TBD).",
    no_args_is_help=True,
)

PROMPTS_DIR = "prompts"  # Local directory for prompts


@app.command("list")
def list_prompts(
    # project_id: str = typer.Option(None, "--project-id", "-p", help="GCP Project ID (currently unused)."),
    # location: str = typer.Option("us-central1", "--location", "-l", help="GCP Location/Region (currently unused).")
):
    """
    Lists available prompt definition files from the local 'prompts/' directory.
    (Vertex AI integration is currently deferred).
    """
    typer.echo(f"Listing prompts from local directory: '{PROMPTS_DIR}'")
    typer.echo("(Note: Vertex AI Prompt Registry integration is currently deferred.)")

    if not os.path.exists(PROMPTS_DIR) or not os.path.isdir(PROMPTS_DIR):
        typer.echo(f"Directory '{PROMPTS_DIR}/' not found.")
        typer.echo(
            "Please create it and add your prompt definition files (e.g., .txt, .md, .yaml)."
        )
        return

    prompt_files = [
        f
        for f in os.listdir(PROMPTS_DIR)
        if os.path.isfile(os.path.join(PROMPTS_DIR, f))
        and not f.startswith(".")
        and f != "__init__.py"
    ]

    if not prompt_files:
        typer.echo(f"No prompt files found in '{PROMPTS_DIR}/'.")
    else:
        typer.echo(typer.style("Available local prompt files:", bold=True))
        for pf in sorted(prompt_files):
            typer.echo(f"- {pf}")


@app.command("get")
def get_prompt(
    prompt_filename: str = typer.Argument(
        ...,
        help="The filename of the prompt to retrieve from the local 'prompts/' directory.",
    )
):
    """
    Displays the content of a specific prompt file from the local 'prompts/' directory.
    (Vertex AI integration is currently deferred).
    """
    typer.echo(
        f"(Note: Vertex AI Prompt Registry integration is currently deferred for 'get' command.)"
    )

    if not os.path.exists(PROMPTS_DIR) or not os.path.isdir(PROMPTS_DIR):
        typer.secho(
            f"Error: Prompts directory '{PROMPTS_DIR}' not found.", fg=typer.colors.RED
        )
        raise typer.Exit(code=1)

    file_path = os.path.join(PROMPTS_DIR, prompt_filename)

    if not os.path.isfile(file_path):
        typer.secho(
            f"Error: Prompt file '{prompt_filename}' not found in '{PROMPTS_DIR}'.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        typer.echo(content)
    except Exception as e:
        typer.secho(
            f"Error reading prompt file '{prompt_filename}': {e}", fg=typer.colors.RED
        )
        raise typer.Exit(code=1)


# Placeholder for other prompt commands (create, update)
# These will also need to be adapted for local files or Vertex AI integration later.

if __name__ == "__main__":
    app()
