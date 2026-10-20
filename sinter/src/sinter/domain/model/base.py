"""Base de todos os modelos: chaves camelCase no YAML e no JSON (AD-38)."""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

API_VERSION = "sinter.dev/v1"


class SinterModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_by_name=True,
        validate_by_alias=True,
        serialize_by_alias=True,
        extra="forbid",
        frozen=True,
    )
