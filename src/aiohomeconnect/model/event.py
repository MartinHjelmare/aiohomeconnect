"""Provide event models for the Home Connect API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from mashumaro import field_options
from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class ArrayOfEvents(DataClassJSONMixin):
    """Represent ArrayOfEvents."""

    items: list[Event]


@dataclass
class Event(DataClassJSONMixin):
    """Represent Event."""

    key: EventKey
    name: str | None
    uri: str | None
    timestamp: int
    level: str
    handling: str
    value: str | float | bool
    display_value: str | None = field(metadata=field_options(alias="displayvalue"))
    unit: str | None


class EventKey(StrEnum):
    """Represent an event key."""

    # TODO(Martin Hjelmare): Add all event keys  # noqa: FIX002
    # https://github.com/MartinHjelmare/aiohomeconnect/issues/21

    BSH_COMMON_ROOT_SELECTED_PROGRAM = "BSH.Common.Root.SelectedProgram"
    BSH_COMMON_ROOT_ACTIVE_PROGRAM = "BSH.Common.Root.ActiveProgram"
    BSH_COMMON_OPTION_START_IN_RELATIVE = "BSH.Common.Option.StartInRelative"
    BSH_COMMON_OPTION_FINISH_IN_RELATIVE = "BSH.Common.Option.FinishInRelative"
    BSH_COMMON_OPTION_DURATION = "BSH.Common.Option.Duration"
