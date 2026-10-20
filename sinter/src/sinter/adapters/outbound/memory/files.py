"""CatalogFiles em memória, para testes da aplicação."""

from collections.abc import Mapping

_MANIFEST_SUFFIXES = (".yaml", ".yml")


class MemoryCatalogFiles:
    def __init__(self, files: Mapping[str, str]) -> None:
        self._files = dict(files)

    def list_manifests(self) -> list[str]:
        return sorted(
            p
            for p in self._files
            if p.endswith(_MANIFEST_SUFFIXES) and "docs" not in p.split("/")[:-1]
        )

    def read(self, path: str) -> str:
        return self._files[path]

    def exists(self, path: str) -> bool:
        return path in self._files or any(p.startswith(f"{path}/") for p in self._files)
