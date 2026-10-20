"""Relação modernized_by: aplicação → aplicação, no domínio da origem (FR-10, AD-19)."""

from collections.abc import Iterable

from sinter.domain.model.catalog import Catalog
from sinter.domain.model.relation import Relation
from sinter.domain.model.subdomain import Subdomain
from sinter.domain.validation.engine import FileFacts, Problem, problem, rule
from sinter.domain.validation.finding import ERROR


def _app_domains(catalog: Catalog) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in catalog.valid_manifests("Subdomain"):
        assert isinstance(m.model, Subdomain)
        for app in m.model.spec.applications:
            out.setdefault(app.id, m.model.metadata.domain)
    return out


@rule(code="RELATION_ENDPOINT_NOT_FOUND", severity=ERROR)
def endpoints_exist(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    apps = {e.id for e in catalog.entries if e.kind == "Application"}
    for m in catalog.valid_manifests("Relation"):
        assert isinstance(m.model, Relation)
        for field_name, value in (("source", m.model.spec.source), ("target", m.model.spec.target)):
            if value not in apps:
                yield problem(
                    m, "spec", field_name, message=f"aplicação '{value}' não existe no catálogo"
                )


@rule(code="RELATION_ID_MISMATCH", severity=ERROR)
def id_matches(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    """O id nasce de origem e tipo (o alvo da criação pode mudar depois, AD-19)."""
    for m in catalog.valid_manifests("Relation"):
        assert isinstance(m.model, Relation)
        spec = m.model.spec
        prefix = f"rel-{spec.source}--{spec.type}--"
        if not m.model.metadata.id.startswith(prefix):
            yield problem(
                m, "metadata", "id", message=f"id deve começar com '{prefix}' (origem e tipo)"
            )


@rule(code="RELATION_OWNER_MISMATCH", severity=ERROR)
def owned_by_source_domain(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    owners = _app_domains(catalog)
    for m in catalog.valid_manifests("Relation"):
        assert isinstance(m.model, Relation)
        owner = owners.get(m.model.spec.source)
        if owner is not None and m.model.metadata.domain != owner:
            yield problem(
                m,
                "metadata",
                "domain",
                message=f"a relação mora no domínio da origem ('{owner}')",
            )
