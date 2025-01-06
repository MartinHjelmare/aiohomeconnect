"""Provide image models for the Home Connect API."""

from __future__ import annotations

from dataclasses import dataclass, field

from mashumaro import field_options
from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class ArrayOfImages(DataClassJSONMixin):
    """List of images available from the home appliance."""

    images: list[Image]


@dataclass
class Image(DataClassJSONMixin):
    """Represent Image."""

    key: str
    image_key: str = field(metadata=field_options(alias="imagekey"))
    preview_image_key: str = field(metadata=field_options(alias="previewimagekey"))
    timestamp: int
    quality: str
    name: str | None = None
