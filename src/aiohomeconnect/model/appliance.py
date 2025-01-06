"""Provide appliance models for the Home Connect API."""

from __future__ import annotations

from dataclasses import dataclass, field

from mashumaro import field_options
from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class HomeAppliance(DataClassJSONMixin):
    """Represent HomeAppliance."""

    ha_id: str | None = field(default=None, metadata=field_options(alias="haId"))
    name: str | None = None
    type: str | None = None
    brand: str | None = None
    vib: str | None = None
    e_number: str | None = field(default=None, metadata=field_options(alias="enumber"))
    connected: bool | None = None


@dataclass
class ArrayOfHomeAppliances(DataClassJSONMixin):
    """Object containing an array of home appliances."""

    homeappliances: list[HomeAppliance]
