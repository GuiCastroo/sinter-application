"""Ids: formato com prefixo do Apêndice A.8 e unicidade no catálogo."""

from collections import defaultdict
from collections.abc import Iterable

from sinter.domain.model.catalog import Catalog, Entry
from sinter.domain.model.registry import ADR_ID, ID_SLUG, RELATION_ID, prefix_for
from sinter.domain.validation.engine import FileFacts, Problem, problem_at, rule
from sinter.domain.validation.finding import ERROR, Related


@rule(code="ID_FORMAT_INVALID", severity=ERROR)
def id_format(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    for e in catalog.entries:
        if e.kind == "Decision":
            if not ADR_ID.match(e.id):
                yield problem_at(e, message=f"id '{e.id}' deve ser 'ADR-<ID-DOMÍNIO>-NNN'")
            continue
        if e.kind == "Relation":
            if not RELATION_ID.match(e.id):
                yield problem_at(
                    e, message=f"id '{e.id}' deve ser 'rel-<app-origem>--<tipo>--<app-alvo>'"
                )
            continue
        prefix = prefix_for(e.kind)
        if prefix is None:
            if not ID_SLUG.match(e.id):
                yield problem_at(e, message=f"id '{e.id}' fora do formato (minúsculas e hífen)")
            continue
        rest = e.id[len(prefix) :] if e.id.startswith(prefix) else None
        if rest is None or not ID_SLUG.match(rest):
            yield problem_at(
                e, message=f"id '{e.id}' deve ser '{prefix}<slug>' (minúsculas, números e hífen)"
            )


@rule(code="DUPLICATE_ID", severity=ERROR)
def duplicate_id(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    by_id: dict[str, list[Entry]] = defaultdict(list)
    for e in catalog.entries:
        by_id[e.id].append(e)
    for ident in sorted(by_id):
        group = sorted(by_id[ident], key=lambda e: (e.file, e.line or 0))
        first = group[0]
        for dup in group[1:]:
            yield problem_at(
                dup,
                message=f"id '{ident}' repetido (já usado em {first.file})",
                related=[Related(file=first.file, path=first.path)],
            )
