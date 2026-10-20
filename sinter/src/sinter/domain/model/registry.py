"""Registro de kinds: o ÚNICO lugar com kind → modelo, prefixo de id e caminho canônico (AD-40)."""

import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from sinter.domain.model.base import SinterModel
from sinter.domain.model.domain import Domain
from sinter.domain.model.journey import Journey
from sinter.domain.model.organization import Organization
from sinter.domain.model.regulation import Regulation
from sinter.domain.model.relation import Relation
from sinter.domain.model.repository_list import RepositoryList
from sinter.domain.model.standard import Standard
from sinter.domain.model.subdomain import Subdomain

SUPPORTED_SCHEMA_VERSION = 1

ID_SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DOMAIN_ID = re.compile(r"^[A-Z0-9]{2,8}$")
ADR_ID = re.compile(r"^ADR-([A-Z0-9]{2,8})-(\d{3})$")
RELATION_ID = re.compile(r"^rel-(app-[a-z0-9-]+?)--([a-z_]+)--(app-[a-z0-9-]+)$")
# Ids sem arquivo: só o formato é conferido (FR-17).
EXTERNAL_ID = re.compile(r"^ext-[a-z0-9]+(-[a-z0-9]+)*$")
EVENT_ID = re.compile(r"^evt-[a-z0-9]+(-[a-z0-9]+)*$")
SCHEDULER_ID = re.compile(r"^agenda-[a-z0-9]+(-[a-z0-9]+)*$")


DomainFolder = Callable[[str], str | None]
"""Dado o id de um domínio (dom-x), devolve a pasta dele (`domains/x`) ou None."""


@dataclass(frozen=True)
class KindInfo:
    kind: str
    model: type[SinterModel]
    prefix: str | None
    canonical_path: Callable[[Any, "DomainFolder"], str | None]
    """Caminho onde o item deve morar; None se depende de um domínio que não existe."""
    calc_fields: tuple[str, ...] = ()
    """Campos `(calc)` do Apêndice A: a CLI calcula, ninguém escreve (AD-4)."""


def _meta_id(item: Any) -> str:
    return str(item.metadata.id)


def domain_folder_of(domain_id: str) -> str:
    """Pasta canônica de um domínio a partir do id-domínio (sempre em minúsculas, AD-40)."""
    return f"domains/{domain_id.lower()}"


def _inside_domain(sub_folder: str) -> Callable[[Any, DomainFolder], str | None]:
    def path(item: Any, folder_of: DomainFolder) -> str | None:
        folder = folder_of(item.metadata.domain)
        return None if folder is None else f"{folder}/{sub_folder}/{_meta_id(item)}.yaml"

    return path


KINDS: dict[str, KindInfo] = {
    info.kind: info
    for info in (
        KindInfo(
            "Organization", Organization, "org-", lambda _m, _f: "organization.yaml", ("domains",)
        ),
        KindInfo("RepositoryList", RepositoryList, None, lambda _m, _f: "repositories.yaml"),
        KindInfo("Regulation", Regulation, "reg-", lambda m, _f: f"regulations/{_meta_id(m)}.yaml"),
        KindInfo("Standard", Standard, "std-", lambda m, _f: f"standards/{_meta_id(m)}.yaml"),
        KindInfo(
            "Domain",
            Domain,
            "dom-",
            lambda m, _f: f"{domain_folder_of(m.metadata.domain_id)}/domain.yaml",
            ("boundaries", "repositories", "journeys", "modernizationOverview", "counts"),
        ),
        KindInfo("Subdomain", Subdomain, "sub-", _inside_domain("subdomains"), ("journeys",)),
        KindInfo(
            "Journey",
            Journey,
            "jor-",
            _inside_domain("journeys"),
            ("sequence", "participants", "subdomains"),
        ),
        KindInfo("Relation", Relation, "rel-", _inside_domain("relations")),
    )
}

# Itens que vivem DENTRO de um manifesto mas têm id global (AD-41).
CHILD_PREFIXES: dict[str, str] = {
    "Area": "area-",
    "Repository": "repo-",
    "Rule": "rule-",
    "Data": "dat-",
    "Doc": "doc-",
    "Application": "app-",
}

# Listas dentro de um manifesto cujos itens têm id global (AD-41): (caminho, kind do item).
CHILD_LISTS: dict[str, tuple[tuple[tuple[str, ...], str], ...]] = {
    "Organization": ((("spec", "areas"), "Area"),),
    "RepositoryList": ((("spec", "repositories"), "Repository"),),
    "Regulation": ((("spec", "docs"), "Doc"),),
    "Standard": ((("spec", "docs"), "Doc"),),
    "Domain": (
        (("spec", "rules"), "Rule"),
        (("spec", "decisions"), "Decision"),
        (("spec", "data"), "Data"),
        (("spec", "docs"), "Doc"),
    ),
    "Journey": ((("spec", "decisions"), "Decision"), (("spec", "docs"), "Doc")),
    "Subdomain": (
        (("spec", "applications"), "Application"),
        (("spec", "rules"), "Rule"),
        (("spec", "decisions"), "Decision"),
        (("spec", "data"), "Data"),
        (("spec", "docs"), "Doc"),
    ),
}


def prefix_for(kind: str) -> str | None:
    if kind in KINDS:
        return KINDS[kind].prefix
    return CHILD_PREFIXES.get(kind)
