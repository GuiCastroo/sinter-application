import pytest

from sinter.domain.services.text import fold


@pytest.mark.parametrize(
    ("a", "b"),
    [
        ("Câmbio", "cambio"),
        ("  Boleta ", "boleta"),
        ("Natureza da Operação", "natureza da operacao"),
    ],
)
def test_fold_ignora_maiusculas_e_acentos(a: str, b: str) -> None:
    assert fold(a) == fold(b)
