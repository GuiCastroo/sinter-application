"""Frases em linguagem natural: o único lugar que as produz (AD-45)."""


def _plural(n: int, singular: str, plural: str) -> str:
    return f"{n} {singular if n == 1 else plural}"


def validation_summary(errors: int, warnings: int, files: int) -> str:
    return (
        f"{_plural(errors, 'erro', 'erros')}, {_plural(warnings, 'aviso', 'avisos')} "
        f"em {_plural(files, 'arquivo', 'arquivos')}."
    )
