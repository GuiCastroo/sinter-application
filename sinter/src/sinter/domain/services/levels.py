"""Consulta por nível (AD-24, AD-39): o ÚNICO lugar que monta as visões."""

from sinter.domain.model.catalog import Catalog, Entry, ParsedManifest
from sinter.domain.model.domain import Domain
from sinter.domain.model.journey import Journey
from sinter.domain.model.organization import Organization
from sinter.domain.model.subdomain import Subdomain
from sinter.domain.model.views import (
    ApplicationLevel0,
    AppSummary,
    DomainLevel0,
    DomainLevel1,
    Gap,
    JourneyLevel0,
    Level0,
    Omitted,
    OrganizationLevel0,
    OtherLevel0,
    SubdomainLevel0,
    SubdomainLevel1,
)
from sinter.domain.services import inheritance


def _subdomains_of(catalog: Catalog, domain_id: str) -> list[Subdomain]:
    return [
        m.model
        for m in catalog.valid_manifests("Subdomain")
        if isinstance(m.model, Subdomain)
        and m.model.metadata.domain == domain_id
        and m.model.metadata.status == "approved"
    ]


def _journeys_of(catalog: Catalog, domain_id: str) -> list[Journey]:
    return [
        m.model
        for m in catalog.valid_manifests("Journey")
        if isinstance(m.model, Journey)
        and m.model.metadata.domain == domain_id
        and m.model.metadata.status == "approved"
    ]


def _gaps(does: list[str], does_not: list[str], unknowns: list[str]) -> list[Gap]:
    pairs = (("does", does), ("doesNot", does_not), ("unknowns", unknowns))
    return [Gap(field=name) for name, values in pairs if not values]


def level0_of_manifest(catalog: Catalog, m: ParsedManifest) -> Level0:
    model = m.model
    if isinstance(model, Domain):
        subs = _subdomains_of(catalog, model.metadata.id)
        return DomainLevel0(
            id=model.metadata.id,
            kind="Domain",
            name=model.metadata.name,
            status=model.metadata.status,
            purpose=model.spec.purpose.strip(),
            domain_id=model.metadata.domain_id,
            area=model.metadata.area,
            counts={
                "subdomains": len(subs),
                "applications": sum(len(s.spec.applications) for s in subs),
                "journeys": len(_journeys_of(catalog, model.metadata.id)),
            },
        )
    if isinstance(model, Subdomain):
        return SubdomainLevel0(
            id=model.metadata.id,
            kind="Subdomain",
            name=model.metadata.name,
            status=model.metadata.status,
            purpose=model.spec.purpose.strip(),
            counts={
                "applications": len(model.spec.applications),
            },
        )
    if isinstance(model, Journey):
        return JourneyLevel0(
            id=model.metadata.id,
            kind="Journey",
            name=model.metadata.name,
            status=model.metadata.status,
            purpose=model.spec.purpose.strip(),
            domain=model.metadata.domain,
            counts={
                "stages": len(model.spec.stages),
                "steps": sum(len(s.steps) for s in model.spec.stages),
            },
        )
    if isinstance(model, Organization):
        return OrganizationLevel0(
            id=model.metadata.id,
            kind="Organization",
            name=model.metadata.name,
            status=model.metadata.status,
            counts={
                "areas": len(model.spec.areas),
                "domains": sum(
                    1
                    for dm in catalog.valid_manifests("Domain")
                    if isinstance(dm.model, Domain) and dm.model.metadata.status == "approved"
                ),
            },
        )
    meta = getattr(model, "metadata", None)
    return OtherLevel0(
        id=m.id or "",
        kind=m.kind or "?",
        name=str(getattr(meta, "name", m.id)),
        status=getattr(meta, "status", None),
    )


def level0_of_entry(catalog: Catalog, entry: Entry) -> Level0:
    """Itens que moram dentro de outro arquivo (aplicação, regra, área…)."""
    owner = catalog.manifest_of_file(entry.file)
    if entry.kind == "Application" and owner is not None and isinstance(owner.model, Subdomain):
        for app in owner.model.spec.applications:
            if app.id == entry.id:
                return ApplicationLevel0(
                    id=app.id,
                    kind="Application",
                    name=app.name,
                    lifecycle=app.lifecycle,
                    domain=owner.model.metadata.domain,
                    counts={"repositories": len(app.repositories)},
                )
    return OtherLevel0(id=entry.id, kind=entry.kind, name=entry.id)


def domain_level1(catalog: Catalog, m: ParsedManifest) -> DomainLevel1:
    assert isinstance(m.model, Domain)
    d = m.model
    by_id = {s.metadata.id: s for s in _subdomains_of(catalog, d.metadata.id)}
    subdomains = []
    for sub_id in d.spec.subdomains:
        sub_m = catalog.manifest(sub_id)
        if sub_m is not None and sub_id in by_id and by_id[sub_id].metadata.status == "approved":
            view = level0_of_manifest(catalog, sub_m)
            if isinstance(view, SubdomainLevel0):
                subdomains.append(view)
    return DomainLevel1(
        **level0_of_manifest(catalog, m).model_dump(),
        does=d.spec.does,
        does_not=d.spec.does_not,
        unknowns=d.spec.unknowns,
        gaps=_gaps(d.spec.does, d.spec.does_not, d.spec.unknowns),
        subdomains=subdomains,
        main_journeys=[
            j
            for j in d.spec.main_journeys
            if j in {x.metadata.id for x in _journeys_of(catalog, d.metadata.id)}
        ],
        operation=inheritance.operation(d, None),
        modernization=d.spec.modernization,
        **inheritance.domain_knowledge(catalog, d).model_dump(),
    )


def subdomain_level1(catalog: Catalog, m: ParsedManifest) -> SubdomainLevel1:
    assert isinstance(m.model, Subdomain)
    s = m.model
    parent_m = catalog.manifest(s.metadata.domain)
    parent = (
        parent_m.model
        if parent_m is not None
        and isinstance(parent_m.model, Domain)
        and parent_m.model.metadata.status == "approved"
        else None
    )
    return SubdomainLevel1(
        **level0_of_manifest(catalog, m).model_dump(),
        domain=s.metadata.domain,
        does=s.spec.does,
        does_not=s.spec.does_not,
        unknowns=s.spec.unknowns,
        gaps=_gaps(s.spec.does, s.spec.does_not, s.spec.unknowns),
        applications=[
            AppSummary(id=a.id, name=a.name, lifecycle=a.lifecycle, aliases=a.aliases)
            for a in s.spec.applications
        ],
        operation=inheritance.operation(s, parent),
        modernization=s.spec.modernization,
        **inheritance.subdomain_knowledge(catalog, s, parent).model_dump(),
    )


def omitted(ident: str, level: int, kind: str) -> list[Omitted]:
    if level == 0:
        return [
            Omitted(
                what="faz / não faz / não sabemos, filhos e conhecimento",
                command=f"sinter get {ident} --level 1",
            )
        ]
    if kind in ("Domain", "Subdomain"):
        return [
            Omitted(
                what="vizinhança",
                command=f"sinter get {ident} --level 2",
            )
        ]
    return []
