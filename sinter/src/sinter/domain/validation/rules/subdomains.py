"""Subdomínio, aplicações e dados (FR-7, FR-8, FR-19)."""

from collections import Counter
from collections.abc import Iterable

from sinter.domain.model.blocks import DataAsset
from sinter.domain.model.catalog import Catalog, ParsedManifest
from sinter.domain.model.domain import Domain
from sinter.domain.model.subdomain import Subdomain
from sinter.domain.validation.engine import FileFacts, Problem, problem, rule
from sinter.domain.validation.finding import ERROR


def _domains(catalog: Catalog) -> dict[str, tuple[ParsedManifest, Domain]]:
    out: dict[str, tuple[ParsedManifest, Domain]] = {}
    for m in catalog.valid_manifests("Domain"):
        assert isinstance(m.model, Domain)
        out.setdefault(m.model.metadata.id, (m, m.model))
    return out


def _subdomains(catalog: Catalog) -> Iterable[tuple[ParsedManifest, Subdomain]]:
    for m in catalog.valid_manifests("Subdomain"):
        assert isinstance(m.model, Subdomain)
        yield m, m.model


@rule(code="SUBDOMAIN_DOMAIN_NOT_FOUND", severity=ERROR)
def domain_exists(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    domains = _domains(catalog)
    for m, sub in _subdomains(catalog):
        if sub.metadata.domain not in domains:
            yield problem(
                m,
                "metadata",
                "domain",
                message=f"domínio '{sub.metadata.domain}' não existe no catálogo",
            )


@rule(code="SUBDOMAIN_SUMMARY_MISMATCH", severity=ERROR)
def summary_matches(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    """O sumário `subdomains:` do domínio bate com os arquivos que dizem pertencer a ele (AD-22)."""
    # Lê o domínio direto dos dados: subdomínio que falhou no schema continua contando (AD-29).
    members: dict[str, list[str]] = {}
    present: set[str] = set()
    for sub_m in catalog.manifests:
        if sub_m.kind != "Subdomain" or sub_m.id is None:
            continue
        present.add(sub_m.id)
        meta = sub_m.data.get("metadata") if isinstance(sub_m.data, dict) else None
        owner = meta.get("domain") if isinstance(meta, dict) else None
        if isinstance(owner, str):
            members.setdefault(owner, []).append(sub_m.id)

    for dom_id, (m, domain) in sorted(_domains(catalog).items()):
        listed = domain.spec.subdomains
        counts = Counter(listed)
        actual = set(members.get(dom_id, []))
        for i, sub_id in enumerate(listed):
            if counts[sub_id] > 1 and listed.index(sub_id) != i:
                yield problem(m, "spec", "subdomains", i, message=f"'{sub_id}' repetido no sumário")
            elif sub_id not in actual and sub_id not in present:
                yield problem(
                    m,
                    "spec",
                    "subdomains",
                    i,
                    message=f"'{sub_id}' está no sumário mas não há arquivo desse subdomínio",
                )
            elif sub_id not in actual:
                yield problem(
                    m,
                    "spec",
                    "subdomains",
                    i,
                    message=f"'{sub_id}' está no sumário mas o arquivo diz que é de outro domínio",
                )
        for sub_id in sorted(actual - set(listed)):
            yield problem(
                m,
                "spec",
                "subdomains",
                message=f"falta '{sub_id}' no sumário (o arquivo diz domain: {dom_id})",
            )


@rule(code="APP_ID_DOMAIN_MISMATCH", severity=ERROR)
def app_id_uses_domain_id(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    domains = _domains(catalog)
    for m, sub in _subdomains(catalog):
        found = domains.get(sub.metadata.domain)
        if found is None:
            continue
        prefix = f"app-{found[1].metadata.domain_id.lower()}-"
        for i, app in enumerate(sub.spec.applications):
            if not app.id.startswith(prefix):
                yield problem(
                    m,
                    "spec",
                    "applications",
                    i,
                    "id",
                    message=f"id da aplicação deve ser '{prefix}<slug>'",
                )


@rule(code="APP_REPO_NOT_FOUND", severity=ERROR)
def app_repos_exist(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    repos = {e.id for e in catalog.entries if e.kind == "Repository"}
    for m, sub in _subdomains(catalog):
        for i, app in enumerate(sub.spec.applications):
            for j, use in enumerate(app.repositories):
                if use.repo not in repos:
                    yield problem(
                        m,
                        "spec",
                        "applications",
                        i,
                        "repositories",
                        j,
                        "repo",
                        message=f"repo '{use.repo}' não está em repositories.yaml",
                    )


def _data_owners(catalog: Catalog) -> Iterable[tuple[ParsedManifest, list[DataAsset]]]:
    for m, domain in _domains(catalog).values():
        yield m, domain.spec.data
    for m, sub in _subdomains(catalog):
        yield m, sub.spec.data


@rule(code="DATA_LAYER_NOT_FOUND", severity=ERROR)
def data_layers_exist(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    org = catalog.organization()
    if org is None:
        return
    layers = [layer.id for layer in org.spec.data_layers]
    for m, assets in _data_owners(catalog):
        for i, asset in enumerate(assets):
            for name in asset.layers:
                if name not in layers:
                    known = ", ".join(layers) or "nenhuma"
                    yield problem(
                        m,
                        "spec",
                        "data",
                        i,
                        "layers",
                        name,
                        message=f"camada '{name}' não está em organization.yaml (camadas: {known})",
                    )


@rule(code="DATA_PRODUCER_NOT_FOUND", severity=ERROR)
def data_producer_exists(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    apps = {e.id for e in catalog.entries if e.kind == "Application"}
    for m, assets in _data_owners(catalog):
        for i, asset in enumerate(assets):
            if asset.produced_by is not None and asset.produced_by not in apps:
                yield problem(
                    m,
                    "spec",
                    "data",
                    i,
                    "producedBy",
                    message=f"aplicação '{asset.produced_by}' não existe no catálogo",
                )
