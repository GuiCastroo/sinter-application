"""Carrega o catálogo inteiro num Catalog imutável (AD-29)."""

from sinter.domain.errors import SinterError
from sinter.domain.model.catalog import Catalog, ParsedManifest, build_catalog
from sinter.domain.model.registry import SUPPORTED_SCHEMA_VERSION
from sinter.domain.services.references import documents, resolve_doc_path
from sinter.domain.validation.engine import FileFacts
from sinter.domain.validation.finding import ERROR, Finding
from sinter.domain.validation.schema import parse_manifest
from sinter.ports.outbound.catalog_files import CatalogFiles
from sinter.ports.outbound.manifest_codec import ManifestCodec, ManifestSyntaxError

ORGANIZATION_FILE = "organization.yaml"


def _file_finding(file: str, code: str, message: str, line: int | None = None) -> Finding:
    return Finding(code=code, severity=ERROR, file=file, path="", line=line, message=message)


def load(files: CatalogFiles, codec: ManifestCodec) -> tuple[Catalog, list[Finding]]:
    if not files.exists(ORGANIZATION_FILE):
        raise SinterError(
            "USAGE_NOT_A_CATALOG",
            f"a pasta não é um catálogo do Sinter (falta {ORGANIZATION_FILE})",
        )

    parsed: list[ParsedManifest] = []
    findings: list[Finding] = []
    for path in files.list_manifests():
        try:
            docs = codec.split(files.read(path))
        except ManifestSyntaxError as exc:
            findings.append(_file_finding(path, "YAML_SYNTAX_ERROR", exc.message, exc.line))
            continue
        if not docs:
            findings.append(_file_finding(path, "MANIFEST_EMPTY", "arquivo sem manifesto"))
            continue
        if len(docs) > 1:
            findings.append(
                _file_finding(
                    path,
                    "MANIFEST_MULTIPLE_DOCUMENTS",
                    "um arquivo do catálogo tem um manifesto só",
                )
            )
        doc = docs[0]
        manifest, schema_findings = parse_manifest(path, doc.data, doc.positions)
        parsed.append(manifest)
        findings.extend(schema_findings)

    catalog = build_catalog(parsed)
    org = catalog.organization()
    if org is not None and org.spec.schema_version > SUPPORTED_SCHEMA_VERSION:
        raise SinterError(
            "CATALOG_VERSION_UNSUPPORTED",
            f"o catálogo usa schemaVersion {org.spec.schema_version}; "
            f"esta versão do Sinter suporta até {SUPPORTED_SCHEMA_VERSION}. Atualize o Sinter.",
            {"catalog": org.spec.schema_version, "supported": SUPPORTED_SCHEMA_VERSION},
        )
    return catalog, findings


def file_facts(catalog: Catalog, files: CatalogFiles) -> FileFacts:
    """Fatos de arquivo que as regras precisam, calculados igual no validate e no apply (AD-31)."""
    paths = {
        resolve_doc_path(at.manifest.file, at.doc.path)
        for at in documents(catalog)
        if at.doc.path is not None
    }
    return FileFacts(existing=frozenset(p for p in paths if files.exists(p)))
