import pytest

from sinter.adapters.outbound.memory.files import MemoryCatalogFiles
from sinter.bootstrap import build
from sinter.domain.errors import SinterError
from sinter.ports.inbound.validate import ValidateRequest, ValidateResult

ORG = """apiVersion: sinter.dev/v1
kind: Organization
metadata: {{ id: org-acme, name: ACME, status: approved }}
spec:
  schemaVersion: {version}
  areas:
    - {{ id: area-varejo, name: Varejo }}
"""

REG = """apiVersion: sinter.dev/v1
kind: Regulation
metadata: {{ id: {id}, name: R, status: approved }}
spec:
  jurisdiction: BR
  effective: {{ from: 2020-01-01 }}
{extra}"""


def _validate(files: dict[str, str]) -> ValidateResult:
    return build(None, files=MemoryCatalogFiles(files)).validate(ValidateRequest())


def _codes(result: ValidateResult) -> list[str]:
    return [f.code for f in result.report.errors]


def _org(version: int = 1) -> str:
    return ORG.format(version=version)


def test_catalogo_minimo_valido() -> None:
    result = _validate({"organization.yaml": _org()})
    assert result.report.errors == []
    assert result.summary == "0 erros, 0 avisos em 1 arquivo."


def test_campo_obrigatorio_e_campo_desconhecido() -> None:
    bad = REG.format(id="reg-a", extra="  inventado: 1\n").replace("  jurisdiction: BR\n", "")
    result = _validate({"organization.yaml": _org(), "regulations/reg-a.yaml": bad})
    by_code = {f.code: f for f in result.report.errors}
    assert by_code["SCHEMA_REQUIRED_FIELD"].path == "spec.jurisdiction"
    assert by_code["SCHEMA_UNKNOWN_FIELD"].path == "spec.inventado"
    assert by_code["SCHEMA_UNKNOWN_FIELD"].file == "regulations/reg-a.yaml"
    assert by_code["SCHEMA_UNKNOWN_FIELD"].line == 6


def test_kind_desconhecido() -> None:
    text = (
        "apiVersion: sinter.dev/v1\nkind: Coisa\n"
        "metadata: { id: x-a, name: X, status: approved }\nspec: {}\n"
    )
    result = _validate({"organization.yaml": _org(), "coisa.yaml": text})
    assert _codes(result) == ["SCHEMA_UNKNOWN_KIND"]


def test_id_fora_do_prefixo() -> None:
    org = _org().replace("area-varejo", "varejo")
    reg = REG.format(id="regulacao-a", extra="")
    result = _validate({"organization.yaml": org, "regulations/regulacao-a.yaml": reg})
    paths = {(f.code, f.path) for f in result.report.errors}
    assert ("ID_FORMAT_INVALID", "spec.areas[varejo]") in paths
    assert ("ID_FORMAT_INVALID", "metadata.id") in paths


def test_id_repetido_cita_os_dois_arquivos() -> None:
    reg = REG.format(id="reg-a", extra="")
    result = _validate(
        {"organization.yaml": _org(), "regulations/reg-a.yaml": reg, "regulations/reg-b.yaml": reg}
    )
    dup = next(f for f in result.report.errors if f.code == "DUPLICATE_ID")
    assert dup.file == "regulations/reg-b.yaml"
    assert dup.related[0].file == "regulations/reg-a.yaml"


def test_supersedes_inexistente() -> None:
    reg = REG.format(id="reg-a", extra="  supersedes: reg-velha\n")
    result = _validate({"organization.yaml": _org(), "regulations/reg-a.yaml": reg})
    assert _codes(result) == ["REGULATION_SUPERSEDES_NOT_FOUND"]


def test_arquivo_fora_do_lugar() -> None:
    reg = REG.format(id="reg-a", extra="")
    result = _validate({"organization.yaml": _org(), "regulations/outro-nome.yaml": reg})
    assert _codes(result) == ["FILE_NOT_CANONICAL"]


def test_yaml_quebrado_nao_impede_o_resto() -> None:
    result = _validate({"organization.yaml": _org(), "regulations/reg-a.yaml": "a: [1\n"})
    assert _codes(result) == ["YAML_SYNTAX_ERROR"]


def test_schema_version_maior_e_recusado() -> None:
    with pytest.raises(SinterError) as exc:
        _validate({"organization.yaml": _org(version=99)})
    assert exc.value.code == "CATALOG_VERSION_UNSUPPORTED"
    assert exc.value.exit_code == 1


def test_pasta_sem_organizacao_nao_e_catalogo() -> None:
    with pytest.raises(SinterError) as exc:
        _validate({"repositories.yaml": "a: 1\n"})
    assert exc.value.code == "USAGE_NOT_A_CATALOG"
    assert exc.value.exit_code == 2
