"""Onde cada manifesto cita outros itens: o mapa que as regras de referência percorrem."""

from collections.abc import Iterable, Iterator
from dataclasses import dataclass

from sinter.domain.model.blocks import DataAsset, Decision, Doc, Evidence, Rule
from sinter.domain.model.catalog import Catalog, ParsedManifest
from sinter.domain.model.domain import Domain
from sinter.domain.model.journey import Journey
from sinter.domain.model.regulation import Regulation
from sinter.domain.model.relation import Relation
from sinter.domain.model.standard import Standard
from sinter.domain.model.subdomain import Subdomain
from sinter.domain.validation.finding import Segment

Path = tuple[Segment, ...]

# Prefixo → kind do índice, para referências que aceitam vários tipos (evidência).
KIND_BY_PREFIX: dict[str, str] = {
    "doc-": "Doc",
    "repo-": "Repository",
    "sub-": "Subdomain",
    "app-": "Application",
    "dom-": "Domain",
    "jor-": "Journey",
    "reg-": "Regulation",
    "std-": "Standard",
    "rule-": "Rule",
    "dat-": "Data",
    "ADR-": "Decision",
}


@dataclass(frozen=True)
class Ref:
    """Referência que tem de existir no catálogo, a um dos `kinds`."""

    manifest: ParsedManifest
    path: Path
    value: str
    kinds: tuple[str, ...]


@dataclass(frozen=True)
class OpenRef:
    """Referência que pode ser sub- (tem de existir), dom- (aviso se faltar) ou ext- (formato)."""

    manifest: ParsedManifest
    path: Path
    value: str


@dataclass(frozen=True)
class DocAt:
    manifest: ParsedManifest
    path: Path
    doc: Doc


def _evidence(m: ParsedManifest, base: Path, items: list[Evidence]) -> Iterator[Ref]:
    for i, ev in enumerate(items):
        for prefix, kind in KIND_BY_PREFIX.items():
            if ev.source.startswith(prefix):
                yield Ref(m, (*base, i, "source"), ev.source, (kind,))
                break


def _rules(m: ParsedManifest, rules: list[Rule]) -> Iterator[Ref]:
    for i, r in enumerate(rules):
        for j, reg in enumerate(r.regulations):
            yield Ref(m, ("spec", "rules", i, "regulations", j), reg, ("Regulation",))
        yield from _evidence(m, ("spec", "rules", i, "evidence"), r.evidence)


def _decisions(m: ParsedManifest, decisions: list[Decision]) -> Iterator[Ref]:
    for i, d in enumerate(decisions):
        if d.supersedes is not None:
            yield Ref(m, ("spec", "decisions", i, "supersedes"), d.supersedes, ("Decision",))
        yield from _evidence(m, ("spec", "decisions", i, "evidence"), d.evidence)


def _knowledge(m: ParsedManifest, regulations: list[str], standards: list[str]) -> Iterator[Ref]:
    for i, reg in enumerate(regulations):
        yield Ref(m, ("spec", "regulations", i), reg, ("Regulation",))
    for i, std in enumerate(standards):
        yield Ref(m, ("spec", "standards", i), std, ("Standard",))


def _level(m: ParsedManifest, spec: Domain | Subdomain) -> Iterator[Ref]:
    s = spec.spec
    yield from _knowledge(m, s.regulations, s.standards)
    yield from _rules(m, s.rules)
    yield from _decisions(m, s.decisions)
    if s.modernization is not None and s.modernization.decision is not None:
        yield Ref(m, ("spec", "modernization", "decision"), s.modernization.decision, ("Decision",))


def references(catalog: Catalog) -> Iterator[Ref]:
    for m in catalog.valid_manifests():
        model = m.model
        if isinstance(model, Domain):
            yield from _level(m, model)
            for i, repo in enumerate(model.spec.shared_repositories):
                yield Ref(m, ("spec", "sharedRepositories", i), repo, ("Repository",))
            for i, jor in enumerate(model.spec.main_journeys):
                yield Ref(m, ("spec", "mainJourneys", i), jor, ("Journey",))
        elif isinstance(model, Subdomain):
            yield from _level(m, model)
        elif isinstance(model, Journey):
            yield from _knowledge(m, model.spec.regulations, model.spec.standards)
            yield from _decisions(m, model.spec.decisions)
        elif isinstance(model, Relation):
            yield from _evidence(m, ("spec", "evidence"), model.spec.evidence)


def _data_open_refs(m: ParsedManifest, data: list[DataAsset]) -> Iterator[OpenRef]:
    for i, asset in enumerate(data):
        for layer, info in asset.layers.items():
            for j, consumer in enumerate(info.consumers):
                yield OpenRef(m, ("spec", "data", i, "layers", layer, "consumers", j), consumer)


def open_references(catalog: Catalog) -> Iterator[OpenRef]:
    for m in catalog.valid_manifests():
        model = m.model
        if isinstance(model, Domain):
            yield from _data_open_refs(m, model.spec.data)
        elif isinstance(model, Subdomain):
            yield from _data_open_refs(m, model.spec.data)
            b = model.spec.boundaries
            if b is not None:
                for i, edge_in in enumerate(b.in_):
                    yield OpenRef(m, ("spec", "boundaries", "in", i, "from"), edge_in.from_)
                for i, edge_out in enumerate(b.out):
                    yield OpenRef(m, ("spec", "boundaries", "out", i, "to"), edge_out.to)
        elif isinstance(model, Journey):
            for si, stage in enumerate(model.spec.stages):
                for pi, step in enumerate(stage.steps):
                    if step.calls is not None and step.calls.startswith("dom-"):
                        path: Path = ("spec", "stages", si, "steps", pi, "calls")
                        yield OpenRef(m, path, step.calls)


def _doc_list(m: ParsedManifest, base: Path, docs: Iterable[Doc]) -> Iterator[DocAt]:
    for i, doc in enumerate(docs):
        yield DocAt(m, (*base, i), doc)


def documents(catalog: Catalog) -> Iterator[DocAt]:
    """Todo doc ligado a um nível, aplicação, repo de aplicação ou dado."""
    for m in catalog.valid_manifests():
        model = m.model
        if isinstance(model, Domain | Subdomain | Journey | Regulation | Standard):
            yield from _doc_list(m, ("spec", "docs"), model.spec.docs)
        if isinstance(model, Domain | Subdomain):
            for i, asset in enumerate(model.spec.data):
                yield from _doc_list(m, ("spec", "data", i, "docs"), asset.docs)
        if isinstance(model, Subdomain):
            for i, app in enumerate(model.spec.applications):
                yield from _doc_list(m, ("spec", "applications", i, "docs"), app.docs)
                for j, use in enumerate(app.repositories):
                    base: Path = ("spec", "applications", i, "repositories", j, "docs")
                    yield from _doc_list(m, base, use.docs)


def resolve_doc_path(manifest_file: str, path: str) -> str:
    """O `path` de um doc é relativo à pasta do domínio (ou à raiz, fora de domains/)."""
    parts = manifest_file.split("/")
    if len(parts) >= 2 and parts[0] == "domains":
        return f"domains/{parts[1]}/{path}"
    return path
