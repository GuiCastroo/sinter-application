"""Índice de headings e extração de seções Markdown, sem I/O."""

from dataclasses import dataclass

from sinter.domain.services.text import gh_anchor


@dataclass(frozen=True)
class Heading:
    title: str
    anchor: str
    level: int
    size_lines: int


@dataclass(frozen=True)
class MarkdownIndex:
    headings: tuple[Heading, ...]
    sections: tuple[tuple[int, int, int], ...]


def index_markdown(source: str) -> MarkdownIndex:
    lines = source.splitlines()
    raw: list[tuple[int, int, str]] = []
    fence: tuple[str, int] | None = None
    for i, line in enumerate(lines):
        stripped = line.lstrip(" ")
        if fence is not None:
            marker = _fence_marker(line)
            if (
                marker is not None
                and marker[0] == fence[0]
                and marker[1] >= fence[1]
                and not marker[2].strip()
            ):
                fence = None
            continue
        marker = _fence_marker(line)
        if marker is not None:
            fence = (marker[0], marker[1])
            continue
        spaces = len(line) - len(stripped)
        if spaces > 3 or not stripped.startswith("#"):
            continue
        n = len(stripped) - len(stripped.lstrip("#"))
        if not 1 <= n <= 6 or len(stripped) > n and stripped[n] not in " \t":
            continue
        title = stripped[n:].strip()
        closing_hashes = len(title) - len(title.rstrip("#"))
        if closing_hashes and title[:-closing_hashes].endswith((" ", "\t")):
            title = title[:-closing_hashes].rstrip()
        raw.append((i, n, title))
    used: set[str] = set()
    anchors: list[str] = []
    for _, _, title in raw:
        base = gh_anchor(title) or "section"
        anchor = base
        suffix = 0
        while anchor in used:
            suffix += 1
            anchor = f"{base}-{suffix}"
        used.add(anchor)
        anchors.append(anchor)
    section_spans: list[tuple[int, int, int]] = []
    headings: list[Heading] = []
    for j, (start, level, title) in enumerate(raw):
        end = len(lines)
        for next_start, next_level, _ in raw[j + 1 :]:
            if next_level <= level:
                end = next_start
                break
        section_spans.append((start, end, level))
        headings.append(Heading(title, anchors[j], level, max(0, end - start)))
    return MarkdownIndex(tuple(headings), tuple(section_spans))


def _fence_marker(line: str) -> tuple[str, int, str] | None:
    stripped = line.lstrip(" ")
    if len(line) - len(stripped) > 3 or not stripped or stripped[0] not in "`~":
        return None
    char = stripped[0]
    length = len(stripped) - len(stripped.lstrip(char))
    if length < 3:
        return None
    return char, length, stripped[length:]


def section_content(source: str, index: MarkdownIndex, anchor: str) -> str | None:
    for heading, (start, end, _) in zip(index.headings, index.sections, strict=True):
        if heading.anchor == anchor:
            return "\n".join(source.splitlines()[start:end]).rstrip()
    return None
