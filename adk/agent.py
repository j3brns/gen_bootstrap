import logging

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import GoogleSearch  # Example built-in ADK tool

from tools.example_tool import get_current_time_tool  # Your custom tool

logger = logging.getLogger(__name__)

root_agent = LlmAgent(
    name="gen_bootstrap_core_assistant",
    model="gemini-1.5-pro-latest",  # Using Gemini 1.5 Pro as requested
    instruction=(
        "You are the gen-bootstrap assistant, a helpful AI designed to "
        "demonstrate the capabilities of the Google Agent Development Kit (ADK) "
        "within this scaffold project. Your primary goal is to assist the user "
        "with their queries by providing information and leveraging the tools "
        "available to you. Available tools are:\n"
        "- get_current_time_async: Use this to find the current time for any timezone.\n"
        "- GoogleSearch: Use this for general knowledge questions or finding "
        "current information online.\n"
        "Be polite, clear, and make sure to tell the user which tool you are "
        "using if you decide to use one."
    ),
    tools=[
        get_current_time_tool,
        GoogleSearch,
    ],
    verbose=True,
)

logger.info(
    f"ADK Agent '{root_agent.name}' initialized. "
    f"Model: '{root_agent.model_config.model}'. "
    f"Tools: {[tool.name for tool in root_agent.tools_by_name.values()]}"
)
