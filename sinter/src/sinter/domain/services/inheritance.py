"""O ÚNICO lugar que soma próprio + herdado e marca a origem (AD-22)."""

from sinter.domain.model.blocks import Doc, GlossaryTerm, Operation
from sinter.domain.model.catalog import Catalog
from sinter.domain.model.domain import Domain
from sinter.domain.model.subdomain import Subdomain
from sinter.domain.model.views import (
    DecisionView,
    DocView,
    IdentifiedDocView,
    Knowledge,
    OperationView,
    RefView,
    RuleView,
    TermView,
)
from sinter.domain.services.references import documents


def _docs(docs: list[Doc], origin: str, catalog_docs: dict[str, Doc]) -> list[DocView]:
    out: list[DocView] = []
    for d in docs:
        if d.ref is not None:
            target = catalog_docs.get(d.ref)
            if target is None:
                continue
            d = target
        assert d.title is not None and d.type is not None
        out.append(
            IdentifiedDocView(
                id=d.id, title=d.title, type=d.type, path=d.path, url=d.url, origin=origin
            )
            if d.id is not None
            else DocView(title=d.title, type=d.type, path=d.path, url=d.url, origin=origin)
        )
    return out


def _terms(terms: list[GlossaryTerm], origin: str) -> list[TermView]:
    return [
        TermView(
            term=t.term,
            definition=t.definition,
            synonyms=t.synonyms,
            not_to_confuse_with=t.not_to_confuse_with,
            origin=origin,
        )
        for t in terms
    ]


def catalog_docs(catalog: Catalog) -> dict[str, Doc]:
    """Docs com id, para resolver `ref:`."""
    return {at.doc.id: at.doc for at in documents(catalog) if at.doc.id is not None}


def _own(level: Domain | Subdomain, docs_by_id: dict[str, Doc]) -> Knowledge:
    origin = level.metadata.id
    s = level.spec
    return Knowledge(
        rules=[
            RuleView(
                id=r.id,
                statement=r.statement,
                exceptions=r.exceptions,
                regulations=r.regulations,
                origin=origin,
            )
            for r in s.rules
        ],
        regulations=[RefView(id=x, origin=origin) for x in s.regulations],
        standards=[RefView(id=x, origin=origin) for x in s.standards],
        decisions=[
            DecisionView(id=d.id, title=d.title, date=d.date, decision=d.decision, origin=origin)
            for d in s.decisions
        ],
        docs=_docs(s.docs, origin, docs_by_id),
        glossary=_terms(s.glossary, origin),
    )


def _concat(first: Knowledge, then: Knowledge) -> Knowledge:
    """Próprio primeiro, herdado depois; o que o nível já tem não se repete."""

    def merge_refs(a: list[RefView], b: list[RefView]) -> list[RefView]:
        seen = {x.id for x in a}
        return [*a, *(x for x in b if x.id not in seen)]

    return Knowledge(
        rules=[*first.rules, *then.rules],
        regulations=merge_refs(first.regulations, then.regulations),
        standards=merge_refs(first.standards, then.standards),
        decisions=[*first.decisions, *then.decisions],
        docs=[
            *first.docs,
            *(
                d
                for d in then.docs
                if not isinstance(d, IdentifiedDocView)
                or d.id not in {x.id for x in first.docs if isinstance(x, IdentifiedDocView)}
            ),
        ],
        glossary=[*first.glossary, *then.glossary],
    )


def domain_knowledge(catalog: Catalog, domain: Domain) -> Knowledge:
    docs_by_id = catalog_docs(catalog)
    org = catalog.organization()
    inherited = Knowledge(
        glossary=_terms(org.spec.glossary, org.metadata.id) if org is not None else []
    )
    return _concat(_own(domain, docs_by_id), inherited)


def subdomain_knowledge(catalog: Catalog, sub: Subdomain, domain: Domain | None) -> Knowledge:
    own = _own(sub, catalog_docs(catalog))
    if domain is None:
        return own
    return _concat(own, domain_knowledge(catalog, domain))


def operation(level: Domain | Subdomain, parent: Domain | None) -> OperationView | None:
    """Operação: o subdomínio herda do domínio cada campo que não declarar (FR-21)."""
    own = level.spec.operation
    inherited = parent.spec.operation if parent is not None else None
    if own is None and inherited is None:
        return None
    if own is None:
        assert inherited is not None and parent is not None
        fields = [k for k, v in inherited.model_dump().items() if v not in (None, [])]
        return OperationView(
            value=inherited,
            origin=parent.metadata.id,
            inherited_fields=fields,
            inherited_from=parent.metadata.id,
        )
    if inherited is None:
        return OperationView(value=own, origin=level.metadata.id)
    merged: dict[str, object] = {}
    taken: list[str] = []
    for name in Operation.model_fields:
        mine = getattr(own, name)
        theirs = getattr(inherited, name)
        if name not in own.model_fields_set and theirs not in (None, []):
            merged[name] = theirs
            taken.append(name)
        else:
            merged[name] = mine
    return OperationView(
        value=Operation.model_validate(merged),
        origin=level.metadata.id,
        inherited_fields=sorted(taken),
        inherited_from=parent.metadata.id if taken and parent is not None else None,
    )
