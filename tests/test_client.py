"""Test the client."""

from httpx import AsyncClient
from pytest_httpx import HTTPXMock, IteratorStream

from aiohomeconnect.client import AbstractAuth

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
