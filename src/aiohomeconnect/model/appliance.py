"""Provide appliance models for the Home Connect API."""

from __future__ import annotations

from dataclasses import dataclass, field

from mashumaro import field_options
from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class HomeAppliance(DataClassJSONMixin):
    """Represent HomeAppliance."""

    ha_id: str = field(metadata=field_options(alias="haId"))
    name: str
    type: str
    brand: str
    vib: str
    e_number: str = field(metadata=field_options(alias="enumber"))
    connected: bool


@dataclass
class ArrayOfHomeAppliances(DataClassJSONMixin):
    """Object containing an array of home appliances."""

    homeappliances: list[HomeAppliance]
