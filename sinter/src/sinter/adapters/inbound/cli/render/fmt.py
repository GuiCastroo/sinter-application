"""Saída textual do `sinter fmt`."""

from sinter.ports.inbound.fmt import FmtResult


def render(result: FmtResult) -> str:
    lines = [
        f"ERRO  {finding.file}  {finding.message}  [{finding.code}]"
        for finding in result.report.errors
    ]
    lines.append(result.summary)
    return "\n".join(lines)
