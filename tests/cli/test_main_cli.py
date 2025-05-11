# tests/cli/test_main_cli.py
import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock, call
from cli.main import app # Main CLI app

runner = CliRunner()

# Expected APIs to be enabled by setup-gcp
EXPECTED_APIS = [
    "run.googleapis.com",
    "iam.googleapis.com",
    "secretmanager.googleapis.com",
    "aiplatform.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    "cloudbuild.googleapis.com",
    "artifactregistry.googleapis.com",
]

@patch("cli.main.shutil.which") # To mock `gcloud` being found
@patch("cli.main.subprocess.run")
@patch("cli.main.project_settings") # To control default project_id
def test_setup_gcp_enables_apis(mock_proj_settings, mock_subprocess_run, mock_shutil_which):
    """Test that 'setup-gcp' attempts to enable all required APIs."""
    mock_shutil_which.return_value = "/path/to/gcloud" # Simulate gcloud is installed
    mock_proj_settings.gcp_project_id = "test-project-id"
    
    # Simulate successful subprocess calls
    mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="Done.", stderr="")

    result = runner.invoke(app, ["setup-gcp"]) # Use default project ID from settings

    assert result.exit_code == 0 
    
    # Check that 'gcloud services enable ...' was called correctly
    # It should be called once with all APIs
    enable_api_call_found = False
    for call_obj in mock_subprocess_run.call_args_list:
        args, kwargs = call_obj
        command_list = args[0]
        if "gcloud" in command_list and "services" in command_list and "enable" in command_list:
            enable_api_call_found = True
            # Check if all expected APIs are in the command
            for api in EXPECTED_APIS:
                assert api in command_list
            # Check if the project is correctly specified
            assert "--project=test-project-id" in command_list
            break
    assert enable_api_call_found, "gcloud services enable command not found in subprocess calls"

@patch("cli.main.shutil.which")
@patch("cli.main.subprocess.run")
@patch("cli.main.project_settings")
def test_setup_gcp_sets_iam_aiplatform_user(mock_proj_settings, mock_subprocess_run, mock_shutil_which):
    """Test 'setup-gcp' grants 'roles/aiplatform.user' to the default service account."""
    mock_shutil_which.return_value = "/path/to/gcloud"
    test_project_id = "test-iam-project"
    mock_proj_settings.gcp_project_id = test_project_id
    
    mock_project_number = "123456789012"
    default_sa_email = f"{mock_project_number}-compute@developer.gserviceaccount.com"

    # Configure mock_subprocess_run for multiple calls:
    # 1. For enabling APIs (already tested, but will be called)
    # 2. For 'gcloud projects describe' to get project number
    # 3. For 'gcloud projects add-iam-policy-binding' for aiplatform.user
    mock_subprocess_run.side_effect = [
        MagicMock(returncode=0, stdout="APIs enabled/verified.", stderr=""), # API enable
        MagicMock(returncode=0, stdout=mock_project_number + "\n", stderr=""), # Project describe
        MagicMock(returncode=0, stdout="IAM policy updated.", stderr=""),      # IAM binding
    ]

    result = runner.invoke(app, ["setup-gcp", "--project", test_project_id])
    assert result.exit_code == 0

    # Check the calls to subprocess.run
    assert mock_subprocess_run.call_count >= 2 # At least API enable and project describe, then IAM

    # Check for 'gcloud projects describe' call
    describe_call_args = None
    for call_obj in mock_subprocess_run.call_args_list:
        args, kwargs = call_obj
        command_list = args[0]
        if "gcloud" in command_list and "projects" in command_list and "describe" in command_list:
            describe_call_args = command_list
            break
    assert describe_call_args is not None, "'gcloud projects describe' not called"
    assert test_project_id in describe_call_args
    assert "--format=value(projectNumber)" in describe_call_args

    # Check for 'gcloud projects add-iam-policy-binding' for aiplatform.user
    iam_binding_call_args = None
    for call_obj in mock_subprocess_run.call_args_list:
        args, kwargs = call_obj
        command_list = args[0]
        if ("gcloud" in command_list and 
            "projects" in command_list and 
            "add-iam-policy-binding" in command_list and
            f"--member=serviceAccount:{default_sa_email}" in command_list and
            "--role=roles/aiplatform.user" in command_list):
            iam_binding_call_args = command_list
            break
    assert iam_binding_call_args is not None, "IAM binding for aiplatform.user not called correctly"
    assert test_project_id in iam_binding_call_args

@patch("cli.main.shutil.which")
@patch("cli.main.subprocess.run")
@patch("cli.main.project_settings")
def test_setup_gcp_sets_iam_secretmanager_accessor(mock_proj_settings, mock_subprocess_run, mock_shutil_which):
    """Test 'setup-gcp' grants 'roles/secretmanager.secretAccessor' to the default service account."""
    mock_shutil_which.return_value = "/path/to/gcloud"
    test_project_id = "test-iam-project"
    mock_proj_settings.gcp_project_id = test_project_id
    
    mock_project_number = "123456789012"
    default_sa_email = f"{mock_project_number}-compute@developer.gserviceaccount.com"

    # Configure mock_subprocess_run for multiple calls:
    # 1. For enabling APIs (already tested, but will be called)
    # 2. For 'gcloud projects describe' to get project number
    # 3. For 'gcloud projects add-iam-policy-binding' for aiplatform.user
    # 4. For 'gcloud projects add-iam-policy-binding' for secretmanager.secretAccessor
    mock_subprocess_run.side_effect = [
        MagicMock(returncode=0, stdout="APIs enabled/verified.", stderr=""), # API enable
        MagicMock(returncode=0, stdout=mock_project_number + "\n", stderr=""), # Project describe
        MagicMock(returncode=0, stdout="IAM policy updated for aiplatform.user.", stderr=""), # IAM binding for Vertex AI
        MagicMock(returncode=0, stdout="IAM policy updated for secretmanager.secretAccessor.", stderr=""), # IAM binding for Secret Manager
    ]

    result = runner.invoke(app, ["setup-gcp", "--project", test_project_id])
    assert result.exit_code == 0

    # Check for 'gcloud projects add-iam-policy-binding' for secretmanager.secretAccessor
    secretmanager_binding_call_args = None
    for call_obj in mock_subprocess_run.call_args_list:
        args, kwargs = call_obj
        command_list = args[0]
        if ("gcloud" in command_list and 
            "projects" in command_list and 
            "add-iam-policy-binding" in command_list and
            f"--member=serviceAccount:{default_sa_email}" in command_list and
            "--role=roles/secretmanager.secretAccessor" in command_list):
            secretmanager_binding_call_args = command_list
            break
    assert secretmanager_binding_call_args is not None, "IAM binding for secretmanager.secretAccessor not called correctly"
    assert test_project_id in secretmanager_binding_call_args
