"""Provide command models for the Home Connect API."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class ArrayOfCommands(DataClassJSONMixin):
    """Represent ArrayOfCommands."""

    commands: list[Command]


@dataclass
class Command(DataClassJSONMixin):
    """Represent Command."""

    key: CommandKey
    name: str | None = None


@dataclass
class PutCommand(DataClassJSONMixin):
    """Represent PutCommand."""

    key: CommandKey
    value: Any


@dataclass
class PutCommands(DataClassJSONMixin):
    """A list of commands of the home appliance."""

    data: list[PutCommand]


class CommandKey(StrEnum):
    """Represent a command key."""

    BSH_COMMON_ACKNOWLEDGE_EVENT = "BSH.Common.Command.AcknowledgeEvent"
    BSH_COMMON_OPEN_DOOR = "BSH.Common.Command.OpenDoor"
    BSH_COMMON_PARTLY_OPEN_DOOR = "BSH.Common.Command.PartlyOpenDoor"
    BSH_COMMON_PAUSE_PROGRAM = "BSH.Common.Command.PauseProgram"
    BSH_COMMON_RESUME_PROGRAM = "BSH.Common.Command.ResumeProgram"
