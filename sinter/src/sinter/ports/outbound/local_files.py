"""Arquivos FORA do catálogo (AD-36): só schema_export e skills_install usam."""

from typing import Protocol


class LocalFiles(Protocol):
    def read(self, path: str) -> str | None:
        """Conteúdo do arquivo, ou None se não existe."""
        ...

    def write(self, path: str, text: str) -> None:
        """Grava criando as pastas que faltam."""
        ...
