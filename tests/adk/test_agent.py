import importlib
from unittest.mock import MagicMock, patch

import pytest
from google.adk.tools import GoogleSearch

# Module to be tested
import adk.agent
from tools.example_tool import get_current_time_tool

# Original settings, to be restored if necessary, though pytest's patching handles this well.
# from config import settings as original_project_settings


@pytest.fixture(autouse=True)
def reload_agent_module():
    """Fixture to ensure adk.agent is reloaded for each test, applying patches."""
    importlib.reload(adk.agent)


def test_agent_initialization_with_default_model(mocker):
    """
    Test that the root_agent is initialized with the model specified in settings.
    """
    test_model_name = "gemini-test-model"

    # Mock the settings object that adk.agent will import
    mock_settings = MagicMock()
    mock_settings.default_gemini_model = test_model_name

    mocker.patch("adk.agent.settings", mock_settings)

    # Reload adk.agent to re-initialize root_agent with the mocked settings
    importlib.reload(adk.agent)

    assert adk.agent.root_agent.model_config.model == test_model_name
    assert adk.agent.root_agent.name == "gen_bootstrap_core_assistant"


def test_agent_initialization_with_tools(mocker):
    """
    Test that the root_agent is initialized with the expected tools.
    """
    # No specific settings mock needed here if we're just checking default tools
    # Reload adk.agent to ensure a fresh state if other tests modified it
    importlib.reload(adk.agent)

    agent_tools = adk.agent.root_agent.tools_by_name

    assert len(agent_tools) == 2

    # Check for custom tool
    assert get_current_time_tool.name in agent_tools
    assert agent_tools[get_current_time_tool.name] is get_current_time_tool

    # Check for built-in ADK tool
    # GoogleSearch tool might not have a .name attribute in the same way,
    # or its name might be dynamically generated. Let's check by type or a known name.
    # The ADK's GoogleSearch tool typically has the name "GoogleSearch"
    google_search_tool_name = "GoogleSearch"  # Assuming this is the default name
    assert google_search_tool_name in agent_tools

    # Verify the type of the GoogleSearch tool if possible
    # This depends on how GoogleSearch is structured and if its instance is directly comparable
    found_google_search = False
    for tool_instance in agent_tools.values():
        if isinstance(tool_instance, GoogleSearch):
            found_google_search = True
            # We can also check its name if it's consistent
            assert tool_instance.name == google_search_tool_name
            break
    assert found_google_search, "GoogleSearch tool instance not found in agent tools"
