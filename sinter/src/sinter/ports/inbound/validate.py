"""Contrato do `sinter validate`."""

from sinter.domain.model.base import SinterModel
from sinter.ports.inbound.common import Report


class ValidateRequest(SinterModel):
    pass


class ValidateResult(SinterModel):
    report: Report
    files_checked: int
    summary: str
