"""Provide error models for the Home Connect API."""

from __future__ import annotations

from dataclasses import dataclass

from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class UnauthorizedError(DataClassJSONMixin):
    """Represent UnauthorizedError."""

    key: str
    description: str | None


@dataclass
class ForbiddenError(DataClassJSONMixin):
    """Represent ForbiddenError."""

    key: str
    description: str | None


@dataclass
class NotFoundError(DataClassJSONMixin):
    """Represent NotFoundError."""

    key: str
    description: str | None


@dataclass
class NoProgramSelectedError(DataClassJSONMixin):
    """Represent NoProgramSelectedError."""

    key: str
    description: str | None


@dataclass
class NoProgramActiveError(DataClassJSONMixin):
    """Represent NoProgramActiveError."""

    key: str
    description: str | None


@dataclass
class NotAcceptableError(DataClassJSONMixin):
    """Represent NotAcceptableError."""

    key: str
    description: str | None


@dataclass
class RequestTimeoutError(DataClassJSONMixin):
    """Represent RequestTimeoutError."""

    key: str
    description: str | None


@dataclass
class ConflictError(DataClassJSONMixin):
    """Represent ConflictError."""

    key: str
    description: str | None


@dataclass
class SelectedProgramNotSetError(DataClassJSONMixin):
    """Represent SelectedProgramNotSetError."""

    key: str
    description: str | None


@dataclass
class ActiveProgramNotSetError(DataClassJSONMixin):
    """Represent ActiveProgramNotSetError."""

    key: str
    description: str | None


@dataclass
class WrongOperationStateError(DataClassJSONMixin):
    """Represent WrongOperationStateError."""

    key: str
    description: str | None


@dataclass
class ProgramNotAvailableError(DataClassJSONMixin):
    """Represent ProgramNotAvailableError."""

    key: str
    description: str | None


@dataclass
class UnsupportedMediaTypeError(DataClassJSONMixin):
    """Represent UnsupportedMediaTypeError."""

    key: str
    description: str | None


@dataclass
class TooManyRequestsError(DataClassJSONMixin):
    """Represent TooManyRequestsError."""

    key: str
    description: str | None


@dataclass
class InternalServerError(DataClassJSONMixin):
    """Represent InternalServerError."""

    key: str
    description: str | None


@dataclass
class Conflict(DataClassJSONMixin):
    """Represent Conflict."""

    key: str
    description: str | None
