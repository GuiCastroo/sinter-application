"""Contrato do `sinter fmt`."""

from pydantic import Field

from sinter.domain.model.base import SinterModel
from sinter.ports.inbound.common import Report


class FmtRequest(SinterModel):
    path: str | None = None
    check: bool = False


class FmtResult(SinterModel):
    report: Report
    files_checked: int
    files_changed: list[str] = Field(default_factory=list)
    summary: str
