# tests/cli/test_tools_cli.py
import os
import shutil

import pytest
from typer.testing import CliRunner

from cli.main import \
    app  # Assuming cli.main.py will be updated to add tools subcommand

runner = CliRunner()


@pytest.fixture
def empty_tools_dir(tmp_path):
    """Creates a temporary empty tools directory."""
    tools_path = tmp_path / "tools"
    tools_path.mkdir()
    # Create an __init__.py to make it a package
    (tools_path / "__init__.py").touch()
    return tools_path


def test_tools_list_empty_dir(monkeypatch, empty_tools_dir):
    """
    Test 'gen-bootstrap tools list' when the tools directory is empty.
    """
    # We need to make the CLI command look for tools in our temporary empty_tools_dir
    # This will likely involve monkeypatching a function or a constant
    # in the tools_cli module that defines where to look for tools.
    # For now, let's assume the command will be adapted to be testable.
    # We also need to ensure the main 'app' can find the 'tools' subcommand.

    # This is a preliminary version of the test.
    # It will likely fail until tools_cli.py is created and integrated.
    # And until we can properly patch the tools directory path.

    # Let's simulate that the tools directory is 'empty_tools_dir'
    # This is a placeholder for a more robust patching mechanism later.
    # For now, we'll assume the command might print a default message if it can't find tools.
    # Or, if it tries to access a hardcoded 'tools/' relative to cwd,
    # we might need to run from a specific temp CWD.

    # For this initial TDD step, we'll just call the command and expect it to not crash,
    # and to contain some indicative text once the command structure is in place.
    # The real assertions will come after tools_cli.py is created.

    # Temporarily change CWD for the test if tools_cli.py uses relative paths for 'tools/'
    original_cwd = os.getcwd()
    # Create a dummy tools dir in the temp_path that the command might find
    project_root_for_test = empty_tools_dir.parent
    # The 'tools' dir is already created by empty_tools_dir fixture inside project_root_for_test

    # To make this test work initially, we'll assume tools_cli.py will be created
    # and will have a list command that, if it finds no tools, prints a specific message.
    # We'll also assume cli.main.py is updated to register this 'tools' subcommand.

    # This test will fail until cli.main.py and cli.tools_cli.py are set up.
    # For now, let's just assert that the command can be invoked without error
    # once the basic structure is there. The real check for "No tools found"
    # will be more robust once the tools_cli module exists.

    # For the very first run, we might just expect an error or specific help text
    # if the 'tools list' command isn't fully implemented.
    # Let's assume for now that if 'tools_cli.py' is created with a basic 'list' command,
    # and it's added to 'cli/main.py', invoking 'tools list' might just run.
    # The assertion for "No tools found" will be refined.

    # This test is more of a setup for the TDD cycle.
    # The actual assertion will be:
    # result = runner.invoke(app, ["tools", "list"])
    # assert result.exit_code == 0
    # assert "No tools found" in result.stdout # or similar message

    # Patch the TOOLS_DIR constant in the tools_cli module to use our empty temp dir
    monkeypatch.setattr("cli.tools_cli.TOOLS_DIR", str(empty_tools_dir))

    result = runner.invoke(app, ["tools", "list"])

    assert result.exit_code == 0
    # The exact message format might change, but it should indicate no tools.
    assert f"No tools found in '{str(empty_tools_dir)}'." in result.stdout


@pytest.fixture
def populated_tools_dir(tmp_path):
    """Creates a temporary tools directory with a mock tool file."""
    tools_path = tmp_path / "tools"
    tools_path.mkdir()
    (tools_path / "__init__.py").touch()  # Make it a package

    import textwrap  # Import textwrap

    # Define the mock tool content with consistent indentation
    # that textwrap.dedent can process correctly.
    mock_tool_content = textwrap.dedent(
        """
        from google.adk.tools import FunctionTool

        async def MockToolAlpha(param1: str):
            '''This is a mock tool for testing purposes.'''
            # Docstring as description
            return f"Mocked with {param1}"

        mock_tool_instance = FunctionTool(MockToolAlpha)

        async def MockToolBeta(data: int):
            '''A second mock tool for variety.'''
            # Docstring as description
            return data * 2

        another_mock_tool_instance = FunctionTool(MockToolBeta)

        not_a_tool = "just a string"
    """
    )
    (tools_path / "mock_tool_module.py").write_text(mock_tool_content)
    return tools_path


def test_tools_list_with_tools(monkeypatch, populated_tools_dir):
    """
    Test 'gen-bootstrap tools list' when the tools directory contains tool files.
    """
    monkeypatch.setattr("cli.tools_cli.TOOLS_DIR", str(populated_tools_dir))

    result = runner.invoke(app, ["tools", "list"])

    assert result.exit_code == 0
    assert "Available tools:" in result.stdout  # Or similar header
    assert "MockToolAlpha" in result.stdout
    assert "This is a mock tool for testing purposes." in result.stdout
    assert "MockToolBeta" in result.stdout
    assert "A second mock tool for variety." in result.stdout
    assert "not_a_tool" not in result.stdout  # Ensure non-tool variables are not listed


def test_tools_describe_tool_found(monkeypatch, populated_tools_dir):
    """
    Test 'gen-bootstrap tools describe <tool_name>' when the tool is found.
    """
    monkeypatch.setattr("cli.tools_cli.TOOLS_DIR", str(populated_tools_dir))
    tool_name_to_describe = "MockToolAlpha"
    result = runner.invoke(app, ["tools", "describe", tool_name_to_describe])

    assert result.exit_code == 0
    assert f"Tool: {tool_name_to_describe}" in result.stdout
    assert "Description: This is a mock tool for testing purposes." in result.stdout
    assert "Parameters:" in result.stdout
    assert (
        "param1: str" in result.stdout
    )  # Based on 'async def MockToolAlpha(param1: str)'
    # We might also want to assert the full docstring of the function itself.
    # For now, checking for key parts is sufficient for the initial test.


def test_tools_describe_tool_not_found(monkeypatch, populated_tools_dir):
    """
    Test 'gen-bootstrap tools describe <tool_name>' when the tool is not found.
    """
    monkeypatch.setattr("cli.tools_cli.TOOLS_DIR", str(populated_tools_dir))
    tool_name_to_describe = "NonExistentTool"
    result = runner.invoke(app, ["tools", "describe", tool_name_to_describe])

    assert result.exit_code != 0  # Expecting a non-zero exit code for error
    assert f"Error: Tool '{tool_name_to_describe}' not found." in result.stdout
