"""Composição: o ÚNICO lugar que instancia adaptadores de saída e casos de uso (AD-27)."""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from sinter.adapters.outbound.local_fs.files import FsLocalFiles
from sinter.adapters.outbound.yaml_fs.codec import RuamelCodec
from sinter.adapters.outbound.yaml_fs.files import FsCatalogFiles
from sinter.application.schema_export import SchemaExport
from sinter.application.validate import Validate
from sinter.ports.outbound.catalog_files import CatalogFiles
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
        codec: ManifestCodec,
        local: LocalFiles,
    ) -> None:
        self.sinter_version = sinter_version
        self._files = files
        self._codec = codec
        self.schema_export = SchemaExport(local)

    @property
    def validate(self) -> Validate:
        if self._files is None:
            raise RuntimeError("este comando precisa de um catálogo (bootstrap sem catalog_root)")
        return Validate(self._files, self._codec)


def build(
    catalog_root: Path | None,
    *,
    sinter_version: str | None = None,
    files: CatalogFiles | None = None,
    codec: ManifestCodec | None = None,
    local: LocalFiles | None = None,
) -> Container:
    if files is None and catalog_root is not None:
        files = FsCatalogFiles(catalog_root)
    return Container(
        sinter_version=sinter_version or package_version(),
        files=files,
        codec=codec or RuamelCodec(),
        local=local or FsLocalFiles(Path.cwd()),
    )
