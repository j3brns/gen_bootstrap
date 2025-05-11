import importlib
from unittest.mock import MagicMock

import pytest
# Correct import path for the google_search function
from google.adk.tools import (
    google_search,
)

# Module to be tested
import adk.agent
from tools.example_tool import (
    get_current_time_tool,
)

# Original settings, to be restored if necessary.
# from config import settings as original_project_settings


@pytest.fixture(autouse=True)
def reload_agent_module():
    """Fixture to ensure adk.agent is reloaded for each test, applying patches."""
    importlib.reload(adk.agent)


def test_agent_initialization_with_default_model(mocker):
    """
    Test that the root_agent is initialized with the model specified in settings.
    """
    test_model_name = "gemini-1.5-pro-latest"

    # Mock the settings object that adk.agent will import
    mock_settings = MagicMock()
    mock_settings.default_gemini_model = test_model_name

    mocker.patch("adk.agent.settings", mock_settings)

    # Reload adk.agent to re-initialize root_agent with the mocked settings
    importlib.reload(adk.agent)

    assert adk.agent.root_agent.model == test_model_name
    assert adk.agent.root_agent.name == "gen_bootstrap_core_assistant"


def test_agent_initialization_with_tools(mocker):
    """
    Test that the root_agent is initialized with the expected tools.
    """
    # No specific settings mock needed here if we're just checking default tools
    # Reload adk.agent to ensure a fresh state if other tests modified it
    importlib.reload(adk.agent)

    agent_tools = adk.agent.root_agent.tools

    assert len(agent_tools) == 2

    # Check for custom tool
    assert get_current_time_tool in agent_tools

    # Check for built-in ADK tool (google_search function)
    assert google_search in agent_tools
