"""Como cada comando acha o catálogo (AD-47).

Ordem: --catalog > SINTER_CATALOG > subir pastas até achar organization.yaml.
"""

import os
from pathlib import Path

from sinter.domain.errors import SinterError

ORGANIZATION_FILE = "organization.yaml"


def resolve_root(explicit: Path | None, cwd: Path | None = None) -> Path:
    if explicit is not None:
        root = explicit.resolve()
        if not (root / ORGANIZATION_FILE).is_file():
            raise SinterError(
                "USAGE_NOT_A_CATALOG",
                f"'{explicit}' não é um catálogo do Sinter (falta {ORGANIZATION_FILE})",
                {"path": str(explicit)},
            )
        return root
    env = os.environ.get("SINTER_CATALOG")
    if env:
        return resolve_root(Path(env))
    start = (cwd or Path.cwd()).resolve()
    for folder in (start, *start.parents):
        if (folder / ORGANIZATION_FILE).is_file():
            return folder
    raise SinterError(
        "USAGE_NOT_A_CATALOG",
        "nenhum catálogo encontrado aqui nem nas pastas acima; use --catalog <pasta>",
    )
