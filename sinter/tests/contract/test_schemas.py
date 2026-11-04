"""`schemas/` versionado tem de bater com os modelos (AD-12). Para regravar: uv run poe schemas."""

import json
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
    expected = {f"out/{name}" for name in contract_schemas(published_results())}
    assert set(first.changed) == set(first.files) == expected
    assert "out/get-result.schema.json" in expected
    assert second.changed == []
    assert local.files == snapshot


def test_schema_usa_chaves_camel_case() -> None:
    domain = contract_schemas({})["domain.schema.json"]
    assert '"domainId"' in domain
    assert '"domain_id"' not in domain


def test_get_schema_discriminates_level0_kind() -> None:
    schema = json.loads(contract_schemas(published_results())["get-result.schema.json"])
    choices = schema["properties"]["item"]["anyOf"]
    discriminated = next(choice for choice in choices if "discriminator" in choice)
    assert discriminated["discriminator"]["propertyName"] == "kind"
    assert "Domain" in discriminated["discriminator"]["mapping"]


def test_level1_schema_keeps_facts_but_not_redundant_wrappers() -> None:
    schema = json.loads(contract_schemas(published_results())["get-result.schema.json"])
    props = schema["$defs"]["DomainLevel1"]["properties"]
    assert {"domainId", "does", "doesNot", "subdomains", "rules", "docs"} <= set(props)
    assert "level0" not in props and "knowledge" not in props
