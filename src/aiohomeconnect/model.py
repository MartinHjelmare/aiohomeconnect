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


class ProgramKey(StrEnum):
    """Represent program keys."""

    CONSUMER_PRODUCTS_CLEANING_ROBOT_BASIC_GO_HOME = (
        "ConsumerProducts.CleaningRobot.Program.Basic.GoHome"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_CLEANING_CLEAN_ALL = (
        "ConsumerProducts.CleaningRobot.Program.Cleaning.CleanAll"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_CLEANING_CLEAN_MAP = (
        "ConsumerProducts.CleaningRobot.Program.Cleaning.CleanMap"
    )


class OptionKey(StrEnum):
    """Represent option keys."""

    CONSUMER_PRODUCTS_CLEANING_ROBOT_CLEANING_MODE = (
        "ConsumerProducts.CleaningRobot.Option.CleaningMode"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_REFERENCE_MAP_ID = (
        "ConsumerProducts.CleaningRobot.Option.ReferenceMapId"
    )


class StatusKey(StrEnum):
    """Represent status keys."""

    BSH_COMMON_BATTERY_CHARGING_STATE = "BSH.Common.Status.BatteryChargingState"
    BSH_COMMON_BATTERY_LEVEL = "BSH.Common.Status.BatteryLevel"
    BSH_COMMON_CHARGING_CONNECTION = "BSH.Common.Status.ChargingConnection"
    BSH_COMMON_DOOR_STATE = "BSH.Common.Status.DoorState"
    BSH_COMMON_LOCAL_CONTROL_ACTIVE = "BSH.Common.Status.LocalControlActive"
    BSH_COMMON_OPERATION_STATE = "BSH.Common.Status.OperationState"
    BSH_COMMON_REMOTE_CONTROL_ACTIVE = "BSH.Common.Status.RemoteControlActive"
    BSH_COMMON_REMOTE_CONTROL_START_ALLOWED = (
        "BSH.Common.Status.RemoteControlStartAllowed"
    )
    BSH_COMMON_VIDEO_CAMERA_STATE = "BSH.Common.Status.Video.CameraState"
    REFRIGERATION_COMMON_DOOR_BOTTLE_COOLER = (
        "Refrigeration.Common.Status.Door.BottleCooler"
    )
    REFRIGERATION_COMMON_DOOR_CHILLER = "Refrigeration.Common.Status.Door.Chiller"
    REFRIGERATION_COMMON_DOOR_CHILLER_COMMON = (
        "Refrigeration.Common.Status.Door.ChillerCommon"
    )
    REFRIGERATION_COMMON_DOOR_CHILLER_LEFT = (
        "Refrigeration.Common.Status.Door.ChillerLeft"
    )
    REFRIGERATION_COMMON_DOOR_CHILLER_RIGHT = (
        "Refrigeration.Common.Status.Door.ChillerRight"
    )
    REFRIGERATION_COMMON_DOOR_FLEX_COMPARTMENT = (
        "Refrigeration.Common.Status.Door.FlexCompartment"
    )
    REFRIGERATION_COMMON_DOOR_FREEZER = "Refrigeration.Common.Status.Door.Freezer"
    REFRIGERATION_COMMON_DOOR_REFRIGERATOR = (
        "Refrigeration.Common.Status.Door.Refrigerator"
    )
    REFRIGERATION_COMMON_DOOR_REFRIGERATOR_2 = (
        "Refrigeration.Common.Status.Door.Refrigerator2"
    )
    REFRIGERATION_COMMON_DOOR_REFRIGERATOR_3 = (
        "Refrigeration.Common.Status.Door.Refrigerator3"
    )
    REFRIGERATION_COMMON_DOOR_WINE_COMPARTMENT = (
        "Refrigeration.Common.Status.Door.WineCompartment"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_COFFEE = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterCoffee"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_COFFEE_AND_MILK = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterCoffeeAndMilk"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_FROTHY_MILK = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterFrothyMilk"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_HOT_MILK = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterHotMilk"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_HOT_WATER = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterHotWater"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_HOT_WATER_CUPS = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterHotWaterCups"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_MILK = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterMilk"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_POWDER_COFFEE = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterPowderCoffee"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_RISTRETTO_ESPRESSO = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterRistrettoEspresso"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_DUST_BOX_INSERTED = (
        "ConsumerProducts.CleaningRobot.Status.DustBoxInserted"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_LAST_SELECTED_MAP = (
        "ConsumerProducts.CleaningRobot.Status.LastSelectedMap"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_LIFTED = (
        "ConsumerProducts.CleaningRobot.Status.Lifted"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_LOST = "ConsumerProducts.CleaningRobot.Status.Lost"


class SettingKey(StrEnum):
    """Represent setting keys."""

    BSH_COMMON_POWER_STATE = "BSH.Common.Setting.PowerState"
    BSH_COMMON_TEMPERATURE_UNIT = "BSH.Common.Setting.TemperatureUnit"
    BSH_COMMON_LIQUID_VOLUME_UNIT = "BSH.Common.Setting.LiquidVolumeUnit"
    BSH_COMMON_CHILD_LOCK = "BSH.Common.Setting.ChildLock"
    BSH_COMMON_ALARM_CLOCK = "BSH.Common.Setting.AlarmClock"
    CONSUMER_PRODUCTS_COFFEE_MAKER_CUP_WARMER = (
        "ConsumerProducts.CoffeeMaker.Setting.CupWarmer"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_CURRENT_MAP = (
        "ConsumerProducts.CleaningRobot.Setting.CurrentMap"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_NAME_OF_MAP_1 = (
        "ConsumerProducts.CleaningRobot.Setting.NameOfMap1"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_NAME_OF_MAP_2 = (
        "ConsumerProducts.CleaningRobot.Setting.NameOfMap2"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_NAME_OF_MAP_3 = (
        "ConsumerProducts.CleaningRobot.Setting.NameOfMap3"
    )
    COOKING_COMMON_LIGHTNING = "Cooking.Common.Setting.Lighting"
    COOKING_OVEN_SABBATH_MODE = "Cooking.Oven.Setting.SabbathMode"
    REFRIGERATION_COMMON_BOTTLE_COOLER_SETPOINT_TEMPERATURE = (
        "Refrigeration.Common.Setting.BottleCooler.SetpointTemperature"
    )
    REFRIGERATION_COMMON_CHILLER_LEFT_SETPOINT_TEMPERATURE = (
        "Refrigeration.Common.Setting.ChillerLeft.SetpointTemperature"
    )
    REFRIGERATION_COMMON_CHILLER_COMMON_SETPOINT_TEMPERATURE = (
        "Refrigeration.Common.Setting.ChillerCommon.SetpointTemperature"
    )
    REFRIGERATION_COMMON_CHILLER_RIGHT_SETPOINT_TEMPERATURE = (
        "Refrigeration.Common.Setting.ChillerRight.SetpointTemperature"
    )
    REFRIGERATION_COMMON_DISPENSER_ENABLED = (
        "Refrigeration.Common.Setting.Dispenser.Enabled"
    )
    REFRIGERATION_COMMON_DOOR_ASSISTANT_FRIDGE = (
        "Refrigeration.Common.Setting.Door.AssistantFridge"
    )
    REFRIGERATION_COMMON_DOOR_ASSISTANT_FREEZER = (
        "Refrigeration.Common.Setting.Door.AssistantFreezer"
    )
    REFRIGERATION_COMMON_DOOR_ASSISTANT_FORCE_FRIDGE = (
        "Refrigeration.Common.Setting.Door.AssistantForceFridge"
    )
    REFRIGERATION_COMMON_DOOR_ASSISTANT_FORCE_FREEZER = (
        "Refrigeration.Common.Setting.Door.AssistantForceFreezer"
    )
    REFRIGERATION_COMMON_DOOR_ASSISTANT_TIMEOUT_FRIDGE = (
        "Refrigeration.Common.Setting.Door.AssistantTimeoutFridge"
    )
    REFRIGERATION_COMMON_DOOR_ASSISTANT_TIMEOUT_FREEZER = (
        "Refrigeration.Common.Setting.Door.AssistantTimeoutFreezer"
    )
    REFRIGERATION_COMMON_DOOR_ASSISTANT_TRIGGER_FRIDGE = (
        "Refrigeration.Common.Setting.Door.AssistantTriggerFridge"
    )
    REFRIGERATION_COMMON_DOOR_ASSISTANT_TRIGGER_FREEZER = (
        "Refrigeration.Common.Setting.Door.AssistantTriggerFreezer"
    )
    REFRIGERATION_COMMON_ECO_MODE = "Refrigeration.Common.Setting.EcoMode"
    REFRIGERATION_COMMON_FRESH_MODE = "Refrigeration.Common.Setting.FreshMode"
    REFRIGERATION_COMMON_LIGHT_EXTERNAL_BRIGHTNESS = (
        "Refrigeration.Common.Setting.Light.External.Brightness"
    )
    REFRIGERATION_COMMON_LIGHT_INTERNAL_BRIGHTNESS = (
        "Refrigeration.Common.Setting.Light.Internal.Brightness"
    )
    REFRIGERATION_COMMON_LIGHT_EXTERNAL_POWER = (
        "Refrigeration.Common.Setting.Light.External.Power"
    )
    REFRIGERATION_COMMON_LIGHT_INTERNAL_POWER = (
        "Refrigeration.Common.Setting.Light.Internal.Power"
    )
    REFRIGERATION_COMMON_SABBATH_MODE = "Refrigeration.Common.Setting.SabbathMode"
    REFRIGERATION_COMMON_VACATION_MODE = "Refrigeration.Common.Setting.VacationMode"
    REFRIGERATION_COMMON_WINE_COMPARTMENT_SETPOINT_TEMPERATURE = (
        "Refrigeration.Common.Setting.WineCompartment.SetpointTemperature"
    )
    REFRIGERATION_COMMON_WINE_COMPARTMENT_2_SETPOINT_TEMPERATURE = (
        "Refrigeration.Common.Setting.WineCompartment2.SetpointTemperature"
    )
    REFRIGERATION_COMMON_WINE_COMPARTMENT_3_SETPOINT_TEMPERATURE = (
        "Refrigeration.Common.Setting.WineCompartment3.SetpointTemperature"
    )
    REFRIGERATION_FRIDGE_FREEZER_SETPOINT_TEMPERATURE_REFRIGERATOR = (
        "Refrigeration.FridgeFreezer.Setting.SetpointTemperatureRefrigerator"
    )
    REFRIGERATION_FRIDGE_FREEZER_SETPOINT_TEMPERATURE_FREEZER = (
        "Refrigeration.FridgeFreezer.Setting.SetpointTemperatureFreezer"
    )
    REFRIGERATION_FRIDGE_FREEZER_SUPER_MODE_REFRIGERATOR = (
        "Refrigeration.FridgeFreezer.Setting.SuperModeRefrigerator"
    )
    REFRIGERATION_FRIDGE_FREEZER_SUPER_MODE_FREEZER = (
        "Refrigeration.FridgeFreezer.Setting.SuperModeFreezer"
    )


class CommandKey(StrEnum):
    """Represent command keys."""

    BSH_COMMON_ACKNOWLEDGE_EVENT = "BSH.Common.Command.AcknowledgeEvent"
    BSH_COMMON_OPEN_DOOR = "BSH.Common.Command.OpenDoor"
    BSH_COMMON_PARTLY_OPEN_DOOR = "BSH.Common.Command.PartlyOpenDoor"
    BSH_COMMON_PAUSE_PROGRAM = "BSH.Common.Command.PauseProgram"
    BSH_COMMON_RESUME_PROGRAM = "BSH.Common.Command.ResumeProgram"


class EventKey(StrEnum):
    """Represent event keys."""

    BSH_COMMON_ROOT_SELECTED_PROGRAM = "BSH.Common.Root.SelectedProgram"
    BSH_COMMON_ROOT_ACTIVE_PROGRAM = "BSH.Common.Root.ActiveProgram"
    BSH_COMMON_OPTION_START_IN_RELATIVE = "BSH.Common.Option.StartInRelative"
    BSH_COMMON_OPTION_FINISH_IN_RELATIVE = "BSH.Common.Option.FinishInRelative"
    BSH_COMMON_OPTION_DURATION = "BSH.Common.Option.Duration"
