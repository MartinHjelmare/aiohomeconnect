"""Provide a client to receive Server Sent Events (SSE) from the Home Connect API."""

from collections.abc import Callable, Coroutine
from json import JSONDecodeError
import logging
from typing import Any

from httpx import AsyncClient, ReadTimeout, Timeout
from httpx_sse import ServerSentEvent, aconnect_sse
from mashumaro.exceptions import InvalidFieldValue

from .model import ArrayOfEvents, Event, EventKey, EventTypes, Language

_LOGGER = logging.getLogger(__name__)


class SSEClient:
    """Represent a SSE client to receive events for the Home Connect API."""

    def __init__(self, client: AsyncClient) -> None:
        """Initialize the SSE client."""
        self._status_callbacks: dict[
            str, dict[EventKey, Callable[[Event], Coroutine[Any, Any, None]]]
        ] = {}
        self._event_callbacks: dict[
            str, dict[EventKey, Callable[[Event], Coroutine[Any, Any, None]]]
        ] = {}
        self._notify_callbacks: dict[
            str, dict[EventKey, Callable[[Event], Coroutine[Any, Any, None]]]
        ] = {}

        async def foo_function(_: EventTypes, __: str) -> None:
            pass

        self.home_appliances_changes_callback: Callable[
            [EventTypes, str], Coroutine[Any, Any, None]
        ] = foo_function
        self._client = client

    async def _stream(
        self,
        url: str,
        *,
        accept_language: Language | None = None,
    ) -> None:
        """Stream events from the Home Connect API."""
        async with aconnect_sse(
            self._client,
            "GET",
            url,
            timeout=Timeout(60),
            headers={
                "Accept-Language": accept_language,
            },
        ) as event_source:
            event_source.response.raise_for_status()
            try:
                async for event in event_source.aiter_sse():
                    _LOGGER.debug(
                        'Received event type "%s" with the following data: %s',
                        event.event,
                        event.data,
                    )
                    await self._message_handler(event)
            except ReadTimeout:
                _LOGGER.debug("Connection timed out")
            else:
                _LOGGER.debug("Connection closed cleanly")

    async def stream_all_events(
        self,
        *,
        accept_language: Language | None = None,
    ) -> None:
        """Stream all events from the Home Connect API."""
        await self._stream(
            "/homeappliances/events",
            accept_language=accept_language,
        )

    async def stream_events(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = None,
    ) -> None:
        """Stream events for a specific home appliance from the Home Connect API."""
        await self._stream(
            f"/homeappliances/{ha_id}/events",
            accept_language=accept_language,
        )

    async def _message_handler(self, message_event: ServerSentEvent) -> None:
        """Match event with callback for event type."""
        event_type = EventTypes(message_event.event)
        if event_type == EventTypes.KEEP_ALIVE:
            return
        ha_id = message_event.id
        match event_type:
            case EventTypes.STATUS | EventTypes.EVENT | EventTypes.NOTIFY:
                try:
                    events = ArrayOfEvents.from_json(message_event.data)
                except JSONDecodeError as err:
                    _LOGGER.debug("Error parsing event: %s", err)
                except InvalidFieldValue as err:
                    _LOGGER.debug("Error parsing event: %s", err)
                else:
                    await self._event_handler(events, event_type, ha_id)
            case (
                EventTypes.CONNECTED
                | EventTypes.DISCONNECTED
                | EventTypes.PAIRED
                | EventTypes.DEPAIRED
            ):
                await self.home_appliances_changes_callback(event_type, ha_id)

    async def _event_handler(
        self, events: ArrayOfEvents, event_type: EventTypes, ha_id: str
    ) -> None:
        async def default_function(_: Event) -> None:
            pass

        for event in events.items:
            match event_type:
                case EventTypes.STATUS:
                    callback = self._status_callbacks.get(ha_id, {}).get(
                        event.key,
                        default_function,
                    )
                case EventTypes.EVENT:
                    callback = self._event_callbacks.get(ha_id, {}).get(
                        event.key,
                        default_function,
                    )
                case EventTypes.NOTIFY:
                    callback = self._notify_callbacks.get(ha_id, {}).get(
                        event.key,
                        default_function,
                    )
            await callback(event)

    def register_status_callback(
        self,
        ha_id: str,
        event_key: EventKey,
        cb: Callable[[Event], Coroutine[Any, Any, None]],
    ) -> Callable[[], None]:
        """Register a status callback for a specific home appliance and event key."""
        if (
            ha_id in self._status_callbacks
            and event_key in self._status_callbacks[ha_id]
        ):
            _LOGGER.warning(
                "Status callback for %s already exists, overwriting", str(event_key)
            )

        self._status_callbacks.setdefault(ha_id, {})[event_key] = cb

        def remove_callback() -> None:
            self.deregister_status_callback(ha_id, event_key)

        return remove_callback

    def deregister_status_callback(self, ha_id: str, event_key: EventKey) -> None:
        """Deregister status callback for a specific home appliance and event key."""
        if (
            ha_id in self._status_callbacks
            and event_key in self._status_callbacks[ha_id]
        ):
            del self._status_callbacks[ha_id][event_key]

    def register_event_callback(
        self,
        ha_id: str,
        event_key: EventKey,
        cb: Callable[[Event], Coroutine[Any, Any, None]],
    ) -> Callable[[], None]:
        """Register a event callback for a specific home appliance and event key."""
        if ha_id in self._event_callbacks and event_key in self._event_callbacks[ha_id]:
            _LOGGER.warning(
                "Event callback for %s already exists, overwriting", str(event_key)
            )

        self._event_callbacks.setdefault(ha_id, {})[event_key] = cb

        def remove_callback() -> None:
            self.deregister_event_callback(ha_id, event_key)

        return remove_callback

    def deregister_event_callback(self, ha_id: str, event_key: EventKey) -> None:
        """Deregister event callback for a specific home appliance and event key."""
        if ha_id in self._event_callbacks and event_key in self._event_callbacks[ha_id]:
            del self._event_callbacks[ha_id][event_key]

    def register_notify_callback(
        self,
        ha_id: str,
        event_key: EventKey,
        cb: Callable[[Event], Coroutine[Any, Any, None]],
    ) -> Callable[[], None]:
        """Register a notify callback for a specific home appliance and event key."""
        if (
            ha_id in self._notify_callbacks
            and event_key in self._notify_callbacks[ha_id]
        ):
            _LOGGER.warning(
                "Notify callback for %s already exists, overwriting", str(event_key)
            )

        self._notify_callbacks.setdefault(ha_id, {})[event_key] = cb

        def remove_callback() -> None:
            self.deregister_notify_callback(ha_id, event_key)

        return remove_callback

    def deregister_notify_callback(self, ha_id: str, event_key: EventKey) -> None:
        """Deregister notify callback for a specific home appliance and event key."""
        if (
            ha_id in self._notify_callbacks
            and event_key in self._notify_callbacks[ha_id]
        ):
            del self._notify_callbacks[ha_id][event_key]
