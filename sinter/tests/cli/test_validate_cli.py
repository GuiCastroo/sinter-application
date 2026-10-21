import json
import shutil
from collections.abc import Callable
from pathlib import Path

import pytest

from sinter.adapters.inbound.cli.app import run

EXEMPLO = Path(__file__).parents[1] / "fixtures" / "exemplo-catalogo"


def test_help_mostra_validate(capsys: pytest.CaptureFixture[str]) -> None:
    assert run(["--help"]) == 0
    assert "validate" in capsys.readouterr().out


def test_raiz_do_exemplo_passa(raiz_catalogo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert run(["validate", str(raiz_catalogo)]) == 0
    assert "0 erros, 0 avisos em 11 arquivos." in capsys.readouterr().out


def test_json_da_raiz_do_exemplo(
    raiz_catalogo: Path, capsys: pytest.CaptureFixture[str], golden: Callable[[str, str], None]
) -> None:
    assert run(["validate", str(raiz_catalogo), "--json"]) == 0
    out = capsys.readouterr().out
    golden("validate_raiz.json", out)
    assert json.loads(out)["report"] == {"errors": [], "warnings": []}


def test_erro_de_validacao_sai_com_1(
    raiz_catalogo: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = raiz_catalogo / "standards" / "std-api-rest.yaml"
    path.write_text(path.read_text().replace("  summary:", "  sumario:"))
    assert run(["validate", str(raiz_catalogo), "--json"]) == 1
    errors = json.loads(capsys.readouterr().out)["report"]["errors"]
    assert {e["code"] for e in errors} == {"SCHEMA_REQUIRED_FIELD", "SCHEMA_UNKNOWN_FIELD"}
    assert all(e["file"] == "standards/std-api-rest.yaml" for e in errors)


def test_pasta_que_nao_e_catalogo_sai_com_2(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert run(["validate", str(tmp_path), "--json"]) == 2
    assert json.loads(capsys.readouterr().out)["error"]["code"] == "USAGE_NOT_A_CATALOG"


def test_opcao_invalida_sai_com_2(capsys: pytest.CaptureFixture[str]) -> None:
    assert run(["validate", "--nao-existe", "--json"]) == 2
    assert json.loads(capsys.readouterr().out)["error"]["code"] == "USAGE_INVALID_OPTION"


def test_acha_o_catalogo_subindo_pastas(
    raiz_catalogo: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    sub = raiz_catalogo / "regulations"
    monkeypatch.chdir(sub)
    monkeypatch.delenv("SINTER_CATALOG", raising=False)
    assert run(["validate"]) == 0


def test_exemplo_completo_passa(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], golden: Callable[[str, str], None]
) -> None:
    root = tmp_path / "catalogo"
    shutil.copytree(EXEMPLO, root)
    code = run(["validate", str(root), "--json"])
    out = capsys.readouterr().out
    report = json.loads(out)["report"]
    assert report["errors"] == []  # SM-1: zero erros
    assert {w["code"] for w in report["warnings"]} == {"DOM_REF_NOT_IN_CATALOG"}
    assert code == 0
    golden("validate_exemplo.json", out)
