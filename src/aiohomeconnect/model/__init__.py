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
    Event,
    EventKey,
    EventMessage,
    EventType,
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
    "Event",
    "EventKey",
    "EventMessage",
    "EventType",
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


class Language(StrEnum):
    """Represent the language for the response."""

    DE = "de-DE"
    EN = "en-US"
    EN_GB = "en-GB"
