# tests/cli/test_prompts_cli.py
import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from cli.main import app # Main CLI app

runner = CliRunner()

# Mock the structure of the Prompt object returned by vertexai.preview.prompts
class MockSDKPrompt:
    def __init__(self, id, prompt_name, version_id=None, prompt_data=None, system_instruction=None, variables=None, model_name=None):
        self.id = str(id)
        self.prompt_name = prompt_name
        self.version_id = str(version_id) if version_id else "1" # Default to version "1" if None
        self.prompt_data = prompt_data
        self.system_instruction = system_instruction
        self.variables = variables
        self.model_name = model_name

    def __lt__(self, other): # For sorting if needed
        if self.prompt_name == other.prompt_name:
            return self.id < other.id
        return self.prompt_name < other.prompt_name


@patch("cli.prompts_cli.aiplatform.init") # Patch aiplatform.init in prompts_cli
def test_prompts_list_no_prompts_found(mock_ai_init, monkeypatch):
    """Test 'prompts list' when no Vertex AI prompts are found."""
    with patch("cli.prompts_cli.prompts.list") as mock_prompts_list:
        mock_prompts_list.return_value = [] # Simulate no prompts

        result = runner.invoke(app, ["prompts", "list", "--project-id", "test-project"])
        
        assert result.exit_code == 0
        # The command prepends an init message, then the "No prompts found" message
        assert "Initialized Vertex AI for project: test-project, location: us-central1" in result.stdout
        assert "No prompts found in project test-project (location: us-central1)." in result.stdout
        mock_ai_init.assert_called_once_with(project="test-project", location="us-central1")
        mock_prompts_list.assert_called_once()

@patch("cli.prompts_cli.aiplatform.init")
def test_prompts_list_with_prompts(mock_ai_init, monkeypatch):
    """Test 'prompts list' with some Vertex AI prompts."""
    mock_prompt1 = MockSDKPrompt(id="123", prompt_name="my-first-prompt", version_id="1", prompt_data="Hello {name}")
    mock_prompt2 = MockSDKPrompt(id="456", prompt_name="another-prompt", version_id="2", prompt_data="Test prompt")
    
    with patch("cli.prompts_cli.prompts.list") as mock_prompts_list:
        mock_prompts_list.return_value = [mock_prompt1, mock_prompt2]

        result = runner.invoke(app, ["prompts", "list", "--project-id", "test-project"])
        
        assert result.exit_code == 0
        assert "Initialized Vertex AI for project: test-project, location: us-central1" in result.stdout
        assert "Prompts in project test-project (location: us-central1):" in result.stdout
        assert "my-first-prompt (Version: 1)" in result.stdout
        assert "another-prompt (Version: 2)" in result.stdout
        mock_ai_init.assert_called_once_with(project="test-project", location="us-central1")
        mock_prompts_list.assert_called_once()

@patch("cli.prompts_cli.aiplatform.init")
def test_prompts_get_prompt_found(mock_ai_init, monkeypatch):
    """Test 'prompts get <prompt_id>' when a Vertex AI prompt is found."""
    prompt_id_to_get = "12345"
    mock_retrieved_prompt = MockSDKPrompt(
        id=prompt_id_to_get,
        prompt_name="test-prompt-alpha",
        version_id="3",
        prompt_data="Describe {subject} in one sentence.",
        system_instruction="Be concise.",
        variables=[{"subject": "world"}],
        model_name="gemini-pro"
    )
    with patch("cli.prompts_cli.prompts.get") as mock_prompts_get:
        mock_prompts_get.return_value = mock_retrieved_prompt

        result = runner.invoke(app, ["prompts", "get", prompt_id_to_get, "--project-id", "test-project"])

        assert result.exit_code == 0
        assert "Initialized Vertex AI for project: test-project, location: us-central1" in result.stdout
        assert f"Prompt Details (ID: {prompt_id_to_get}):" in result.stdout
        assert "Name: test-prompt-alpha" in result.stdout
        assert "Version ID: 3" in result.stdout
        assert "Prompt Template:" in result.stdout
        assert "Describe {subject} in one sentence." in result.stdout
        assert "System Instruction:" in result.stdout
        assert "Be concise." in result.stdout
        assert "Variables:" in result.stdout
        assert "subject (Example: world)" in result.stdout
        assert "Model: gemini-pro" in result.stdout
        
        mock_ai_init.assert_called_once_with(project="test-project", location="us-central1")
        mock_prompts_get.assert_called_once_with(prompt_id=prompt_id_to_get, version_id=None)

@pytest.fixture
def temp_prompt_file(tmp_path):
    """Helper to create a temporary prompt definition YAML file."""
    def _create_file(filename="prompt_def.yaml", content=None, is_valid_yaml=True, has_all_fields=True):
        file_path = tmp_path / filename
        if content:
            file_path.write_text(content)
            return file_path

        if not is_valid_yaml:
            file_path.write_text("prompt_name: my-prompt\ninvalid_yaml: [missing_colon")
            return file_path
        
        data = {
            "prompt_name": "test-suite-prompt",
            "prompt_data": "This is a {variable}.",
            "model_name": "gemini-1.0-pro", # Example model
            "system_instruction": "Be a test prompt.",
            "variables": [{"variable": "test value"}]
        }
        if not has_all_fields:
            del data["prompt_data"] # Remove a required field for testing

        import yaml
        file_path.write_text(yaml.dump(data))
        return file_path
    return _create_file

@patch("cli.prompts_cli.aiplatform.init")
@patch("cli.prompts_cli.prompts.create_version")
@patch("cli.prompts_cli.LocalPrompt") # Patch the LocalPrompt class constructor
def test_prompts_create_success(mock_local_prompt_constructor, mock_create_version, mock_ai_init, temp_prompt_file):
    """Test 'prompts create --file <path>' successfully."""
    prompt_file_path = temp_prompt_file()

    # Mock the return value of LocalPrompt constructor
    mock_created_local_prompt_obj = MagicMock()
    mock_local_prompt_constructor.return_value = mock_created_local_prompt_obj
    
    # Mock the return value of prompts.create_version (should be a Prompt object with an ID)
    mock_saved_prompt = MockSDKPrompt(id="new-prompt-123", prompt_name="test-suite-prompt", version_id="1")
    mock_create_version.return_value = mock_saved_prompt

    result = runner.invoke(app, ["prompts", "create", "--file", str(prompt_file_path), "--project-id", "test-project"])

    assert result.exit_code == 0
    assert "Initialized Vertex AI for project: test-project, location: us-central1" in result.stdout
    assert "Successfully created/updated prompt: test-suite-prompt (ID: new-prompt-123, Version: 1)" in result.stdout
    
    mock_ai_init.assert_called_once_with(project="test-project", location="us-central1")
    # Check that LocalPrompt was called with expected data from the file
    # This requires knowing the exact structure of data read from YAML
    # For simplicity, we'll just check it was called. More specific checks can be added.
    mock_local_prompt_constructor.assert_called_once() 
    # Example of more specific check if needed:
    # called_args, called_kwargs = mock_local_prompt_constructor.call_args
    # assert called_kwargs.get("prompt_name") == "test-suite-prompt"
    
    mock_create_version.assert_called_once_with(prompt=mock_created_local_prompt_obj)

@patch("cli.prompts_cli.aiplatform.init") # Mock init to prevent actual SDK calls for this error test
def test_prompts_create_file_not_found(mock_ai_init):
    """Test 'prompts create' when the definition file is not found."""
    # Pass project-id to satisfy _initialize_vertexai if it's called before file check
    result = runner.invoke(app, ["prompts", "create", "--file", "non_existent_file.yaml", "--project-id", "test-project"])
    assert result.exit_code != 0
    assert "Error: Prompt definition file 'non_existent_file.yaml' not found." in result.stdout
    # Since _initialize_vertexai is called after file checks, it should not be called here.
    mock_ai_init.assert_not_called()


@patch("cli.prompts_cli.aiplatform.init")
def test_prompts_create_invalid_yaml_file(mock_ai_init, temp_prompt_file):
    """Test 'prompts create' with an invalid YAML file."""
    invalid_file = temp_prompt_file(is_valid_yaml=False)
    result = runner.invoke(app, ["prompts", "create", "--file", str(invalid_file), "--project-id", "test-project"])
    assert result.exit_code != 0
    assert f"Error parsing YAML from file '{str(invalid_file)}'" in result.stdout
    mock_ai_init.assert_not_called()


@patch("cli.prompts_cli.aiplatform.init")
def test_prompts_create_missing_fields_in_file(mock_ai_init, temp_prompt_file):
    """Test 'prompts create' when YAML is valid but misses required fields."""
    partial_file = temp_prompt_file(has_all_fields=False) # Missing 'prompt_data'
    result = runner.invoke(app, ["prompts", "create", "--file", str(partial_file), "--project-id", "test-project"])
    assert result.exit_code != 0
    assert f"Error: Missing required field 'prompt_data' in prompt definition file '{str(partial_file)}'." in result.stdout
    mock_ai_init.assert_not_called()

@patch("cli.prompts_cli.aiplatform.init")
def test_prompts_get_prompt_not_found(mock_ai_init, monkeypatch):
    """Test 'prompts get <prompt_id>' when a Vertex AI prompt is not found."""
    prompt_id_to_get = "non-existent-id"
    
    with patch("cli.prompts_cli.prompts.get") as mock_prompts_get:
        # Simulate the SDK raising a google.api_core.exceptions.NotFound error
        from google.api_core import exceptions as api_exceptions
        mock_prompts_get.side_effect = api_exceptions.NotFound("Prompt not found")

        result = runner.invoke(app, ["prompts", "get", prompt_id_to_get, "--project-id", "test-project"])

        assert result.exit_code == 1 # Expecting failure
        assert "Initialized Vertex AI for project: test-project, location: us-central1" in result.stdout
        assert f"Error retrieving prompt '{prompt_id_to_get}': 404 Prompt not found" in result.stdout
        
        mock_ai_init.assert_called_once_with(project="test-project", location="us-central1")
        mock_prompts_get.assert_called_once_with(prompt_id=prompt_id_to_get, version_id=None)
