"""Provide status models for the Home Connect API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from mashumaro import field_options
from mashumaro.mixins.json import DataClassJSONMixin

from aiohomeconnect.const import LOGGER


@dataclass
class Status(DataClassJSONMixin):
    """Represent Status."""

    key: StatusKey
    raw_key: str = field(metadata=field_options(alias="key"))
    value: Any
    name: str | None = None
    display_value: str | None = field(
        default=None, metadata=field_options(alias="displayvalue")
    )
    unit: str | None = None
    type: str | None = None
    constraints: StatusConstraints | None = None


@dataclass
class StatusConstraints(DataClassJSONMixin):
    """Represent StatusConstraints."""

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
class ArrayOfStatus(DataClassJSONMixin):
    """List of status of the home appliance."""

    status: list[Status]


class StatusKey(StrEnum):
    """Represent a status key."""

    @classmethod
    def _missing_(cls, value: object) -> StatusKey:
        """Return UNKNOWN for missing keys."""
        LOGGER.debug("Unknown status key: %s", value)
        return cls.UNKNOWN

    UNKNOWN = "unknown"
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
    COOKING_OVEN_CURRENT_CAVITY_TEMPERATURE = (
        "Cooking.Oven.Status.CurrentCavityTemperature"
    )
