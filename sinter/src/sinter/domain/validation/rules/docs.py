"""Docs: caminho OU link, tipo da lista da organização, arquivo que existe (FR-6, FR-14)."""

from collections.abc import Iterable

from sinter.domain.model.catalog import Catalog
from sinter.domain.services.references import documents, resolve_doc_path
from sinter.domain.validation.engine import FileFacts, Problem, problem, rule
from sinter.domain.validation.finding import ERROR


@rule(code="DOC_PATH_OR_URL", severity=ERROR)
def path_or_url(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    for at in documents(catalog):
        doc = at.doc
        if doc.ref is None and (doc.path is None) == (doc.url is None):
            yield problem(
                at.manifest, *at.path, message="doc precisa de 'path' OU 'url' (um dos dois)"
            )


@rule(code="DOC_TYPE_UNKNOWN", severity=ERROR)
def known_type(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    org = catalog.organization()
    if org is None:
        return
    types = org.spec.doc_types
    for at in documents(catalog):
        if at.doc.type is not None and at.doc.type not in types:
            yield problem(
                at.manifest,
                *at.path,
                "type",
                message=(
                    f"tipo '{at.doc.type}' não está em organization.docTypes ({', '.join(types)})"
                ),
            )


@rule(code="DOC_PATH_NOT_FOUND", severity=ERROR)
def path_exists(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    for at in documents(catalog):
        if at.doc.path is None:
            continue
        full = resolve_doc_path(at.manifest.file, at.doc.path)
        if full not in facts.existing:
            yield problem(at.manifest, *at.path, "path", message=f"arquivo '{full}' não existe")


@rule(code="DOC_REF_NOT_FOUND", severity=ERROR)
def ref_exists(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    docs = {e.id for e in catalog.entries if e.kind == "Doc"}
    for at in documents(catalog):
        if at.doc.ref is not None and at.doc.ref not in docs:
            yield problem(
                at.manifest, *at.path, "ref", message=f"doc '{at.doc.ref}' não existe no catálogo"
            )
