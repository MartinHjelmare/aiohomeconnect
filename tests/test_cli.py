"""Tests for the CLI."""

from typer.testing import CliRunner

from aiohomeconnect.cli import cli

runner = CliRunner()


def test_help() -> None:
    """The help message includes the CLI name."""
    result = runner.invoke(cli, ["authorize", "--help"])
    assert result.exit_code == 0
    assert "Authorize the client" in result.stdout
