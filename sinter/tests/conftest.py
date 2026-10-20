import shutil
from pathlib import Path

import pytest

TESTS = Path(__file__).parent
EXEMPLO = TESTS / "fixtures" / "exemplo-catalogo"
GOLDEN = TESTS / "golden"
ROOT_FILES = ("organization.yaml", "repositories.yaml", "regulations", "standards")


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--update-golden", action="store_true", help="Regrava os arquivos de tests/golden/."
    )


@pytest.fixture
def raiz_catalogo(tmp_path: Path) -> Path:
    """Só a raiz do exemplo (organização, repos, regulações, padrões): o que a Story 1.1 conhece."""
    root = tmp_path / "catalogo"
    root.mkdir()
    for name in ROOT_FILES:
        src = EXEMPLO / name
        if src.is_dir():
            shutil.copytree(src, root / name)
        else:
            shutil.copy(src, root / name)
    return root


@pytest.fixture
def catalogo_com_dominios(raiz_catalogo: Path) -> Path:
    """Raiz + o domain.yaml de cada domínio do exemplo: o que a Story 1.2 conhece."""
    for domain_file in sorted((EXEMPLO / "domains").glob("*/domain.yaml")):
        target = raiz_catalogo / domain_file.relative_to(EXEMPLO)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(domain_file, target)
    return raiz_catalogo


@pytest.fixture
def golden(request: pytest.FixtureRequest):  # type: ignore[no-untyped-def]
    update = bool(request.config.getoption("--update-golden"))

    def check(name: str, actual: str) -> None:
        path = GOLDEN / name
        if update or not path.exists():
            path.write_text(actual, encoding="utf-8")
        assert actual == path.read_text(encoding="utf-8"), f"saída mudou: {path}"

    return check
