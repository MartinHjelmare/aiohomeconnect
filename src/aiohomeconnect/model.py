"""Provide a model for the Home Connect API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from mashumaro import field_options
from mashumaro.mixins.json import DataClassJSONMixin


class ContentType(StrEnum):
    """Represent the content type for the response."""

    APPLICATION_JSON = "application/vnd.bsh.sdk.v1+json"
    EVENT_STREAM = "text/event-stream"


class Language(StrEnum):
    """Represent the language for the response."""

    DE = "de-DE"
    EN = "en-US"
    EN_GB = "en-GB"


@dataclass
class HomeAppliance(DataClassJSONMixin):
    """Represent HomeAppliance."""

    ha_id: str | None = field(metadata=field_options(alias="haId"))
    name: str | None
    type: str | None
    brand: str | None
    vib: str | None
    e_number: str | None = field(metadata=field_options(alias="enumber"))
    connected: bool | None


@dataclass
class ArrayOfHomeAppliances(DataClassJSONMixin):
    """Object containing an array of home appliances."""

    homeappliances: list[HomeAppliance]


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


@dataclass
class ArrayOfEvents(DataClassJSONMixin):
    """Represent ArrayOfEvents."""

    items: list[Event]


@dataclass
class Event(DataClassJSONMixin):
    """Represent Event."""

    key: str
    name: str | None
    uri: str | None
    timestamp: int
    level: str
    handling: str
    value: str | float | bool
    display_value: str | None = field(metadata=field_options(alias="displayvalue"))
    unit: str | None


@dataclass
class Program(DataClassJSONMixin):
    """Represent Program."""

    key: str
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

    key: str
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

    key: str
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

    key: str
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

    key: str
    name: str | None
    type: str
    unit: str | None
    constraints: ProgramDefinitionConstraints | None


@dataclass
class Option(DataClassJSONMixin):
    """Represent Option."""

    key: str
    name: str | None
    value: Any
    display_value: str | None = field(metadata=field_options(alias="displayvalue"))
    unit: str | None


@dataclass
class ArrayOfOptions(DataClassJSONMixin):
    """List of options."""

    options: list[Option]


@dataclass
class ArrayOfImages(DataClassJSONMixin):
    """List of images available from the home appliance."""

    images: list[Image]


@dataclass
class Image(DataClassJSONMixin):
    """Represent Image."""

    key: str
    name: str | None
    image_key: str = field(metadata=field_options(alias="imagekey"))
    preview_image_key: str = field(metadata=field_options(alias="previewimagekey"))
    timestamp: int
    quality: str


@dataclass
class GetSetting(DataClassJSONMixin):
    """Specific setting of the home appliance."""

    key: str
    name: str | None
    value: Any
    display_value: str | None = field(metadata=field_options(alias="displayvalue"))
    unit: str | None
    type: str | None
    constraints: SettingConstraints | None


@dataclass
class SettingConstraints(DataClassJSONMixin):
    """Represent SettingConstraints."""

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
    access: str | None


@dataclass
class ArrayOfSettings(DataClassJSONMixin):
    """List of settings of the home appliance."""

    settings: list[GetSetting]


@dataclass
class PutSetting(DataClassJSONMixin):
    """Specific setting of the home appliance."""

    key: str
    value: Any


@dataclass
class PutSettings(DataClassJSONMixin):
    """List of settings of the home appliance."""

    data: list[PutSetting]


@dataclass
class Status(DataClassJSONMixin):
    """Represent Status."""

    key: str
    name: str | None
    value: Any
    display_value: str | None = field(metadata=field_options(alias="displayvalue"))
    unit: str | None
    type: str | None
    constraints: StatusConstraints | None


@dataclass
class StatusConstraints(DataClassJSONMixin):
    """Represent StatusConstraints."""

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
    access: str | None


@dataclass
class ArrayOfStatus(DataClassJSONMixin):
    """List of status of the home appliance."""

    status: list[Status]


@dataclass
class ArrayOfCommands(DataClassJSONMixin):
    """Represent ArrayOfCommands."""

    commands: list[Command]


@dataclass
class Command(DataClassJSONMixin):
    """Represent Command."""

    key: str
    name: str | None


@dataclass
class PutCommand(DataClassJSONMixin):
    """Represent PutCommand."""

    key: str
    value: Any


@dataclass
class PutCommands(DataClassJSONMixin):
    """A list of commands of the home appliance."""

    data: list[PutCommand]


class CommandKey(StrEnum):
    """Represent a base class for command keys."""


class CommandKeyBSHCommon(CommandKey):
    """BSH Common command keys."""

    PAUSE_PROGRAM = "BSH.Common.Command.PauseProgram"
    RESUME_PROGRAM = "BSH.Common.Command.ResumeProgram"
    OPEN_DOOR = "BSH.Common.Command.OpenDoor"
    PARTLY_OPEN_DOOR = "BSH.Common.Command.PartlyOpenDoor"
    ACKNOWLEDGE_EVENT = "BSH.Common.Command.AcknowledgeEvent"


class StatusKey(StrEnum):
    """Represent a base class for status keys."""


class StatusKeyBSHCommon(StatusKey):
    """BSH Common Status keys."""

    BATTERY_CHARGING_STATE = "BSH.Common.Status.BatteryChargingState"
    BATTERY_LEVEL = "BSH.Common.Status.BatteryLevel"
    CHARGING_CONNECTION = "BSH.Common.Status.ChargingConnection"
    DOOR_STATE = "BSH.Common.Status.DoorState"
    LOCAL_CONTROL_ACTIVE = "BSH.Common.Status.LocalControlActive"
    OPERATION_STATE = "BSH.Common.Status.OperationState"
    REMOTE_CONTROL_ACTIVE = "BSH.Common.Status.RemoteControlActive"
    REMOTE_CONTROL_START_ALLOWED = "BSH.Common.Status.RemoteControlStartAllowed"
    VIDEO_CAMERA_STATE = "BSH.Common.Status.Video.CameraState"


class StatusKeyRefrigerationCommon(StatusKey):
    """Refrigeration Common Status keys."""

    DOOR_BOTTLE_COOLER = "Refrigeration.Common.Status.Door.BottleCooler"
    DOOR_CHILLER = "Refrigeration.Common.Status.Door.Chiller"
    DOOR_CHILLER_COMMON = "Refrigeration.Common.Status.Door.ChillerCommon"
    DOOR_CHILLER_LEFT = "Refrigeration.Common.Status.Door.ChillerLeft"
    DOOR_CHILLER_RIGHT = "Refrigeration.Common.Status.Door.ChillerRight"
    DOOR_FLEX_COMPARTMENT = "Refrigeration.Common.Status.Door.FlexCompartment"
    DOOR_FREEZER = "Refrigeration.Common.Status.Door.Freezer"
    DOOR_REFRIGERATOR = "Refrigeration.Common.Status.Door.Refrigerator"
    DOOR_REFRIGERATOR_2 = "Refrigeration.Common.Status.Door.Refrigerator2"
    DOOR_REFRIGERATOR_3 = "Refrigeration.Common.Status.Door.Refrigerator3"
    DOOR_WINE_COMPARTMENT = "Refrigeration.Common.Status.Door.WineCompartment"


class StatusKeyConsumerProductsCoffeeMaker(StatusKey):
    """ConsumerProducts CoffeeMaker Status keys."""

    BEVERAGE_COUNTER_COFFEE = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterCoffee"
    )
    BEVERAGE_COUNTER_COFFEE_AND_MILK = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterCoffeeAndMilk"
    )
    BEVERAGE_COUNTER_FROTHY_MILK = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterFrothyMilk"
    )
    BEVERAGE_COUNTER_HOT_MILK = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterHotMilk"
    )
    BEVERAGE_COUNTER_HOT_WATER = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterHotWater"
    )
    BEVERAGE_COUNTER_HOT_WATER_CUPS = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterHotWaterCups"
    )
    BEVERAGE_COUNTER_MILK = "ConsumerProducts.CoffeeMaker.Status.BeverageCounterMilk"
    BEVERAGE_COUNTER_POWDER_COFFEE = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterPowderCoffee"
    )
    BEVERAGE_COUNTER_RISTRETTO_ESPRESSO = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterRistrettoEspresso"
    )


class StatusKeyConsumerProductsCleaningRobot(StatusKey):
    """ConsumerProducts CleaningRobot Status keys."""

    DUST_BOX_INSERTED = "ConsumerProducts.CleaningRobot.Status.DustBoxInserted"
    LAST_SELECTED_MAP = "ConsumerProducts.CleaningRobot.Status.LastSelectedMap"
    LIFTED = "ConsumerProducts.CleaningRobot.Status.Lifted"
    LOST = "ConsumerProducts.CleaningRobot.Status.Lost"
