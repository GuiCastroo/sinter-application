"""Regulações: `supersedes` aponta para uma regulação que existe."""

from collections.abc import Iterable

from sinter.domain.model.catalog import Catalog
from sinter.domain.model.regulation import Regulation
from sinter.domain.validation.engine import FileFacts, Problem, problem, rule
from sinter.domain.validation.finding import ERROR


@rule(code="REGULATION_SUPERSEDES_NOT_FOUND", severity=ERROR)
def supersedes_exists(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    for m in catalog.valid_manifests("Regulation"):
        assert isinstance(m.model, Regulation)
        target = m.model.spec.supersedes
        if target is not None and not catalog.find(target, "Regulation"):
            yield problem(
                m, "spec", "supersedes", message=f"regulação '{target}' não existe no catálogo"
            )
