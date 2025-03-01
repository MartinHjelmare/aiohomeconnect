"""Provide error models for the Home Connect API."""

from __future__ import annotations

from dataclasses import dataclass

from mashumaro.mixins.json import DataClassJSONMixin


class HomeConnectError(Exception):
    """Base class for Home Connect exceptions."""


@dataclass
class HomeConnectApiError(HomeConnectError, DataClassJSONMixin):
    """Base class for Home Connect API exceptions."""

    key: str
    description: str | None = None

    def __str__(self) -> str:
        """Return the string representation of the error."""
        return f"{self.description} ({self.key})"

    def __repr__(self) -> str:
        """Return the representation of the error."""
        return f"{self.description} ({self.key})"


@dataclass
class UnauthorizedError(HomeConnectApiError):
    """Represent UnauthorizedError."""


@dataclass
class ForbiddenError(HomeConnectApiError):
    """Represent ForbiddenError."""


@dataclass
class NotFoundError(HomeConnectApiError):
    """Represent NotFoundError."""


@dataclass
class NoProgramSelectedError(HomeConnectApiError):
    """Represent NoProgramSelectedError."""


@dataclass
class NoProgramActiveError(HomeConnectApiError):
    """Represent NoProgramActiveError."""


@dataclass
class NotAcceptableError(HomeConnectApiError):
    """Represent NotAcceptableError."""


@dataclass
class RequestTimeoutError(HomeConnectApiError):
    """Represent RequestTimeoutError."""


@dataclass
class ConflictError(HomeConnectApiError):
    """Represent ConflictError."""


@dataclass
class SelectedProgramNotSetError(HomeConnectApiError):
    """Represent SelectedProgramNotSetError."""


@dataclass
class ActiveProgramNotSetError(HomeConnectApiError):
    """Represent ActiveProgramNotSetError."""


@dataclass
class WrongOperationStateError(HomeConnectApiError):
    """Represent WrongOperationStateError."""


@dataclass
class ProgramNotAvailableError(HomeConnectApiError):
    """Represent ProgramNotAvailableError."""


@dataclass
class UnsupportedMediaTypeError(HomeConnectApiError):
    """Represent UnsupportedMediaTypeError."""


@dataclass
class TooManyRequestsError(HomeConnectApiError):
    """Represent TooManyRequestsError."""

    retry_after: int | None = None


@dataclass
class InternalServerError(HomeConnectApiError):
    """Represent InternalServerError."""


@dataclass
class Conflict(HomeConnectApiError):  # noqa: N818
    """Represent Conflict."""


class HomeConnectRequestError(HomeConnectError):
    """Represent the error cause when the event stream ends abruptly."""


class EventStreamInterruptedError(HomeConnectError):
    """Represent the error cause when the event stream ends abruptly."""
