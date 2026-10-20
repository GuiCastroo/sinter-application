"""domains/<d>/relations/rel-*.yaml — kind: Relation (Apêndice A.7).

No passo 1, só o tipo modernized_by.
"""

from typing import Literal

from pydantic import Field

from sinter.domain.model.base import SinterModel
from sinter.domain.model.blocks import Evidence, Metadata


class RelationMetadata(Metadata):
    domain: str


class RelationSpec(SinterModel):
    source: str
    type: Literal["modernized_by"]
    target: str
    phase: Literal["planned", "in-progress", "done"]
    evidence: list[Evidence] = Field(min_length=1)


class Relation(SinterModel):
    api_version: Literal["sinter.dev/v1"]
    kind: Literal["Relation"]
    metadata: RelationMetadata
    spec: RelationSpec
