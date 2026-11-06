"""Provide appliance models for the Home Connect API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from mashumaro import field_options
from mashumaro.mixins.json import DataClassJSONMixin

from aiohomeconnect.const import LOGGER


class ApplianceType(StrEnum):
    """Represent an appliance type."""

    @classmethod
    def _missing_(cls, value: object) -> ApplianceType:
        """Return UNKNOWN or mapped ones for missing keys."""
        LOGGER.debug("Unknown appliance type: %s", value)
        return cls.UNKNOWN

    UNKNOWN = "unknown"
    AIR_CONDITIONER = "AirConditioner"
    CLEANING_ROBOT = "CleaningRobot"
    COFFEE_MAKER = "CoffeeMaker"
    COOK_PROCESSOR = "CookProcessor"
    DISHWASHER = "Dishwasher"
    DRYER = "Dryer"
    FREEZER = "Freezer"
    FRIDGE_FREEZER = "FridgeFreezer"
    HOB = "Hob"
    HOOD = "Hood"
    MICROWAVE = "Microwave"
    OVEN = "Oven"
    REFRIGERATOR = "Refrigerator"
    WARMING_DRAWER = "WarmingDrawer"
    WASHER = "Washer"
    WASHER_DRYER = "WasherDryer"
    WINE_COOLER = "WineCooler"


@dataclass
class HomeAppliance(DataClassJSONMixin):
    """Represent HomeAppliance."""

    ha_id: str = field(metadata=field_options(alias="haId"))
    name: str
    type: ApplianceType
    brand: str
    vib: str
    e_number: str = field(metadata=field_options(alias="enumber"))
    connected: bool


@dataclass
class ArrayOfHomeAppliances(DataClassJSONMixin):
    """Object containing an array of home appliances."""

    homeappliances: list[HomeAppliance]
