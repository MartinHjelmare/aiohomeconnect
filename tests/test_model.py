"""Tests for the model module."""

from aiohomeconnect.model import EventKey, OptionKey, ProgramKey, SettingKey, StatusKey


def test_unknown_enum_values() -> None:
    """Test that the _missing_ method returns the UNKNOWN value."""
    value = "a not known value"
    assert EventKey(value) is EventKey.UNKNOWN
    assert OptionKey(value) is OptionKey.UNKNOWN
    assert ProgramKey(value) is ProgramKey.UNKNOWN
    assert SettingKey(value) is SettingKey.UNKNOWN
    assert StatusKey(value) is StatusKey.UNKNOWN


async def test_options_settings_status_references_at_events() -> None:
    """Test that options, settings and status enum keys are referenced in events.

    Check that all OptionKey, SettingKey and StatusKey are referenced in EventKey also.
    """
    for option_key in OptionKey.__members__.values():
        assert option_key in EventKey.__members__.values(), (
            f"OptionKey.{option_key.name} not in EventKey enumeration"
        )
    for setting_key in SettingKey.__members__.values():
        assert setting_key in EventKey.__members__.values(), (
            f"SettingKey.{setting_key.name} not in EventKey enumeration"
        )
    for status_key in StatusKey.__members__.values():
        assert status_key in EventKey.__members__.values(), (
            f"StatusKey.{status_key.name} not in EventKey enumeration"
        )
    for event_key in EventKey.__members__.values():
        if ".Option." in event_key.value:
            assert event_key in OptionKey.__members__.values(), (
                f"EventKey.{event_key.name} not in OptionKey enumeration"
            )
        if ".Setting." in event_key.value:
            assert event_key in SettingKey.__members__.values(), (
                f"EventKey.{event_key.name} not in SettingKey enumeration"
            )
        if ".Status." in event_key.value:
            assert event_key in StatusKey.__members__.values(), (
                f"EventKey.{event_key.name} not in StatusKey enumeration"
            )
