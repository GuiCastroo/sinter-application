import datetime as dt
from pathlib import Path

import pytest

from sinter.adapters.outbound.yaml_fs.codec import RuamelCodec
from sinter.adapters.outbound.yaml_fs.files import FsCatalogFiles, FsCatalogWriter
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


def test_format_ordena_envelope_modelos_e_preserva_comentarios() -> None:
    text = """spec:
  areas:
    - name: Varejo
      # comentário do valor do nome
      id: area-varejo
      description: Área de vendas
  schemaVersion: 1
kind: Organization
metadata:
  status: approved
  name: ACME
  id: org-acme
apiVersion: sinter.dev/v1
"""

    formatted = RuamelCodec().format(text)

    envelope = [line for line in formatted.splitlines() if ":" in line and not line.startswith(" ")]
    assert envelope == [
        "apiVersion: sinter.dev/v1",
        "kind: Organization",
        "metadata:",
        "spec:",
    ]
    assert formatted.index("  id: org-acme") < formatted.index("  name: ACME")
    assert formatted.index("  schemaVersion: 1") < formatted.index("  areas:")
    assert "    - id: area-varejo" in formatted
    assert formatted.index("      name: Varejo") > formatted.index("    - id: area-varejo")
    comment_block = "\n".join(
        [
            "      name: Varejo",
            "      # comentário do valor do nome",
            "      description:",
        ]
    )
    assert comment_block in formatted


def test_format_invalido_so_reordena_envelope() -> None:
    text = """spec:
  z: 1
  a: 2
kind: Organization
metadata: {}
apiVersion: sinter.dev/v1
"""

    formatted = RuamelCodec().format(text)

    assert formatted.index("apiVersion:") < formatted.index("kind:")
    assert formatted.index("kind:") < formatted.index("metadata:")
    assert formatted.index("metadata:") < formatted.index("spec:")
    assert formatted.index("  z:") < formatted.index("  a:")


def test_format_normaliza_lf_newline_e_e_idempotente() -> None:
    codec = RuamelCodec()
    formatted = codec.format("kind: Coisa\r\napiVersion: x\r\n")
    assert "\r" not in formatted
    assert formatted.endswith("\n")
    assert codec.format(formatted) == formatted


def test_format_remove_espacos_finais_de_comentario_sem_mudar_escalar() -> None:
    text = """apiVersion: sinter.dev/v1   # envelope   
kind: Organization
metadata: {id: org-acme, name: ACME, status: approved}
spec:
  schemaVersion: 1
  extraNote: |-
    valor com espaços significativos   
"""

    formatted = RuamelCodec().format(text)

    assert "apiVersion: sinter.dev/v1   # envelope\n" in formatted
    assert "    valor com espaços significativos   \n" in formatted


def test_write_all_grava_lote_e_rejeita_caminho_fora_da_raiz(tmp_path: Path) -> None:
    writer = FsCatalogWriter(tmp_path)
    writer.write_all({"domains/x/domain.yaml": "kind: Domain\n"})
    assert (tmp_path / "domains/x/domain.yaml").read_text() == "kind: Domain\n"
    with pytest.raises(ValueError):
        writer.write_all({"../outside.yaml": "bad\n"})


def test_read_preserva_newlines_originais_para_o_check(tmp_path: Path) -> None:
    path = tmp_path / "organization.yaml"
    path.write_bytes(b"apiVersion: sinter.dev/v1\r\nkind: Organization\r\n")

    assert "\r\n" in FsCatalogFiles(tmp_path).read("organization.yaml")
