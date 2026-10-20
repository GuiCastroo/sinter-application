"""Cada manifesto mora no caminho canônico do seu kind (AD-40)."""

from collections.abc import Iterable

from sinter.domain.model.catalog import Catalog
from sinter.domain.model.domain import Domain
from sinter.domain.model.registry import KINDS, domain_folder_of
from sinter.domain.validation.engine import FileFacts, Problem, problem, rule
from sinter.domain.validation.finding import ERROR


@rule(code="FILE_NOT_CANONICAL", severity=ERROR)
def canonical_path(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    folders = {
        m.model.metadata.id: domain_folder_of(m.model.metadata.domain_id)
        for m in catalog.valid_manifests("Domain")
        if isinstance(m.model, Domain)
    }
    for m in catalog.valid_manifests():
        if m.kind is None:
            continue
        expected = KINDS[m.kind].canonical_path(m.model, folders.get)
        if expected is not None and m.file.lower() != expected.lower():
            yield problem(m, "kind", message=f"um {m.kind} deve estar em '{expected}'")
