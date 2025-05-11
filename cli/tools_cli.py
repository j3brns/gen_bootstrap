# cli/tools_cli.py
import importlib.util
import inspect
import os
import sys

import typer
from google.adk.tools import FunctionTool

app = typer.Typer(
    name="tools", help="Manage and inspect agent tools.", no_args_is_help=True
)

# Directory where custom tools are expected to be found
TOOLS_DIR = "tools"


@app.command("list")
def list_tools():
    """
    Lists available agent tools from the tools/ directory.
    """
    if not os.path.exists(TOOLS_DIR) or not os.path.isdir(TOOLS_DIR):
        typer.secho(f"Tools directory '{TOOLS_DIR}' not found.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    discovered_tools = _discover_tools(TOOLS_DIR)

    if not discovered_tools:
        typer.echo(f"No tools found in '{TOOLS_DIR}'.")
    else:
        typer.echo(typer.style("Available tools:", bold=True))
        for tool in sorted(
            discovered_tools, key=lambda t: t.name
        ):  # Assuming tool has .name
            typer.echo(
                f"- {typer.style(tool.name, fg=typer.colors.GREEN)}: {tool.description}"
            )  # Assuming tool has .description


def _discover_tools(tools_dir_path: str) -> list[FunctionTool]:
    """Helper function to discover FunctionTool instances in a directory."""
    discovered_tools = []
    if not os.path.exists(tools_dir_path) or not os.path.isdir(tools_dir_path):
        # This case should ideally be handled by the caller or return an empty list/raise error
        return discovered_tools

    original_sys_path = list(sys.path)
    # Add tools_dir_path to sys.path to allow direct import of modules within it
    # This is simplified; for robustness, consider if tools_dir_path is already in sys.path
    # or if it's relative and needs to be made
    # absolute.
    # For modules directly in tools_dir_path (e.g. tools_dir_path/my_tool.py),
    # their parent dir (tools_dir_path) needs to be in path for `from my_tool import...`
    # if they are not installed packages.
    # If tools_dir_path is 'tools', and project root is in sys.path,
    # then `import tools.module_name` should work.
    # The import f"tools.{module_name}" below assumes 'tools' is a package.
    # If TOOLS_DIR is an absolute path, we might need to add its parent to sys.path
    # or adjust the module name for import_module.

    # Let's assume TOOLS_DIR is a path like "tools" relative to project root,
    # and project root is in sys.path.
    # We need to ensure the modules *inside* TOOLS_DIR can be imported.
    # A common way is to add TOOLS_DIR itself to the path if modules are standalone,
    # or ensure TOOLS_DIR is a package and import its submodules.

    # The current import `f"tools.{module_name}"` implies that `TOOLS_DIR` (e.g. "tools")
    # is a package itself, or at least `tools` is a namespace from which we load.
    # If TOOLS_DIR is a path to a directory *containing* modules, not a package name itself,
    # the import logic needs care.
    # Let's stick to the spec_from_file_location which is more robust for arbitrary paths.

    if (
        tools_dir_path not in sys.path
    ):  # Ensure the specific tools_dir_path is searchable
        sys.path.insert(0, str(tools_dir_path))

    for filename in os.listdir(tools_dir_path):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name_for_spec = filename[:-3]  # e.g., "mock_tool_module"
            module_file_path = os.path.join(tools_dir_path, filename)

            # Construct a unique module name for importlib to avoid collisions
            # This could be based on the path or a fixed prefix
            # if tools_dir_path is standard.
            # For instance, if tools_dir_path is "tools", then "tools.mock_tool_module"
            # If tools_dir_path is temporary, like in tests, need a stable way.
            # Let's use a fixed prefix for dynamically loaded tool modules.
            dynamic_module_name = (
                f"genbootstrap_cli_discovered_tools.{module_name_for_spec}"
            )

            try:
                spec = importlib.util.spec_from_file_location(
                    dynamic_module_name, module_file_path
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[
                        dynamic_module_name
                    ] = module  # Important for inspect to find the module
                    spec.loader.exec_module(module)
                else:
                    # This case might not be hit if spec_from_file_location fails first
                    typer.secho(
                        f"Warning: Could not load module spec for {filename}",
                        fg=typer.colors.YELLOW,
                        err=True,
                    )
                    continue

                for name, obj in inspect.getmembers(module):
                    if isinstance(obj, FunctionTool):
                        discovered_tools.append(obj)
            except ImportError as e:
                typer.secho(
                    f"Warning: Could not import module {filename}: {e}",
                    fg=typer.colors.YELLOW,
                    err=True,
                )
            except Exception as e:
                # Print to stderr so it doesn't interfere with stdout for successful listings
                typer.secho(
                    f"Warning: Error inspecting module {filename}: {e}",
                    fg=typer.colors.YELLOW,
                    err=True,
                )

    sys.path = original_sys_path  # Restore original sys.path
    return discovered_tools


@app.command("describe")
def describe_tool(
    tool_name: str = typer.Argument(
        ...,
        help="The name of the tool to describe.",
    )
):
    """
    Shows detailed information (description, parameters, docstring) for a specified tool.
    """
    tools = _discover_tools(TOOLS_DIR)
    found_tool: FunctionTool | None = None
    for tool in tools:
        if tool.name == tool_name:  # Assuming tool has .name
            found_tool = tool
            break

    if not found_tool:
        typer.secho(f"Error: Tool '{tool_name}' not found.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.echo(typer.style(f"Tool: {found_tool.name}", bold=True, fg=typer.colors.CYAN))

    description = found_tool.description or "No description provided."
    typer.echo(typer.style("Description:", bold=True) + f" {description}")

    # Inspect the underlying function for parameters and full docstring
    if hasattr(found_tool, "func") and callable(found_tool.func):
        actual_func = found_tool.func
        sig = inspect.signature(actual_func)

        typer.echo(typer.style("Parameters:", bold=True))
        if not sig.parameters:
            typer.echo("  No parameters.")
        else:
            for name, param in sig.parameters.items():
                param_type_obj = param.annotation
                param_type_str = "Any"  # Default
                if param_type_obj != inspect.Parameter.empty:
                    if hasattr(param_type_obj, "__name__"):
                        param_type_str = param_type_obj.__name__
                    else:
                        # For complex types like typing.Union, typing.Optional, etc.
                        # str(param_type_obj) gives a better representation.
                        param_type_str = str(param_type_obj)

                default_val = (
                    f" (default: {param.default})"
                    if param.default != inspect.Parameter.empty
                    else ""
                )
                typer.echo(f"  - {name}: {param_type_str}{default_val}")

        func_doc = inspect.getdoc(actual_func)
        if (
            func_doc and func_doc.strip() != description.strip()
        ):  # Show full doc if different from .description
            typer.echo(typer.style("Function Docstring:", bold=True))
            typer.echo(func_doc)
        elif not func_doc:
            typer.echo(
                typer.style("Function Docstring:", bold=True) + " Not available."
            )

    else:
        typer.echo(
            typer.style("Parameters:", bold=True)
            + " Could not inspect underlying function."
        )
        typer.echo(
            typer.style("Function Docstring:", bold=True)
            + " Could not inspect underlying function."
        )


if __name__ == "__main__":
    app()
