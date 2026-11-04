import json
import shutil
from pathlib import Path

import pytest

from sinter.adapters.inbound.cli.app import run

EXAMPLE = Path(__file__).parents[1] / "fixtures" / "exemplo-catalogo"


def get(ident: str, *args: str) -> int:
    return run(["get", ident, "--catalog", str(EXAMPLE), *args])


def test_level0_json_identity_and_counts(capsys: pytest.CaptureFixture[str]) -> None:
    assert get("dom-pagv", "--level", "0", "--json") == 0
    result = json.loads(capsys.readouterr().out)
    assert result["item"]["domainId"] == "PAGV"
    assert result["item"]["counts"]["subdomains"] == 3
    assert "does" not in result["item"]


def test_text_has_children_names_counts_and_knowledge(capsys: pytest.CaptureFixture[str]) -> None:
    assert get("dom-camb", "--level", "1") == 0
    out = capsys.readouterr().out
    for value in ["Cotação", "sub-camb-cotacao", "ADR-CAMB-002", "reg-bcb-cambio", "Boleta"]:
        assert value in out
    assert "CAMB" in out and "area-cambio" in out
    assert "applications=1" in out


def test_subdomain_text_marks_origin_of_regulations(capsys: pytest.CaptureFixture[str]) -> None:
    assert get("sub-pagv-conciliacao") == 0
    out = capsys.readouterr().out
    assert "herdado de dom-pagv" in out
    assert "reg-lgpd" in out


def test_empty_lists_are_explicit(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = Path(shutil.copytree(EXAMPLE, tmp_path / "catalog"))
    file = root / "domains/pagv/domain.yaml"
    from sinter.bootstrap import build

    container = build(root)
    doc = container._codec.split(file.read_text())[0]
    # Retain a valid Domain schema and change only the feature under test.
    from sinter.domain.model.domain import Domain

    domain = Domain.model_validate(doc.data)
    domain = domain.model_copy(
        update={"spec": domain.spec.model_copy(update={"does": [], "does_not": [], "unknowns": []})}
    )
    import json as json_module

    # JSON is valid YAML and keeps this synthetic variation schema-checked.
    file.write_text(json_module.dumps(domain.model_dump(mode="json", by_alias=True)))
    assert run(["get", "dom-pagv", "--catalog", str(root)]) == 0
    out = capsys.readouterr().out
    for label in ["faz", "não faz", "não sabemos"]:
        assert f"{label}: (não preenchido)" in out


def test_missing_id_json_exit_one(capsys: pytest.CaptureFixture[str]) -> None:
    assert get("dom-pag", "--json") == 1
    error = json.loads(capsys.readouterr().out)["error"]
    assert error["code"] == "ITEM_NOT_FOUND"
    assert "dom-pagv" in error["details"]["suggestions"]


def test_invalid_level_is_usage_error(capsys: pytest.CaptureFixture[str]) -> None:
    assert get("dom-pagv", "--level", "3", "--json") == 2
    assert json.loads(capsys.readouterr().out)["error"]["code"] == "USAGE_INVALID_OPTION"


def test_json_determinism_and_omitted(capsys: pytest.CaptureFixture[str]) -> None:
    assert get("dom-camb", "--json") == 0
    first = capsys.readouterr().out
    assert get("dom-camb", "--json") == 0
    assert capsys.readouterr().out == first
    assert json.loads(first)["omitted"][0]["command"].endswith("--level 2")


def test_missing_catalog_is_environment_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert run(["get", "dom-pagv", "--catalog", str(tmp_path), "--json"]) == 2
    assert json.loads(capsys.readouterr().out)["error"]["code"] == "USAGE_NOT_A_CATALOG"
