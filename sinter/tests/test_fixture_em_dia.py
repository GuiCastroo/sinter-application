"""A fixture é cópia do exemplo do PRD; este teste acusa quando os dois divergem."""

from pathlib import Path

import pytest

EXEMPLO = Path(__file__).parent / "fixtures" / "exemplo-catalogo"

PRD_EXEMPLO = Path(__file__).parents[2] / "docs" / "prd-dominio-2026-10-17" / "exemplo-catalogo"


def _files(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


@pytest.mark.skipif(not PRD_EXEMPLO.exists(), reason="exemplo do PRD fora deste checkout")
def test_fixture_igual_ao_exemplo_do_prd() -> None:
    assert _files(EXEMPLO) == _files(PRD_EXEMPLO)
