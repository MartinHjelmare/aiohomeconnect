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
