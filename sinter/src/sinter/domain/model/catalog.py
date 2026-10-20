"""O catálogo carregado: imutável, indexado por id (AD-29, AD-41)."""

from collections.abc import Iterator, Mapping
from dataclasses import dataclass, field
from typing import Any

from sinter.domain.model.base import SinterModel
from sinter.domain.model.organization import Organization
from sinter.domain.validation.finding import Positions, format_path, line_for


@dataclass(frozen=True)
class ParsedManifest:
    """Um arquivo do catálogo depois de lido: dados brutos + modelo (se passou no schema)."""

    file: str
    data: Any
    positions: Positions = field(default_factory=dict)
    kind: str | None = None
    model: SinterModel | None = None

    @property
    def valid(self) -> bool:
        return self.model is not None

    @property
    def id(self) -> str | None:
        meta = self.data.get("metadata") if isinstance(self.data, dict) else None
        ident = meta.get("id") if isinstance(meta, dict) else None
        return ident if isinstance(ident, str) else None


@dataclass(frozen=True)
class Entry:
    id: str
    kind: str
    file: str
    path: str
    line: int | None
    valid: bool


@dataclass(frozen=True)
class Catalog:
    manifests: tuple[ParsedManifest, ...]
    entries: tuple[Entry, ...]

    def valid_manifests(self, kind: str | None = None) -> Iterator[ParsedManifest]:
        for m in self.manifests:
            if m.valid and (kind is None or m.kind == kind):
                yield m

    def find(self, ident: str, kind: str | None = None) -> list[Entry]:
        return [e for e in self.entries if e.id == ident and (kind is None or e.kind == kind)]

    def organization(self) -> Organization | None:
        for m in self.valid_manifests("Organization"):
            if isinstance(m.model, Organization):
                return m.model
        return None


_CHILD_LISTS: Mapping[str, tuple[str, str]] = {
    "Organization": ("areas", "Area"),
    "RepositoryList": ("repositories", "Repository"),
}


def _child_entries(m: ParsedManifest) -> Iterator[Entry]:
    if m.kind is None or m.kind not in _CHILD_LISTS:
        return
    list_name, child_kind = _CHILD_LISTS[m.kind]
    spec = m.data.get("spec") if isinstance(m.data, dict) else None
    items = spec.get(list_name) if isinstance(spec, dict) else None
    if not isinstance(items, list):
        return
    for i, item in enumerate(items):
        ident = item.get("id") if isinstance(item, dict) else None
        if isinstance(ident, str):
            segments = ("spec", list_name, i)
            yield Entry(
                id=ident,
                kind=child_kind,
                file=m.file,
                path=format_path(m.data, segments),
                line=line_for(m.positions, segments),
                valid=m.valid,
            )


def build_catalog(manifests: list[ParsedManifest]) -> Catalog:
    ordered = tuple(sorted(manifests, key=lambda m: m.file))
    entries: list[Entry] = []
    for m in ordered:
        if m.id is not None:
            entries.append(
                Entry(
                    id=m.id,
                    kind=m.kind or "?",
                    file=m.file,
                    path="metadata.id",
                    line=line_for(m.positions, ("metadata", "id")),
                    valid=m.valid,
                )
            )
        entries.extend(_child_entries(m))
    return Catalog(manifests=ordered, entries=tuple(entries))
