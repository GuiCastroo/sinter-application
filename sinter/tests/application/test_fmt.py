import ast
from pathlib import Path

from sinter.adapters.outbound.memory.files import MemoryCatalogFiles, MemoryCatalogWriter
from sinter.adapters.outbound.yaml_fs.codec import RuamelCodec
from sinter.application.fmt import Fmt
from sinter.bootstrap import build
from sinter.domain.errors import SinterError
from sinter.ports.inbound.fmt import FmtRequest

ORG = """spec:
  areas: []
  schemaVersion: 1
kind: Organization
metadata: {status: approved, name: ACME, id: org-acme}
apiVersion: sinter.dev/v1
"""


def _fmt(files: MemoryCatalogFiles, *, path: str | None = None, check: bool = False):
    writer = MemoryCatalogWriter(files)
    return build(None, files=files, writer=writer).fmt(FmtRequest(path=path, check=check))


def test_fmt_escreve_formato_canonico_e_segunda_execucao_nao_muda() -> None:
    files = MemoryCatalogFiles({"organization.yaml": ORG})

    first = _fmt(files)
    second = _fmt(files)

    assert first.files_changed == ["organization.yaml"]
    assert "apiVersion:" in files.read("organization.yaml")
    assert second.files_changed == []
    assert second.summary == "0 manifesto(s) formatado(s)."


def test_fmt_check_lista_sem_escrever() -> None:
    files = MemoryCatalogFiles({"organization.yaml": ORG})

    result = _fmt(files, check=True)

    assert files.read("organization.yaml") == ORG
    assert result.files_changed == []
    assert [finding.code for finding in result.report.errors] == ["FILE_NOT_FORMATTED"]
    assert result.report.errors[0].file == "organization.yaml"


def test_fmt_arquivo_individual_nao_toca_nos_outros() -> None:
    files = MemoryCatalogFiles({"organization.yaml": ORG, "other.yaml": "a: 1\n"})

    result = _fmt(files, path="organization.yaml")

    assert result.files_changed == ["organization.yaml"]
    assert files.read("other.yaml") == "a: 1\n"


def test_fmt_nao_interpreta_yaml_invalido_como_sucesso() -> None:
    broken = "kind: [\n"
    files = MemoryCatalogFiles({"organization.yaml": broken})

    result = _fmt(files)

    assert files.read("organization.yaml") == broken
    assert [finding.code for finding in result.report.errors] == ["YAML_SYNTAX_ERROR"]


def test_fmt_recusa_arquivo_que_nao_esta_no_catalogo() -> None:
    files = MemoryCatalogFiles({"organization.yaml": ORG})

    try:
        _fmt(files, path="absent.yaml")
    except SinterError as error:
        assert error.code == "ITEM_NOT_FOUND"
    else:
        raise AssertionError("era esperado um erro de manifesto ausente")


def test_fmt_recusa_codec_que_altera_dados_sem_escrever() -> None:
    class ChangingCodec(RuamelCodec):
        def format(self, text: str) -> str:
            return super().format(text).replace("schemaVersion: 1", "schemaVersion: 2")

    files = MemoryCatalogFiles({"organization.yaml": ORG})
    before = files.read("organization.yaml")
    use_case = Fmt(files, MemoryCatalogWriter(files), ChangingCodec())

    result = use_case(FmtRequest())

    assert [finding.code for finding in result.report.errors] == ["FMT_SEMANTIC_CHANGE"]
    assert files.read("organization.yaml") == before


def test_fmt_lote_com_erro_nao_anuncia_arquivos_nao_gravados() -> None:
    files = MemoryCatalogFiles({"organization.yaml": ORG, "broken.yaml": "kind: [\n"})
    before = files.read("organization.yaml")

    result = _fmt(files)

    assert [finding.code for finding in result.report.errors] == ["YAML_SYNTAX_ERROR"]
    assert files.read("organization.yaml") == before
    assert result.files_changed == []
    assert result.summary == (
        "2 manifesto(s) conferido(s); nenhum arquivo foi gravado devido a erros."
    )


def test_only_write_use_cases_import_catalog_writer_port() -> None:
    application = Path(__file__).parents[2] / "src" / "sinter" / "application"
    allowed_writers = {"apply.py", "catalog_init.py", "fmt.py"}
    writer_module = "sinter.ports.outbound.catalog_writer"
    violations: list[str] = []
    for path in application.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports_writer = any(
            (isinstance(node, ast.ImportFrom) and node.module == writer_module)
            or (
                isinstance(node, ast.Import)
                and any(alias.name == writer_module for alias in node.names)
            )
            for node in ast.walk(tree)
        )
        if imports_writer and path.name not in allowed_writers:
            violations.append(path.relative_to(application).as_posix())

    assert violations == []
