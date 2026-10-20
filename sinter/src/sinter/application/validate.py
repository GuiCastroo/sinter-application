"""Caso de uso do `sinter validate`."""

from sinter.application.load import load
from sinter.domain.services.summary import validation_summary
from sinter.domain.validation.engine import FileFacts, validate_catalog
from sinter.ports.inbound.common import Report
from sinter.ports.inbound.validate import ValidateRequest, ValidateResult
from sinter.ports.outbound.catalog_files import CatalogFiles
from sinter.ports.outbound.manifest_codec import ManifestCodec


class Validate:
    def __init__(self, files: CatalogFiles, codec: ManifestCodec) -> None:
        self._files = files
        self._codec = codec

    def __call__(self, request: ValidateRequest) -> ValidateResult:
        catalog, load_findings = load(self._files, self._codec)
        findings = [*load_findings, *validate_catalog(catalog, FileFacts())]
        report = Report.from_findings(findings)
        files_checked = len(self._files.list_manifests())
        return ValidateResult(
            report=report,
            files_checked=files_checked,
            summary=validation_summary(len(report.errors), len(report.warnings), files_checked),
        )
