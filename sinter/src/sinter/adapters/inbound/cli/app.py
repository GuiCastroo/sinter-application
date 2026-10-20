"""Ponto de entrada da CLI: registra comandos e traduz erros em código de saída (AD-33)."""

import sys
import traceback
from collections.abc import Sequence

import typer

from sinter.adapters.inbound.cli.commands import validate
from sinter.adapters.inbound.cli.errors import envelope, internal_error, usage_error
from sinter.adapters.inbound.cli.render.json import to_json
from sinter.domain.errors import SinterError

app = typer.Typer(
    name="sinter",
    help="Sinter: catálogo de contexto para agentes de código.",
    add_completion=False,
    no_args_is_help=True,
    pretty_exceptions_enable=False,
)


@app.callback()
def _root() -> None:
    """Sinter: catálogo de contexto para agentes de código."""


validate.register(app)


def _fail(err: SinterError, json_out: bool) -> int:
    if json_out:
        typer.echo(to_json(envelope(err)))
    else:
        typer.echo(f"erro: {err.message} [{err.code}]", err=True)
    return err.exit_code


def run(argv: Sequence[str]) -> int:
    args = list(argv)
    json_out = "--json" in args
    debug = "--debug" in args
    if debug:
        args.remove("--debug")
    try:
        rv = app(args=args, prog_name="sinter", standalone_mode=False)
    except SinterError as err:
        return _fail(err, json_out)
    except typer.Exit as exc:
        return int(exc.exit_code)
    except typer.Abort:
        return 1
    except typer.TyperException as exc:  # erro de uso: opção ou argumento inválido
        formatter = getattr(exc, "format_message", None)
        message = formatter() if callable(formatter) else str(exc)
        return _fail(usage_error(str(message)), json_out)
    except Exception as exc:
        if debug:
            traceback.print_exc()
        return _fail(internal_error(exc), json_out)
    return rv if isinstance(rv, int) else 0


def main() -> None:
    sys.exit(run(sys.argv[1:]))
