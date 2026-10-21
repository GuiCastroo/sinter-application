"""Glossário: um termo tem um sentido só na linha organização → domínio → subdomínio (FR-20)."""

from collections.abc import Iterable, Iterator

from sinter.domain.model.blocks import GlossaryTerm
from sinter.domain.model.catalog import Catalog, ParsedManifest
from sinter.domain.model.domain import Domain
from sinter.domain.model.organization import Organization
from sinter.domain.model.subdomain import Subdomain
from sinter.domain.services.text import fold
from sinter.domain.validation.engine import FileFacts, Problem, problem, rule
from sinter.domain.validation.finding import ERROR, Related

Defined = dict[str, tuple[ParsedManifest, int]]


def _names(term: GlossaryTerm) -> Iterator[str]:
    yield fold(term.term)
    for synonym in term.synonyms:
        yield fold(synonym)


def _check(
    m: ParsedManifest, terms: list[GlossaryTerm], inherited: Defined
) -> tuple[list[Problem], Defined]:
    """Confere os termos de um nível contra os herdados e entre si; devolve o que fica definido."""
    problems: list[Problem] = []
    defined: Defined = dict(inherited)
    for i, term in enumerate(terms):
        for name in _names(term):
            if name in defined:
                where, j = defined[name]
                problems.append(
                    problem(
                        m,
                        "spec",
                        "glossary",
                        i,
                        message=f"'{term.term}' já está definido em {where.file}; não redefinir",
                        related=[Related(file=where.file, path=f"spec.glossary[{j}]")],
                    )
                )
                break
        else:
            for name in _names(term):
                defined[name] = (m, i)
    return problems, defined


@rule(code="GLOSSARY_TERM_REDEFINED", severity=ERROR)
def no_redefinition(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    org_defined: Defined = {}
    for m in catalog.valid_manifests("Organization"):
        assert isinstance(m.model, Organization)
        problems, org_defined = _check(m, m.model.spec.glossary, {})
        yield from problems

    domain_defined: dict[str, Defined] = {}
    for m in catalog.valid_manifests("Domain"):
        assert isinstance(m.model, Domain)
        problems, defined = _check(m, m.model.spec.glossary, org_defined)
        domain_defined[m.model.metadata.id] = defined
        yield from problems

    for m in catalog.valid_manifests("Subdomain"):
        assert isinstance(m.model, Subdomain)
        inherited = domain_defined.get(m.model.metadata.domain, org_defined)
        problems, _ = _check(m, m.model.spec.glossary, inherited)
        yield from problems
