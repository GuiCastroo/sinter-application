import shutil
from pathlib import Path

import pytest

from sinter.bootstrap import build
from sinter.domain.errors import SinterError
from sinter.domain.model.views import DomainLevel1, SubdomainLevel1
from sinter.ports.inbound.get import GetRequest, GetResult

EXAMPLE = Path(__file__).parents[1] / "fixtures" / "exemplo-catalogo"


def copy_catalog(tmp_path: Path) -> Path:
    return Path(shutil.copytree(EXAMPLE, tmp_path / "catalog"))


def test_get_domain_level1() -> None:
    result = build(EXAMPLE).get(GetRequest(id="dom-pagv"))
    assert isinstance(result.item, DomainLevel1)
    assert result.level == 1
    assert result.item.knowledge.rules
    assert result.report.errors == []


def test_get_subdomain_knowledge() -> None:
    result = build(EXAMPLE).get(GetRequest(id="sub-pagv-conciliacao"))
    assert isinstance(result.item, SubdomainLevel1)
    assert result.item.domain == "dom-pagv"
    assert any(r.origin == "dom-pagv" for r in result.item.rules)


def test_missing_id_has_up_to_three_stable_suggestions() -> None:
    with pytest.raises(SinterError) as caught:
        build(EXAMPLE).get(GetRequest(id="dom-pag"))
    error = caught.value
    assert error.code == "ITEM_NOT_FOUND"
    assert error.exit_code == 1
    assert 1 <= len(error.details["suggestions"]) <= 3
    assert "dom-pagv" in error.details["suggestions"]


def test_invalid_manifest_is_not_internal_error(tmp_path: Path) -> None:
    root = copy_catalog(tmp_path)
    file = root / "domains/pagv/domain.yaml"
    file.write_text(file.read_text().replace("  purpose:", "  purposeTypo:"))
    with pytest.raises(SinterError) as caught:
        build(root).get(GetRequest(id="dom-pagv"))
    assert caught.value.code == "ITEM_NOT_FOUND"
    assert "inválido" in caught.value.message


@pytest.mark.parametrize("status", ["candidate", "rejected", "deprecated"])
def test_direct_get_shows_unapproved_status(tmp_path: Path, status: str) -> None:
    root = copy_catalog(tmp_path)
    file = root / "domains/pagv/domain.yaml"
    file.write_text(file.read_text().replace("status: approved", f"status: {status}"))
    result = build(root).get(GetRequest(id="dom-pagv"))
    assert result.item.status == status


def test_schema_findings_elsewhere_are_not_silently_discarded(tmp_path: Path) -> None:
    root = copy_catalog(tmp_path)
    file = root / "standards/std-api-rest.yaml"
    file.write_text(file.read_text().replace("  summary:", "  summaryTypo:"))
    result = build(root).get(GetRequest(id="dom-pagv"))
    assert result.report.errors
    assert all(f.file == "standards/std-api-rest.yaml" for f in result.report.errors)


def test_json_round_trip_preserves_specific_level1_type() -> None:
    result = build(EXAMPLE).get(GetRequest(id="dom-camb"))
    restored = GetResult.model_validate_json(result.model_dump_json(by_alias=True))
    assert isinstance(restored.item, DomainLevel1)
    assert restored == result


def test_level2_is_honestly_reported_as_level1_until_u3() -> None:
    result = build(EXAMPLE).get(GetRequest(id="dom-pagv", level=2))
    assert result.level == 1
    assert result.omitted[0].command.endswith("--level 2")
