"""`sinter validate [pasta]`."""

from pathlib import Path
from typing import Annotated

import typer

from sinter.adapters.inbound.cli.catalog_root import resolve_root
from sinter.adapters.inbound.cli.errors import exit_code
from sinter.adapters.inbound.cli.render.json import to_json
from sinter.adapters.inbound.cli.render.validate import render
from sinter.bootstrap import build
from sinter.ports.inbound.validate import ValidateRequest


def validate(
    pasta: Annotated[Path | None, typer.Argument(help="Pasta do catálogo.")] = None,
    catalog: Annotated[Path | None, typer.Option("--catalog", help="Pasta do catálogo.")] = None,
    json_out: Annotated[bool, typer.Option("--json", help="Saída em JSON.")] = False,
) -> int:
    """Confere o catálogo inteiro e lista cada erro com arquivo e motivo."""
    root = resolve_root(pasta or catalog)
    result = build(root).validate(ValidateRequest())
    typer.echo(to_json(result) if json_out else render(result))
    return exit_code(result)


def register(app: typer.Typer) -> None:
    app.command("validate")(validate)
