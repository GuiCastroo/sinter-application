import json
import shutil
from pathlib import Path

from sinter.adapters.inbound.cli.app import run
from sinter.adapters.outbound.yaml_fs.codec import RuamelCodec

EXAMPLE = Path(__file__).parents[1] / "fixtures" / "exemplo-catalogo"


def test_fmt_check_nao_escreve_e_retorna_um_manifesto_fora_do_formato(
    tmp_path: Path, capsys
) -> None:
    root = tmp_path / "catalog"
    shutil.copytree(EXAMPLE, root)
    target = root / "domains" / "pagv" / "domain.yaml"
    before = target.read_bytes()

    code = run(["fmt", "--catalog", str(root), str(target), "--check", "--json"])

    result = json.loads(capsys.readouterr().out)
    assert code == (1 if result["report"]["errors"] else 0)
    assert target.read_bytes() == before
    if result["report"]["errors"]:
        assert result["report"]["errors"][0]["code"] == "FILE_NOT_FORMATTED"


def test_fmt_por_arquivo_nao_formata_os_irmaos(tmp_path: Path, capsys) -> None:
    root = tmp_path / "catalog"
    shutil.copytree(EXAMPLE, root)
    target = root / "domains" / "pagv" / "domain.yaml"
    other = root / "organization.yaml"
    other_before = other.read_bytes()

    assert run(["fmt", str(target)]) == 0
    capsys.readouterr()

    assert other.read_bytes() == other_before
    assert RuamelCodec().format(target.read_text()) == target.read_text()


def test_fmt_sem_argument_formata_todo_exemplo_idempotentemente(tmp_path: Path, capsys) -> None:
    root = tmp_path / "catalog"
    shutil.copytree(EXAMPLE, root)
    codec = RuamelCodec()
    paths = sorted(p for p in root.rglob("*") if p.is_file() and p.suffix in {".yaml", ".yml"})
    before = {p: codec.split(p.read_text())[0].data for p in paths}

    assert run(["fmt", "--catalog", str(root)]) == 0
    capsys.readouterr()
    assert run(["fmt", "--catalog", str(root)]) == 0
    output = capsys.readouterr().out

    assert "0 manifesto(s) formatado(s)." in output
    for path in paths:
        text = path.read_text()
        assert codec.format(text) == text
        assert codec.split(text)[0].data == before[path]


def test_fmt_check_com_verificacao_de_todos_os_arquivos(tmp_path: Path, capsys) -> None:
    root = tmp_path / "catalog"
    shutil.copytree(EXAMPLE, root)
    target = root / "domains" / "pagv" / "domain.yaml"
    original = target.read_bytes()
    target.write_text(target.read_text().replace("kind: Domain", "kind: Domain "))
    before = target.read_bytes()

    result = run(["fmt", "--catalog", str(root), "--check"])
    output = capsys.readouterr().out

    assert result == 1
    assert "domains/pagv/domain.yaml" in output
    assert target.read_bytes() == before
    assert before != original


def test_fmt_detecta_crlf_no_check_e_grava_lf(tmp_path: Path, capsys) -> None:
    root = tmp_path / "catalog"
    shutil.copytree(EXAMPLE, root)
    target = root / "domains" / "pagv" / "domain.yaml"
    canonical = RuamelCodec().format(target.read_text())
    target.write_bytes(canonical.replace("\n", "\r\n").encode())
    before = target.read_bytes()

    assert run(["fmt", "--catalog", str(root), str(target), "--check"]) == 1
    capsys.readouterr()
    assert target.read_bytes() == before

    assert run(["fmt", "--catalog", str(root), str(target)]) == 0
    capsys.readouterr()
    after = target.read_bytes()
    assert b"\r\n" not in after
    assert after.endswith(b"\n")
    assert run(["fmt", "--catalog", str(root), str(target), "--check"]) == 0


def test_validate_trata_formato_nao_canonico_como_aviso(tmp_path: Path, capsys) -> None:
    root = tmp_path / "catalog"
    shutil.copytree(EXAMPLE, root)
    target = root / "domains" / "pagv" / "domain.yaml"
    target.write_text(target.read_text().replace("kind: Domain", "kind: Domain "))

    result = run(["validate", str(root), "--json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert any(w["code"] == "FILE_NOT_FORMATTED" for w in payload["report"]["warnings"])
