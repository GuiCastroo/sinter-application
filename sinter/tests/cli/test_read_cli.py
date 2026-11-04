import json
from pathlib import Path

import pytest

from sinter.adapters.inbound.cli.app import run

EXAMPLE = Path(__file__).parents[1] / "fixtures" / "exemplo-catalogo"


def invoke(target: str, *args: str) -> int:
    return run(["read", target, "--catalog", str(EXAMPLE), *args])


def test_cli_summary_does_not_print_document_body(capsys: pytest.CaptureFixture[str]) -> None:
    assert invoke("doc-pagv-politica-estorno") == 0
    output = capsys.readouterr().out
    assert "prazos" in output
    assert "Não processar" not in output


def test_cli_anchor_prints_content(capsys: pytest.CaptureFixture[str]) -> None:
    assert invoke("doc-pagv-politica-estorno#prazos") == 0
    assert "## Prazos" in capsys.readouterr().out


def test_cli_url_prints_warning(capsys: pytest.CaptureFixture[str]) -> None:
    assert invoke("doc-pagv-glossario") == 0
    output = capsys.readouterr().out
    assert "https://wiki.acme.local/pagv/glossario" in output
    assert "não lê conteúdo externo" in output


def test_cli_missing_anchor_exit_one_lists_anchors(capsys: pytest.CaptureFixture[str]) -> None:
    assert invoke("doc-pagv-politica-estorno#bad", "--json") == 1
    error = json.loads(capsys.readouterr().out)["error"]
    assert error["code"] == "ANCHOR_NOT_FOUND"
    assert error["details"]["available"]


def test_cli_json_heading_summary(capsys: pytest.CaptureFixture[str]) -> None:
    assert invoke("doc-pagv-politica-estorno", "--json") == 0
    data = json.loads(capsys.readouterr().out)
    assert data["content"] is None and data["headings"]


def test_cli_unknown_document_exit_one(capsys: pytest.CaptureFixture[str]) -> None:
    assert invoke("missing-doc", "--json") == 1
    assert json.loads(capsys.readouterr().out)["error"]["code"] == "ITEM_NOT_FOUND"
