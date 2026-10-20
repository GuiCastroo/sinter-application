"""A única serialização de saída (AD-38): camelCase, ordem dos campos, null explícito."""

from pydantic import BaseModel


def to_json(model: BaseModel) -> str:
    return model.model_dump_json(by_alias=True, indent=2)
