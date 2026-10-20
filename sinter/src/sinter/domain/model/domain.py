"""domains/<d>/domain.yaml — kind: Domain (Apêndice A.2)."""

from typing import Literal

from pydantic import Field

from sinter.domain.model.base import SinterModel
from sinter.domain.model.blocks import (
    DataAsset,
    Decision,
    Doc,
    GlossaryTerm,
    Metadata,
    Modernization,
    Operation,
    Rule,
)


class DomainMetadata(Metadata):
    domain_id: str
    area: str


class DomainSpec(SinterModel):
    parent: str
    purpose: str
    does: list[str] = Field(default_factory=list)
    does_not: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)
    subdomains: list[str]
    shared_repositories: list[str] = Field(default_factory=list)
    rules: list[Rule] = Field(default_factory=list)
    main_journeys: list[str] = Field(default_factory=list)
    glossary: list[GlossaryTerm] = Field(default_factory=list)
    operation: Operation | None = None
    modernization: Modernization | None = None
    data: list[DataAsset] = Field(default_factory=list)
    regulations: list[str] = Field(default_factory=list)
    standards: list[str] = Field(default_factory=list)
    decisions: list[Decision] = Field(default_factory=list)
    docs: list[Doc] = Field(default_factory=list)
    next_task_number: int | None = None
    next_adr_number: int | None = None
    delivery: Literal["direct", "pr"] | None = None


class Domain(SinterModel):
    api_version: Literal["sinter.dev/v1"]
    kind: Literal["Domain"]
    metadata: DomainMetadata
    spec: DomainSpec
