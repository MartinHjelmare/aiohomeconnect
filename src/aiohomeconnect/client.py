"""Provide a client for Home Connect API."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator, AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from httpx import (
    AsyncClient,
    ReadTimeout,
    RemoteProtocolError,
    RequestError,
    Response,
    Timeout,
    codes,
)
from httpx_sse import EventSource, aconnect_sse

from aiohomeconnect.model import EventMessage, EventType

from .const import LOGGER
from .model import (
    ArrayOfAvailablePrograms,
    ArrayOfCommands,
    ArrayOfHomeAppliances,
    ArrayOfImages,
    ArrayOfOptions,
    ArrayOfPrograms,
    ArrayOfSettings,
    ArrayOfStatus,
    CommandKey,
    GetSetting,
    HomeAppliance,
    Language,
    Option,
    OptionKey,
    Program,
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
from .model.error import (
    ActiveProgramNotSetError,
    Conflict,
    ConflictError,
    EventStreamInterruptedError,
    ForbiddenError,
    HomeConnectApiError,
    HomeConnectRequestError,
    InternalServerError,
    NoProgramActiveError,
    NoProgramSelectedError,
    NotAcceptableError,
    NotFoundError,
    ProgramNotAvailableError,
    RequestTimeoutError,
    SelectedProgramNotSetError,
    TooManyRequestsError,
    UnauthorizedError,
    UnsupportedMediaTypeError,
    WrongOperationStateError,
)


def _raise_generic_error(response: Response) -> None:
    """Raise a generic error if the response is an error."""
    if response.is_error:
        raise (
            HomeConnectApiError.from_dict(error)
            if response.content and (error := response.json().get("error"))
            else HomeConnectApiError(
                "unknown",
                f"Unknown HTTP error (Status code: {response.status_code})",
            )
        )


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
        headers["accept"] = "application/vnd.bsh.sdk.v1+json"
        data = kwargs.pop("data", None)
        if data is not None:
            headers["content-type"] = "application/vnd.bsh.sdk.v1+json"

        LOGGER.debug("Request: %s %s | Data: %s", method, url, data)

        try:
            response = await self.client.request(
                method,
                f"{self.host}/api{url}",
                **kwargs,
                headers=headers,
                json={"data": data} if data is not None else None,
                timeout=Timeout(5, read=30),
            )
        except RequestError as e:
            raise HomeConnectRequestError(f"{type(e).__name__}: {e}") from e

        LOGGER.debug("Response: \n%s", response.text)

        match response.status_code:
            case codes.UNAUTHORIZED:
                raise UnauthorizedError.from_dict(response.json()["error"])
            case codes.FORBIDDEN:
                raise ForbiddenError.from_dict(response.json()["error"])
            case codes.NOT_ACCEPTABLE:
                raise NotAcceptableError.from_dict(response.json()["error"])
            case codes.REQUEST_TIMEOUT:
                raise RequestTimeoutError.from_dict(response.json()["error"])
            case codes.UNSUPPORTED_MEDIA_TYPE:
                raise UnsupportedMediaTypeError.from_dict(response.json()["error"])
            case codes.TOO_MANY_REQUESTS:
                err = TooManyRequestsError.from_dict(response.json()["error"])
                retry_after = response.headers.get("Retry-After")
                err.retry_after = int(retry_after) if retry_after else None
                raise err
            case codes.INTERNAL_SERVER_ERROR:
                raise InternalServerError.from_dict(response.json()["error"])
            case _:
                return response

    @asynccontextmanager
    async def connect_sse(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> AsyncIterator[EventSource]:
        """Create a SSE connection."""
        headers = await self._get_headers(kwargs.pop("headers", None))

        try:
            async with aconnect_sse(
                self.client,
                method,
                f"{self.host}/api{url}",
                **kwargs,
                headers=headers,
            ) as event_source:
                yield event_source
        except (ReadTimeout, RemoteProtocolError) as e:
            raise EventStreamInterruptedError(f"{type(e).__name__}: {e}") from e
        except RequestError as e:
            raise HomeConnectRequestError(f"{type(e).__name__}: {e}") from e


class Client:
    """Represent a client for the Home Connect API."""

    def __init__(self, auth: AbstractAuth) -> None:
        """Initialize the client."""
        self._auth = auth

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
        _raise_generic_error(response)
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
        _raise_generic_error(response)
        return HomeAppliance.from_dict(response.json()["data"])

    async def get_all_programs(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = Language.EN,
    ) -> ArrayOfPrograms:
        """Get all programs of a given home appliance."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/programs",
            headers={"Accept-Language": accept_language},
        )
        match response.status_code:
            case codes.CONFLICT:
                raise Conflict.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)
        return ArrayOfPrograms.from_dict(response.json()["data"])

    async def get_available_programs(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = Language.EN,
    ) -> ArrayOfAvailablePrograms:
        """Get all currently available programs on the given home appliance."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/programs/available",
            headers={"Accept-Language": accept_language},
        )
        match response.status_code:
            case codes.CONFLICT:
                raise WrongOperationStateError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)
        return ArrayOfAvailablePrograms.from_dict(response.json()["data"])

    async def get_available_program(
        self,
        ha_id: str,
        *,
        program_key: ProgramKey,
        accept_language: Language | None = Language.EN,
    ) -> ProgramDefinition:
        """Get a specific available program."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/programs/available/{program_key}",
            headers={"Accept-Language": accept_language},
        )
        match response.status_code:
            case codes.CONFLICT:
                raise ProgramNotAvailableError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)
        return ProgramDefinition.from_dict(response.json()["data"])

    async def get_active_program(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = Language.EN,
    ) -> Program:
        """Get the active program."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/programs/active",
            headers={"Accept-Language": accept_language},
        )
        match response.status_code:
            case codes.NOT_FOUND:
                raise NoProgramActiveError.from_dict(response.json()["error"])
            case codes.CONFLICT:
                raise ConflictError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)
        return Program.from_dict(response.json()["data"])

    async def start_program(
        self,
        ha_id: str,
        *,
        program_key: ProgramKey,
        name: str | None = None,
        options: list[Option] | None = None,
        accept_language: Language | None = Language.EN,
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
        program = Program(key=program_key, name=name, options=options)
        response = await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/programs/active",
            headers={"Accept-Language": accept_language},
            data=program.to_dict(),
        )
        match response.status_code:
            case codes.CONFLICT:
                raise ConflictError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)

    async def stop_program(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = Language.EN,
    ) -> None:
        """Stop the active program."""
        response = await self._auth.request(
            "DELETE",
            f"/homeappliances/{ha_id}/programs/active",
            headers={"Accept-Language": accept_language},
        )
        match response.status_code:
            case codes.CONFLICT:
                raise WrongOperationStateError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)

    async def get_active_program_options(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = Language.EN,
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
        match response.status_code:
            case codes.NOT_FOUND:
                raise NoProgramActiveError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)
        return ArrayOfOptions.from_dict(response.json()["data"])

    async def set_active_program_options(
        self,
        ha_id: str,
        *,
        array_of_options: ArrayOfOptions,
        accept_language: Language | None = Language.EN,
    ) -> None:
        """Set all options of the active program.

        Update the options for the currently running program.
        With this API endpoint, you have to provide all options with
        their new values. If you want to update only one option, you can use the
        endpoint specific to that option.

        Please note that changing options of the running program is currently only
        supported by ovens.
        """
        response = await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/programs/active/options",
            headers={"Accept-Language": accept_language},
            data=array_of_options.to_dict(),
        )
        match response.status_code:
            case codes.CONFLICT:
                raise ActiveProgramNotSetError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)

    async def get_active_program_option(
        self,
        ha_id: str,
        *,
        option_key: OptionKey,
        accept_language: Language | None = Language.EN,
    ) -> Option:
        """Get a specific option of the active program."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/programs/active/options/{option_key}",
            headers={"Accept-Language": accept_language},
        )
        match response.status_code:
            case codes.NOT_FOUND:
                raise NoProgramActiveError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)
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
        accept_language: Language | None = Language.EN,
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
        response = await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/programs/active/options/{option_key}",
            headers={"Accept-Language": accept_language},
            data=option.to_dict(),
        )
        match response.status_code:
            case codes.CONFLICT:
                raise ActiveProgramNotSetError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)

    async def get_selected_program(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = Language.EN,
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
        match response.status_code:
            case codes.NOT_FOUND:
                raise NoProgramSelectedError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)
        return Program.from_dict(response.json()["data"])

    async def set_selected_program(
        self,
        ha_id: str,
        *,
        program_key: ProgramKey,
        name: str | None = None,
        options: list[Option] | None = None,
        accept_language: Language | None = Language.EN,
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
        program = Program(key=program_key, name=name, options=options)
        response = await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/programs/selected",
            headers={"Accept-Language": accept_language},
            data=program.to_dict(),
        )
        match response.status_code:
            case codes.CONFLICT:
                raise ConflictError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)

    async def get_selected_program_options(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = Language.EN,
    ) -> ArrayOfOptions:
        """Get all options of the selected program."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/programs/selected/options",
            headers={"Accept-Language": accept_language},
        )
        match response.status_code:
            case codes.NOT_FOUND:
                raise NoProgramSelectedError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)
        return ArrayOfOptions.from_dict(response.json()["data"])

    async def set_selected_program_options(
        self,
        ha_id: str,
        *,
        array_of_options: ArrayOfOptions,
        accept_language: Language | None = Language.EN,
    ) -> None:
        """Set all options of the selected program."""
        response = await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/programs/selected/options",
            headers={"Accept-Language": accept_language},
            data=array_of_options.to_dict(),
        )
        match response.status_code:
            case codes.CONFLICT:
                raise SelectedProgramNotSetError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)

    async def get_selected_program_option(
        self,
        ha_id: str,
        *,
        option_key: OptionKey,
        accept_language: Language | None = Language.EN,
    ) -> Option:
        """Get a specific option of the selected program."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/programs/selected/options/{option_key}",
            headers={"Accept-Language": accept_language},
        )
        match response.status_code:
            case codes.NOT_FOUND:
                raise NoProgramSelectedError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)
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
        accept_language: Language | None = Language.EN,
    ) -> None:
        """Set a specific option of the selected program."""
        option = Option(
            key=option_key,
            name=name,
            value=value,
            display_value=display_value,
            unit=unit,
        )
        response = await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/programs/selected/options/{option_key}",
            headers={"Accept-Language": accept_language},
            data=option.to_dict(),
        )
        match response.status_code:
            case codes.CONFLICT:
                raise SelectedProgramNotSetError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)

    async def get_images(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = Language.EN,
    ) -> ArrayOfImages:
        """Get a list of available images."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/images",
            headers={"Accept-Language": accept_language},
        )
        _raise_generic_error(response)
        return ArrayOfImages.from_dict(response.json()["data"])

    async def get_image(
        self,
        ha_id: str,
        *,
        image_key: str,
    ) -> None:
        """Get a specific image."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/images/{image_key}",
            headers=None,
        )
        match response.status_code:
            case codes.NOT_FOUND:
                raise NotFoundError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)

    async def get_settings(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = Language.EN,
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
        _raise_generic_error(response)
        return ArrayOfSettings.from_dict(response.json()["data"])

    async def set_settings(
        self,
        ha_id: str,
        *,
        put_settings: PutSettings,
        accept_language: Language | None = Language.EN,
    ) -> None:
        """Set multiple settings."""
        response = await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/settings",
            headers={"Accept-Language": accept_language},
            data=put_settings.to_dict(),
        )
        match response.status_code:
            case codes.CONFLICT:
                raise ConflictError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)

    async def get_setting(
        self,
        ha_id: str,
        *,
        setting_key: SettingKey,
        accept_language: Language | None = Language.EN,
    ) -> GetSetting:
        """Get a specific setting."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/settings/{setting_key}",
            headers={"Accept-Language": accept_language},
        )
        match response.status_code:
            case codes.NOT_FOUND:
                raise NotFoundError.from_dict(response.json()["error"])
            case codes.CONFLICT:
                raise ConflictError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)
        return GetSetting.from_dict(response.json()["data"])

    async def set_setting(
        self,
        ha_id: str,
        *,
        setting_key: SettingKey,
        value: Any,
        accept_language: Language | None = Language.EN,
    ) -> None:
        """Set a specific setting."""
        put_setting = PutSetting(key=setting_key, value=value)
        response = await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/settings/{setting_key}",
            headers={"Accept-Language": accept_language},
            data=put_setting.to_dict(),
        )
        match response.status_code:
            case codes.NOT_FOUND:
                raise NotFoundError.from_dict(response.json()["error"])
            case codes.CONFLICT:
                raise ConflictError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)

    async def get_status(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = Language.EN,
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
        match response.status_code:
            case codes.CONFLICT:
                raise ConflictError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)
        return ArrayOfStatus.from_dict(response.json()["data"])

    async def get_status_value(
        self,
        ha_id: str,
        *,
        status_key: StatusKey,
        accept_language: Language | None = Language.EN,
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
        match response.status_code:
            case codes.NOT_FOUND:
                raise NotFoundError.from_dict(response.json()["error"])
            case codes.CONFLICT:
                raise ConflictError.from_dict(response.json()["error"])
            case _:
                _raise_generic_error(response)
        return Status.from_dict(response.json()["data"])

    async def get_available_commands(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = Language.EN,
    ) -> ArrayOfCommands:
        """Get a list of available and writable commands."""
        response = await self._auth.request(
            "GET",
            f"/homeappliances/{ha_id}/commands",
            headers={"Accept-Language": accept_language},
        )
        _raise_generic_error(response)
        return ArrayOfCommands.from_dict(response.json()["data"])

    async def put_commands(
        self,
        ha_id: str,
        *,
        put_commands: PutCommands,
        accept_language: Language | None = Language.EN,
    ) -> None:
        """Execute multiple commands."""
        response = await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/commands",
            headers={"Accept-Language": accept_language},
            data=put_commands.to_dict(),
        )
        _raise_generic_error(response)

    async def put_command(
        self,
        ha_id: str,
        *,
        command_key: CommandKey,
        value: Any,
        accept_language: Language | None = Language.EN,
    ) -> None:
        """Execute a specific command."""
        put_command = PutCommand(key=command_key, value=value)
        response = await self._auth.request(
            "PUT",
            f"/homeappliances/{ha_id}/commands/{command_key}",
            headers={"Accept-Language": accept_language},
            data=put_command.to_dict(),
        )
        _raise_generic_error(response)

    async def stream_all_events(
        self,
        *,
        accept_language: Language | None = Language.EN,
    ) -> AsyncGenerator[EventMessage]:
        """Get stream of events for all appliances.

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
        # We use 60 seconds timeout because at least every 55 seconds a KEEP-ALIVE event
        # will be sent. See https://api-docs.home-connect.com/events/#availability-matrix
        async with self._auth.connect_sse(
            "GET",
            "/homeappliances/events",
            timeout=Timeout(60),
            headers={
                "Accept-Language": accept_language,
            },
        ) as event_source:
            response = event_source.response
            if response.is_error:
                await response.aread()
                match event_source.response.status_code:
                    case codes.UNAUTHORIZED:
                        raise UnauthorizedError.from_dict(response.json()["error"])
                    case codes.FORBIDDEN:
                        raise ForbiddenError.from_dict(response.json()["error"])
                    case codes.NOT_ACCEPTABLE:
                        raise NotAcceptableError.from_dict(response.json()["error"])
                    case codes.TOO_MANY_REQUESTS:
                        raise TooManyRequestsError.from_dict(response.json()["error"])
                    case codes.INTERNAL_SERVER_ERROR:
                        raise InternalServerError.from_dict(response.json()["error"])
                    case _:
                        _raise_generic_error(response)

            async for sse in event_source.aiter_sse():
                LOGGER.debug("Event: %s", sse)

                if (
                    # _value2member_map_ is required for Python 3.11,
                    # remove after dropping support for it.
                    sse.event not in EventType._value2member_map_
                    or sse.event == EventType.KEEP_ALIVE
                ):
                    continue
                yield EventMessage.from_server_sent_event(sse)

    async def stream_events(
        self,
        ha_id: str,
        *,
        accept_language: Language | None = Language.EN,
    ) -> AsyncGenerator[EventMessage]:
        """Get stream of events for one appliance.

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
        # We use 60 seconds timeout because at least every 55 seconds a KEEP-ALIVE event
        # will be sent. See https://api-docs.home-connect.com/events/#availability-matrix
        async with self._auth.connect_sse(
            "GET",
            f"/homeappliances/{ha_id}/events",
            timeout=Timeout(60),
            headers={
                "Accept-Language": accept_language,
            },
        ) as event_source:
            response = event_source.response
            if response.is_error:
                await response.aread()
                match event_source.response.status_code:
                    case codes.UNAUTHORIZED:
                        raise UnauthorizedError.from_dict(response.json()["error"])
                    case codes.FORBIDDEN:
                        raise ForbiddenError.from_dict(response.json()["error"])
                    case codes.NOT_ACCEPTABLE:
                        raise NotAcceptableError.from_dict(response.json()["error"])
                    case codes.TOO_MANY_REQUESTS:
                        raise TooManyRequestsError.from_dict(response.json()["error"])
                    case codes.INTERNAL_SERVER_ERROR:
                        raise InternalServerError.from_dict(response.json()["error"])
                    case _:
                        _raise_generic_error(response)

            async for sse in event_source.aiter_sse():
                if (
                    # _value2member_map_ is required for Python 3.11,
                    # remove after dropping support for it.
                    sse.event not in EventType._value2member_map_
                    or sse.event == EventType.KEEP_ALIVE
                ):
                    continue
                yield EventMessage.from_server_sent_event(sse)
