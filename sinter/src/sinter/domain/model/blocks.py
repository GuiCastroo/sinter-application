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
