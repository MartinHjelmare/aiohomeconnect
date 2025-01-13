"""Provide a CLI for Home Connect API."""

import asyncio

from fastapi import FastAPI, HTTPException
from rich import print as rich_print
import typer
import uvicorn

from aiohomeconnect.model import StatusKey
from aiohomeconnect.model.error import (
    EventStreamInterruptedError,
    HomeConnectApiError,
    HomeConnectRequestError,
)

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
    try:
        client = CLIClient(client_id, client_secret)
        rich_print(await client.get_home_appliances())
    except HomeConnectApiError as e:
        rich_print(f"{type(e).__name__}: {e}")
    except HomeConnectRequestError as e:
        rich_print(e)


@cli.command()
def get_operation_state(client_id: str, client_secret: str, ha_id: str) -> None:
    """Get the operation state of the device."""
    asyncio.run(_get_operation_state(client_id, client_secret, ha_id))


async def _get_operation_state(client_id: str, client_secret: str, ha_id: str) -> None:
    """Get the operation state of the device."""
    try:
        client = CLIClient(client_id, client_secret)
        rich_print(
            await client.get_status_value(
                ha_id, status_key=StatusKey.BSH_COMMON_OPERATION_STATE
            )
        )
    except HomeConnectApiError as e:
        rich_print(f"{type(e).__name__}: {e}")
    except HomeConnectRequestError as e:
        rich_print(e)


@cli.command()
def subscribe_all_appliances_events(client_id: str, client_secret: str) -> None:
    """Subscribe and print events from all the appliances."""
    asyncio.run(_subscribe_all_appliances_events(client_id, client_secret))


async def _subscribe_all_appliances_events(client_id: str, client_secret: str) -> None:
    """Subscribe and print events from all the appliances."""
    client = CLIClient(client_id, client_secret)
    while True:
        try:
            async for event in client.stream_all_events():
                rich_print(event)
        except EventStreamInterruptedError as e:
            rich_print(f"{e} continuing...")
        except HomeConnectApiError as e:
            rich_print(f"{type(e).__name__}: {e}")
            break
        except HomeConnectRequestError as e:
            rich_print(e)
            break


@cli.command()
def subscribe_appliance_events(client_id: str, client_secret: str, ha_id: str) -> None:
    """Subscribe and print events from one appliance."""
    asyncio.run(_subscribe_appliance_events(client_id, client_secret, ha_id))


async def _subscribe_appliance_events(
    client_id: str, client_secret: str, ha_id: str
) -> None:
    """Subscribe and print events from one appliance."""
    client = CLIClient(client_id, client_secret)
    while True:
        try:
            async for event in client.stream_events(ha_id):
                rich_print(event)
        except EventStreamInterruptedError as e:
            rich_print(f"{e}, continuing...")
        except HomeConnectApiError as e:
            rich_print(f"{type(e).__name__}: {e}")
            break
        except HomeConnectRequestError as e:
            rich_print(e)
            break


if __name__ == "__main__":
    cli()
