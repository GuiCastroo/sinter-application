"""Domínio: id-domínio, área, pai e ADRs com o id-domínio certo (FR-3, FR-4)."""

from collections import defaultdict
from collections.abc import Iterable

from sinter.domain.model.blocks import Decision
from sinter.domain.model.catalog import Catalog, ParsedManifest
from sinter.domain.model.domain import Domain
from sinter.domain.model.registry import ADR_ID, DOMAIN_ID
from sinter.domain.model.subdomain import Subdomain
from sinter.domain.validation.engine import FileFacts, Problem, problem, rule
from sinter.domain.validation.finding import ERROR, Related


def _domains(catalog: Catalog) -> Iterable[tuple[ParsedManifest, Domain]]:
    for m in catalog.valid_manifests("Domain"):
        assert isinstance(m.model, Domain)
        yield m, m.model


@rule(code="DOMAIN_ID_FORMAT_INVALID", severity=ERROR)
def domain_id_format(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    for m, d in _domains(catalog):
        if not DOMAIN_ID.match(d.metadata.domain_id):
            yield problem(
                m,
                "metadata",
                "domainId",
                message=(
                    f"id-domínio '{d.metadata.domain_id}' deve ter 2 a 8 "
                    "letras maiúsculas ou números"
                ),
            )


@rule(code="DOMAIN_ID_DUPLICATE", severity=ERROR)
def domain_id_unique(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    by_id: dict[str, list[ParsedManifest]] = defaultdict(list)
    for m, d in _domains(catalog):
        by_id[d.metadata.domain_id.upper()].append(m)
    for domain_id in sorted(by_id):
        first, *others = by_id[domain_id]
        for m in others:
            yield problem(
                m,
                "metadata",
                "domainId",
                message=f"id-domínio '{domain_id}' já é usado em {first.file}",
                related=[Related(file=first.file, path="metadata.domainId")],
            )


@rule(code="DOMAIN_AREA_NOT_FOUND", severity=ERROR)
def area_exists(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    org = catalog.organization()
    if org is None:
        return
    areas = {a.id for a in org.spec.areas}
    for m, d in _domains(catalog):
        if d.metadata.area not in areas:
            known = ", ".join(sorted(areas)) or "nenhuma"
            yield problem(
                m,
                "metadata",
                "area",
                message=f"área '{d.metadata.area}' não está em organization.yaml (áreas: {known})",
            )


@rule(code="DOMAIN_PARENT_NOT_ORGANIZATION", severity=ERROR)
def parent_is_organization(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    org = catalog.organization()
    if org is None:
        return
    for m, d in _domains(catalog):
        if d.spec.parent != org.metadata.id:
            yield problem(
                m,
                "spec",
                "parent",
                message=f"o pai do domínio deve ser a organização '{org.metadata.id}'",
            )


@rule(code="ADR_DOMAIN_MISMATCH", severity=ERROR)
def adr_uses_own_domain_id(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    by_id = {d.metadata.id: d for _m, d in _domains(catalog)}
    owners: list[tuple[ParsedManifest, Domain, list[Decision]]] = [
        (m, d, d.spec.decisions) for m, d in _domains(catalog)
    ]
    for m in catalog.valid_manifests("Subdomain"):
        assert isinstance(m.model, Subdomain)
        parent = by_id.get(m.model.metadata.domain)
        if parent is not None:
            owners.append((m, parent, m.model.spec.decisions))
    for m, d, decisions in owners:
        for i, decision in enumerate(decisions):
            match = ADR_ID.match(decision.id)
            if match and match.group(1) != d.metadata.domain_id:
                yield problem(
                    m,
                    "spec",
                    "decisions",
                    i,
                    message=(
                        f"ADR '{decision.id}' deve usar o id-domínio deste domínio: "
                        f"ADR-{d.metadata.domain_id}-NNN"
                    ),
                )
