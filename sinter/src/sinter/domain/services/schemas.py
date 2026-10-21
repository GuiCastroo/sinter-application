"""O contrato publicado: JSON Schema gerado dos modelos (AD-12, AD-38)."""

import json
import re

from pydantic import BaseModel

from sinter.domain.model.registry import KINDS


def _kebab(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()


def render_schema(model: type[BaseModel]) -> str:
    schema = model.model_json_schema(by_alias=True, mode="validation")
    return json.dumps(schema, indent=2, ensure_ascii=False) + "\n"


def contract_schemas(extra: dict[str, type[BaseModel]]) -> dict[str, str]:
    """Nome do arquivo → JSON Schema, em ordem estável: um por kind + os resultados da CLI."""
    out: dict[str, str] = {}
    for kind in sorted(KINDS):
        out[f"{_kebab(kind)}.schema.json"] = render_schema(KINDS[kind].model)
    for name in sorted(extra):
        out[f"{name}.schema.json"] = render_schema(extra[name])
    return out
