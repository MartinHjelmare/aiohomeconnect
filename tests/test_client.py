"""Test the client."""

import json
from typing import Any

import httpx
from httpx import AsyncClient
import pytest
from pytest_httpx import HTTPXMock, IteratorStream

from aiohomeconnect.client import AbstractAuth, Client
from aiohomeconnect.model import EventKey, EventType

TEST_ACCESS_TOKEN = "1234"


class AuthClient(AbstractAuth):
    """Use the abstract auth."""

    async def async_get_access_token(self) -> str:
        """Return a valid access token."""
        return TEST_ACCESS_TOKEN


async def test_abstract_auth_request(
    httpx_client: AsyncClient, httpx_mock: HTTPXMock
) -> None:
    """Test the abstract auth request."""
    url_query = "key1=value1&key2=value2"
    httpx_mock.add_response(
        url=f"https://example.com/api/test?{url_query}",
        json={"test": "test_result"},
    )

    params = {"key1": "value1", "key2": "value2"}
    client = AuthClient(httpx_client, "https://example.com")
    response = await client.request("GET", "/test", params=params)

    assert response.status_code == 200
    assert response.json() == {"test": "test_result"}
    request = httpx_mock.get_request()
    assert request
    assert request.headers["authorization"] == f"Bearer {TEST_ACCESS_TOKEN}"
    assert request.url.query.decode(encoding="utf-8") == "key1=value1&key2=value2"


async def test_abstract_auth_sse(
    httpx_client: AsyncClient, httpx_mock: HTTPXMock
) -> None:
    """Test the abstract auth sse."""
    url_query = "key1=value1&key2=value2"

    httpx_mock.add_response(
        url=f"https://example.com/api/test?{url_query}",
        stream=IteratorStream(
            [
                b'data: {"test": "test_result"}\n\n',
                b'data: {"test": "test_result"}\n\n',
            ]
        ),
        headers={"Content-Type": "text/event-stream"},
    )

    params = {"key1": "value1", "key2": "value2"}
    client = AuthClient(httpx_client, "https://example.com")
    async with client.connect_sse("GET", "/test", params=params) as event_source:
        assert event_source.response.status_code == 200
        num_events = 0
        async for event in event_source.aiter_sse():
            assert event.data == '{"test": "test_result"}'
            num_events += 1
        assert num_events == 2

    request = httpx_mock.get_request()
    assert request
    assert request.headers["authorization"] == f"Bearer {TEST_ACCESS_TOKEN}"
    assert request.url.query.decode(encoding="utf-8") == "key1=value1&key2=value2"


@pytest.mark.parametrize(
    "event_data",
    [
        {
            "items": [
                {
                    "handling": "none",
                    "key": EventKey.DISHCARE_DISHWASHER_OPTION_HALF_LOAD.value,
                    "level": "hint",
                    "timestamp": 1733611453,
                    "uri": "/a/random/relative/uri",
                    "value": True,
                },
                {
                    "handling": "none",
                    "key": EventKey.BSH_COMMON_OPTION_REMAINING_PROGRAM_TIME.value,
                    "level": "hint",
                    "timestamp": 1733611453,
                    "unit": "seconds",
                    "uri": "/a/random/relative/uri",
                    "value": 13800,
                },
            ]
        },
        {
            "items": [
                {
                    "handling": "acknowledge",
                    "key": EventKey.BSH_COMMON_EVENT_PROGRAM_ABORTED.value,
                    "level": "hint",
                    "timestamp": 1733616930,
                    "value": "BSH.Common.EnumType.EventPresentState.Present",
                }
            ],
        },
        {
            "handling": "none",
            "key": "BSH.Common.Appliance.Disconnected",
            "level": "hint",
            "timestamp": 1733611817,
            "value": True,
        },
        None,
    ],
)
async def test_stream_all_events(
    httpx_client: AsyncClient, httpx_mock: HTTPXMock, event_data: dict[str, Any] | None
) -> None:
    """Test stream all events."""
    ha_id = "SIEMENS-HCS02DWH1-6BE58C26DCC1"
    event_type = EventType.NOTIFY
    httpx_mock.add_response(
        url="https://example.com/api/homeappliances/events",
        stream=IteratorStream(
            [
                "\n".join(
                    [
                        f"id: {ha_id}",
                        f"data: {json.dumps(event_data) if event_data else ""}",
                        f"event: {event_type}",
                        "\n",
                    ]
                ).encode()
            ]
        ),
        headers={"Content-Type": "text/event-stream"},
    )

    client = Client(AuthClient(httpx_client, "https://example.com"))

    async for event_message in client.stream_all_events():
        assert event_message.ha_id == ha_id
        assert event_message.type == event_type
        if not event_data:
            assert len(event_message.data.items) == 0
        elif items := event_data.get("items"):
            assert len(event_message.data.items) == len(items)
        else:
            assert len(event_message.data.items) == 1


async def test_stream_all_events_http_error(
    httpx_client: AsyncClient, httpx_mock: HTTPXMock
) -> None:
    """Test stream all events http error."""
    httpx_mock.add_response(
        url="https://example.com/api/homeappliances/events",
        status_code=500,
    )

    client = Client(AuthClient(httpx_client, "https://example.com"))

    with pytest.raises(httpx.HTTPStatusError, match=r".*500 Internal Server Error.*"):
        await anext(client.stream_all_events())


@pytest.mark.parametrize(
    "event_data",
    [
        {
            "items": [
                {
                    "handling": "none",
                    "key": EventKey.DISHCARE_DISHWASHER_OPTION_HALF_LOAD.value,
                    "level": "hint",
                    "timestamp": 1733611453,
                    "uri": "/a/random/relative/uri",
                    "value": True,
                },
                {
                    "handling": "none",
                    "key": EventKey.BSH_COMMON_OPTION_REMAINING_PROGRAM_TIME.value,
                    "level": "hint",
                    "timestamp": 1733611453,
                    "unit": "seconds",
                    "uri": "/a/random/relative/uri",
                    "value": 13800,
                },
            ]
        },
        {
            "items": [
                {
                    "handling": "acknowledge",
                    "key": EventKey.BSH_COMMON_EVENT_PROGRAM_ABORTED.value,
                    "level": "hint",
                    "timestamp": 1733616930,
                    "value": "BSH.Common.EnumType.EventPresentState.Present",
                }
            ],
        },
        {
            "handling": "none",
            "key": "BSH.Common.Appliance.Disconnected",
            "level": "hint",
            "timestamp": 1733611817,
            "value": True,
        },
        None,
    ],
)
async def test_stream_events(
    httpx_client: AsyncClient, httpx_mock: HTTPXMock, event_data: dict[str, Any] | None
) -> None:
    """Test stream events from a specific home appliance."""
    ha_id = "SIEMENS-HCS02DWH1-6BE58C26DCC1"
    event_type = EventType.NOTIFY
    httpx_mock.add_response(
        url=f"https://example.com/api/homeappliances/{ha_id}/events",
        stream=IteratorStream(
            [
                "\n".join(
                    [
                        f"id: {ha_id}",
                        f"data: {json.dumps(event_data) if event_data else ""}",
                        f"event: {event_type}",
                        "\n",
                    ]
                ).encode()
            ]
        ),
        headers={"Content-Type": "text/event-stream"},
    )

    client = Client(AuthClient(httpx_client, "https://example.com"))

    async for event_message in client.stream_events(ha_id):
        assert event_message.ha_id == ha_id
        assert event_message.type == event_type
        if not event_data:
            assert len(event_message.data.items) == 0
        elif items := event_data.get("items"):
            assert len(event_message.data.items) == len(items)
        else:
            assert len(event_message.data.items) == 1


async def test_stream_events_http_error(
    httpx_client: AsyncClient, httpx_mock: HTTPXMock
) -> None:
    """Test stream events from a specific home appliance http error."""
    ha_id = "SIEMENS-HCS02DWH1-6BE58C26DCC1"
    httpx_mock.add_response(
        url=f"https://example.com/api/homeappliances/{ha_id}/events",
        status_code=500,
    )

    client = Client(AuthClient(httpx_client, "https://example.com"))

    with pytest.raises(httpx.HTTPStatusError, match=r".*500 Internal Server Error.*"):
        await anext(client.stream_events(ha_id))
