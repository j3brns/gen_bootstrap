# tests/cli/test_main_cli.py
import os  # Added for mocking os functions
from unittest.mock import MagicMock, call, patch

import pytest
from typer.testing import CliRunner

from cli.main import app  # Main CLI app

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


@patch("cli.main.shutil.which")  # To mock `gcloud` being found
@patch("cli.main.subprocess.run")
@patch("cli.main.project_settings")  # To control default project_id
def test_setup_gcp_enables_apis(
    mock_proj_settings, mock_subprocess_run, mock_shutil_which
):
    """Test that 'setup-gcp' attempts to enable all required APIs."""
    mock_shutil_which.return_value = "/path/to/gcloud"  # Simulate gcloud is installed
    mock_proj_settings.gcp_project_id = "test-project-id"

    # Simulate successful subprocess calls
    mock_subprocess_run.return_value = MagicMock(
        returncode=0, stdout="Done.", stderr=""
    )

    result = runner.invoke(app, ["setup-gcp"])  # Use default project ID from settings

    assert result.exit_code == 0

    # Check that 'gcloud services enable ...' was called correctly
    # It should be called once with all APIs
    enable_api_call_found = False
    for call_obj in mock_subprocess_run.call_args_list:
        args, kwargs = call_obj
        command_list = args[0]
        if (
            "gcloud" in command_list
            and "services" in command_list
            and "enable" in command_list
        ):
            enable_api_call_found = True
            # Check if all expected APIs are in the command
            for api in EXPECTED_APIS:
                assert api in command_list
            # Check if the project is correctly specified
            assert "--project=test-project-id" in command_list
            break
    assert (
        enable_api_call_found
    ), "gcloud services enable command not found in subprocess calls"


@patch("cli.main.shutil.which")
@patch("cli.main.subprocess.run")
@patch("cli.main.project_settings")
def test_setup_gcp_sets_iam_aiplatform_user(
    mock_proj_settings, mock_subprocess_run, mock_shutil_which
):
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
        MagicMock(
            returncode=0, stdout="APIs enabled/verified.", stderr=""
        ),  # API enable
        MagicMock(
            returncode=0, stdout=mock_project_number + "\n", stderr=""
        ),  # Project describe
        MagicMock(returncode=0, stdout="IAM policy updated.", stderr=""),  # IAM binding
    ]

    result = runner.invoke(app, ["setup-gcp", "--project", test_project_id])
    assert result.exit_code == 0

    # Check the calls to subprocess.run
    assert (
        mock_subprocess_run.call_count >= 2
    )  # At least API enable and project describe, then IAM

    # Check for 'gcloud projects describe' call
    describe_call_args = None
    for call_obj in mock_subprocess_run.call_args_list:
        args, kwargs = call_obj
        command_list = args[0]
        if (
            "gcloud" in command_list
            and "projects" in command_list
            and "describe" in command_list
        ):
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
        if (
            "gcloud" in command_list
            and "projects" in command_list
            and "add-iam-policy-binding" in command_list
            and f"--member=serviceAccount:{default_sa_email}" in command_list
            and "--role=roles/aiplatform.user" in command_list
        ):
            iam_binding_call_args = command_list
            break
    assert (
        iam_binding_call_args is not None
    ), "IAM binding for aiplatform.user not called correctly"
    assert test_project_id in iam_binding_call_args


@patch("cli.main.shutil.which")
@patch("cli.main.subprocess.run")
@patch("cli.main.project_settings")
def test_setup_gcp_sets_iam_secretmanager_accessor(
    mock_proj_settings, mock_subprocess_run, mock_shutil_which
):
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
        MagicMock(
            returncode=0, stdout="APIs enabled/verified.", stderr=""
        ),  # API enable
        MagicMock(
            returncode=0, stdout=mock_project_number + "\n", stderr=""
        ),  # Project describe
        MagicMock(
            returncode=0, stdout="IAM policy updated for aiplatform.user.", stderr=""
        ),  # IAM binding for Vertex AI
        MagicMock(
            returncode=0,
            stdout="IAM policy updated for secretmanager.secretAccessor.",
            stderr="",
        ),  # IAM binding for Secret Manager
    ]

    result = runner.invoke(app, ["setup-gcp", "--project", test_project_id])
    assert result.exit_code == 0

    # Check for 'gcloud projects add-iam-policy-binding' for secretmanager.secretAccessor
    secretmanager_binding_call_args = None
    for call_obj in mock_subprocess_run.call_args_list:
        args, kwargs = call_obj
        command_list = args[0]
        if (
            "gcloud" in command_list
            and "projects" in command_list
            and "add-iam-policy-binding" in command_list
            and f"--member=serviceAccount:{default_sa_email}" in command_list
            and "--role=roles/secretmanager.secretAccessor" in command_list
        ):
            secretmanager_binding_call_args = command_list
            break
    assert (
        secretmanager_binding_call_args is not None
    ), "IAM binding for secretmanager.secretAccessor not called correctly"
    assert test_project_id in secretmanager_binding_call_args


@patch("cli.main.os.makedirs")
@patch("cli.main.os.remove")
@patch("cli.main.os.path.exists")
@patch("cli.main.subprocess.run")
def test_cli_test_command_simple_run(
    mock_subprocess_run, mock_os_path_exists, mock_os_remove, mock_os_makedirs
):
    """Test 'gen-bootstrap test' simple invocation without coverage."""
    mock_subprocess_run.return_value = MagicMock(
        returncode=0, stdout="Pytest run successful", stderr=""
    )

    result = runner.invoke(app, ["test"])

    assert result.exit_code == 0
    # Check if "Running tests..." is in stdout, Typer prints this before subprocess call
    # For more precise check of subprocess output, it's better to inspect what's passed to typer.echo
    # For now, checking result.stdout is a general approach.
    assert "Running tests..." in result.stdout
    assert (
        "Pytest run successful" in result.stdout
    )  # This comes from the mocked subprocess.run

    # Check that subprocess.run was called with the correct basic command
    mock_subprocess_run.assert_called_once()
    called_args = mock_subprocess_run.call_args[0][0]
    assert called_args[:4] == ["poetry", "run", "pytest", "tests"]
    # Ensure no coverage flags are present if not requested
    assert "--cov=." not in called_args


@patch("cli.main.os.makedirs")
@patch("cli.main.os.remove")
@patch("cli.main.os.path.exists")
@patch("cli.main.subprocess.run")
def test_cli_test_command_with_coverage(
    mock_subprocess_run, mock_os_path_exists, mock_os_remove, mock_os_makedirs
):
    """Test 'gen-bootstrap test --coverage' invocation."""
    mock_subprocess_run.return_value = MagicMock(
        returncode=0, stdout="Pytest run with coverage successful", stderr=""
    )
    # Simulate that .coverage_data directory and .coverage file might or might not exist
    # The command should try to create .coverage_data if coverage is on.
    # The clean logic inside the 'test' command is only triggered if '--clean' is also passed.
    # So, for this test, os.remove for .coverage file won't be called without --clean.

    result = runner.invoke(app, ["test", "--coverage"])

    assert result.exit_code == 0
    assert "Running tests..." in result.stdout
    assert "Pytest run with coverage successful" in result.stdout

    mock_subprocess_run.assert_called_once()
    called_args = mock_subprocess_run.call_args[0][0]

    assert "poetry" in called_args
    assert "run" in called_args
    assert "pytest" in called_args
    assert "tests" in called_args  # Default path
    assert "--cov=." in called_args
    assert "--cov-report=term" in called_args  # Default report format

    # Check that os.makedirs was called to ensure .coverage_data directory exists
    mock_os_makedirs.assert_any_call(".coverage_data", exist_ok=True)
    # os.remove and os.path.exists for cleaning are only called if --clean is true
    mock_os_remove.assert_not_called()


@patch("cli.main.os.makedirs")
@patch("cli.main.os.remove")
@patch("cli.main.os.path.exists")
@patch("cli.main.subprocess.run")
def test_cli_test_command_with_html_report(
    mock_subprocess_run, mock_os_path_exists, mock_os_remove, mock_os_makedirs
):
    """Test 'gen-bootstrap test --coverage --html --output-dir reports'."""
    mock_subprocess_run.return_value = MagicMock(
        returncode=0, stdout="HTML report generated", stderr=""
    )
    # Mock that the output directory for reports needs to be created
    mock_os_path_exists.return_value = False  # General mock for path checks

    result = runner.invoke(
        app, ["test", "--coverage", "--html", "--output-dir", "reports"]
    )

    assert result.exit_code == 0
    assert "HTML coverage report generated in reports/html" in result.stdout

    mock_subprocess_run.assert_called_once()
    called_args = mock_subprocess_run.call_args[0][0]
    assert "--cov-report=html:reports/html" in called_args

    # Check that os.makedirs was called for .coverage_data and the output_dir
    mock_os_makedirs.assert_any_call(".coverage_data", exist_ok=True)
    mock_os_makedirs.assert_any_call("reports", exist_ok=True)


@patch("cli.main.os.makedirs")
@patch("cli.main.os.remove")
@patch("cli.main.os.path.exists")
@patch("cli.main.subprocess.run")
def test_cli_test_command_with_junit_xml(
    mock_subprocess_run, mock_os_path_exists, mock_os_remove, mock_os_makedirs
):
    """Test 'gen-bootstrap test --coverage --junit --output-dir reports'."""
    mock_subprocess_run.return_value = MagicMock(
        returncode=0, stdout="JUnit XML generated", stderr=""
    )
    mock_os_path_exists.return_value = False  # General mock for path checks

    result = runner.invoke(
        app, ["test", "--coverage", "--junit", "--output-dir", "reports"]
    )

    assert result.exit_code == 0

    mock_subprocess_run.assert_called_once()
    called_args = mock_subprocess_run.call_args[0][0]
    assert f"--junitxml=reports/junit.xml" in called_args

    mock_os_makedirs.assert_any_call(".coverage_data", exist_ok=True)
    mock_os_makedirs.assert_any_call("reports", exist_ok=True)


@patch("cli.main.os.makedirs")
@patch("cli.main.os.remove")
@patch("cli.main.os.path.exists")
@patch("cli.main.subprocess.run")
def test_cli_test_command_with_clean(
    mock_subprocess_run, mock_os_path_exists, mock_os_remove, mock_os_makedirs
):
    """Test 'gen-bootstrap test --coverage --clean'."""
    mock_subprocess_run.return_value = MagicMock(
        returncode=0, stdout="Tests run after clean", stderr=""
    )

    # Simulate that the .coverage file exists to test its removal
    def side_effect_os_path_exists(path):
        if path == os.path.join(".coverage_data", ".coverage"):
            return True
        return False  # For other potential os.path.exists calls

    mock_os_path_exists.side_effect = side_effect_os_path_exists

    result = runner.invoke(app, ["test", "--coverage", "--clean"])

    assert result.exit_code == 0
    assert "Cleaning coverage data..." in result.stdout
    assert "Coverage data file removed." in result.stdout

    mock_os_makedirs.assert_any_call(".coverage_data", exist_ok=True)
    mock_os_remove.assert_called_once_with(os.path.join(".coverage_data", ".coverage"))

    mock_subprocess_run.assert_called_once()
    called_args = mock_subprocess_run.call_args[0][0]
    assert "--cov=." in called_args


@patch("cli.main.os.makedirs")  # Mocks for coverage directory creation
@patch("cli.main.subprocess.run")
def test_cli_test_command_with_custom_path(mock_subprocess_run, mock_os_makedirs):
    """Test 'gen-bootstrap test --path specific_tests/'."""
    mock_subprocess_run.return_value = MagicMock(
        returncode=0, stdout="Tests run for custom path", stderr=""
    )

    result = runner.invoke(app, ["test", "--path", "specific_tests/"])

    assert result.exit_code == 0
    assert "Tests run for custom path" in result.stdout

    mock_subprocess_run.assert_called_once()
    called_args = mock_subprocess_run.call_args[0][0]
    assert "specific_tests/" in called_args
    # Ensure makedirs for .coverage_data is not called if --coverage is not specified
    mock_os_makedirs.assert_not_called()


@patch("cli.main.subprocess.run")
def test_cli_test_command_failure(mock_subprocess_run):
    """Test 'gen-bootstrap test' when pytest fails."""
    mock_subprocess_run.return_value = MagicMock(
        returncode=1, stdout="Some tests failed", stderr="Error details"
    )

    result = runner.invoke(app, ["test"])

    assert result.exit_code == 1  # CLI should exit with pytest's error code
    assert "Some tests failed" in result.stdout
    assert "Error details" in result.stdout  # stderr from pytest is echoed
    assert "Tests failed with return code: 1" in result.stdout


@patch("cli.main.subprocess.run")
def test_cli_test_command_pytest_not_found(mock_subprocess_run):
    """Test 'gen-bootstrap test' when poetry/pytest is not found."""
    mock_subprocess_run.side_effect = FileNotFoundError("poetry not found")

    result = runner.invoke(app, ["test"])

    assert result.exit_code == 1  # CLI should exit with code 1
    assert "ERROR: 'poetry' or 'pytest' not found." in result.stdout
