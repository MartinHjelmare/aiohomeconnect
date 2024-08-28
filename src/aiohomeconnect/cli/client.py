"""Provide a CLI client for Home Connect API."""

from __future__ import annotations

import asyncio
import contextlib
import json
from pathlib import Path
import time
from typing import Any

from authlib.integrations.httpx_client import AsyncOAuth2Client
from httpx import AsyncClient

from aiohomeconnect.client import AbstractAuth, Client
from aiohomeconnect.const import API_ENDPOINT, OAUTH2_AUTHORIZE, OAUTH2_TOKEN

TOKEN_FILE = "token.json"  # noqa: S105
TOKEN_EXPIRES_MARGIN = 20


class CLIClient(Client):
    """Represent a CLI client for Home Connect API."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str | None = None,
        scope: str | None = None,
    ) -> None:
        """Initialize the client."""
        super().__init__(
            Auth(
                AsyncClient(),
                API_ENDPOINT,
                TokenManager(
                    client_id=client_id,
                    client_secret=client_secret,
                    redirect_uri=redirect_uri,
                    scope=scope,
                ),
            ),
        )


class Auth(AbstractAuth):
    """Implement the authentication."""

    def __init__(
        self,
        httpx_client: AsyncClient,
        host: str,
        token_manager: TokenManager,
    ) -> None:
        """Initialize the auth."""
        super().__init__(httpx_client, host)
        self.token_manager = token_manager

    async def async_get_access_token(self) -> str:
        """Return a valid access token."""
        if self.token_manager.access_token is None:
            await self.token_manager.load_access_token()
        if self.token_manager.access_token is None:
            raise ValueError("No access token available")
        if self.token_manager.is_token_valid():
            return self.token_manager.access_token

        await self.token_manager.refresh_access_token()
        await self.token_manager.save_access_token()

        return self.token_manager.access_token


class TokenManager:
    """Manage the tokens for authentication."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str | None = None,
        scope: str | None = None,
    ) -> None:
        """Initialize the token manager."""
        self.access_token: str | None = None
        self._refresh_token: str | None = None
        self._state: str | None = None
        self._token: dict[str, Any] = {}
        self._client = AsyncOAuth2Client(
            client_id,
            client_secret,
            scope=scope,
            redirect_uri=redirect_uri,
        )

    async def create_authorization_url(self) -> str:
        """Create the authorization URL."""
        uri, self._state = self._client.create_authorization_url(
            OAUTH2_AUTHORIZE,
        )
        return uri

    def is_token_valid(self) -> bool:
        """Check if the token is valid."""
        return self._token["expires_at"] > time.time() + TOKEN_EXPIRES_MARGIN

    async def fetch_access_token(self, code: str) -> None:
        """Fetch the access token."""
        token = self._token = await self._client.fetch_token(
            OAUTH2_TOKEN,
            code=code,
            grant_type="authorization_code",
            state=self._state,
        )
        self._validate_token()
        self.access_token = token["access_token"]
        await self.save_access_token()

    async def load_access_token(self) -> None:
        """Load the access token."""
        await asyncio.to_thread(self._load_access_token)
        self.access_token = self._token.get("access_token")
        self._refresh_token = self._token.get("refresh_token")

    async def refresh_access_token(self) -> None:
        """Refresh the access token."""
        token = self._token = await self._client.refresh_token(
            OAUTH2_TOKEN,
            refresh_token=self._refresh_token,
            client_id=self._client.client_id,
            client_secret=self._client.client_secret,
        )
        self._validate_token()
        self.access_token = token["access_token"]
        self._refresh_token = token["refresh_token"]

    async def save_access_token(self) -> None:
        """Save the access token."""
        await asyncio.to_thread(self._save_access_token)

    def _load_access_token(self) -> None:
        """Load the access token."""
        with contextlib.suppress(FileNotFoundError):
            self._token = json.loads(Path(TOKEN_FILE).read_text(encoding="utf-8"))

    def _save_access_token(self) -> None:
        """Save the access token."""
        Path(TOKEN_FILE).write_text(json.dumps(self._token, indent=2), encoding="utf-8")

    def _validate_token(self) -> None:
        """Validate the token."""
        token = self._token
        token["expires_in"] = int(token["expires_in"])
        token["expires_at"] = time.time() + token["expires_in"]
