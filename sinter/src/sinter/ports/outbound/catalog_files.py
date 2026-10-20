"""Leitura dos arquivos do catálogo, presa à raiz (AD-28).

A escrita fica em catalog_writer (Epic 3).
"""

from typing import Protocol


class CatalogFiles(Protocol):
    def list_manifests(self) -> list[str]:
        """Caminhos POSIX relativos à raiz, ordenados, dos manifestos YAML (fora de `docs/`)."""
        ...

    def read(self, path: str) -> str: ...

    def exists(self, path: str) -> bool: ...
