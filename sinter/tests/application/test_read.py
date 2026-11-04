import shutil
from pathlib import Path

import pytest

from sinter.bootstrap import build
from sinter.domain.errors import SinterError
from sinter.ports.inbound.read import ReadRequest

EXAMPLE = Path(__file__).parents[1] / "fixtures" / "exemplo-catalogo"


def test_read_by_id_and_anchor_returns_section_only() -> None:
    result = build(EXAMPLE).read(ReadRequest(target="doc-pagv-politica-estorno#prazos"))
    assert result.content.startswith("## Prazos")
    assert "## Exceções" not in result.content


def test_read_by_declared_path() -> None:
    result = build(EXAMPLE).read(ReadRequest(target="docs/negocio/politica-estorno.md"))
    assert result.content is None
    assert result.headings
    assert "Não processar" not in str(result.model_dump())


@pytest.mark.parametrize(
    "unsafe_path",
    ["../../outside.md", "../organization.md", "docs/arquitetura/enviar-moeda.drawio"],
)
def test_doc_id_rejects_unsafe_declared_paths(tmp_path: Path, unsafe_path: str) -> None:
    root = Path(shutil.copytree(EXAMPLE, tmp_path / "catalog"))
    manifest = root / "domains/pagv/domain.yaml"
    manifest.write_text(
        manifest.read_text().replace("docs/negocio/politica-estorno.md", unsafe_path)
    )
    with pytest.raises(SinterError, match="fora de docs/ ou não Markdown"):
        build(root).read(ReadRequest(target="doc-pagv-politica-estorno"))


def test_missing_anchor_reports_available() -> None:
    with pytest.raises(SinterError) as caught:
        build(EXAMPLE).read(ReadRequest(target="doc-pagv-politica-estorno#unknown"))
    assert caught.value.code == "ANCHOR_NOT_FOUND"
    assert caught.value.exit_code == 1
    assert caught.value.details["available"]


def test_url_document_is_returned_without_fetching() -> None:
    result = build(EXAMPLE).read(ReadRequest(target="doc-pagv-glossario"))
    assert result.locator == "https://wiki.acme.local/pagv/glossario"
    assert "não lê conteúdo externo" in result.warning


@pytest.mark.parametrize(
    "target", ["../../organization.md", "README.md", "docs/arquitetura/enviar-moeda.drawio"]
)
def test_rejects_unregistered_or_unsafe_path(target: str) -> None:
    with pytest.raises(SinterError):
        build(EXAMPLE).read(ReadRequest(target=target))


def test_read_by_id_is_json_serializable() -> None:
    result = build(EXAMPLE).read(ReadRequest(target="doc-pagv-politica-estorno"))
    assert result.model_dump_json()


def test_read_refuses_file_symlink_outside_catalog(tmp_path: Path) -> None:
    root = Path(shutil.copytree(EXAMPLE, tmp_path / "catalog"))
    target = root / "domains/pagv/docs/negocio/politica-estorno.md"
    outside = tmp_path / "outside.md"
    outside.write_text("# Conteúdo fora do catálogo\n")
    target.unlink()
    target.symlink_to(outside)

    with pytest.raises(SinterError, match="links simbólicos não são permitidos"):
        build(root).read(ReadRequest(target="doc-pagv-politica-estorno"))


def test_read_refuses_symlink_to_file_inside_catalog_but_outside_docs(tmp_path: Path) -> None:
    root = Path(shutil.copytree(EXAMPLE, tmp_path / "catalog"))
    target = root / "domains/pagv/docs/negocio/politica-estorno.md"
    outside_docs = root / "domains/pagv/private.md"
    outside_docs.write_text("# Conteúdo fora de docs\n")
    target.unlink()
    target.symlink_to("../../private.md")

    with pytest.raises(SinterError, match="links simbólicos não são permitidos"):
        build(root).read(ReadRequest(target="doc-pagv-politica-estorno"))
