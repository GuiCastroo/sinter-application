"""Finding e o formato único de `path` (AD-35)."""

import re
from collections.abc import Iterable, Mapping, Sequence
from typing import Any, Literal

from pydantic import Field

from sinter.domain.model.base import SinterModel

Severity = Literal["error", "warning"]
ERROR: Severity = "error"
WARNING: Severity = "warning"

Segment = str | int
Positions = Mapping[tuple[Segment, ...], int]


def format_path(data: Any, segments: Sequence[Segment]) -> str:
    """`spec.applications[app-x].lifecycle`: item de lista pelo id (se tiver), senão pelo índice."""
    out = ""
    current = data
    for seg in segments:
        if isinstance(seg, int):
            item = current[seg] if isinstance(current, list) and 0 <= seg < len(current) else None
            ident = item.get("id") if isinstance(item, dict) else None
            out += f"[{ident}]" if isinstance(ident, str) and ident else f"[{seg}]"
            current = item
        else:
            out += f".{seg}" if out else seg
            current = current.get(seg) if isinstance(current, dict) else None
    return out


def line_for(positions: Positions, segments: Sequence[Segment]) -> int | None:
    """Linha (1-based) do trecho mais específico conhecido do caminho."""
    for end in range(len(segments), -1, -1):
        line = positions.get(tuple(segments[:end]))
        if line is not None:
            return line
    return None


class Related(SinterModel):
    file: str
    path: str


class Finding(SinterModel):
    code: str
    severity: Severity
    file: str
    path: str
    message: str
    line: int | None = None
    source: str | None = None
    related: list[Related] = Field(default_factory=list)

    @classmethod
    def at(
        cls,
        *,
        code: str,
        severity: Severity,
        file: str,
        data: Any,
        positions: Positions,
        segments: Sequence[Segment],
        message: str,
        related: Iterable[Related] = (),
    ) -> "Finding":
        return cls(
            code=code,
            severity=severity,
            file=file,
            path=format_path(data, segments),
            line=line_for(positions, segments),
            message=message,
            related=list(related),
        )


_PATH_TOKEN = re.compile(r"\[(\d+)\]|\[([^\]]*)\]|([^.\[\]]+)")


def _path_key(path: str) -> tuple[tuple[int, str, int], ...]:
    key: list[tuple[int, str, int]] = []
    for index, ident, name in _PATH_TOKEN.findall(path):
        if index:
            key.append((1, "", int(index)))
        else:
            key.append((0, ident or name, 0))
    return tuple(key)


def sort_key(f: Finding) -> tuple[Any, ...]:
    """Ordem: file, line, path (índice numérico), code, message (AD-35)."""
    return (f.file, f.line or 0, _path_key(f.path), f.code, f.message)
