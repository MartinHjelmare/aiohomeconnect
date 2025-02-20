"""Provide a CLI for Home Connect API."""

import asyncio
import logging
from typing import Any

from fastapi import FastAPI, HTTPException
from rich import print as rich_print
import typer
import uvicorn

from aiohomeconnect.model import OptionKey, StatusKey
from aiohomeconnect.model.error import (
    EventStreamInterruptedError,
    HomeConnectApiError,
    HomeConnectRequestError,
)

from .client import CLIClient, TokenManager

cli = typer.Typer()
app = FastAPI()
logging.basicConfig(level=logging.WARNING)
logging.getLogger("aiohomeconnect").setLevel(logging.DEBUG)

LOGGER = logging.getLogger(__name__)


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
                detail="Missing both code and error parameter, one is required",
            )
        token = await fetch_token(code)
        rich_print(f"Token fetched: {token}")
        return {"code": code, "state": state}

    server = uvicorn.Server(
        uvicorn.Config("aiohomeconnect.cli:app", port=5000, log_level="info"),
    )

    async def fetch_token(code: str) -> dict[str, Any]:
        """Stop the server."""
        return await token_manager.fetch_access_token(code)

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
def set_selected_program_option(
    client_id: str,
    client_secret: str,
    ha_id: str,
    *,
    option_key: OptionKey,
    bool_value: bool | None = None,
    float_value: float | None = None,
    string_value: str | None = None,
) -> None:
    """Set an option of a program on an appliance."""
    value: bool | float | str
    if float_value is not None:
        value = float_value
    elif string_value is not None:
        value = string_value
    elif bool_value is not None:
        value = bool_value
    else:
        raise ValueError("One of bool_value, float_value, or string_value must be set")
    LOGGER.debug("Setting option %s to %s", option_key, value)
    asyncio.run(
        _set_selected_program_option(
            client_id, client_secret, ha_id, option_key=option_key, value=value
        )
    )


async def _set_selected_program_option(
    client_id: str,
    client_secret: str,
    ha_id: str,
    *,
    option_key: OptionKey,
    value: Any,
) -> None:
    """Set an option of a program on an appliance."""
    try:
        client = CLIClient(client_id, client_secret)
        await client.set_selected_program_option(
            ha_id, option_key=option_key, value=value
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
