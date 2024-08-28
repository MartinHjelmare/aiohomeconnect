"""Provide a CLI for Home Connect API."""

import asyncio

from fastapi import FastAPI, HTTPException
from rich import print
import typer
import uvicorn

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

    print(f"Visit the following URL to authorize this client:\n{uri}")
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
    print(await client.get_appliances())


@cli.command()
def get_operation_state(client_id: str, client_secret: str, ha_id: str) -> None:
    """Get the operation state of the device."""
    asyncio.run(_get_operation_state(client_id, client_secret, ha_id))


async def _get_operation_state(client_id: str, client_secret: str, ha_id: str) -> None:
    """Get the operation state of the device."""
    client = CLIClient(client_id, client_secret)
    print(await client.get_operation_state(ha_id))


if __name__ == "__main__":
    cli()
