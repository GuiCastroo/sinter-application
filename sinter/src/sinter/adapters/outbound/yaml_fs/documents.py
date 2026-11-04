"""Leitura segura de Markdown do catálogo, limitada fisicamente a `docs/`."""

from pathlib import Path, PurePosixPath

from sinter.ports.outbound.catalog_document_reader import CatalogDocumentReadError


class FsCatalogDocumentReader:
    def __init__(self, root: Path) -> None:
        self._root = root

    def read_markdown(self, path: str) -> str:
        relative = PurePosixPath(path)
        if (
            relative.is_absolute()
            or ".." in relative.parts
            or "\\" in path
            or relative.suffix.lower() != ".md"
            or "docs" not in relative.parts
        ):
            raise CatalogDocumentReadError(f"caminho não permitido: {path}")

        docs_index = relative.parts.index("docs")
        docs_parts = relative.parts[: docs_index + 1]
        try:
            root = self._root.resolve(strict=True)
            docs_root = root.joinpath(*docs_parts)
            target = root.joinpath(*relative.parts)
            current = root
            for part in relative.parts:
                current = current / part
                if current.is_symlink():
                    raise CatalogDocumentReadError(f"links simbólicos não são permitidos: {path}")
            physical_docs_root = docs_root.resolve(strict=True)
            physical_target = target.resolve(strict=True)
            physical_docs_root.relative_to(root)
            physical_target.relative_to(physical_docs_root)
            if not physical_docs_root.is_dir() or not physical_target.is_file():
                raise CatalogDocumentReadError(f"documento não encontrado: {path}")
            return physical_target.read_text(encoding="utf-8")
        except CatalogDocumentReadError:
            raise
        except (OSError, RuntimeError, ValueError) as exc:
            raise CatalogDocumentReadError(
                f"documento fora da raiz docs permitida: {path}"
            ) from exc
