"""Blocos que se repetem em vários kinds (Apêndice A: envelope, DOC, GLOSSÁRIO)."""

import datetime as dt
from typing import Literal, Self

from pydantic import Field, model_validator

from sinter.domain.model.base import SinterModel

Status = Literal["candidate", "approved", "rejected", "deprecated", "superseded"]


class Metadata(SinterModel):
    id: str
    name: str
    status: Status
    owners: list[str] = Field(default_factory=list)


class Doc(SinterModel):
    """Um doc ligado a um nível: arquivo em docs/ (path) ou link (url), ou reuso por id (ref)."""

    ref: str | None = None
    id: str | None = None
    title: str | None = None
    type: str | None = None
    path: str | None = None
    url: str | None = None
    date: dt.date | None = None
    verified_at: dt.date | None = None

    @model_validator(mode="after")
    def _ref_or_full(self) -> Self:
        if self.ref is not None:
            others = (self.id, self.title, self.type, self.path, self.url, self.date)
            if any(v is not None for v in others):
                raise ValueError("doc com 'ref' não pode ter outros campos")
        elif self.title is None or self.type is None:
            raise ValueError("doc precisa de 'title' e 'type' (ou só 'ref')")
        return self


class GlossaryTerm(SinterModel):
    term: str
    definition: str
    synonyms: list[str] = Field(default_factory=list)
    not_to_confuse_with: str | None = None


Extraction = Literal["human", "extracted", "inferred"]
Criticality = Literal["baixa", "media", "alta", "critica"]


class Evidence(SinterModel):
    source: str
    locator: str
    version: str | dt.date | None = None
    content_hash: str | None = None
    extraction: Extraction


class Rule(SinterModel):
    id: str
    statement: str
    exceptions: list[str] = Field(default_factory=list)
    example: str | None = None
    regulations: list[str] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)


class Decision(SinterModel):
    id: str
    title: str
    date: dt.date
    context: str
    decision: str
    consequences: list[str] = Field(default_factory=list)
    supersedes: str | None = None
    evidence: list[Evidence] = Field(default_factory=list)


class Operation(SinterModel):
    hours: str | None = None
    batch_windows: list[str] = Field(default_factory=list)
    criticality: Criticality | None = None
    volume: str | None = None


class Modernization(SinterModel):
    goal: str
    decision: str | None = None


class DataLayerInfo(SinterModel):
    location: str
    format: str | None = None
    refresh: str | None = None
    quality: list[str] = Field(default_factory=list)
    consumers: list[str] = Field(default_factory=list)


class DataAsset(SinterModel):
    id: str
    name: str
    description: str | None = None
    produced_by: str | None = None
    personal_data: bool
    layers: dict[str, DataLayerInfo]
    docs: list[Doc] = Field(default_factory=list)
