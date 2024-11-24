"""Provide program models for the Home Connect API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from mashumaro import field_options
from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class Program(DataClassJSONMixin):
    """Represent Program."""

    key: ProgramKey
    name: str | None
    options: list[Option] | None
    constraints: ProgramConstraints | None


@dataclass
class ProgramConstraints(DataClassJSONMixin):
    """Represent ProgramConstraints."""

    access: str | None


@dataclass
class ArrayOfAvailablePrograms(DataClassJSONMixin):
    """Represent ArrayOfAvailablePrograms."""

    programs: list[EnumerateAvailableProgram]


@dataclass
class EnumerateAvailableProgramConstraints(DataClassJSONMixin):
    """Represent EnumerateAvailableProgramConstraints."""

    execution: Execution | None


@dataclass
class EnumerateAvailableProgram(DataClassJSONMixin):
    """Represent EnumerateAvailableProgram."""

    key: ProgramKey
    name: str | None
    constraints: EnumerateAvailableProgramConstraints | None


@dataclass
class ArrayOfPrograms(DataClassJSONMixin):
    """Represent ArrayOfPrograms."""

    programs: list[EnumerateProgram]
    active: Program | None
    selected: Program | None


@dataclass
class EnumerateProgramConstraints(DataClassJSONMixin):
    """Represent EnumerateProgramConstraints."""

    available: bool | None
    execution: Execution | None


@dataclass
class EnumerateProgram(DataClassJSONMixin):
    """Represent EnumerateProgram."""

    key: ProgramKey
    name: str | None
    constraints: EnumerateProgramConstraints | None


class Execution(StrEnum):
    """Execution right of the program."""

    NONE = "none"
    SELECT_ONLY = "selectonly"
    START_ONLY = "startonly"
    SELECT_AND_START = "selectandstart"


@dataclass
class ProgramDefinition(DataClassJSONMixin):
    """Represent ProgramDefinition."""

    key: ProgramKey
    name: str | None
    options: list[ProgramDefinitionOption] | None


@dataclass
class ProgramDefinitionConstraints(DataClassJSONMixin):
    """Represent ProgramDefinitionConstraints."""

    min: int | None
    max: int | None
    step_size: int | None = field(metadata=field_options(alias="stepsize"))
    allowed_values: list[str | None] | None = field(
        metadata=field_options(alias="allowedvalues")
    )
    display_values: list[str | None] | None = field(
        metadata=field_options(alias="displayvalues")
    )
    default: Any | None
    live_update: bool | None = field(metadata=field_options(alias="liveupdate"))


@dataclass
class ProgramDefinitionOption(DataClassJSONMixin):
    """Represent ProgramDefinitionOption."""

    key: OptionKey
    name: str | None
    type: str
    unit: str | None
    constraints: ProgramDefinitionConstraints | None


@dataclass
class Option(DataClassJSONMixin):
    """Represent Option."""

    key: OptionKey
    name: str | None
    value: Any
    display_value: str | None = field(metadata=field_options(alias="displayvalue"))
    unit: str | None


@dataclass
class ArrayOfOptions(DataClassJSONMixin):
    """List of options."""

    options: list[Option]


class OptionKey(StrEnum):
    """Represent an option key."""

    # TODO(Martin Hjelmare): Add all option keys  # noqa: FIX002
    # https://github.com/MartinHjelmare/aiohomeconnect/issues/22

    CONSUMER_PRODUCTS_CLEANING_ROBOT_CLEANING_MODE = (
        "ConsumerProducts.CleaningRobot.Option.CleaningMode"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_REFERENCE_MAP_ID = (
        "ConsumerProducts.CleaningRobot.Option.ReferenceMapId"
    )


class ProgramKey(StrEnum):
    """Represent a program key."""

    # TODO(Martin Hjelmare): Add all program keys  # noqa: FIX002
    # https://github.com/MartinHjelmare/aiohomeconnect/issues/23

    CONSUMER_PRODUCTS_CLEANING_ROBOT_BASIC_GO_HOME = (
        "ConsumerProducts.CleaningRobot.Program.Basic.GoHome"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_CLEANING_CLEAN_ALL = (
        "ConsumerProducts.CleaningRobot.Program.Cleaning.CleanAll"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_CLEANING_CLEAN_MAP = (
        "ConsumerProducts.CleaningRobot.Program.Cleaning.CleanMap"
    )
