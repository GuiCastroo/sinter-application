"""Texto do `sinter validate`."""

from sinter.domain.validation.finding import Finding
from sinter.ports.inbound.validate import ValidateResult

_LABEL = {"error": "ERRO ", "warning": "AVISO"}


def _line(f: Finding) -> str:
    where = f"{f.file}:{f.line}" if f.line else f.file
    path = f"  {f.path}" if f.path else ""
    return f"{_LABEL[f.severity]}  {where}{path}  {f.message}  [{f.code}]"


def render(result: ValidateResult) -> str:
    lines = [_line(f) for f in (*result.report.errors, *result.report.warnings)]
    lines.append(result.summary)
    return "\n".join(lines)
