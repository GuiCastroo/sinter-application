"""A formatação canônica é um aviso em `validate` (AD-30, AD-37)."""

from collections.abc import Iterable

from sinter.domain.model.catalog import Catalog
from sinter.domain.validation.engine import FileFacts, Problem, problem, rule


@rule(code="FILE_NOT_FORMATTED", severity="warning")
def formatting(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    for manifest in catalog.manifests:
        if facts.formatted.get(manifest.file) is False:
            yield problem(
                manifest,
                message="manifesto fora do formato canônico; rode `sinter fmt`",
            )
