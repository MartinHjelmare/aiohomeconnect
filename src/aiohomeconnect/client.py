"""Provide a client for Home Connect API."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Callable, Coroutine
from contextlib import asynccontextmanager
from json import JSONDecodeError
import logging
from typing import Any

from httpx import AsyncClient, ReadTimeout, Response, Timeout
from httpx_sse import EventSource, ServerSentEvent, aconnect_sse
from mashumaro.exceptions import InvalidFieldValue

from .model import (
    ArrayOfAvailablePrograms,
    ArrayOfCommands,
    ArrayOfEvents,
    ArrayOfHomeAppliances,
    ArrayOfImages,
    ArrayOfOptions,
    ArrayOfPrograms,
    ArrayOfSettings,
    ArrayOfStatus,
    CommandKey,
    Event,
    EventKey,
    EventTypes,
    GetSetting,
    HomeAppliance,
    Language,
    Option,
    OptionKey,
    Program,
    ProgramConstraints,
    ProgramDefinition,
    ProgramKey,
    PutCommand,
    PutCommands,
    PutSetting,
    PutSettings,
    SettingKey,
    Status,
    StatusKey,
)

_LOGGER = logging.getLogger(__name__)


class AbstractAuth(ABC):
    """Abstract class to make authenticated requests."""

    def __init__(self, httpx_client: AsyncClient, host: str) -> None:
        """Initialize the auth."""
        self.client = httpx_client
        self.host = host

    @abstractmethod
    async def async_get_access_token(self) -> str:
        """Return a valid access token."""

    async def _get_headers(self, headers: dict[str, str] | None) -> dict[str, str]:
        """Return the headers for the request."""
        headers = {} if headers is None else dict(headers)
        headers = {key: val for key, val in headers.items() if val is not None}

        access_token = await self.async_get_access_token()
        headers["authorization"] = f"Bearer {access_token}"
        return headers

    async def request(self, method: str, url: str, **kwargs: Any) -> Response:
        """Make a request.

        The url parameter must start with a slash.
        """
        headers = await self._get_headers(kwargs.pop("headers", None))

        return await self.client.request(
            method,
            f"{self.host}/api{url}",
            **kwargs,
            headers=headers,
        )

    @asynccontextmanager
    async def connect_sse(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> AsyncIterator[EventSource]:
        """Create a SSE connection."""
        headers = await self._get_headers(kwargs.pop("headers", None))

        async with aconnect_sse(
            self.client,
            method,
            f"{self.host}/api{url}",
            **kwargs,
            headers=headers,
        ) as event_source:
            yield event_source


class SSEClient:
    """Represent a SSE client to receive events for the Home Connect API."""

    def __init__(self, auth: AbstractAuth) -> None:
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
        self._auth = auth

    async def _stream(
        self,
        url: str,
        *,
        accept_language: Language | None = None,
    ) -> None:
        """Stream events from the Home Connect API."""
        async with self._auth.connect_sse(
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


class Client:
    """Represent a client for the Home Connect API."""

    def __init__(self, auth: AbstractAuth) -> None:
        """Initialize the client."""
        self._auth = auth
        self._sse = SSEClient(auth)

    @property
    def sse(self) -> SSEClient:
        """Return the SSE client."""
        return self._sse

    async def get_home_appliances(self) -> ArrayOfHomeAppliances:
        """Get all home appliances which are paired with the logged-in user account.

        This endpoint returns a list of all home appliances which are paired
        with the logged-in user account. All paired home appliances are returned
        independent of their current connection state. The connection state can
        be retrieved within the field 'connected' of the respective home appliance.
        The haId is the primary access key for further API access to a specific
        home appliance.
        """
        response = await self._auth.request(
            "GET",
            "/homeappliances",
            headers=None,
        )
        return ArrayOfHomeAppliances.from_dict(response.json()["data"])

    async def get_specific_appliance(
        self,
        ha_id: str,
    ) -> HomeAppliance:
        """Get a specific paired home appliance.

        This endpoint returns a specific home appliance which is paired with the
        logged-in user account. It is returned independent of their current
        connection state. The connection state can be retrieved within the field
        'connected' of the respective home appliance.
        The haId is the primary access key for further API access to a specific
        home appliance.
        """
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}",
            headers=None,
        )
        return HomeAppliance.from_dict(response.json()["data"])

    async def get_all_programs(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = None,
    ) -> ArrayOfPrograms:
        """Get all programs of a given home appliance."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/programs",
            headers={"Accept-Language": accept_language},
        )
        return ArrayOfPrograms.from_dict(response.json()["data"])

    async def get_available_programs(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = None,
    ) -> ArrayOfAvailablePrograms:
        """Get all currently available programs on the given home appliance."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/programs/available",
            headers={"Accept-Language": accept_language},
        )
        return ArrayOfAvailablePrograms.from_dict(response.json()["data"])

    async def get_available_program(
        self,
        ha_id: str,
        *,
        program_key: ProgramKey,
        accept_language: Language | None = None,
    ) -> ProgramDefinition:
        """Get a specific available program."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/programs/available/{program_key}",
            headers={"Accept-Language": accept_language},
        )
        return ProgramDefinition.from_dict(response.json()["data"])

    async def get_active_program(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = None,
    ) -> Program:
        """Get the active program."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/programs/active",
            headers={"Accept-Language": accept_language},
        )
        return Program.from_dict(response.json()["data"])

    async def start_program(
        self,
        ha_id: str,
        *,
        program_key: ProgramKey,
        name: str | None = None,
        options: list[Option] | None = None,
        constraints: ProgramConstraints | None = None,
        accept_language: Language | None = None,
    ) -> None:
        """Start the given program.

        By putting a program object to this endpoint, the system will try to
        start it if all preconditions are fulfilled:
        * Home appliance is connected
        * *Remote Control* and *Remote Control Start Allowed* is enabled
        * No other program is currently active

        Furthermore, the program must exist on the home appliance and its
        options must be set correctly.
        Keys of program, which can be executed on an oven, are for instance:
        * *Cooking.Oven.Program.HeatingMode.HotAir*
        * *Cooking.Oven.Program.HeatingMode.TopBottomHeating*
        * *Cooking.Oven.Program.HeatingMode.PizzaSetting*
        * *Cooking.Oven.Program.HeatingMode.PreHeating*

        Keys for options of these oven programs are:
        * *Cooking.Oven.Option.SetpointTemperature*: 30 - 250 °C
        * *BSH.Common.Option.Duration*: 1 - 86340 seconds

        For further documentation, visit the appliance-specific programs pages:
        * [Cleaning Robot](https://api-docs.home-connect.com/programs-and-options?#cleaning-robot)
        * [Coffee Machine](https://api-docs.home-connect.com/programs-and-options?#coffee-machine)
        * [Cooktop](https://api-docs.home-connect.com/programs-and-options?#cooktop)
        * [Cook Processor](https://api-docs.home-connect.com/programs-and-options?#cook-processor)
        * [Dishwasher](https://api-docs.home-connect.com/programs-and-options?#dishwasher)
        * [Dryer](https://api-docs.home-connect.com/programs-and-options?#dryer)
        * [Hood](https://api-docs.home-connect.com/programs-and-options?#hood)
        * [Oven](https://api-docs.home-connect.com/programs-and-options?#oven)
        * [Warming Drawer](https://api-docs.home-connect.com/programs-and-options?#warming-drawer)
        * [Washer](https://api-docs.home-connect.com/programs-and-options?#washer)
        * [Washer Dryer](https://api-docs.home-connect.com/programs-and-options?#washer-dryer)

        There are no programs available for freezers, fridge freezers,
        refrigerators and wine coolers.
        """
        program = Program(
            key=program_key, name=name, options=options, constraints=constraints
        )
        await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/programs/active",
            headers={"Accept-Language": accept_language},
            data=program.to_dict(),
        )

    async def stop_program(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = None,
    ) -> None:
        """Stop the active program."""
        await self._auth.request(
            "DELETE",
            f"/homeappliances/{ha_id}/programs/active",
            headers={"Accept-Language": accept_language},
        )

    async def get_active_program_options(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = None,
    ) -> ArrayOfOptions:
        """Get all options of the active program.

        You can retrieve a list of options of the currently running program.

        For detailed documentation of the available options,
        visit the appliance-specific programs pages:
        * [Cleaning Robot](https://api-docs.home-connect.com/programs-and-options?#cleaning-robot)
        * [Coffee Machine](https://api-docs.home-connect.com/programs-and-options?#coffee-machine)
        * [Cooktop](https://api-docs.home-connect.com/programs-and-options?#cooktop)
        * [Cook Processor](https://api-docs.home-connect.com/programs-and-options?#cook-processor)
        * [Dishwasher](https://api-docs.home-connect.com/programs-and-options?#dishwasher)
        * [Dryer](https://api-docs.home-connect.com/programs-and-options?#dryer)
        * [Hood](https://api-docs.home-connect.com/programs-and-options?#hood)
        * [Oven](https://api-docs.home-connect.com/programs-and-options?#oven)
        * [Warming Drawer](https://api-docs.home-connect.com/programs-and-options?#warming-drawer)
        * [Washer](https://api-docs.home-connect.com/programs-and-options?#washer)
        * [Washer Dryer](https://api-docs.home-connect.com/programs-and-options?#washer-dryer)
        """
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/programs/active/options",
            headers={"Accept-Language": accept_language},
        )
        return ArrayOfOptions.from_dict(response.json()["data"])

    async def set_active_program_options(
        self,
        ha_id: str,
        *,
        array_of_options: ArrayOfOptions,
        accept_language: Language | None = None,
    ) -> None:
        """Set all options of the active program.

        Update the options for the currently running program.
        With this API endpoint, you have to provide all options with
        their new values. If you want to update only one option, you can use the
        endpoint specific to that option.

        Please note that changing options of the running program is currently only
        supported by ovens.
        """
        await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/programs/active/options",
            headers={"Accept-Language": accept_language},
            data=array_of_options.to_dict(),
        )

    async def get_active_program_option(
        self,
        ha_id: str,
        *,
        option_key: OptionKey,
        accept_language: Language | None = None,
    ) -> Option:
        """Get a specific option of the active program."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/programs/active/options/{option_key}",
            headers={"Accept-Language": accept_language},
        )
        return Option.from_dict(response.json()["data"])

    async def set_active_program_option(
        self,
        ha_id: str,
        *,
        option_key: OptionKey,
        value: Any,
        name: str | None = None,
        display_value: str | None = None,
        unit: str | None = None,
        accept_language: Language | None = None,
    ) -> None:
        """Set a specific option of the active program.

        This operation can be used to modify one specific option of the active
        program, e.g. to extend the duration of the active program by
        another 5 minutes.

        Please note that changing options of the running program is currently only
        supported by ovens.
        """
        option = Option(
            key=option_key,
            name=name,
            value=value,
            display_value=display_value,
            unit=unit,
        )
        await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/programs/active/options/{option_key}",
            headers={"Accept-Language": accept_language},
            data=option.to_dict(),
        )

    async def get_selected_program(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = None,
    ) -> Program:
        """Get the selected program.

        In most cases the selected program is the program which is currently
        shown on the display of the home appliance. This program can then be
        manually adjusted or started on the home appliance itself.
        """
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/programs/selected",
            headers={"Accept-Language": accept_language},
        )
        return Program.from_dict(response.json()["data"])

    async def set_selected_program(
        self,
        ha_id: str,
        *,
        program_key: ProgramKey,
        name: str | None = None,
        options: list[Option] | None = None,
        constraints: ProgramConstraints | None = None,
        accept_language: Language | None = None,
    ) -> None:
        """Select the given program.

        In most cases the selected program is the program which is currently
        shown on the display of the home appliance. This program can then be
        manually adjusted or started on the home appliance itself.

        A selected program will not be started automatically. You don't have
        to set a program as selected first if you intend to start it via API -
        you can set it directly as active program.

        Selecting a program will update the available options and constraints
        directly from the home appliance. Any changes to the available options
        due to the state of the appliance is only reflected in the selected program.
        """
        program = Program(
            key=program_key, name=name, options=options, constraints=constraints
        )
        await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/programs/selected",
            headers={"Accept-Language": accept_language},
            data=program.to_dict(),
        )

    async def get_selected_program_options(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = None,
    ) -> ArrayOfOptions:
        """Get all options of the selected program."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/programs/selected/options",
            headers={"Accept-Language": accept_language},
        )
        return ArrayOfOptions.from_dict(response.json()["data"])

    async def set_selected_program_options(
        self,
        ha_id: str,
        *,
        array_of_options: ArrayOfOptions,
        accept_language: Language | None = None,
    ) -> None:
        """Set all options of the selected program."""
        await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/programs/selected/options",
            headers={"Accept-Language": accept_language},
            data=array_of_options.to_dict(),
        )

    async def get_selected_program_option(
        self,
        ha_id: str,
        *,
        option_key: OptionKey,
        accept_language: Language | None = None,
    ) -> Option:
        """Get a specific option of the selected program."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/programs/selected/options/{option_key}",
            headers={"Accept-Language": accept_language},
        )
        return Option.from_dict(response.json()["data"])

    async def set_selected_program_option(
        self,
        ha_id: str,
        *,
        option_key: OptionKey,
        value: Any,
        name: str | None = None,
        display_value: str | None = None,
        unit: str | None = None,
        accept_language: Language | None = None,
    ) -> None:
        """Set a specific option of the selected program."""
        option = Option(
            key=option_key,
            name=name,
            value=value,
            display_value=display_value,
            unit=unit,
        )
        await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/programs/selected/options/{option_key}",
            headers={"Accept-Language": accept_language},
            data=option.to_dict(),
        )

    async def get_images(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = None,
    ) -> ArrayOfImages:
        """Get a list of available images."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/images",
            headers={"Accept-Language": accept_language},
        )
        return ArrayOfImages.from_dict(response.json()["data"])

    async def get_image(
        self,
        ha_id: str,
        *,
        image_key: str,
    ) -> None:
        """Get a specific image."""
        await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/images/{image_key}",
            headers=None,
        )

    async def get_settings(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = None,
    ) -> ArrayOfSettings:
        """Get a list of available settings.

        Get a list of available setting of the home appliance.

        Further documentation
        can be found [here](https://api-docs.home-connect.com/settings).
        """
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/settings",
            headers={"Accept-Language": accept_language},
        )
        return ArrayOfSettings.from_dict(response.json()["data"])

    async def set_settings(
        self,
        ha_id: str,
        *,
        put_settings: PutSettings,
        accept_language: Language | None = None,
    ) -> None:
        """Set multiple settings."""
        await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/settings",
            headers={"Accept-Language": accept_language},
            data=put_settings.to_dict(),
        )

    async def get_setting(
        self,
        ha_id: str,
        *,
        setting_key: SettingKey,
        accept_language: Language | None = None,
    ) -> GetSetting:
        """Get a specific setting."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/settings/{setting_key}",
            headers={"Accept-Language": accept_language},
        )
        return GetSetting.from_dict(response.json()["data"])

    async def set_setting(
        self,
        ha_id: str,
        *,
        setting_key: SettingKey,
        value: Any,
        accept_language: Language | None = None,
    ) -> None:
        """Set a specific setting."""
        put_setting = PutSetting(key=setting_key, value=value)
        await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/settings/{setting_key}",
            headers={"Accept-Language": accept_language},
            data=put_setting.to_dict(),
        )

    async def get_status(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = None,
    ) -> ArrayOfStatus:
        """Get a list of available status.

        A detailed description of the available status
        can be found [here](https://api-docs.home-connect.com/states).
        """
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/status",
            headers={"Accept-Language": accept_language},
        )
        return ArrayOfStatus.from_dict(response.json()["data"])

    async def get_status_value(
        self,
        ha_id: str,
        *,
        status_key: StatusKey,
        accept_language: Language | None = None,
    ) -> Status:
        """Get a specific status.

        A detailed description of the available status
        can be found [here](https://api-docs.home-connect.com/states).
        """
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/status/{status_key}",
            headers={"Accept-Language": accept_language},
        )
        return Status.from_dict(response.json()["data"])

    async def get_available_commands(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = None,
    ) -> ArrayOfCommands:
        """Get a list of available and writable commands."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/commands",
            headers={"Accept-Language": accept_language},
        )
        return ArrayOfCommands.from_dict(response.json()["data"])

    async def put_commands(
        self,
        ha_id: str,
        *,
        put_commands: PutCommands,
        accept_language: Language | None = None,
    ) -> None:
        """Execute multiple commands."""
        await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/commands",
            headers={"Accept-Language": accept_language},
            data=put_commands.to_dict(),
        )

    async def put_command(
        self,
        ha_id: str,
        *,
        command_key: CommandKey,
        value: Any,
        accept_language: Language | None = None,
    ) -> None:
        """Execute a specific command."""
        put_command = PutCommand(key=command_key, value=value)
        await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/commands/{command_key}",
            headers={"Accept-Language": accept_language},
            data=put_command.to_dict(),
        )

    async def get_all_events(
        self,
        *,
        accept_language: Language | None = None,
    ) -> ArrayOfEvents:
        """Get stream of events for all appliances - NOT WORKING WITH SWAGGER.

        Server Sent Events are available as Eventsource API in JavaScript
        and are implemented by various HTTP client libraries and tools
        including curl.

        Unfortunately, SSE is not compatible to OpenAPI specs and can therefore
        not be properly specified within this API description.

        An SSE event contains three parts separated by linebreaks: event, data and id.
        Different events are separated by empty lines.

        The event field can be one of these types:
        KEEP-ALIVE, STATUS, EVENT, NOTIFY, CONNECTED, DISCONNECTED, PAIRED, DEPAIRED.

        In case of all event types (except KEEP-ALIVE),
        the "data" field is populated with the JSON object defined below.

        The id contains the home appliance ID. (except for KEEP-ALIVE event type)

        Further documentation can be found here:
        * [Events availability matrix](https://api-docs.home-connect.com/events#availability-matrix)
        * [Program changes](https://api-docs.home-connect.com/events#program-changes)
        * [Option changes](https://api-docs.home-connect.com/events#option-changes)
        * [Program progress changes](https://api-docs.home-connect.com/events#program-progress-changes)
        * [Home appliance state changes](https://api-docs.home-connect.com/events#home-appliance-state-changes)
        """
        response = await self._auth.request(
            "GET",
            "/homeappliances/events",
            headers={"Accept-Language": accept_language},
        )
        return ArrayOfEvents.from_dict(response.json()["data"])

    async def get_events(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = None,
    ) -> ArrayOfEvents:
        """Get stream of events for one appliance - NOT WORKING WITH SWAGGER.

        If you want to do a one-time query of the current status, you can ask for
        the content-type `application/vnd.bsh.sdk.v1+json` and get the status
        as normal HTTP response.

        If you want an ongoing stream of events in real time, ask for the content
        type `text/event-stream` and you'll get a stream as Server Sent Events.

        Server Sent Events are available as Eventsource API in JavaScript
        and are implemented by various HTTP client libraries and tools
        including curl.

        Unfortunately, SSE is not compatible to OpenAPI specs and can therefore
        not be properly specified within this API description.

        An SSE event contains three parts separated by linebreaks: event, data and id.
        Different events are separated by empty lines.

        The event field can be one of these types:
        KEEP-ALIVE, STATUS, EVENT, NOTIFY, CONNECTED, DISCONNECTED.

        In case of all event types (except KEEP-ALIVE),
        the "data" field is populated with the JSON object defined below.

        The id contains the home appliance ID.

        Further documentation can be found here:
        * [Events availability matrix](https://api-docs.home-connect.com/events#availability-matrix)
        * [Program changes](https://api-docs.home-connect.com/events#program-changes)
        * [Option changes](https://api-docs.home-connect.com/events#option-changes)
        * [Program progress changes](https://api-docs.home-connect.com/events#program-progress-changes)
        * [Home appliance state changes](https://api-docs.home-connect.com/events#home-appliance-state-changes)
        """
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/events",
            headers={"Accept-Language": accept_language},
        )
        return ArrayOfEvents.from_dict(response.json()["data"])
