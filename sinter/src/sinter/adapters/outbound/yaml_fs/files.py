"""CatalogFiles no disco."""

from pathlib import Path

_MANIFEST_SUFFIXES = {".yaml", ".yml"}
_SKIPPED_DIRS = {"docs"}


class FsCatalogFiles:
    def __init__(self, root: Path) -> None:
        self._root = root

    def list_manifests(self) -> list[str]:
        found: list[str] = []
        for path in self._root.rglob("*"):
            rel = path.relative_to(self._root)
            if any(p.startswith(".") or p in _SKIPPED_DIRS for p in rel.parts[:-1]):
                continue
            if (
                path.is_file()
                and path.suffix in _MANIFEST_SUFFIXES
                and not path.name.startswith(".")
            ):
                found.append(rel.as_posix())
        return sorted(found)

    def read(self, path: str) -> str:
        return (self._root / path).read_text(encoding="utf-8")

    def exists(self, path: str) -> bool:
        return (self._root / path).exists()
