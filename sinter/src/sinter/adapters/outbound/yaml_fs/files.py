"""CatalogFiles no disco."""

import os
import tempfile
from pathlib import Path, PurePosixPath

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
        with (self._root / path).open(encoding="utf-8", newline="") as stream:
            return stream.read()

    def exists(self, path: str) -> bool:
        return (self._root / path).exists()


class FsCatalogWriter:
    def __init__(self, root: Path) -> None:
        self._root = root

    def write_all(self, contents: dict[str, str]) -> None:
        """Grava os manifestos em temporários no mesmo volume e restaura em falha."""
        staged: dict[Path, Path] = {}
        originals: dict[Path, bytes | None] = {}
        replaced: list[Path] = []
        try:
            for relative, text in contents.items():
                rel = PurePosixPath(relative)
                if rel.is_absolute() or ".." in rel.parts or "\\" in relative:
                    raise ValueError(f"caminho de manifesto inválido: {relative}")
                target = (self._root / Path(*rel.parts)).resolve()
                target.relative_to(self._root.resolve())
                target.parent.mkdir(parents=True, exist_ok=True)
                originals[target] = target.read_bytes() if target.exists() else None
                fd, name = tempfile.mkstemp(
                    prefix=f".{target.name}.", suffix=".tmp", dir=target.parent
                )
                temp = Path(name)
                staged[target] = temp
                with os.fdopen(fd, "wb") as stream:
                    stream.write(text.encode("utf-8"))

            for target, temp in staged.items():
                os.replace(temp, target)
                replaced.append(target)
        except BaseException:
            for target in reversed(replaced):
                previous = originals[target]
                if previous is None:
                    target.unlink(missing_ok=True)
                else:
                    fd, name = tempfile.mkstemp(
                        prefix=f".{target.name}.rollback.", suffix=".tmp", dir=target.parent
                    )
                    with os.fdopen(fd, "wb") as stream:
                        stream.write(previous)
                    os.replace(name, target)
            raise
        finally:
            for temp in staged.values():
                temp.unlink(missing_ok=True)
