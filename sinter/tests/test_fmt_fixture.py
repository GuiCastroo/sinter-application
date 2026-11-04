import shutil
from pathlib import Path

from sinter.adapters.outbound.yaml_fs.codec import RuamelCodec
from sinter.adapters.outbound.yaml_fs.files import FsCatalogFiles, FsCatalogWriter

EXAMPLE = Path(__file__).parent / "fixtures" / "exemplo-catalogo"


def test_format_e_idempotente_para_todos_os_manifestos_do_exemplo(tmp_path: Path) -> None:
    root = tmp_path / "catalog"
    shutil.copytree(EXAMPLE, root)
    files = FsCatalogFiles(root)
    codec = RuamelCodec()
    original = {path: codec.split(files.read(path))[0].data for path in files.list_manifests()}

    formatted = {path: codec.format(files.read(path)) for path in files.list_manifests()}
    FsCatalogWriter(root).write_all(formatted)

    for path in files.list_manifests():
        text = files.read(path)
        assert codec.format(text) == text
        assert codec.split(text)[0].data == original[path]
