"""Provide common fixtures for tests."""

from collections.abc import AsyncGenerator

from httpx import AsyncClient
import pytest


@pytest.fixture
async def httpx_client() -> AsyncGenerator[AsyncClient, None]:
    """Return an authenticated HTTP client."""
    async with AsyncClient() as client:
        yield client
