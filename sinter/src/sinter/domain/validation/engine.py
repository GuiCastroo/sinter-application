"""Fase 2 da validação: registro de regras puras com código estável (AD-31)."""

import importlib
import pkgutil
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field

from sinter.domain.model.catalog import Catalog, Entry, ParsedManifest
from sinter.domain.validation.finding import (
    Finding,
    Related,
    Segment,
    Severity,
    format_path,
    line_for,
)


@dataclass(frozen=True)
class FileFacts:
    """Fatos de arquivo calculados pela aplicação, iguais no `validate` e no `apply`."""

    formatted: Mapping[str, bool] = field(default_factory=dict)


@dataclass(frozen=True)
class Problem:
    """O que uma regra encontra; o motor carimba o código e a severidade da regra."""

    file: str
    path: str
    line: int | None
    message: str
    related: tuple[Related, ...] = ()


def problem(
    m: ParsedManifest, *segments: Segment, message: str, related: Iterable[Related] = ()
) -> Problem:
    return Problem(
        file=m.file,
        path=format_path(m.data, segments),
        line=line_for(m.positions, segments),
        message=message,
        related=tuple(related),
    )


def problem_at(entry: Entry, *, message: str, related: Iterable[Related] = ()) -> Problem:
    return Problem(
        file=entry.file,
        path=entry.path,
        line=entry.line,
        message=message,
        related=tuple(related),
    )


RuleFn = Callable[[Catalog, FileFacts], Iterable[Problem]]


@dataclass(frozen=True)
class RegisteredRule:
    code: str
    severity: Severity
    fn: RuleFn


_RULES: dict[str, RegisteredRule] = {}


def rule(*, code: str, severity: Severity) -> Callable[[RuleFn], RuleFn]:
    def register(fn: RuleFn) -> RuleFn:
        if code in _RULES:
            raise ValueError(f"código de regra repetido: {code}")
        _RULES[code] = RegisteredRule(code=code, severity=severity, fn=fn)
        return fn

    return register


def _load_rules() -> None:
    from sinter.domain.validation import rules

    for info in pkgutil.iter_modules(rules.__path__):
        importlib.import_module(f"{rules.__name__}.{info.name}")


def registered_rules() -> list[RegisteredRule]:
    _load_rules()
    return [_RULES[code] for code in sorted(_RULES)]


def validate_catalog(catalog: Catalog, facts: FileFacts | None = None) -> list[Finding]:
    facts = facts or FileFacts()
    findings: list[Finding] = []
    for r in registered_rules():
        for p in r.fn(catalog, facts):
            findings.append(
                Finding(
                    code=r.code,
                    severity=r.severity,
                    file=p.file,
                    path=p.path,
                    line=p.line,
                    message=p.message,
                    related=list(p.related),
                )
            )
    return findings
