"""Caso de uso do `sinter schema export`: grava o contrato JSON Schema (AD-12, AD-36)."""

from sinter.domain.services.schemas import contract_schemas
from sinter.ports.inbound.schema_export import (
    SchemaExportRequest,
    SchemaExportResult,
    published_results,
)
from sinter.ports.outbound.local_files import LocalFiles


class SchemaExport:
    def __init__(self, local: LocalFiles) -> None:
        self._local = local

    def __call__(self, request: SchemaExportRequest) -> SchemaExportResult:
        target = request.target.rstrip("/")
        files: list[str] = []
        changed: list[str] = []
        for name, text in contract_schemas(published_results()).items():
            path = f"{target}/{name}"
            files.append(path)
            if self._local.read(path) != text:
                self._local.write(path, text)
                changed.append(path)
        return SchemaExportResult(
            files=files,
            changed=changed,
            summary=f"{len(files)} schemas em {target}/; {len(changed)} alterados.",
        )
