"""organization.yaml — kind: Organization (Apêndice A.1)."""

from typing import Literal

from pydantic import Field

from sinter.domain.model.base import SinterModel
from sinter.domain.model.blocks import GlossaryTerm, Metadata

DEFAULT_DOC_TYPES = ("negocio", "ata", "pauta", "runbook", "arquitetura", "gerado", "link")


class Area(SinterModel):
    id: str
    name: str
    description: str | None = None


class DataLayer(SinterModel):
    id: str
    name: str
    meaning: str | None = None


class OrganizationSpec(SinterModel):
    schema_version: int
    areas: list[Area]
    data_layers: list[DataLayer] = Field(default_factory=list)
    glossary: list[GlossaryTerm] = Field(default_factory=list)
    doc_types: list[str] = Field(default_factory=lambda: list(DEFAULT_DOC_TYPES))
    vocabulary: dict[str, str] = Field(default_factory=dict)


class Organization(SinterModel):
    api_version: Literal["sinter.dev/v1"]
    kind: Literal["Organization"]
    metadata: Metadata
    spec: OrganizationSpec
