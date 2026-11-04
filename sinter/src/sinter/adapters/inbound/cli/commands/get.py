"""`sinter get <id> [--level 0|1|2]`."""

from pathlib import Path
from typing import Annotated

import typer

from sinter.adapters.inbound.cli.catalog_root import resolve_root
from sinter.adapters.inbound.cli.errors import exit_code
from sinter.adapters.inbound.cli.render.get import render
from sinter.adapters.inbound.cli.render.json import to_json
from sinter.bootstrap import build
from sinter.ports.inbound.get import GetRequest


def get(
    item_id: Annotated[str, typer.Argument(metavar="ID", help="Id do item (ex.: dom-pagv).")],
    level: Annotated[int, typer.Option("--level", min=0, max=2, help="Nível de detalhe.")] = 1,
    catalog: Annotated[Path | None, typer.Option("--catalog", help="Pasta do catálogo.")] = None,
    json_out: Annotated[bool, typer.Option("--json", help="Saída em JSON.")] = False,
) -> int:
    """Mostra um item do geral para o detalhe, com o herdado marcado."""
    result = build(resolve_root(catalog)).get(GetRequest(id=item_id, level=level))
    typer.echo(to_json(result) if json_out else render(result))
    return exit_code(result)


def register(app: typer.Typer) -> None:
    app.command("get")(get)
