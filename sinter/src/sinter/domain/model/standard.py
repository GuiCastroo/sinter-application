"""standards/std-*.yaml — kind: Standard (Apêndice A.1)."""

from typing import Literal

from pydantic import Field

from sinter.domain.model.base import SinterModel
from sinter.domain.model.blocks import Doc, Metadata

AppliesTo = Literal["api", "evento", "batch", "dados", "front"]


class StandardSpec(SinterModel):
    summary: str
    applies_to: list[AppliesTo] = Field(default_factory=list)
    docs: list[Doc] = Field(default_factory=list)


class Standard(SinterModel):
    api_version: Literal["sinter.dev/v1"]
    kind: Literal["Standard"]
    metadata: Metadata
    spec: StandardSpec
