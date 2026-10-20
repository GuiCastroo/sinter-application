"""Composição: o ÚNICO lugar que instancia adaptadores de saída e casos de uso (AD-27)."""

from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from sinter.adapters.outbound.yaml_fs.codec import RuamelCodec
from sinter.adapters.outbound.yaml_fs.files import FsCatalogFiles
from sinter.application.validate import Validate
from sinter.ports.outbound.catalog_files import CatalogFiles
from sinter.ports.outbound.manifest_codec import ManifestCodec


def package_version() -> str:
    try:
        return version("sinter")
    except PackageNotFoundError:
        return "0.0.0"


@dataclass(frozen=True)
class Container:
    sinter_version: str
    validate: Validate


def build(
    catalog_root: Path | None,
    *,
    sinter_version: str | None = None,
    files: CatalogFiles | None = None,
    codec: ManifestCodec | None = None,
) -> Container:
    if files is None:
        if catalog_root is None:
            raise ValueError("catalog_root ou files é obrigatório")
        files = FsCatalogFiles(catalog_root)
    codec = codec or RuamelCodec()
    return Container(
        sinter_version=sinter_version or package_version(),
        validate=Validate(files, codec),
    )
