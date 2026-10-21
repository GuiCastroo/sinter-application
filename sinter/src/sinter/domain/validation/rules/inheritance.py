"""Herança sem exceção: repetir no subdomínio o que já vem do domínio não acrescenta nada (FR-6)."""

from collections.abc import Iterable

from sinter.domain.model.catalog import Catalog
from sinter.domain.model.domain import Domain
from sinter.domain.model.subdomain import Subdomain
from sinter.domain.validation.engine import FileFacts, Problem, problem, rule
from sinter.domain.validation.finding import WARNING


@rule(code="INHERITED_REPEATED", severity=WARNING)
def repeated_from_domain(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    domains = {
        m.model.metadata.id: m.model
        for m in catalog.valid_manifests("Domain")
        if isinstance(m.model, Domain)
    }
    for m in catalog.valid_manifests("Subdomain"):
        assert isinstance(m.model, Subdomain)
        domain = domains.get(m.model.metadata.domain)
        if domain is None:
            continue
        for field_name, own, inherited in (
            ("regulations", m.model.spec.regulations, domain.spec.regulations),
            ("standards", m.model.spec.standards, domain.spec.standards),
        ):
            for i, value in enumerate(own):
                if value in inherited:
                    yield problem(
                        m,
                        "spec",
                        field_name,
                        i,
                        message=f"'{value}' já vem do domínio por herança; pode tirar daqui",
                    )
