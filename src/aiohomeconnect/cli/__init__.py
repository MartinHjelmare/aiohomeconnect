"""Provide a CLI for Home Connect API."""

import asyncio

from fastapi import FastAPI, HTTPException
from rich import print as rich_print
import typer
import uvicorn

from aiohomeconnect.model import Event, EventKey, EventTypes, StatusKey

from .client import CLIClient, TokenManager

cli = typer.Typer()
app = FastAPI()


@cli.command()
def authorize(
    client_id: str,
    client_secret: str,
) -> None:
    """Authorize the client."""
    asyncio.run(_authorize(client_id, client_secret))


async def _authorize(client_id: str, client_secret: str) -> None:
    """Authorize the client."""
    token_manager = TokenManager(
        client_id=client_id,
        client_secret=client_secret,
    )
    uri = await token_manager.create_authorization_url()

    @app.get("/auth/external/callback")
    async def authorize_callback(
        state: str,
        code: str | None = None,
        error: str | None = None,
    ) -> dict[str, str]:
        """Handle the authorization callback."""
        if error is not None:
            return {"error": error, "state": state}
        if code is None:
            raise HTTPException(
                status_code=400,
                detail="Missing both core and error parameter, one is required",
            )
        await fetch_token(code)
        return {"code": code, "state": state}

    server = uvicorn.Server(
        uvicorn.Config("aiohomeconnect.cli:app", port=5000, log_level="info"),
    )

    async def fetch_token(code: str) -> None:
        """Stop the server."""
        await token_manager.fetch_access_token(code)

    rich_print(f"Visit the following URL to authorize this client:\n{uri}")
    await server.serve()


@cli.command()
def get_appliances(
    client_id: str,
    client_secret: str,
) -> None:
    """Get the appliances."""
    asyncio.run(_get_appliances(client_id, client_secret))


async def _get_appliances(
    client_id: str,
    client_secret: str,
) -> None:
    """Get the appliances."""
    client = CLIClient(client_id, client_secret)
    rich_print(await client.get_home_appliances())


@cli.command()
def get_operation_state(client_id: str, client_secret: str, ha_id: str) -> None:
    """Get the operation state of the device."""
    asyncio.run(_get_operation_state(client_id, client_secret, ha_id))


async def _get_operation_state(client_id: str, client_secret: str, ha_id: str) -> None:
    """Get the operation state of the device."""
    client = CLIClient(client_id, client_secret)
    rich_print(
        await client.get_status_value(
            ha_id, status_key=StatusKey.BSH_COMMON_OPERATION_STATE
        )
    )


@cli.command()
def subscribe_to_home_appliance_changes(client_id: str, client_secret: str) -> None:
    """Subscribe to events for home appliances.

    The events types handled are:
    - CONNECTED
    - DISCONNECTED
    - PAIRED
    - DEPAIRED
    """
    asyncio.run(_subscribe_to_home_appliance_changes(client_id, client_secret))


async def _subscribe_to_home_appliance_changes(
    client_id: str, client_secret: str
) -> None:
    """Subscribe to events."""
    client = CLIClient(client_id, client_secret)
    client.sse.home_appliances_changes_callback = _receive_applicance_changes
    await client.sse.stream_all_events()


async def _receive_applicance_changes(event_type: EventTypes, ha_id: str) -> None:
    """Receive events."""
    print("Home appliance ID:", ha_id)
    rich_print(event_type)


@cli.command()
def subscribe_to_status_events(
    client_id: str, client_secret: str, ha_id: str, keys: list[str]
) -> None:
    """Subscribe to events with the STATUS event type."""
    asyncio.run(_subscribe_to_status_events(client_id, client_secret, ha_id, keys))


async def _subscribe_to_status_events(
    client_id: str,
    client_secret: str,
    ha_id: str,
    keys: list[str],
) -> None:
    """Subscribe to status events."""
    client = CLIClient(client_id, client_secret)
    for key in keys:
        client.sse.register_status_callback(ha_id, EventKey(key), _receive_event)
    await client.sse.stream_all_events()


@cli.command()
def subscribe_to_events(
    client_id: str, client_secret: str, ha_id: str, keys: list[str]
) -> None:
    """Subscribe to events with the EVENT event type."""
    asyncio.run(_subscribe_to_events(client_id, client_secret, ha_id, keys))


async def _subscribe_to_events(
    client_id: str,
    client_secret: str,
    ha_id: str,
    keys: list[str],
) -> None:
    """Subscribe to events."""
    client = CLIClient(client_id, client_secret)
    for key in keys:
        client.sse.register_event_callback(ha_id, EventKey(key), _receive_event)
    await client.sse.stream_all_events()


@cli.command()
def subscribe_to_notify_events(
    client_id: str, client_secret: str, ha_id: str, keys: list[str]
) -> None:
    """Subscribe to events with the NOTIFY event type."""
    asyncio.run(_subscribe_to_notify_events(client_id, client_secret, ha_id, keys))


async def _subscribe_to_notify_events(
    client_id: str,
    client_secret: str,
    ha_id: str,
    keys: list[str],
) -> None:
    """Subscribe to events."""
    client = CLIClient(client_id, client_secret)
    for key in keys:
        client.sse.register_notify_callback(ha_id, EventKey(key), _receive_event)
    await client.sse.stream_all_events()


async def _receive_event(event: Event) -> None:
    """Receive events."""
    rich_print(event)


if __name__ == "__main__":
    cli()
