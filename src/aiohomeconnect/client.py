"""Provide a client for Home Connect API."""
from abc import ABC, abstractmethod
from typing import Any

from httpx import AsyncClient, Response


class AbstractAuth(ABC):
    """Abstract class to make authenticated requests."""

    def __init__(self, httpx_client: AsyncClient, host: str) -> None:
        """Initialize the auth."""
        self.client = httpx_client
        self.host = host

    @abstractmethod
    async def async_get_access_token(self) -> str:
        """Return a valid access token."""

    async def request(self, method: str, url: str, **kwargs: Any) -> Response:
        """Make a request."""
        headers = kwargs.get("headers")
        headers = {} if headers is None else dict(headers)

        access_token = await self.async_get_access_token()
        headers["authorization"] = f"Bearer {access_token}"

        return await self.client.request(
            method,
            f"{self.host}/{url}",
            **kwargs,
            headers=headers,
        )
