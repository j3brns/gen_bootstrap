import datetime
import logging
from zoneinfo import ZoneInfo  # For timezone support

from google.adk.tools.function_tool import FunctionTool

logger = logging.getLogger(__name__)


async def get_current_time_async(timezone_str: str = "UTC") -> str:
    """
    Gets the current time in a specified timezone.
    If no timezone is specified, defaults to UTC.

    Args:
        timezone_str: The timezone string (e.g., 'UTC', 'America/New_York',
                      'Europe/London'). Supports all IANA timezone database names.
    Returns:
        The current time as an ISO formatted string, or an error message.
    """
    logger.info(f"Tool 'get_current_time_async' called with tz: {timezone_str}")
    try:
        if timezone_str.upper() == "UTC":
            now_utc = datetime.datetime.now(datetime.timezone.utc)
            current_time = now_utc.isoformat()
        else:
            try:
                # Use ZoneInfo for proper timezone support
                tz = ZoneInfo(timezone_str)
                now = datetime.datetime.now(tz)
                current_time = now.isoformat()
            except Exception as tz_error:
                logger.error(f"Error with timezone {timezone_str}: {tz_error}")
                now_utc_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
                current_time = (
                    f"Error with timezone '{timezone_str}': {tz_error}. "
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
