"""Test the CLI as a Python module."""

import subprocess
import sys


def test_can_run_as_python_module() -> None:
    """Run the CLI as a Python module."""
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-m", "aiohomeconnect", "--help"],
        check=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert b"aiohomeconnect [OPTIONS]" in result.stdout
