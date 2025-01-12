"""Provide error models for the Home Connect API."""

from __future__ import annotations

from dataclasses import dataclass

from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class HomeConnectError(Exception, DataClassJSONMixin):
    """Represent UnauthorizedError."""

    key: str
    description: str | None = None

    def __str__(self) -> str:
        """Return the string representation of the error."""
        return f"{self.description} ({self.key})"

    def __repr__(self) -> str:
        """Return the representation of the error."""
        return f"{self.description} ({self.key})"


@dataclass
class UnauthorizedError(HomeConnectError):
    """Represent UnauthorizedError."""


@dataclass
class ForbiddenError(HomeConnectError):
    """Represent ForbiddenError."""


@dataclass
class NotFoundError(HomeConnectError):
    """Represent NotFoundError."""


@dataclass
class NoProgramSelectedError(HomeConnectError):
    """Represent NoProgramSelectedError."""


@dataclass
class NoProgramActiveError(HomeConnectError):
    """Represent NoProgramActiveError."""


@dataclass
class NotAcceptableError(HomeConnectError):
    """Represent NotAcceptableError."""


@dataclass
class RequestTimeoutError(HomeConnectError):
    """Represent RequestTimeoutError."""


@dataclass
class ConflictError(HomeConnectError):
    """Represent ConflictError."""


@dataclass
class SelectedProgramNotSetError(HomeConnectError):
    """Represent SelectedProgramNotSetError."""


@dataclass
class ActiveProgramNotSetError(HomeConnectError):
    """Represent ActiveProgramNotSetError."""


@dataclass
class WrongOperationStateError(HomeConnectError):
    """Represent WrongOperationStateError."""


@dataclass
class ProgramNotAvailableError(HomeConnectError):
    """Represent ProgramNotAvailableError."""


@dataclass
class UnsupportedMediaTypeError(HomeConnectError):
    """Represent UnsupportedMediaTypeError."""


@dataclass
class TooManyRequestsError(HomeConnectError):
    """Represent TooManyRequestsError."""


@dataclass
class InternalServerError(HomeConnectError):
    """Represent InternalServerError."""


@dataclass
class Conflict(HomeConnectError):  # noqa: N818
    """Represent Conflict."""


class EventStreamInterruptedError(Exception):
    """Represent the error cause when the event stream ends abruptly."""
