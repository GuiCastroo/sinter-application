"""domains/<d>/journeys/jor-*.yaml — kind: Journey (Apêndice A.4)."""

from typing import Literal, Self

from pydantic import Field, model_validator

from sinter.domain.model.base import SinterModel
from sinter.domain.model.blocks import Decision, Doc, Metadata


class JourneyMetadata(Metadata):
    domain: str


class Step(SinterModel):
    id: str
    capability: str | None = None
    calls: str | None = None
    action: str
    actor: str | None = None
    application: str | None = None
    result: str | None = None
    next: list[str] = Field(default_factory=list)
    parallel_with: list[str] = Field(default_factory=list)
    rules: list[str] = Field(default_factory=list)
    governed_by: list[str] = Field(default_factory=list)
    event: str | None = None
    job: str | None = None
    on_failure: str | None = None

    @model_validator(mode="after")
    def _capability_or_calls(self) -> Self:
        if self.capability is None and self.calls is None:
            raise ValueError(
                "passo precisa de 'capability' (subdomínio) ou, se só externo, 'calls'"
            )
        return self


class Stage(SinterModel):
    id: str
    name: str | None = None
    entry: str | None = None
    via: list[str] = Field(default_factory=list)
    steps: list[Step] = Field(min_length=1)


class JourneySpec(SinterModel):
    variant_of: str | None = None
    purpose: str
    trigger: str
    outcome: str
    orchestrator: str | None = None
    stages: list[Stage] = Field(min_length=1)
    unknowns: list[str] = Field(default_factory=list)
    regulations: list[str] = Field(default_factory=list)
    standards: list[str] = Field(default_factory=list)
    decisions: list[Decision] = Field(default_factory=list)
    docs: list[Doc] = Field(default_factory=list)


class Journey(SinterModel):
    api_version: Literal["sinter.dev/v1"]
    kind: Literal["Journey"]
    metadata: JourneyMetadata
    spec: JourneySpec
