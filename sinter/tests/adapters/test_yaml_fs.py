import datetime as dt
from pathlib import Path

import pytest

from sinter.adapters.outbound.yaml_fs.codec import RuamelCodec
from sinter.adapters.outbound.yaml_fs.files import FsCatalogFiles
from sinter.ports.outbound.manifest_codec import ManifestSyntaxError

TEXT = """# comentário
apiVersion: sinter.dev/v1
kind: Regulation
metadata:
  id: reg-x
spec:
  effective: { from: 2022-12-30, to: null }
  docs:
    - { title: T, type: link }
"""


def test_split_devolve_tipos_padrao_e_linhas() -> None:
    [doc] = RuamelCodec().split(TEXT)
    assert type(doc.data) is dict
    assert doc.data["spec"]["effective"]["from"] == dt.date(2022, 12, 30)
    assert type(doc.data["spec"]["docs"]) is list
    assert doc.positions[("metadata", "id")] == 5
    assert doc.positions[("spec", "docs", 0)] == 9


def test_split_varios_documentos() -> None:
    assert len(RuamelCodec().split("a: 1\n---\nb: 2\n")) == 2


def test_yaml_invalido_tem_linha() -> None:
    with pytest.raises(ManifestSyntaxError) as exc:
        RuamelCodec().split("a: 1\nb: [1, 2\nc: 3\n")
    assert exc.value.line is not None


def test_chave_repetida_e_erro_de_sintaxe() -> None:
    with pytest.raises(ManifestSyntaxError):
        RuamelCodec().split("a: 1\na: 2\n")


def test_lista_manifestos_ignora_docs_e_ocultos(tmp_path: Path) -> None:
    for rel in (
        "organization.yaml",
        "domains/x/domain.yaml",
        "domains/x/docs/a.yaml",
        ".git/c.yaml",
    ):
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("a: 1\n")
    (tmp_path / "notas.md").write_text("x")
    assert FsCatalogFiles(tmp_path).list_manifests() == [
        "domains/x/domain.yaml",
        "organization.yaml",
    ]
