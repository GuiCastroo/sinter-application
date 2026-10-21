"""LocalFiles no disco, relativo a uma pasta base (o diretório atual na CLI)."""

from pathlib import Path


class FsLocalFiles:
    def __init__(self, base: Path) -> None:
        self._base = base

    def read(self, path: str) -> str | None:
        full = self._base / path
        return full.read_text(encoding="utf-8") if full.is_file() else None

    def write(self, path: str, text: str) -> None:
        full = self._base / path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(text, encoding="utf-8", newline="\n")
