"""Tipos usados por mais de um Result (AD-26, AD-35)."""

from collections.abc import Iterable
from typing import Any

from pydantic import Field

from sinter.domain.model.base import SinterModel
from sinter.domain.validation.finding import Finding, sort_key


class Report(SinterModel):
    errors: list[Finding] = Field(default_factory=list)
    warnings: list[Finding] = Field(default_factory=list)

    @classmethod
    def from_findings(cls, findings: Iterable[Finding]) -> "Report":
        ordered = sorted(findings, key=sort_key)
        return cls(
            errors=[f for f in ordered if f.severity == "error"],
            warnings=[f for f in ordered if f.severity == "warning"],
        )


class ErrorBody(SinterModel):
    code: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)


class ErrorEnvelope(SinterModel):
    """Saída de qualquer comando que falha com SinterError (AD-33, AD-37)."""

    error: ErrorBody
