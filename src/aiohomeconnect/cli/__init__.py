"""Provide a CLI for Home Connect API."""

import asyncio
from json import JSONDecodeError

from fastapi import FastAPI, HTTPException
from httpx import ReadTimeout
from httpx_sse import ServerSentEvent
from mashumaro.exceptions import InvalidFieldValue
from rich import print as rich_print
import typer
import uvicorn

from aiohomeconnect.model import EventType, StatusKey
from aiohomeconnect.model.event import ArrayOfEvents

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
def subscribe_to_all_applicances_events(client_id: str, client_secret: str) -> None:
    """Subscribe and print events from all the appliances."""
    asyncio.run(_subscribe_to_all_applicances_events(client_id, client_secret))


async def _subscribe_to_all_applicances_events(
    client_id: str, client_secret: str
) -> None:
    """Subscribe and print events from all the appliances."""
    client = CLIClient(client_id, client_secret)
    async with client.stream_all_events() as event_source:
        try:
            async for event in event_source.aiter_sse():
                _message_handler(event)
        except ReadTimeout:
            print("Connection timed out")
        else:
            print("Connection closed cleanly")


@cli.command()
def subscribe_to_one_applicance_events(
    client_id: str, client_secret: str, ha_id: str
) -> None:
    """Subscribe and print events from one appliance."""
    asyncio.run(_subscribe_to_one_applicance_events(client_id, client_secret, ha_id))


async def _subscribe_to_one_applicance_events(
    client_id: str, client_secret: str, ha_id: str
) -> None:
    """Subscribe and print events from one appliance."""
    client = CLIClient(client_id, client_secret)
    async with client.stream_events(ha_id) as event_source:
        try:
            async for event in event_source.aiter_sse():
                _message_handler(event)
        except ReadTimeout:
            print("Connection timed out")
        else:
            print("Connection closed cleanly")


def _message_handler(message_event: ServerSentEvent) -> None:
    """Handle the message event."""
    event_type = EventType(message_event.event)
    ha_id = message_event.id
    print(f"\nEvent type: {event_type}, Home appliance ID: {ha_id}")
    match event_type:
        case EventType.STATUS | EventType.EVENT | EventType.NOTIFY:
            try:
                events = ArrayOfEvents.from_json(message_event.data)
            except JSONDecodeError as err:
                print(f"Error decoding event: {err}")
            except InvalidFieldValue as err:
                print(f"Error parsing event: {err}")
            else:
                rich_print(events)


if __name__ == "__main__":
    cli()
