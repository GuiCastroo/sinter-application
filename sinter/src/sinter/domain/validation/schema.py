"""Fase 1 da validação: cada manifesto contra o modelo do seu kind (AD-31)."""

from typing import Any

from pydantic import ValidationError

from sinter.domain.model.catalog import ParsedManifest
from sinter.domain.model.registry import KINDS
from sinter.domain.validation.finding import ERROR, Finding, Positions, Segment


def _finding(
    file: str, data: Any, positions: Positions, segments: tuple[Segment, ...], code: str, msg: str
) -> Finding:
    return Finding.at(
        code=code,
        severity=ERROR,
        file=file,
        data=data,
        positions=positions,
        segments=segments,
        message=msg,
    )


def _from_pydantic(error: Any) -> tuple[str, str]:
    kind = error["type"]
    if kind == "missing":
        return "SCHEMA_REQUIRED_FIELD", "campo obrigatório ausente"
    if kind == "extra_forbidden":
        return "SCHEMA_UNKNOWN_FIELD", "campo desconhecido"
    if kind == "literal_error":
        expected = error.get("ctx", {}).get("expected", "")
        return "SCHEMA_INVALID_VALUE", f"valor inválido; esperado {expected}"
    if kind == "value_error":
        return "SCHEMA_INVALID_VALUE", str(error.get("ctx", {}).get("error", error["msg"]))
    return "SCHEMA_INVALID_VALUE", f"valor inválido ({kind}): {error['msg']}"


def parse_manifest(
    file: str, data: Any, positions: Positions
) -> tuple[ParsedManifest, list[Finding]]:
    if not isinstance(data, dict):
        f = _finding(
            file, data, positions, (), "MANIFEST_NOT_MAPPING", "o arquivo não é um manifesto"
        )
        return ParsedManifest(file=file, data=data, positions=positions), [f]

    kind = data.get("kind")
    if not isinstance(kind, str):
        f = _finding(
            file, data, positions, ("kind",), "SCHEMA_REQUIRED_FIELD", "campo obrigatório ausente"
        )
        return ParsedManifest(file=file, data=data, positions=positions), [f]
    if kind not in KINDS:
        known = ", ".join(sorted(KINDS))
        f = _finding(
            file,
            data,
            positions,
            ("kind",),
            "SCHEMA_UNKNOWN_KIND",
            f"kind desconhecido '{kind}'; conhecidos: {known}",
        )
        return ParsedManifest(file=file, data=data, positions=positions, kind=kind), [f]

    try:
        model = KINDS[kind].model.model_validate(data)
    except ValidationError as exc:
        findings = []
        for err in exc.errors():
            code, msg = _from_pydantic(err)
            findings.append(_finding(file, data, positions, tuple(err["loc"]), code, msg))
        return ParsedManifest(file=file, data=data, positions=positions, kind=kind), findings
    return ParsedManifest(file=file, data=data, positions=positions, kind=kind, model=model), []
