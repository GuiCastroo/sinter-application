"""Caso de uso `sinter fmt`: formata manifestos sem criar commits."""

from sinter.domain.errors import SinterError
from sinter.domain.validation.finding import ERROR, Finding
from sinter.ports.inbound.common import Report
from sinter.ports.inbound.fmt import FmtRequest, FmtResult
from sinter.ports.outbound.catalog_files import CatalogFiles
from sinter.ports.outbound.catalog_writer import CatalogWriter
from sinter.ports.outbound.manifest_codec import ManifestCodec, ManifestSyntaxError


class Fmt:
    def __init__(self, files: CatalogFiles, writer: CatalogWriter, codec: ManifestCodec) -> None:
        self._files = files
        self._writer = writer
        self._codec = codec

    def __call__(self, request: FmtRequest) -> FmtResult:
        all_paths = self._files.list_manifests()
        if request.path is None:
            paths = all_paths
        elif request.path in all_paths:
            paths = [request.path]
        else:
            raise SinterError(
                "ITEM_NOT_FOUND",
                f"'{request.path}' não é um manifesto YAML deste catálogo",
                {"path": request.path},
            )

        changed: dict[str, str] = {}
        findings: list[Finding] = []
        for path in paths:
            source = self._files.read(path)
            try:
                formatted = self._codec.format(source)
                original_data = [doc.data for doc in self._codec.split(source)]
                formatted_data = [doc.data for doc in self._codec.split(formatted)]
            except ManifestSyntaxError as exc:
                findings.append(
                    Finding(
                        code="YAML_SYNTAX_ERROR",
                        severity=ERROR,
                        file=path,
                        path="",
                        line=exc.line,
                        message=exc.message,
                    )
                )
                continue
            if original_data != formatted_data:
                findings.append(
                    Finding(
                        code="FMT_SEMANTIC_CHANGE",
                        severity=ERROR,
                        file=path,
                        path="",
                        message=("a formatação alteraria dados YAML; o arquivo não foi gravado"),
                    )
                )
                continue
            if source != formatted:
                changed[path] = formatted
                if request.check:
                    findings.append(
                        Finding(
                            code="FILE_NOT_FORMATTED",
                            severity=ERROR,
                            file=path,
                            path="",
                            message="manifesto fora do formato canônico; rode `sinter fmt`",
                        )
                    )

        wrote_changes = bool(changed and not request.check and not findings)
        if wrote_changes:
            self._writer.write_all(changed)

        report = Report.from_findings(findings)
        if request.check:
            summary = f"{len(paths)} manifesto(s) conferido(s); {len(findings)} fora do formato."
        elif findings:
            summary = (
                f"{len(paths)} manifesto(s) conferido(s); "
                "nenhum arquivo foi gravado devido a erros."
            )
        else:
            summary = f"{len(changed)} manifesto(s) formatado(s)."
        return FmtResult(
            report=report,
            files_checked=len(paths),
            files_changed=sorted(changed) if wrote_changes else [],
            summary=summary,
        )
