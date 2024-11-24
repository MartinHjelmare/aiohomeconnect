"""Provide a model for the Home Connect API."""

from enum import StrEnum

from .appliance import (
    ArrayOfHomeAppliances,
    HomeAppliance,
)
from .command import (
    ArrayOfCommands,
    CommandKey,
    PutCommand,
    PutCommands,
)
from .event import (
    ArrayOfEvents,
    EventKey,
)
from .image import (
    ArrayOfImages,
)
from .program import (
    ArrayOfAvailablePrograms,
    ArrayOfOptions,
    ArrayOfPrograms,
    Option,
    OptionKey,
    Program,
    ProgramConstraints,
    ProgramDefinition,
    ProgramKey,
)
from .setting import (
    ArrayOfSettings,
    GetSetting,
    PutSetting,
    PutSettings,
    SettingKey,
)
from .status import (
    ArrayOfStatus,
    Status,
    StatusKey,
)

__all__ = [
    "ArrayOfAvailablePrograms",
    "ArrayOfCommands",
    "ArrayOfEvents",
    "ArrayOfHomeAppliances",
    "ArrayOfImages",
    "ArrayOfOptions",
    "ArrayOfPrograms",
    "ArrayOfSettings",
    "ArrayOfStatus",
    "CommandKey",
    "EventKey",
    "GetSetting",
    "HomeAppliance",
    "Option",
    "OptionKey",
    "Program",
    "ProgramConstraints",
    "ProgramDefinition",
    "ProgramKey",
    "PutCommand",
    "PutCommands",
    "PutSetting",
    "PutSettings",
    "SettingKey",
    "Status",
    "StatusKey",
]


class ContentType(StrEnum):
    """Represent the content type for the response."""

    APPLICATION_JSON = "application/vnd.bsh.sdk.v1+json"
    EVENT_STREAM = "text/event-stream"


class Language(StrEnum):
    """Represent the language for the response."""

    DE = "de-DE"
    EN = "en-US"
    EN_GB = "en-GB"
