"""Test the main module."""

from aiohomeconnect.main import add


def test_add() -> None:
    """Adding two number works as expected."""
    assert add(1, 1) == 2
