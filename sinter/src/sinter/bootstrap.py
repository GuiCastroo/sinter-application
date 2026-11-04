"""Composição: o ÚNICO lugar que instancia adaptadores de saída e casos de uso (AD-27)."""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from sinter.adapters.outbound.local_fs.files import FsLocalFiles
from sinter.adapters.outbound.yaml_fs.codec import RuamelCodec
from sinter.adapters.outbound.yaml_fs.documents import FsCatalogDocumentReader
from sinter.adapters.outbound.yaml_fs.files import FsCatalogFiles, FsCatalogWriter
from sinter.application.fmt import Fmt
from sinter.application.get import Get
from sinter.application.read import Read
from sinter.application.schema_export import SchemaExport
from sinter.application.validate import Validate
from sinter.ports.outbound.catalog_document_reader import CatalogDocumentReader
from sinter.ports.outbound.catalog_files import CatalogFiles
from sinter.ports.outbound.catalog_writer import CatalogWriter
from sinter.ports.outbound.local_files import LocalFiles
from sinter.ports.outbound.manifest_codec import ManifestCodec


def package_version() -> str:
    try:
        return version("sinter")
    except PackageNotFoundError:
        return "0.0.0"


class Container:
    """Os casos de uso prontos para usar. Os que exigem catálogo só existem se houver raiz."""

    def __init__(
        self,
        sinter_version: str,
        files: CatalogFiles | None,
        writer: CatalogWriter | None,
        doc_reader: CatalogDocumentReader | None,
        codec: ManifestCodec,
        local: LocalFiles,
    ) -> None:
        self.sinter_version = sinter_version
        self._files = files
        self._writer = writer
        self._doc_reader = doc_reader
        self._codec = codec
        self.schema_export = SchemaExport(local)

    def _catalog_files(self) -> CatalogFiles:
        if self._files is None:
            raise RuntimeError("este comando precisa de um catálogo (bootstrap sem catalog_root)")
        return self._files

    @property
    def validate(self) -> Validate:
        return Validate(self._catalog_files(), self._codec)

    @property
    def get(self) -> Get:
        return Get(self._catalog_files(), self._codec)

    @property
    def read(self) -> Read:
        if self._doc_reader is None:
            raise RuntimeError("este comando precisa de um leitor de documentos do catálogo")
        return Read(self._catalog_files(), self._doc_reader, self._codec)

    @property
    def fmt(self) -> Fmt:
        if self._writer is None:
            raise RuntimeError("este comando precisa de uma porta de escrita de catálogo")
        return Fmt(self._catalog_files(), self._writer, self._codec)


def build(
    catalog_root: Path | None,
    *,
    sinter_version: str | None = None,
    files: CatalogFiles | None = None,
    writer: CatalogWriter | None = None,
    doc_reader: CatalogDocumentReader | None = None,
    codec: ManifestCodec | None = None,
    local: LocalFiles | None = None,
) -> Container:
    if files is None and catalog_root is not None:
        files = FsCatalogFiles(catalog_root)
    if writer is None and catalog_root is not None:
        writer = FsCatalogWriter(catalog_root)
    if doc_reader is None and catalog_root is not None:
        doc_reader = FsCatalogDocumentReader(catalog_root)
    return Container(
        sinter_version=sinter_version or package_version(),
        files=files,
        writer=writer,
        doc_reader=doc_reader,
        codec=codec or RuamelCodec(),
        local=local or FsLocalFiles(Path.cwd()),
    )
