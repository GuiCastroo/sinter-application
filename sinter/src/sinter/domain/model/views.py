"""Visões por nível: o que a CLI mostra de cada item. Só levels.py as produz (AD-39)."""

import datetime as dt
from typing import Annotated, Literal

from pydantic import Field

from sinter.domain.model.base import SinterModel
from sinter.domain.model.blocks import Lifecycle, Modernization, Operation, Status


class Level0(SinterModel):
    """Identidade em poucas linhas: o mesmo formato em get, find, list e nos filhos."""

    id: str
    kind: str
    name: str
    status: Status | None = None
    purpose: str | None = None
    counts: dict[str, int] = Field(default_factory=dict)


class DomainLevel0(Level0):
    kind: Literal["Domain"] = "Domain"
    domain_id: str
    area: str


class SubdomainLevel0(Level0):
    kind: Literal["Subdomain"] = "Subdomain"


class JourneyLevel0(Level0):
    kind: Literal["Journey"] = "Journey"
    domain: str


class OrganizationLevel0(Level0):
    kind: Literal["Organization"] = "Organization"


class ApplicationLevel0(Level0):
    kind: Literal["Application"] = "Application"
    domain: str
    lifecycle: Lifecycle


class OtherLevel0(Level0):
    kind: Literal[
        "RepositoryList",
        "Regulation",
        "Standard",
        "Relation",
        "Repository",
        "Rule",
        "Doc",
        "Data",
        "Decision",
        "Area",
        "?",
    ]


Level0View = Annotated[
    DomainLevel0
    | SubdomainLevel0
    | JourneyLevel0
    | OrganizationLevel0
    | ApplicationLevel0
    | OtherLevel0,
    Field(discriminator="kind"),
]


class Inherited[T](SinterModel):
    value: T
    origin: str


class Gap(SinterModel):
    """Campo que ninguém preencheu: a IA sabe que não foi dito, em vez de supor que não há nada."""

    field: str


class Omitted(SinterModel):
    what: str
    command: str


class RuleView(SinterModel):
    id: str
    statement: str
    exceptions: list[str] = Field(default_factory=list)
    regulations: list[str] = Field(default_factory=list)
    origin: str


class DecisionView(SinterModel):
    id: str
    title: str
    date: dt.date
    decision: str
    origin: str


class DocView(SinterModel):
    title: str
    type: str
    path: str | None = None
    url: str | None = None
    origin: str


class IdentifiedDocView(DocView):
    id: str


class TermView(SinterModel):
    term: str
    definition: str
    synonyms: list[str] = Field(default_factory=list)
    not_to_confuse_with: str | None = None
    origin: str


class RefView(SinterModel):
    """Id citado (regulação, padrão) com o nível onde foi declarado."""

    id: str
    origin: str


class OperationView(Inherited[Operation]):
    inherited_fields: list[str] = Field(default_factory=list)
    inherited_from: str | None = None


class Knowledge(SinterModel):
    """Conhecimento do nível: próprio + herdado, cada item com `origin` (AD-22)."""

    rules: list[RuleView] = Field(default_factory=list)
    regulations: list[RefView] = Field(default_factory=list)
    standards: list[RefView] = Field(default_factory=list)
    decisions: list[DecisionView] = Field(default_factory=list)
    docs: list[IdentifiedDocView | DocView] = Field(default_factory=list)
    glossary: list[TermView] = Field(default_factory=list)


class AppSummary(SinterModel):
    id: str
    name: str
    lifecycle: Lifecycle
    aliases: list[str] = Field(default_factory=list)


class DomainLevel1(Knowledge, DomainLevel0):
    does: list[str]
    does_not: list[str]
    unknowns: list[str]
    gaps: list[Gap]
    subdomains: list[SubdomainLevel0]
    main_journeys: list[str]
    operation: OperationView | None = None
    modernization: Modernization | None = None

    @property
    def level0(self) -> DomainLevel0:
        return DomainLevel0.model_validate(
            {name: getattr(self, name) for name in DomainLevel0.model_fields}
        )

    @property
    def knowledge(self) -> Knowledge:
        return Knowledge.model_validate(
            {name: getattr(self, name) for name in Knowledge.model_fields}
        )


class SubdomainLevel1(Knowledge, SubdomainLevel0):
    domain: str
    does: list[str]
    does_not: list[str]
    unknowns: list[str]
    gaps: list[Gap]
    applications: list[AppSummary]
    operation: OperationView | None = None
    modernization: Modernization | None = None

    @property
    def level0(self) -> SubdomainLevel0:
        return SubdomainLevel0.model_validate(
            {name: getattr(self, name) for name in SubdomainLevel0.model_fields}
        )

    @property
    def knowledge(self) -> Knowledge:
        return Knowledge.model_validate(
            {name: getattr(self, name) for name in Knowledge.model_fields}
        )


Level = Literal[0, 1, 2]
