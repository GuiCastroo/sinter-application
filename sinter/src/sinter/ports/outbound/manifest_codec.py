"""Texto YAML ↔ dados, sem vazar tipos do ruamel (AD-28). `format` e `edit` chegam no Epic 3."""

from dataclasses import dataclass, field
from typing import Any, Protocol

from sinter.domain.validation.finding import Positions


@dataclass(frozen=True)
class ManifestText:
    """Um documento YAML: dados como tipos da biblioteca padrão e a linha de cada trecho."""

    index: int
    data: Any
    positions: Positions = field(default_factory=dict)


class ManifestSyntaxError(Exception):
    def __init__(self, message: str, line: int | None) -> None:
        super().__init__(message)
        self.message = message
        self.line = line


class ManifestCodec(Protocol):
    def split(self, text: str) -> list[ManifestText]:
        """Separa os documentos; levanta ManifestSyntaxError se o YAML for inválido."""
        ...
