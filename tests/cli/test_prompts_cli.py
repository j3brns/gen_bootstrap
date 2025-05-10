# tests/cli/test_prompts_cli.py
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

# from cli.main import app # Will import after prompts_cli is added to main app
# from cli.prompts_cli import app as prompts_app # Will import after prompts_cli.py is created

runner = CliRunner()

import os

from cli.main import app  # Assuming cli.main.py is updated


@pytest.fixture
def prompts_dir_setup(tmp_path, monkeypatch):
    """Fixture to set up a temporary prompts directory and patch PROMPTS_DIR."""
    temp_prompts_path = tmp_path / "prompts"
    monkeypatch.setattr("cli.prompts_cli.PROMPTS_DIR", str(temp_prompts_path))
    return temp_prompts_path


def test_prompts_list_dir_not_found(prompts_dir_setup):
    """Test 'prompts list' when the prompts directory does not exist."""
    # prompts_dir_setup patches PROMPTS_DIR but doesn't create the directory itself yet.
    result = runner.invoke(app, ["prompts", "list"])
    assert result.exit_code == 0  # Command should handle gracefully
    assert f"Directory '{str(prompts_dir_setup)}/' not found." in result.stdout


def test_prompts_list_empty_dir(prompts_dir_setup):
    """Test 'prompts list' when the prompts directory is empty."""
    prompts_dir_setup.mkdir()  # Create the directory
    (
        prompts_dir_setup / "__init__.py"
    ).touch()  # Make it a package (though not strictly necessary for file listing)

    result = runner.invoke(app, ["prompts", "list"])
    assert result.exit_code == 0
    assert f"No prompt files found in '{str(prompts_dir_setup)}/'." in result.stdout


def test_prompts_list_with_prompt_files(prompts_dir_setup):
    """Test 'prompts list' with some prompt files."""
    prompts_dir_setup.mkdir()
    (prompts_dir_setup / "my_prompt.txt").write_text("This is a prompt.")
    (prompts_dir_setup / "another_prompt.md").write_text("# Another Prompt")
    (prompts_dir_setup / ".hiddenfile").write_text("hidden")

    result = runner.invoke(app, ["prompts", "list"])
    assert result.exit_code == 0
    assert "Available local prompt files:" in result.stdout
    assert "my_prompt.txt" in result.stdout
    assert "another_prompt.md" in result.stdout
    assert ".hiddenfile" not in result.stdout  # Should ignore hidden files


def test_prompts_get_file_found(prompts_dir_setup):
    """Test 'prompts get <filename>' when the prompt file is found."""
    prompts_dir_setup.mkdir()
    prompt_filename = "sample_prompt.txt"
    prompt_content = "This is the content of the sample prompt."
    (prompts_dir_setup / prompt_filename).write_text(prompt_content)

    result = runner.invoke(app, ["prompts", "get", prompt_filename])
    assert result.exit_code == 0
    assert prompt_content in result.stdout


def test_prompts_get_file_not_found(prompts_dir_setup):
    """Test 'prompts get <filename>' when the prompt file is not found."""
    prompts_dir_setup.mkdir()  # Ensure prompts dir exists but is empty for this test case

    prompt_filename = "non_existent_prompt.txt"
    result = runner.invoke(app, ["prompts", "get", prompt_filename])
    assert result.exit_code != 0
    assert (
        f"Error: Prompt file '{prompt_filename}' not found in '{str(prompts_dir_setup)}'."
        in result.stdout
    )


def test_prompts_get_prompts_dir_not_found(prompts_dir_setup):
    """Test 'prompts get <filename>' when the prompts directory itself does not exist."""
    # prompts_dir_setup only patches the path, test ensures dir is not created here
    prompt_filename = "any_prompt.txt"
    result = runner.invoke(app, ["prompts", "get", prompt_filename])
    assert result.exit_code != 0  # Or 0 if it prints a specific message like list
    assert (
        f"Error: Prompts directory '{str(prompts_dir_setup)}' not found."
        in result.stdout
    )
