# tests/cli/test_secrets_cli.py
import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from cli.main import app # Main CLI app

runner = CliRunner()

# Mock for the Secret object returned by Secret Manager client
class MockGMSecret:
    def __init__(self, name):
        self.name = name # Full resource name, e.g., projects/.../secrets/my-secret

@patch("cli.secrets_cli.secretmanager.SecretManagerServiceClient")
@patch("cli.secrets_cli.project_settings") # To control project_id if not passed via CLI
def test_secrets_list_no_secrets(mock_settings, MockSecretManagerClient, monkeypatch):
    """Test 'secrets list' when no secrets are found."""
    mock_settings.gcp_project_id = "test-project" # Set default project ID for the test
    
    mock_client_instance = MockSecretManagerClient.return_value
    mock_client_instance.list_secrets.return_value = [] # No secrets

    result = runner.invoke(app, ["secrets", "list"]) # Uses default project from mock_settings

    assert result.exit_code == 0
    assert "No secrets found in project test-project." in result.stdout
    mock_client_instance.list_secrets.assert_called_once_with(
        request={"parent": "projects/test-project"}
    )

@patch("cli.secrets_cli.secretmanager.SecretManagerServiceClient")
@patch("cli.secrets_cli.project_settings")
def test_secrets_list_with_secrets(mock_settings, MockSecretManagerClient, monkeypatch):
    """Test 'secrets list' with some secrets found."""
    mock_settings.gcp_project_id = "test-project-with-secrets"
    
    mock_client_instance = MockSecretManagerClient.return_value
    mock_client_instance.list_secrets.return_value = [
        MockGMSecret(name="projects/123/secrets/secret-alpha"),
        MockGMSecret(name="projects/123/secrets/secret-beta"),
    ]

    result = runner.invoke(app, ["secrets", "list", "--project-id", "cli-project"]) # Override default

    assert result.exit_code == 0
    assert "Secrets in project cli-project:" in result.stdout
    assert "- secret-alpha" in result.stdout
    assert "- secret-beta" in result.stdout
    mock_client_instance.list_secrets.assert_called_once_with(
        request={"parent": "projects/cli-project"}
    )

@patch("cli.secrets_cli.secretmanager.SecretManagerServiceClient")
def test_secrets_list_sdk_error(MockSecretManagerClient, monkeypatch):
    """Test 'secrets list' when the SDK call raises an error."""
    # Patch project_settings directly in the module where it's used by list_secrets
    monkeypatch.setattr("cli.secrets_cli.project_settings.gcp_project_id", "error-project", raising=False)

    mock_client_instance = MockSecretManagerClient.return_value
    mock_client_instance.list_secrets.side_effect = Exception("SDK Error")

    result = runner.invoke(app, ["secrets", "list"])
    
    assert result.exit_code == 1
    assert "Error listing secrets: SDK Error" in result.stdout

def test_secrets_list_no_project_id(monkeypatch):
    """Test 'secrets list' when project_id is not configured or provided."""
    # Ensure project_settings.gcp_project_id is None or the default placeholder
    # This requires careful patching as project_settings might be imported at module load.
    # We can patch the 'from config.settings import settings' part.
    
    # Easiest is to ensure the loaded settings object has no valid project_id
    class TempMockSettings:
        gcp_project_id = None # or "your-gcp-project-id"
    
    with patch("cli.secrets_cli.project_settings", TempMockSettings()):
        result = runner.invoke(app, ["secrets", "list"]) # No --project-id provided
        assert result.exit_code == 1
        assert "Project ID is not configured" in result.stdout

# Mock for AccessSecretVersionResponse
class MockAccessSecretVersionResponse:
    def __init__(self, payload_data):
        self.payload = MagicMock()
        self.payload.data = payload_data.encode('utf-8')

@patch("cli.secrets_cli.secretmanager.SecretManagerServiceClient")
@patch("cli.secrets_cli.project_settings")
def test_secrets_get_success(mock_settings, MockSecretManagerClient):
    """Test 'secrets get <secret_id>' successfully retrieves latest version."""
    mock_settings.gcp_project_id = "test-project"
    secret_id = "my-api-key"
    secret_payload = "supersecretvalue"

    mock_client_instance = MockSecretManagerClient.return_value
    mock_client_instance.access_secret_version.return_value = MockAccessSecretVersionResponse(payload_data=secret_payload)

    result = runner.invoke(app, ["secrets", "get", secret_id, "--project-id", "test-project"])

    assert result.exit_code == 0
    assert secret_payload in result.stdout
    expected_name = f"projects/test-project/secrets/{secret_id}/versions/latest"
    mock_client_instance.access_secret_version.assert_called_once_with(name=expected_name)

@patch("cli.secrets_cli.secretmanager.SecretManagerServiceClient")
@patch("cli.secrets_cli.project_settings")
def test_secrets_get_specific_version_success(mock_settings, MockSecretManagerClient):
    """Test 'secrets get <secret_id> --version <num>' successfully."""
    mock_settings.gcp_project_id = "test-project"
    secret_id = "my-db-pass"
    secret_version = "3"
    secret_payload = "version3password"

    mock_client_instance = MockSecretManagerClient.return_value
    mock_client_instance.access_secret_version.return_value = MockAccessSecretVersionResponse(payload_data=secret_payload)

    result = runner.invoke(app, ["secrets", "get", secret_id, "--version", secret_version, "--project-id", "test-project"])

    assert result.exit_code == 0
    assert secret_payload in result.stdout
    expected_name = f"projects/test-project/secrets/{secret_id}/versions/{secret_version}"
    mock_client_instance.access_secret_version.assert_called_once_with(name=expected_name)

@patch("cli.secrets_cli.secretmanager.SecretManagerServiceClient")
@patch("cli.secrets_cli.project_settings")
def test_secrets_get_secret_not_found(mock_settings, MockSecretManagerClient):
    """Test 'secrets get' when secret or version is not found."""
    mock_settings.gcp_project_id = "test-project"
    secret_id = "ghost-secret"
    from google.api_core import exceptions as api_exceptions # Import for exception type

    mock_client_instance = MockSecretManagerClient.return_value
    mock_client_instance.access_secret_version.side_effect = api_exceptions.NotFound("Secret not found")

    result = runner.invoke(app, ["secrets", "get", secret_id, "--project-id", "test-project"])

    assert result.exit_code == 1
    assert f"Error accessing secret '{secret_id}' (version latest): 404 Secret not found" in result.stdout

@patch("cli.secrets_cli.secretmanager.SecretManagerServiceClient")
@patch("cli.secrets_cli.project_settings")
def test_secrets_get_permission_denied(mock_settings, MockSecretManagerClient):
    """Test 'secrets get' when permission is denied."""
    mock_settings.gcp_project_id = "test-project"
    secret_id = "forbidden-secret"
    from google.api_core import exceptions as api_exceptions # Import for exception type

    mock_client_instance = MockSecretManagerClient.return_value
    mock_client_instance.access_secret_version.side_effect = api_exceptions.PermissionDenied("Permission denied")

    result = runner.invoke(app, ["secrets", "get", secret_id, "--project-id", "test-project"])

    assert result.exit_code == 1
    assert f"Error accessing secret '{secret_id}' (version latest): 403 Permission denied" in result.stdout

@patch("cli.secrets_cli.secretmanager.SecretManagerServiceClient")
@patch("cli.secrets_cli.project_settings")
def test_secrets_create_success(mock_settings, MockSecretManagerClient):
    """Test 'secrets create <secret_id>' successfully."""
    mock_settings.gcp_project_id = "test-project"
    secret_id_to_create = "new-secret"

    mock_client_instance = MockSecretManagerClient.return_value
    # The create_secret method returns the created Secret object
    mock_client_instance.create_secret.return_value = MockGMSecret(name=f"projects/test-project/secrets/{secret_id_to_create}")

    result = runner.invoke(app, ["secrets", "create", secret_id_to_create, "--project-id", "test-project"])

    assert result.exit_code == 0
    assert f"Secret '{secret_id_to_create}' created successfully in project test-project." in result.stdout
    
    expected_parent = "projects/test-project"
    # Check the 'secret' argument passed to create_secret for replication policy
    # The SDK expects a 'secret' object, not just a dict for replication.
    # For simplicity, we'll check that it's called with a secret object that has automatic replication.
    # A more detailed check would involve asserting the structure of the passed 'secret' argument.
    mock_client_instance.create_secret.assert_called_once()
    call_args = mock_client_instance.create_secret.call_args
    assert call_args is not None
    # Assuming 'request' is a keyword argument to client.create_secret
    assert 'request' in call_args.kwargs
    request_arg = call_args.kwargs['request']
    assert request_arg['parent'] == expected_parent
    assert request_arg['secret_id'] == secret_id_to_create
    assert 'replication' in request_arg['secret']
    assert 'automatic' in request_arg['secret']['replication']


@patch("cli.secrets_cli.secretmanager.SecretManagerServiceClient")
@patch("cli.secrets_cli.project_settings")
def test_secrets_create_already_exists(mock_settings, MockSecretManagerClient):
    """Test 'secrets create' when the secret already exists."""
    mock_settings.gcp_project_id = "test-project"
    secret_id = "existing-secret"
    from google.api_core import exceptions as api_exceptions

    mock_client_instance = MockSecretManagerClient.return_value
    mock_client_instance.create_secret.side_effect = api_exceptions.AlreadyExists("Secret already exists")

    result = runner.invoke(app, ["secrets", "create", secret_id, "--project-id", "test-project"])

    assert result.exit_code == 1
    assert f"Error creating secret '{secret_id}': 409 Secret already exists" in result.stdout

@patch("cli.secrets_cli.secretmanager.SecretManagerServiceClient")
@patch("cli.secrets_cli.project_settings")
def test_secrets_create_permission_denied(mock_settings, MockSecretManagerClient):
    """Test 'secrets create' when permission is denied."""
    mock_settings.gcp_project_id = "test-project"
    secret_id = "restricted-secret"
    from google.api_core import exceptions as api_exceptions

    mock_client_instance = MockSecretManagerClient.return_value
    mock_client_instance.create_secret.side_effect = api_exceptions.PermissionDenied("Permission denied to create secret")

    result = runner.invoke(app, ["secrets", "create", secret_id, "--project-id", "test-project"])

    assert result.exit_code == 1
    assert f"Error creating secret '{secret_id}': 403 Permission denied to create secret" in result.stdout

# Mock for SecretVersion object
class MockGMSecretVersion:
    def __init__(self, name):
        # name is like projects/PROJECT_NUM/secrets/SECRET_ID/versions/VERSION_ID
        self.name = name
        self.version_id = name.split("/")[-1] # Extract version_id from full name

@patch("cli.secrets_cli.secretmanager.SecretManagerServiceClient")
@patch("cli.secrets_cli.project_settings")
def test_secrets_add_version_with_data_success(mock_settings, MockSecretManagerClient):
    """Test 'secrets add-version --data' successfully."""
    mock_settings.gcp_project_id = "test-project"
    secret_id = "my-secret"
    secret_data = "new_secret_value"
    new_version_id = "5"
    full_version_name = f"projects/test-project/secrets/{secret_id}/versions/{new_version_id}"

    mock_client_instance = MockSecretManagerClient.return_value
    mock_client_instance.add_secret_version.return_value = MockGMSecretVersion(name=full_version_name)

    result = runner.invoke(app, ["secrets", "add-version", secret_id, "--data", secret_data, "--project-id", "test-project"])

    assert result.exit_code == 0
    assert f"Added new version '{new_version_id}' to secret '{secret_id}' in project test-project." in result.stdout
    
    expected_parent = f"projects/test-project/secrets/{secret_id}"
    mock_client_instance.add_secret_version.assert_called_once()
    call_args = mock_client_instance.add_secret_version.call_args
    assert call_args is not None
    assert 'request' in call_args.kwargs
    request_arg = call_args.kwargs['request']
    assert request_arg['parent'] == expected_parent
    assert request_arg['payload']['data'] == secret_data.encode('utf-8')

@patch("cli.secrets_cli.secretmanager.SecretManagerServiceClient")
@patch("cli.secrets_cli.project_settings")
def test_secrets_add_version_with_data_file_success(mock_settings, MockSecretManagerClient, tmp_path):
    """Test 'secrets add-version --data-file' successfully."""
    mock_settings.gcp_project_id = "test-project"
    secret_id = "file-secret"
    secret_data = "content from file"
    new_version_id = "2"
    full_version_name = f"projects/test-project/secrets/{secret_id}/versions/{new_version_id}"

    data_file = tmp_path / "secret_file.txt"
    data_file.write_text(secret_data)

    mock_client_instance = MockSecretManagerClient.return_value
    mock_client_instance.add_secret_version.return_value = MockGMSecretVersion(name=full_version_name)

    result = runner.invoke(app, ["secrets", "add-version", secret_id, "--data-file", str(data_file), "--project-id", "test-project"])

    assert result.exit_code == 0
    assert f"Added new version '{new_version_id}' to secret '{secret_id}' in project test-project." in result.stdout
    
    expected_parent = f"projects/test-project/secrets/{secret_id}"
    mock_client_instance.add_secret_version.assert_called_once()
    call_args = mock_client_instance.add_secret_version.call_args
    assert 'request' in call_args.kwargs
    request_arg = call_args.kwargs['request']
    assert request_arg['parent'] == expected_parent
    assert request_arg['payload']['data'] == secret_data.encode('utf-8')

def test_secrets_add_version_data_and_file_exclusive():
    """Test 'secrets add-version' fails if both --data and --data-file are used."""
    result = runner.invoke(app, ["secrets", "add-version", "any-secret", "--data", "val", "--data-file", "file.txt"])
    assert result.exit_code != 0
    assert "Error: --data and --data-file are mutually exclusive." in result.stdout

def test_secrets_add_version_no_data_or_file():
    """Test 'secrets add-version' fails if neither --data nor --data-file is used."""
    result = runner.invoke(app, ["secrets", "add-version", "any-secret"])
    assert result.exit_code != 0
    assert "Error: Either --data or --data-file must be provided." in result.stdout

@patch("cli.secrets_cli.secretmanager.SecretManagerServiceClient")
@patch("cli.secrets_cli.project_settings")
def test_secrets_add_version_secret_not_found(mock_settings, MockSecretManagerClient):
    """Test 'secrets add-version' when the parent secret is not found."""
    mock_settings.gcp_project_id = "test-project"
    secret_id = "non-existent-secret-for-version"
    from google.api_core import exceptions as api_exceptions

    mock_client_instance = MockSecretManagerClient.return_value
    mock_client_instance.add_secret_version.side_effect = api_exceptions.NotFound("Parent secret not found")

    result = runner.invoke(app, ["secrets", "add-version", secret_id, "--data", "value", "--project-id", "test-project"])
    
    assert result.exit_code == 1
    assert f"Error adding version to secret '{secret_id}': 404 Parent secret not found" in result.stdout

def test_secrets_add_version_data_file_not_found(tmp_path):
    """Test 'secrets add-version --data-file' when the file does not exist."""
    # No need to mock SDK as file check should happen first
    result = runner.invoke(app, ["secrets", "add-version", "any-secret", "--data-file", str(tmp_path / "no_such_file.txt"), "--project-id", "test-project"])
    assert result.exit_code != 0
    assert f"Error: Data file '{str(tmp_path / 'no_such_file.txt')}' not found." in result.stdout
