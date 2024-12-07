"""Test the client."""

from unittest.mock import AsyncMock

from httpx import AsyncClient
import pytest
from pytest_httpx import HTTPXMock, IteratorStream

from aiohomeconnect.client import AbstractAuth, SSEClient
from aiohomeconnect.model.event import ArrayOfEvents, Event, EventKey, EventTypes

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
    ("event_type", "event_key", "register_callback_function"),
    [
        (
            EventTypes.NOTIFY,
            EventKey.BSH_COMMON_SETTING_POWER_STATE,
            "register_notify_callback",
        ),
        (
            EventTypes.EVENT,
            EventKey.BSH_COMMON_SETTING_POWER_STATE,
            "register_event_callback",
        ),
        (
            EventTypes.STATUS,
            EventKey.BSH_COMMON_STATUS_DOOR_STATE,
            "register_status_callback",
        ),
    ],
)
async def test_key_callbacks(
    httpx_client: AsyncClient,
    httpx_mock: HTTPXMock,
    event_type: EventTypes,
    event_key: EventKey,
    register_callback_function: str,
) -> None:
    """Test the SSE Client."""
    ha_id = "BOSCH-HNG6764B6-0000000011FF"
    event = Event(
        event_key,
        1556793979,
        "hint",
        "none",
        200,
        "Target temperature for the oven",
        f"/api/homeappliances/{ha_id}",
        unit="°C",
    )
    events = ArrayOfEvents([event])
    event_data = events.to_json()
    if isinstance(event_data, bytes | bytearray):
        event_data = event_data.decode("utf-8")

    httpx_mock.add_response(
        url=f"https://example.com/api/homeappliances/{ha_id}/events",
        stream=IteratorStream(
            [
                f"event:{event_type}\ndata:{event_data}\nid:{ha_id}\n\n".encode(),
            ]
        ),
        headers={"Content-Type": "text/event-stream"},
    )

    client = AuthClient(httpx_client, "https://example.com")
    sse_client = SSEClient(client)

    mock = AsyncMock()
    deregister_callback = getattr(sse_client, register_callback_function)(
        ha_id, event_key, mock
    )

    await sse_client.stream_events(ha_id)

    mock.assert_called_once_with(event)
    deregister_callback()


@pytest.mark.parametrize(
    "event_type",
    [
        EventTypes.CONNECTED,
        EventTypes.DISCONNECTED,
        EventTypes.PAIRED,
        EventTypes.DEPAIRED,
    ],
)
async def test_home_appliance_changes_callbacks(
    httpx_client: AsyncClient,
    httpx_mock: HTTPXMock,
    event_type: EventTypes,
) -> None:
    """Test the SSE Client."""
    ha_id = "BOSCH-HNG6764B6-0000000011FF"

    httpx_mock.add_response(
        url="https://example.com/api/homeappliances/events",
        stream=IteratorStream(
            [
                f"event:{event_type}\nid:{ha_id}\n\n".encode(),
            ]
        ),
        headers={"Content-Type": "text/event-stream"},
    )

    client = AuthClient(httpx_client, "https://example.com")
    sse_client = SSEClient(client)

    mock = AsyncMock()
    sse_client.home_appliances_changes_callback = mock

    await sse_client.stream_all_events()

    mock.assert_called_once_with(event_type, ha_id)
