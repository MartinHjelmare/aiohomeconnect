"""Provide setting models for the Home Connect API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from mashumaro import field_options
from mashumaro.mixins.json import DataClassJSONMixin

from aiohomeconnect.const import LOGGER


@dataclass
class GetSetting(DataClassJSONMixin):
    """Specific setting of the home appliance."""

    key: SettingKey
    raw_key: str = field(metadata=field_options(alias="key"))
    value: Any
    name: str | None = None
    display_value: str | None = field(
        default=None, metadata=field_options(alias="displayvalue")
    )
    unit: str | None = None
    type: str | None = None
    constraints: SettingConstraints | None = None


@dataclass
class SettingConstraints(DataClassJSONMixin):
    """Represent SettingConstraints."""

    min: int | None = None
    max: int | None = None
    step_size: int | None = field(
        default=None, metadata=field_options(alias="stepsize")
    )
    allowed_values: list[str | None] | None = field(
        default=None, metadata=field_options(alias="allowedvalues")
    )
    display_values: list[str | None] | None = field(
        default=None, metadata=field_options(alias="displayvalues")
    )
    default: Any | None = None
    access: str | None = None


@dataclass
class ArrayOfSettings(DataClassJSONMixin):
    """List of settings of the home appliance."""

    settings: list[GetSetting]


@dataclass
class PutSetting(DataClassJSONMixin):
    """Specific setting of the home appliance."""

    key: SettingKey
    value: Any


@dataclass
class PutSettings(DataClassJSONMixin):
    """List of settings of the home appliance."""

    data: list[PutSetting]


class SettingKey(StrEnum):
    """Represent a setting key."""

    @classmethod
    def _missing_(cls, value: object) -> SettingKey:
        """Return UNKNOWN for missing keys."""
        LOGGER.debug("Unknown setting key: %s", value)
        return cls.UNKNOWN

    UNKNOWN = "unknown"
    BSH_COMMON_POWER_STATE = "BSH.Common.Setting.PowerState"
    BSH_COMMON_TEMPERATURE_UNIT = "BSH.Common.Setting.TemperatureUnit"
    BSH_COMMON_LIQUID_VOLUME_UNIT = "BSH.Common.Setting.LiquidVolumeUnit"
    BSH_COMMON_CHILD_LOCK = "BSH.Common.Setting.ChildLock"
    BSH_COMMON_ALARM_CLOCK = "BSH.Common.Setting.AlarmClock"
    BSH_COMMON_AMBIENT_LIGHT_ENABLED = "BSH.Common.Setting.AmbientLightEnabled"
    BSH_COMMON_AMBIENT_LIGHT_BRIGHTNESS = "BSH.Common.Setting.AmbientLightBrightness"
    BSH_COMMON_AMBIENT_LIGHT_COLOR = "BSH.Common.Setting.AmbientLightColor"
    BSH_COMMON_AMBIENT_LIGHT_CUSTOM_COLOR = "BSH.Common.Setting.AmbientLightCustomColor"
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
    CONSUMER_PRODUCTS_CLEANING_ROBOT_NAME_OF_MAP_4 = (
        "ConsumerProducts.CleaningRobot.Setting.NameOfMap4"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_NAME_OF_MAP_5 = (
        "ConsumerProducts.CleaningRobot.Setting.NameOfMap5"
    )
    COOKING_COMMON_LIGHTING = "Cooking.Common.Setting.Lighting"
    COOKING_COMMON_LIGHTING_BRIGHTNESS = "Cooking.Common.Setting.LightingBrightness"
    COOKING_HOOD_COLOR_TEMPERATURE_PERCENT = (
        "Cooking.Hood.Setting.ColorTemperaturePercent"
    )
    COOKING_HOOD_COLOR_TEMPERATURE = "Cooking.Hood.Setting.ColorTemperature"
    COOKING_OVEN_SABBATH_MODE = "Cooking.Oven.Setting.SabbathMode"
    LAUNDRY_CARE_WASHER_I_DOS_1_BASE_LEVEL = "LaundryCare.Washer.Setting.IDos1BaseLevel"
    LAUNDRY_CARE_WASHER_I_DOS_2_BASE_LEVEL = "LaundryCare.Washer.Setting.IDos2BaseLevel"
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
