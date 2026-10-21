"""Toda referência interna existe; dom- fora do catálogo é aviso; ext- só formato (FR-17)."""

from collections.abc import Iterable

from sinter.domain.model.catalog import Catalog
from sinter.domain.model.registry import EXTERNAL_ID
from sinter.domain.services.references import open_references, references
from sinter.domain.validation.engine import FileFacts, Problem, problem, rule
from sinter.domain.validation.finding import ERROR, WARNING

_LABEL = {
    "Doc": "doc",
    "Repository": "repo",
    "Subdomain": "subdomínio",
    "Application": "aplicação",
    "Domain": "domínio",
    "Journey": "jornada",
    "Regulation": "regulação",
    "Standard": "padrão",
    "Rule": "regra",
    "Data": "dado",
    "Decision": "decisão",
}


def _known(catalog: Catalog) -> set[tuple[str, str]]:
    return {(e.kind, e.id) for e in catalog.entries}


@rule(code="REF_NOT_FOUND", severity=ERROR)
def internal_refs(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    known = _known(catalog)
    for ref in references(catalog):
        if not any((kind, ref.value) in known for kind in ref.kinds):
            label = _LABEL.get(ref.kinds[0], ref.kinds[0])
            yield problem(
                ref.manifest, *ref.path, message=f"{label} '{ref.value}' não existe no catálogo"
            )
    for open_ref in open_references(catalog):
        if open_ref.value.startswith("sub-") and ("Subdomain", open_ref.value) not in known:
            yield problem(
                open_ref.manifest,
                *open_ref.path,
                message=f"subdomínio '{open_ref.value}' não existe no catálogo",
            )


@rule(code="DOM_REF_NOT_IN_CATALOG", severity=WARNING)
def domain_refs(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    """O catálogo cresce aos poucos: domínio vizinho ainda não modelado é aviso, não erro."""
    known = _known(catalog)
    for ref in open_references(catalog):
        if ref.value.startswith("dom-") and ("Domain", ref.value) not in known:
            yield problem(
                ref.manifest,
                *ref.path,
                message=f"domínio '{ref.value}' ainda não está no catálogo",
            )


@rule(code="REF_FORMAT_INVALID", severity=ERROR)
def open_ref_format(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    for ref in open_references(catalog):
        value = ref.value
        if value.startswith(("sub-", "dom-")):
            continue
        if not EXTERNAL_ID.match(value):
            yield problem(
                ref.manifest,
                *ref.path,
                message=f"'{value}' deve ser 'sub-…', 'dom-…' ou 'ext-<slug>'",
            )
