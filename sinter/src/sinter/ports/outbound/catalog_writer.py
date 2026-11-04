"""Porta de escrita de manifestos, injetada só nos casos de uso autorizados (AD-34)."""

from typing import Protocol


class CatalogWriter(Protocol):
    def write_all(self, contents: dict[str, str]) -> None:
        """Grava o lote de manifestos como texto UTF-8."""
        ...
