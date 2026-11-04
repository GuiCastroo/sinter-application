"""Contrato do `sinter read`."""

from pydantic import Field

from sinter.domain.model.base import SinterModel


class ReadRequest(SinterModel):
    target: str


class ReadHeading(SinterModel):
    title: str
    anchor: str
    level: int
    size_lines: int


class ReadResult(SinterModel):
    source: str
    locator: str
    content: str | None = None
    headings: list[ReadHeading] = Field(default_factory=list)
    warning: str | None = None
