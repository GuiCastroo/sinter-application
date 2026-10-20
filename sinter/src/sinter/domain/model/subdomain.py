"""domains/<d>/subdomains/sub-*.yaml — kind: Subdomain (Apêndice A.3)."""

from typing import Literal

from pydantic import Field

from sinter.domain.model.base import SinterModel
from sinter.domain.model.blocks import (
    Application,
    Boundaries,
    DataAsset,
    Decision,
    Doc,
    GlossaryTerm,
    Metadata,
    Modernization,
    Operation,
    Rule,
)


class SubdomainMetadata(Metadata):
    domain: str


class SubdomainSpec(SinterModel):
    purpose: str
    does: list[str] = Field(default_factory=list)
    does_not: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)
    applications: list[Application] = Field(default_factory=list)
    data: list[DataAsset] = Field(default_factory=list)
    rules: list[Rule] = Field(default_factory=list)
    boundaries: Boundaries | None = None
    glossary: list[GlossaryTerm] = Field(default_factory=list)
    operation: Operation | None = None
    modernization: Modernization | None = None
    regulations: list[str] = Field(default_factory=list)
    standards: list[str] = Field(default_factory=list)
    decisions: list[Decision] = Field(default_factory=list)
    docs: list[Doc] = Field(default_factory=list)


class Subdomain(SinterModel):
    api_version: Literal["sinter.dev/v1"]
    kind: Literal["Subdomain"]
    metadata: SubdomainMetadata
    spec: SubdomainSpec
