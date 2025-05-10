import logging
import os

from fastapi import FastAPI

from config import settings as project_settings  # Import project settings
from utils.logging_utils import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

ADK_AGENT_INSTANCE_PATH = "adk.agent:root_agent"
app: FastAPI

try:
    from google.adk.cli.fast_api import get_fast_api_app
    from google.adk.runtime.config import RuntimeConfig

    logger.info(
        f"Init FastAPI app with google-adk helper for agent: {ADK_AGENT_INSTANCE_PATH}"
    )

    adk_runtime_config = RuntimeConfig(
        session_config=RuntimeConfig.SessionConfig(
            store_url=f"sqlite:///{os.getcwd()}/adk_sessions.db"
        ),
        llm_config=RuntimeConfig.LlmConfig(
            model=project_settings.default_gemini_model
        ),  # Configure agent model via settings
    )

    app = get_fast_api_app(
        agent_path_or_dir=ADK_AGENT_INSTANCE_PATH,
        runtime_config=adk_runtime_config,
        web=True,
        title="gen-bootstrap ADK Application (via ADK Helper)",
        description=(
            "A FastAPI application serving an agent built with Google ADK. "
            "Provides ADK standard endpoints like /run, /openapi.json, "
            "and /adk_web for the UI."
        ),
        version="0.2.0-alpha",
    )
    logger.info(
        f"FastAPI app initialized with get_fast_api_app. "
        f"ADK Web UI at /adk_web. Agent: {ADK_AGENT_INSTANCE_PATH}"
    )

except ImportError as e:
    logger.error(
        f"Fatal: Could not import 'get_fast_api_app' from "
        f"'google.adk.cli.fast_api': {e}",
        exc_info=True,
    )
    logger.error("Please ensure 'google-adk' is installed correctly.")
    app = FastAPI(title="gen-bootstrap ADK Application - ERROR", version="0.0.0-error")

    @app.get("/")
    @app.post("/{path:path}")
    async def critical_error_handler():
        return {
            "error": "Critical ADK Integration Missing",
            "message": "Could not initialize application via get_fast_api_app.",
        }


@app.get("/custom_health")
async def custom_health_check():
    logger.info("Custom health endpoint '/custom_health' was called.")
    return {"status": "healthy", "message": "gen-bootstrap custom health OK."}


if __name__ == "__main__":
    print("This app is intended to be run using the CLI or ADK's own tools:")
    print("  To start the FastAPI server (which includes the ADK agent):")
    print("    `poetry run gen-bootstrap run`")
    print("\n  Alternatively, for ADK's native dev UI and CLI runner:")
    print(f"    `poetry run adk web {ADK_AGENT_INSTANCE_PATH}`")
    print(
        f"    `poetry run adk run {ADK_AGENT_INSTANCE_PATH} "
        f'--input "Tell me the time in London"`'
    )
