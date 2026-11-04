"""Texto do `sinter get`: imprime os fatos do Result, sem montar frase nova (AD-32, AD-45)."""

from sinter.domain.model.views import (
    DomainLevel1,
    Knowledge,
    Level0,
    OperationView,
    SubdomainLevel1,
)
from sinter.ports.inbound.get import GetResult

NOT_FILLED = "(não preenchido)"


def _origin(origin: str, own: str) -> str:
    return "" if origin == own else f"  ← herdado de {origin}"


def _list(title: str, values: list[str]) -> list[str]:
    if not values:
        return [f"{title}: {NOT_FILLED}"]
    return [f"{title}:", *(f"  - {v}" for v in values)]


def _level0(item: Level0) -> list[str]:
    lines = [f"{item.id}  [{item.kind}] {item.name}"]
    if item.status:
        lines.append(f"status: {item.status}")
    if item.purpose:
        lines.append(f"propósito: {item.purpose}")
    if item.counts:
        lines.append("contagens: " + ", ".join(f"{key}={n}" for key, n in item.counts.items()))
    return lines


def _operation(op: OperationView | None, own: str) -> list[str]:
    if op is None:
        return []
    v = op.value
    parts = [
        f"horário: {v.hours}" if v.hours else "",
        f"janelas: {', '.join(v.batch_windows)}" if v.batch_windows else "",
        f"criticidade: {v.criticality}" if v.criticality else "",
        f"volume: {v.volume}" if v.volume else "",
    ]
    tail = _origin(op.origin, own)
    if op.inherited_fields:
        tail = f"  ← herdado de {op.inherited_from}: {', '.join(op.inherited_fields)}"
    return [f"operação: {' · '.join(p for p in parts if p)}{tail}"]


def _knowledge(k: Knowledge, own: str) -> list[str]:
    lines: list[str] = []
    if k.rules:
        lines.append("regras:")
        lines += [f"  - {r.id}: {r.statement}{_origin(r.origin, own)}" for r in k.rules]
    for title, refs in (("regulações", k.regulations), ("padrões", k.standards)):
        if refs:
            lines.append(f"{title}:")
            lines += [f"  - {r.id}{_origin(r.origin, own)}" for r in refs]
    if k.decisions:
        lines.append("decisões:")
        lines += [
            f"  - {d.id} {d.title} ({d.date}): {d.decision}{_origin(d.origin, own)}"
            for d in k.decisions
        ]
    if k.glossary:
        lines.append("glossário:")
        lines += [f"  - {t.term}: {t.definition}{_origin(t.origin, own)}" for t in k.glossary]
    if k.docs:
        lines.append("docs:")
        lines += [
            f"  - [{d.type}] {d.title} → {d.path or d.url}{_origin(d.origin, own)}" for d in k.docs
        ]
    return lines


def _common(item: DomainLevel1 | SubdomainLevel1) -> list[str]:
    return [
        *_list("faz", item.does),
        *_list("não faz", item.does_not),
        *_list("não sabemos", item.unknowns),
    ]


def render(result: GetResult) -> str:
    item = result.item
    lines = [result.summary]
    if not isinstance(item, DomainLevel1 | SubdomainLevel1):
        lines += _level0(item)
    elif isinstance(item, DomainLevel1):
        own = item.level0.id
        lines += _level0(item.level0) + _common(item)
        lines.append("subdomínios:")
        for s in item.subdomains:
            lines += [f"  - {line}" for line in _level0(s)]
        if item.main_journeys:
            lines.append(f"jornadas principais: {', '.join(item.main_journeys)}")
        lines += _operation(item.operation, own)
        if item.modernization:
            lines.append(f"modernização: {item.modernization.goal}")
            if item.modernization.decision:
                lines.append(f"decisão: {item.modernization.decision}")
        lines += _knowledge(item.knowledge, own)
    else:
        own = item.level0.id
        lines += _level0(item.level0) + _common(item)
        if item.applications:
            lines.append("aplicações:")
            lines += [f"  - {a.id} ({a.lifecycle}) {a.name}" for a in item.applications]
        lines += _operation(item.operation, own)
        if item.modernization:
            lines.append(f"modernização: {item.modernization.goal}")
            if item.modernization.decision:
                lines.append(f"decisão: {item.modernization.decision}")
        lines += _knowledge(item.knowledge, own)
    lines += [f"(omitido: {o.what} → {o.command})" for o in result.omitted]
    lines += [f"{f.code}: {f.file} {f.path}: {f.message}" for f in result.report.errors]
    lines += [f"{f.code}: {f.file} {f.path}: {f.message}" for f in result.report.warnings]
    return "\n".join(lines)
