"""regulations/reg-*.yaml — kind: Regulation (Apêndice A.1)."""

import datetime as dt
from typing import Literal

from pydantic import Field

from sinter.domain.model.base import SinterModel
from sinter.domain.model.blocks import Doc, Metadata


class Effective(SinterModel):
    from_: dt.date = Field(alias="from")
    to: dt.date | None = None


class RegulationSpec(SinterModel):
    jurisdiction: str
    effective: Effective
    supersedes: str | None = None
    summary: str | None = None
    docs: list[Doc] = Field(default_factory=list)


class Regulation(SinterModel):
    api_version: Literal["sinter.dev/v1"]
    kind: Literal["Regulation"]
    metadata: Metadata
    spec: RegulationSpec
