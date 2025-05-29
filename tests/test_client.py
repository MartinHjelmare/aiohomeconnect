"""Test the client."""

import json

from httpx import AsyncClient, ReadTimeout, RequestError, codes
import pytest
from pytest_httpx import HTTPXMock, IteratorStream

from aiohomeconnect.client import AbstractAuth, Client
from aiohomeconnect.model import ArrayOfEvents, Event, EventKey, EventMessage, EventType
from aiohomeconnect.model.error import (
    EventStreamInterruptedError,
    ForbiddenError,
    HomeConnectApiError,
    HomeConnectRequestError,
    InternalServerError,
    NotAcceptableError,
    RequestTimeoutError,
    TooManyRequestsError,
    UnauthorizedError,
    UnsupportedMediaTypeError,
)

TEST_ACCESS_TOKEN = "1234"
TEST_HA_ID = "SIEMENS-HCS02DWH1-6BE58C26DCC1"
TEST_EVENT_TYPE = EventType.NOTIFY

STREAM_EVENT_CASES = [
    (
        json.dumps(
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
            }
        ),
        EventMessage(
            TEST_HA_ID,
            TEST_EVENT_TYPE,
            ArrayOfEvents(
                [
                    Event(
                        handling="none",
                        key=EventKey.DISHCARE_DISHWASHER_OPTION_HALF_LOAD,
                        raw_key=EventKey.DISHCARE_DISHWASHER_OPTION_HALF_LOAD.value,
                        level="hint",
                        timestamp=1733611453,
                        uri="/a/random/relative/uri",
                        value=True,
                    ),
                    Event(
                        handling="none",
                        key=EventKey.BSH_COMMON_OPTION_REMAINING_PROGRAM_TIME,
                        raw_key=EventKey.BSH_COMMON_OPTION_REMAINING_PROGRAM_TIME.value,
                        level="hint",
                        timestamp=1733611453,
                        unit="seconds",
                        uri="/a/random/relative/uri",
                        value=13800,
                    ),
                ]
            ),
        ),
    ),
    (
        json.dumps(
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
            }
        ),
        EventMessage(
            TEST_HA_ID,
            TEST_EVENT_TYPE,
            ArrayOfEvents(
                [
                    Event(
                        handling="acknowledge",
                        key=EventKey.BSH_COMMON_EVENT_PROGRAM_ABORTED,
                        raw_key=EventKey.BSH_COMMON_EVENT_PROGRAM_ABORTED.value,
                        level="hint",
                        timestamp=1733616930,
                        value="BSH.Common.EnumType.EventPresentState.Present",
                    )
                ]
            ),
        ),
    ),
    (
        json.dumps(
            {
                "handling": "none",
                "key": "BSH.Common.Appliance.Disconnected",
                "level": "hint",
                "timestamp": 1733611817,
                "value": True,
            }
        ),
        EventMessage(
            TEST_HA_ID,
            TEST_EVENT_TYPE,
            ArrayOfEvents(
                [
                    Event(
                        handling="none",
                        key=EventKey.BSH_COMMON_APPLIANCE_DISCONNECTED,
                        raw_key=EventKey.BSH_COMMON_APPLIANCE_DISCONNECTED.value,
                        level="hint",
                        timestamp=1733611817,
                        value=True,
                    )
                ]
            ),
        ),
    ),
    (
        "",
        EventMessage(TEST_HA_ID, TEST_EVENT_TYPE, ArrayOfEvents([])),
    ),
]


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
    ("status_code", "exception"),
    [
        (codes.UNAUTHORIZED, UnauthorizedError),
        (codes.FORBIDDEN, ForbiddenError),
        (codes.NOT_ACCEPTABLE, NotAcceptableError),
        (codes.REQUEST_TIMEOUT, RequestTimeoutError),
        (codes.UNSUPPORTED_MEDIA_TYPE, UnsupportedMediaTypeError),
        (codes.IM_A_TEAPOT, HomeConnectApiError),
        (codes.INTERNAL_SERVER_ERROR, InternalServerError),
    ],
)
async def test_generic_http_error(
    httpx_client: AsyncClient,
    httpx_mock: HTTPXMock,
    status_code: int,
    exception: type[Exception],
) -> None:
    """Test stream all events http error."""
    httpx_mock.add_response(
        url="https://example.com/api/homeappliances",
        status_code=status_code,
        json={
            "error": {"key": "some_error_key", "description": "some_error_description"}
        },
    )

    client = Client(AuthClient(httpx_client, "https://example.com"))

    with pytest.raises(exception):
        await client.get_home_appliances()


async def test_generic_http_error_no_content(
    httpx_client: AsyncClient,
    httpx_mock: HTTPXMock,
) -> None:
    """Test stream all events http error with no content."""
    httpx_mock.add_response(
        url="https://example.com/api/homeappliances",
        status_code=codes.IM_A_TEAPOT,
    )

    client = Client(AuthClient(httpx_client, "https://example.com"))

    with pytest.raises(HomeConnectApiError):
        await client.get_home_appliances()


async def test_rate_limit_error(
    httpx_client: AsyncClient, httpx_mock: HTTPXMock
) -> None:
    """Test the abstract auth request."""
    httpx_mock.add_response(
        url="https://example.com/api/homeappliances",
        status_code=codes.TOO_MANY_REQUESTS,
        json={
            "error": {"key": "some_error_key", "description": "some_error_description"}
        },
        headers={"Retry-After": "1"},
    )

    client = Client(AuthClient(httpx_client, "https://example.com"))

    with pytest.raises(TooManyRequestsError) as exc_info:
        await client.get_home_appliances()

    assert exc_info.value.key == "some_error_key"
    assert exc_info.value.description == "some_error_description"
    assert exc_info.value.retry_after == 1


async def test_request_error(
    httpx_client: AsyncClient,
    httpx_mock: HTTPXMock,
) -> None:
    """Test stream events from a specific home appliance http error."""
    httpx_mock.add_exception(
        exception=RequestError("some error"),
        url="https://example.com/api/homeappliances",
    )

    client = Client(AuthClient(httpx_client, "https://example.com"))

    with pytest.raises(HomeConnectRequestError):
        await client.get_home_appliances()


@pytest.mark.parametrize(
    ("event_data", "event_message"),
    STREAM_EVENT_CASES,
)
async def test_stream_all_events(
    httpx_client: AsyncClient,
    httpx_mock: HTTPXMock,
    event_data: str,
    event_message: EventMessage,
) -> None:
    """Test stream all events."""
    httpx_mock.add_response(
        url="https://example.com/api/homeappliances/events",
        stream=IteratorStream(
            [
                "\n".join(
                    [
                        f"id: {TEST_HA_ID}",
                        f"data: {event_data}",
                        f"event: {TEST_EVENT_TYPE}",
                        "\n",
                    ]
                ).encode()
            ]
        ),
        headers={"Content-Type": "text/event-stream"},
    )

    client = Client(AuthClient(httpx_client, "https://example.com"))

    assert await anext(client.stream_all_events()) == event_message


@pytest.mark.parametrize(
    ("status_code", "exception"),
    [
        (codes.UNAUTHORIZED, UnauthorizedError),
        (codes.FORBIDDEN, ForbiddenError),
        (codes.NOT_ACCEPTABLE, NotAcceptableError),
        (codes.IM_A_TEAPOT, HomeConnectApiError),
        (codes.TOO_MANY_REQUESTS, TooManyRequestsError),
        (codes.INTERNAL_SERVER_ERROR, InternalServerError),
    ],
)
async def test_stream_all_events_http_error(
    httpx_client: AsyncClient,
    httpx_mock: HTTPXMock,
    status_code: int,
    exception: type[Exception],
) -> None:
    """Test stream all events http error."""
    httpx_mock.add_response(
        url="https://example.com/api/homeappliances/events",
        status_code=status_code,
        json={
            "error": {"key": "some_error_key", "description": "some_error_description"}
        },
    )

    client = Client(AuthClient(httpx_client, "https://example.com"))

    with pytest.raises(exception):
        await anext(client.stream_all_events())


@pytest.mark.parametrize(
    ("event_data", "event_message"),
    STREAM_EVENT_CASES,
)
async def test_stream_events(
    httpx_client: AsyncClient,
    httpx_mock: HTTPXMock,
    event_data: str,
    event_message: EventMessage,
) -> None:
    """Test stream events from a specific home appliance."""
    httpx_mock.add_response(
        url=f"https://example.com/api/homeappliances/{TEST_HA_ID}/events",
        stream=IteratorStream(
            [
                "\n".join(
                    [
                        f"id: {TEST_HA_ID}",
                        f"data: {event_data}",
                        f"event: {TEST_EVENT_TYPE}",
                        "\n",
                    ]
                ).encode()
            ]
        ),
        headers={"Content-Type": "text/event-stream"},
    )

    client = Client(AuthClient(httpx_client, "https://example.com"))

    assert await anext(client.stream_events(TEST_HA_ID)) == event_message


@pytest.mark.parametrize(
    ("status_code", "exception"),
    [
        (401, UnauthorizedError),
        (403, ForbiddenError),
        (406, NotAcceptableError),
        (418, HomeConnectApiError),
        (429, TooManyRequestsError),
        (500, InternalServerError),
    ],
)
async def test_stream_events_http_error(
    httpx_client: AsyncClient,
    httpx_mock: HTTPXMock,
    status_code: int,
    exception: type[Exception],
) -> None:
    """Test stream events from a specific home appliance http error."""
    httpx_mock.add_response(
        url=f"https://example.com/api/homeappliances/{TEST_HA_ID}/events",
        status_code=status_code,
        json={
            "error": {"key": "some_error_key", "description": "some_error_description"}
        },
    )

    client = Client(AuthClient(httpx_client, "https://example.com"))

    with pytest.raises(exception):
        await anext(client.stream_events(TEST_HA_ID))


@pytest.mark.parametrize(
    ("exception", "expected_exception"),
    [
        (ReadTimeout, EventStreamInterruptedError),
        (RequestError, HomeConnectRequestError),
    ],
)
async def test_stream_events_request_error(
    httpx_client: AsyncClient,
    httpx_mock: HTTPXMock,
    exception: type[Exception],
    expected_exception: type[Exception],
) -> None:
    """Test stream events from a specific home appliance http error."""
    httpx_mock.add_exception(
        exception=exception("some error"),
        url="https://example.com/api/homeappliances/events",
    )

    client = Client(AuthClient(httpx_client, "https://example.com"))

    with pytest.raises(expected_exception):
        await anext(client.stream_all_events())
