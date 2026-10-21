"""`sinter schema export [pasta]`."""

from typing import Annotated

import typer

from sinter.adapters.inbound.cli.render.json import to_json
from sinter.bootstrap import build
from sinter.ports.inbound.schema_export import SchemaExportRequest

schema_app = typer.Typer(help="Contrato JSON Schema do catálogo e das saídas --json.")


@schema_app.command("export")
def export(
    pasta: Annotated[str, typer.Argument(help="Pasta de destino.")] = "schemas",
    json_out: Annotated[bool, typer.Option("--json", help="Saída em JSON.")] = False,
) -> int:
    """Gera um *.schema.json por kind e por resultado da CLI."""
    result = build(None).schema_export(SchemaExportRequest(target=pasta))
    if json_out:
        typer.echo(to_json(result))
    else:
        typer.echo("\n".join([*(f"alterado  {p}" for p in result.changed), result.summary]))
    return 0


def register(app: typer.Typer) -> None:
    app.add_typer(schema_app, name="schema")
