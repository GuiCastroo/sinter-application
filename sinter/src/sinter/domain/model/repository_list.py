"""repositories.yaml — kind: RepositoryList (Apêndice A.1)."""

from typing import Literal

from sinter.domain.model.base import SinterModel
from sinter.domain.model.blocks import Metadata


class RepositoryRef(SinterModel):
    id: str
    url: str


class RepositoryListSpec(SinterModel):
    repositories: list[RepositoryRef]


class RepositoryList(SinterModel):
    api_version: Literal["sinter.dev/v1"]
    kind: Literal["RepositoryList"]
    metadata: Metadata
    spec: RepositoryListSpec
