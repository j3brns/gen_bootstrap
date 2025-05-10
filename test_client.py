import asyncio
import json
import os

import gradio as gr
import httpx

AGENT_API_URL = os.getenv("AGENT_API_URL", "http://localhost:8080")
# ADK's get_fast_api_app usually exposes the agent at /run
# The payload structure for /run is specific to ADK.
# It often involves a list of "messages" or a structured "input".
ADK_INTERACT_ENDPOINT = f"{AGENT_API_URL}/run"


async def call_agent_api_via_adk_run(
    input_text: str, session_id: str = "gradio_default_session"
) -> str:
    """
    Calls the ADK agent's /run endpoint.
    The payload for ADK's /run is typically structured. This is a common pattern.
    """
    payload = {
        "messages": [
            {"content": {"text": input_text}, "role": "user"}
        ],  # Common ADK messages
        "session_id": session_id,
        # "stream": False,  # Set to True if you want to handle streaming responses
    }
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(ADK_INTERACT_ENDPOINT, json=payload)
            response.raise_for_status()
            response_data = response.json()

            # ADK /run responses are often a list of messages.
            # Extracting the agent's textual response.
            if isinstance(response_data, list) and response_data:
                last_message = response_data[-1]
                if isinstance(last_message, dict) and "content" in last_message:
                    content = last_message["content"]
                    if isinstance(content, dict) and "text" in content:
                        return str(content["text"])
            return json.dumps(response_data, indent=2)  # Fallback
    except httpx.RequestError as e:
        return (
            f"Connection Error: Failed to connect to agent at {ADK_INTERACT_ENDPOINT}. "
            f"Is it running? Details: {e}"
        )
    except httpx.HTTPStatusError as e:
        return f"API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def gradio_interface_sync_wrapper(input_text_sync: str):
    return asyncio.run(call_agent_api_via_adk_run(input_text_sync))


if __name__ == "__main__":
    iface = gr.Interface(
        fn=gradio_interface_sync_wrapper,
        inputs=gr.Textbox(lines=5, label="Enter input for the ADK agent:"),
        outputs=gr.Textbox(label="Agent Response:", lines=15, show_copy_button=True),
        title="gen-bootstrap ADK Agent Test Client (via API)",
        description=(
            f"Interacts with ADK agent served by FastAPI (default: {ADK_INTERACT_ENDPOINT}). "
            "Ensure `gen-bootstrap` FastAPI/ADK server is running "
            "(`poetry run gen-bootstrap run`). Uses common ADK /run patterns."
        ),
    )
    print(f"Launching Gradio interface for agent at {ADK_INTERACT_ENDPOINT}")
    print(
        "Ensure the gen-bootstrap FastAPI/ADK server is running: "
        "`poetry run gen-bootstrap run`"
    )
    iface.launch()
