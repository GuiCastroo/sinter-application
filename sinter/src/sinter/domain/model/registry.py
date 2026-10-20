"""Registro de kinds: o ÚNICO lugar com kind → modelo, prefixo de id e caminho canônico (AD-40)."""

import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from sinter.domain.model.base import SinterModel
from sinter.domain.model.domain import Domain
from sinter.domain.model.organization import Organization
from sinter.domain.model.regulation import Regulation
from sinter.domain.model.repository_list import RepositoryList
from sinter.domain.model.standard import Standard

SUPPORTED_SCHEMA_VERSION = 1

ID_SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DOMAIN_ID = re.compile(r"^[A-Z0-9]{2,8}$")
ADR_ID = re.compile(r"^ADR-([A-Z0-9]{2,8})-(\d{3})$")


@dataclass(frozen=True)
class KindInfo:
    kind: str
    model: type[SinterModel]
    prefix: str | None
    canonical_path: Callable[[Any], str]
    calc_fields: tuple[str, ...] = ()
    """Campos `(calc)` do Apêndice A: a CLI calcula, ninguém escreve (AD-4)."""


def _meta_id(item: Any) -> str:
    return str(item.metadata.id)


KINDS: dict[str, KindInfo] = {
    info.kind: info
    for info in (
        KindInfo("Organization", Organization, "org-", lambda _: "organization.yaml", ("domains",)),
        KindInfo("RepositoryList", RepositoryList, None, lambda _: "repositories.yaml"),
        KindInfo("Regulation", Regulation, "reg-", lambda m: f"regulations/{_meta_id(m)}.yaml"),
        KindInfo("Standard", Standard, "std-", lambda m: f"standards/{_meta_id(m)}.yaml"),
        KindInfo(
            "Domain",
            Domain,
            "dom-",
            lambda m: f"domains/{m.metadata.domain_id.lower()}/domain.yaml",
            ("boundaries", "repositories", "journeys", "modernizationOverview", "counts"),
        ),
    )
}

# Itens que vivem DENTRO de um manifesto mas têm id global (AD-41).
CHILD_PREFIXES: dict[str, str] = {
    "Area": "area-",
    "Repository": "repo-",
    "Rule": "rule-",
    "Data": "dat-",
    "Doc": "doc-",
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
}


def prefix_for(kind: str) -> str | None:
    if kind in KINDS:
        return KINDS[kind].prefix
    return CHILD_PREFIXES.get(kind)
