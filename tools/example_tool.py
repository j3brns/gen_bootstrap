import datetime
import logging

# from zoneinfo import ZoneInfo # Production systems should use this; requires tzdata
from google.adk.tools.function_tool import FunctionTool

logger = logging.getLogger(__name__)


async def get_current_time_async(timezone_str: str = "UTC") -> str:
    """
    Gets the current time in a specified timezone.
    If no timezone is specified, defaults to UTC.

    Args:
        timezone_str: The timezone string (e.g., 'UTC', 'America/New_York',
                      'Europe/London'). 'UTC' is fully implemented.
    Returns:
        The current time as an ISO formatted string, or an error message.
    """
    logger.info(f"Tool 'get_current_time_async' called with tz: {timezone_str}")
    try:
        if timezone_str.upper() == "UTC":
            now_utc = datetime.datetime.now(datetime.timezone.utc)
            current_time = now_utc.isoformat()
        else:
            now_utc_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
            current_time = (
                f"Timezone '{timezone_str}' support is illustrative. "
                f"Current UTC time: {now_utc_iso}"
            )
        logger.info(f"Returning time: {current_time}")
        return current_time
    except Exception as e:
        logger.error(
            f"Error in get_current_time_async for tz {timezone_str}: {e}", exc_info=True
        )
        return (
            f"Error for timezone {timezone_str}. Use standard names "
            f"like 'UTC' or 'America/New_York'."
        )


# The FunctionTool will use the function's __name__ (get_current_time_async)
# and __doc__ string for its name and description by default.
# If a different name or description is desired for the agent,
# this might need to be handled by how the agent consumes the tool,
# or by wrapping/aliasing, if FunctionTool doesn't allow overriding these.
get_current_time_tool = FunctionTool(get_current_time_async)
