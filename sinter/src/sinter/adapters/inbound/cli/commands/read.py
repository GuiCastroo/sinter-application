"""`Sinter read <doc>[#anchor]`."""

from pathlib import Path
from typing import Annotated

import typer

from sinter.adapters.inbound.cli.catalog_root import resolve_root
from sinter.adapters.inbound.cli.errors import exit_code
from sinter.adapters.inbound.cli.render.json import to_json
from sinter.bootstrap import build
from sinter.ports.inbound.read import ReadRequest, ReadResult


def render(result: ReadResult) -> str:
    if result.warning:
        return f"{result.locator}\naviso: {result.warning}"
    if result.content is not None:
        return result.content
    return "\n".join(
        f"{'#' * h.level} {h.title}  #{h.anchor} ({h.size_lines} linhas)" for h in result.headings
    )


def read(
    target: Annotated[str, typer.Argument(metavar="DOC[#ANCHOR]")],
    catalog: Annotated[Path | None, typer.Option("--catalog")] = None,
    json_out: Annotated[bool, typer.Option("--json")] = False,
) -> int:
    result = build(resolve_root(catalog)).read(ReadRequest(target=target))
    typer.echo(to_json(result) if json_out else render(result))
    return exit_code(result)


def register(app: typer.Typer) -> None:
    app.command("read")(read)
