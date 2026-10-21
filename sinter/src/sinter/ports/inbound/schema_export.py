"""Contrato do `sinter schema export`."""

from pydantic import BaseModel

from sinter.domain.model.base import SinterModel
from sinter.ports.inbound.common import ErrorEnvelope
from sinter.ports.inbound.validate import ValidateResult


class SchemaExportRequest(SinterModel):
    target: str = "schemas"


class SchemaExportResult(SinterModel):
    files: list[str]
    changed: list[str]
    summary: str


def published_results() -> dict[str, type[BaseModel]]:
    """Resultados da CLI que também são contrato (o `--json` de cada comando)."""
    return {
        "error": ErrorEnvelope,
        "schema-export-result": SchemaExportResult,
        "validate-result": ValidateResult,
    }
