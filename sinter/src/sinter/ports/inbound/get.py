"""Contrato do `sinter get`."""

from pydantic import Field

from sinter.domain.model.base import SinterModel
from sinter.domain.model.views import DomainLevel1, Level0View, Omitted, SubdomainLevel1
from sinter.ports.inbound.common import Report


class GetRequest(SinterModel):
    id: str
    level: int = Field(default=1, ge=0, le=2)


class GetResult(SinterModel):
    level: int
    item: DomainLevel1 | SubdomainLevel1 | Level0View
    omitted: list[Omitted]
    summary: str
    report: Report = Field(default_factory=Report)
