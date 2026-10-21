"""`schemas/` versionado tem de bater com os modelos (AD-12). Para regravar: uv run poe schemas."""

from pathlib import Path

from sinter.adapters.outbound.memory.local_files import MemoryLocalFiles
from sinter.application.schema_export import SchemaExport
from sinter.domain.services.schemas import contract_schemas
from sinter.ports.inbound.schema_export import SchemaExportRequest, published_results

SCHEMAS = Path(__file__).parents[2] / "schemas"


def test_schemas_versionados_em_dia() -> None:
    expected = contract_schemas(published_results())
    on_disk = {p.name: p.read_text(encoding="utf-8") for p in SCHEMAS.glob("*.schema.json")}
    assert on_disk == expected, "schemas/ desatualizado: rode `uv run poe schemas`"


def test_export_e_deterministico_e_so_grava_o_que_mudou() -> None:
    local = MemoryLocalFiles()
    first = SchemaExport(local)(SchemaExportRequest(target="out"))
    snapshot = dict(local.files)
    second = SchemaExport(local)(SchemaExportRequest(target="out"))
    assert len(first.changed) == len(first.files) == 11
    assert second.changed == []
    assert local.files == snapshot


def test_schema_usa_chaves_camel_case() -> None:
    domain = contract_schemas({})["domain.schema.json"]
    assert '"domainId"' in domain
    assert '"domain_id"' not in domain
