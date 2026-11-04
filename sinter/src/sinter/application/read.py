"""Leitura segura de documentos Markdown associados ao catálogo."""

from pathlib import PurePosixPath

from sinter.application.load import load
from sinter.domain.errors import SinterError
from sinter.domain.services.markdown import index_markdown, section_content
from sinter.domain.services.references import documents, resolve_doc_path
from sinter.ports.inbound.read import ReadHeading, ReadRequest, ReadResult
from sinter.ports.outbound.catalog_document_reader import (
    CatalogDocumentReader,
    CatalogDocumentReadError,
)
from sinter.ports.outbound.catalog_files import CatalogFiles
from sinter.ports.outbound.manifest_codec import ManifestCodec


class Read:
    def __init__(
        self, files: CatalogFiles, doc_reader: CatalogDocumentReader, codec: ManifestCodec
    ) -> None:
        self._files = files
        self._doc_reader = doc_reader
        self._codec = codec

    def __call__(self, request: ReadRequest) -> ReadResult:
        catalog, _ = load(self._files, self._codec)
        target, _, anchor = request.target.partition("#")
        docs = list(documents(catalog))
        found = next((d for d in docs if d.doc.id == target), None)
        if found is None:
            for item in docs:
                canonical = resolve_doc_path(item.manifest.file, item.doc.path or "")
                if item.doc.path and target in {item.doc.path, canonical}:
                    found = item
                    break
        if found is None:
            raise SinterError(
                "ITEM_NOT_FOUND", f"'{target}' não é um documento do catálogo", {"target": target}
            )
        doc = found.doc
        if doc.ref:
            found = next((d for d in docs if d.doc.id == doc.ref), None)
            if found is None:
                raise SinterError(
                    "ITEM_NOT_FOUND", f"referência de documento '{doc.ref}' não encontrada"
                )
            doc = found.doc
        if not doc.path:
            if doc.url:
                return ReadResult(
                    source="url",
                    locator=doc.url,
                    warning="Sinter não lê conteúdo externo; abra a URL manualmente.",
                )
            raise SinterError("ITEM_NOT_FOUND", f"documento '{target}' não possui path ou URL")
        rel = resolve_doc_path(found.manifest.file, doc.path)
        path = PurePosixPath(rel)
        unsafe = (
            path.is_absolute()
            or ".." in path.parts
            or "\\" in rel
            or "docs" not in path.parts
            or path.suffix.lower() != ".md"
        )
        if unsafe:
            raise SinterError(
                "ITEM_NOT_FOUND", f"caminho de documento fora de docs/ ou não Markdown: '{rel}'"
            )
        if not self._files.exists(rel):
            raise SinterError("ITEM_NOT_FOUND", f"arquivo não encontrado: '{rel}'")
        try:
            source = self._doc_reader.read_markdown(rel)
        except CatalogDocumentReadError as exc:
            raise SinterError("ITEM_NOT_FOUND", str(exc), {"path": rel}) from exc
        index = index_markdown(source)
        headings = [ReadHeading(**h.__dict__) for h in index.headings]
        if not anchor:
            return ReadResult(source="catalog", locator=rel, headings=headings)
        content = section_content(source, index, anchor)
        if content is None:
            available = [h.anchor for h in headings]
            raise SinterError(
                "ANCHOR_NOT_FOUND",
                f"anchor '{anchor}' não encontrado. Disponíveis: {', '.join(available)}",
                {"anchor": anchor, "available": available},
            )
        return ReadResult(source="catalog", locator=rel, content=content, headings=headings)
