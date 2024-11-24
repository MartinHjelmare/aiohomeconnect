"""Provide appliance models for the Home Connect API."""

from __future__ import annotations

from dataclasses import dataclass, field

from mashumaro import field_options
from mashumaro.mixins.json import DataClassJSONMixin


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
