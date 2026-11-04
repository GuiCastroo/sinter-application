"""Leitura restrita de documentos Markdown locais do catálogo."""

from typing import Protocol


class CatalogDocumentReadError(Exception):
    pass


class CatalogDocumentReader(Protocol):
    def read_markdown(self, path: str) -> str:
        """Lê um arquivo Markdown dentro de `docs/`, sem seguir links para fora."""
        ...
