"""Registro de kinds: o ÚNICO lugar com kind → modelo, prefixo de id e caminho canônico (AD-40)."""

import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from sinter.domain.model.base import SinterModel
from sinter.domain.model.organization import Organization
from sinter.domain.model.regulation import Regulation
from sinter.domain.model.repository_list import RepositoryList
from sinter.domain.model.standard import Standard

SUPPORTED_SCHEMA_VERSION = 1

ID_SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


@dataclass(frozen=True)
class KindInfo:
    kind: str
    model: type[SinterModel]
    prefix: str | None
    canonical_path: Callable[[Any], str]


def _meta_id(item: Any) -> str:
    return str(item.metadata.id)


KINDS: dict[str, KindInfo] = {
    info.kind: info
    for info in (
        KindInfo("Organization", Organization, "org-", lambda _: "organization.yaml"),
        KindInfo("RepositoryList", RepositoryList, None, lambda _: "repositories.yaml"),
        KindInfo("Regulation", Regulation, "reg-", lambda m: f"regulations/{_meta_id(m)}.yaml"),
        KindInfo("Standard", Standard, "std-", lambda m: f"standards/{_meta_id(m)}.yaml"),
    )
}

# Itens que vivem DENTRO de um manifesto mas têm id global (AD-41).
CHILD_PREFIXES: dict[str, str] = {
    "Area": "area-",
    "Repository": "repo-",
}


def prefix_for(kind: str) -> str | None:
    if kind in KINDS:
        return KINDS[kind].prefix
    return CHILD_PREFIXES.get(kind)
