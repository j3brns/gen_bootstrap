import datetime
from unittest.mock import MagicMock  # Added import
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import pytest

from tools.example_tool import get_current_time_async

# A fixed point in time for consistent testing, in UTC
FIXED_UTC_NOW = datetime.datetime(2023, 10, 26, 10, 0, 0, tzinfo=datetime.timezone.utc)


@pytest.fixture
def mock_datetime_now(mocker):
    """Mocks datetime.datetime.now to control current time."""

    def mocked_now(tz=None):
        # The function get_current_time_async calls datetime.now(tz_object)
        # So, we return the fixed UTC time, localized to the provided tz_object
        if tz is None:  # Should not be called this way by the tool
            return FIXED_UTC_NOW
        return FIXED_UTC_NOW.astimezone(tz)

    mock_dt = mocker.patch("tools.example_tool.datetime")
    mock_dt.datetime.now.side_effect = mocked_now
    return mock_dt.datetime.now


@pytest.mark.asyncio
async def test_get_current_time_default_is_utc(mock_datetime_now):
    """Test that default timezone is UTC."""
    expected_iso_format = FIXED_UTC_NOW.isoformat()

    result = await get_current_time_async()  # Default is "UTC"
    assert result == expected_iso_format


@pytest.mark.asyncio
async def test_get_current_time_explicit_utc(mock_datetime_now):
    """Test with explicit 'UTC' timezone."""
    expected_iso_format = FIXED_UTC_NOW.isoformat()

    result_upper = await get_current_time_async("UTC")
    assert result_upper == expected_iso_format

    result_lower = await get_current_time_async("utc")
    assert result_lower == expected_iso_format


@pytest.mark.asyncio
async def test_get_current_time_valid_timezone_new_york(mock_datetime_now):
    """Test with a valid IANA timezone 'America/New_York'."""
    tz_str = "America/New_York"
    new_york_tz = ZoneInfo(tz_str)
    expected_time_in_new_york = FIXED_UTC_NOW.astimezone(
        new_york_tz
    )
    expected_iso_format = (
        expected_time_in_new_york.isoformat()
    )

    result = await get_current_time_async(
        tz_str
    )
    assert result == expected_iso_format


@pytest.mark.asyncio
async def test_get_current_time_valid_timezone_london(mock_datetime_now):
    """Test with a valid IANA timezone 'Europe/London'."""
    tz_str = "Europe/London"
    london_tz = ZoneInfo(tz_str)
    expected_time_in_london = FIXED_UTC_NOW.astimezone(london_tz)
    expected_iso_format = expected_time_in_london.isoformat()

    result = await get_current_time_async(tz_str)
    assert result == expected_iso_format


@pytest.mark.asyncio
async def test_get_current_time_invalid_timezone(mocker):  # Signature is correct
    """Test with an invalid timezone string."""
    invalid_tz_str = "Invalid/Timezone"

    # Reset all mocks to ensure a clean state for this specific test's mocking strategy
    mocker.resetall()

    # Mock ZoneInfo to raise an error when an invalid timezone string is used
    mock_zoneinfo = mocker.patch(
        "tools.example_tool.ZoneInfo",
        side_effect=ZoneInfoNotFoundError("Test ZoneInfo error: Invalid timezone"),
    )

    # Mock datetime.datetime.now specifically for the UTC call within the except block of the tool
    mock_utc_now_in_except_block = MagicMock(return_value=FIXED_UTC_NOW)

    def selective_datetime_now_mock(tz=None):
        if tz == datetime.timezone.utc:
            return mock_utc_now_in_except_block(tz)
        # This path should ideally not be hit if ZoneInfo mock fails first as expected
        # However, if ZoneInfo(tz_str) somehow didn't raise but returned an unusable tz,
        # and then datetime.now(tz) was called, this would catch it.
        # For this test, we rely on ZoneInfo raising the error.
        raise Exception(
            "datetime.now called with unexpected tz in invalid_timezone test"
        )

    mock_dt = mocker.patch("tools.example_tool.datetime")
    mock_dt.datetime.now.side_effect = selective_datetime_now_mock

    result = await get_current_time_async(invalid_tz_str)

    assert "Error with timezone" in result
    assert f"'{invalid_tz_str}'" in result
    assert (
        "Test ZoneInfo error: Invalid timezone" in result
    )  # Check our mocked ZoneInfo error message
    assert f"Current UTC time: {FIXED_UTC_NOW.isoformat()}" in result

    mock_zoneinfo.assert_called_once_with(invalid_tz_str)
    mock_utc_now_in_except_block.assert_called_once_with(datetime.timezone.utc)
