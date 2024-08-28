"""Provide a client for Home Connect API."""

from __future__ import annotations

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
        """Make a request.

        The url parameter must start with a slash.
        """
        headers = kwargs.get("headers")
        headers = {} if headers is None else dict(headers)

        access_token = await self.async_get_access_token()
        headers["authorization"] = f"Bearer {access_token}"

        return await self.client.request(
            method,
            f"{self.host}{url}",
            **kwargs,
            headers=headers,
        )


class Client:
    """Represent a client for the Home Connect API."""

    def __init__(self, auth: AbstractAuth) -> None:
        """Initialize the client."""
        self._auth = auth

    async def get_appliances(self) -> dict[str, Any]:
        """Return all paired devices."""
        response = await self._auth.request("GET", "/api/homeappliances")
        return response.json()

    async def get_operation_state(self, ha_id: str) -> dict[str, Any]:
        """Return the operation state of the device."""
        response = await self._auth.request(
            "GET",
            f"/api/homeappliances/{ha_id}/status/BSH.Common.Status.OperationState",
        )
        return response.json()
