"""`sinter fmt [arquivo] [--check]`."""

from pathlib import Path
from typing import Annotated

import typer

from sinter.adapters.inbound.cli.catalog_root import resolve_root
from sinter.adapters.inbound.cli.errors import exit_code, usage_error
from sinter.adapters.inbound.cli.render.fmt import render
from sinter.adapters.inbound.cli.render.json import to_json
from sinter.bootstrap import build
from sinter.ports.inbound.fmt import FmtRequest


def fmt(
    arquivo: Annotated[Path | None, typer.Argument(help="Manifesto a formatar.")] = None,
    catalog: Annotated[Path | None, typer.Option("--catalog", help="Pasta do catálogo.")] = None,
    check: Annotated[bool, typer.Option("--check", help="Só confere o formato.")] = False,
    json_out: Annotated[bool, typer.Option("--json", help="Saída em JSON.")] = False,
) -> int:
    """Formata os manifestos do catálogo em ordem canônica, sem criar commit."""
    if arquivo is not None and catalog is None:
        candidate = (Path.cwd() / arquivo).resolve()
        root = resolve_root(None, cwd=candidate.parent)
    else:
        root = resolve_root(catalog)

    relative: str | None = None
    if arquivo is not None:
        candidate = arquivo.resolve() if arquivo.is_absolute() else (Path.cwd() / arquivo).resolve()
        try:
            relative = candidate.relative_to(root.resolve()).as_posix()
        except ValueError:
            if arquivo.is_absolute():
                raise usage_error("o manifesto precisa estar dentro da raiz do catálogo") from None
            candidate = (root / arquivo).resolve()
            try:
                relative = candidate.relative_to(root.resolve()).as_posix()
            except ValueError:
                raise usage_error("o manifesto precisa estar dentro da raiz do catálogo") from None

    result = build(root).fmt(FmtRequest(path=relative, check=check))
    typer.echo(to_json(result) if json_out else render(result))
    return exit_code(result)


def register(app: typer.Typer) -> None:
    app.command("fmt")(fmt)
