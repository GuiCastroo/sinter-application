"""Frases em linguagem natural: o único lugar que as produz (AD-45)."""

from sinter.domain.model.views import ApplicationLevel0, DomainLevel0, JourneyLevel0, Level0


def _plural(n: int, singular: str, plural: str) -> str:
    return f"{n} {singular if n == 1 else plural}"


def validation_summary(errors: int, warnings: int, files: int) -> str:
    return (
        f"{_plural(errors, 'erro', 'erros')}, {_plural(warnings, 'aviso', 'avisos')} "
        f"em {_plural(files, 'arquivo', 'arquivos')}."
    )


def item_summary(item: Level0) -> str:
    """Uma linha de identidade: 'Pagamentos (Varejo) · PAGV · area-varejo · 3 subdomínios'."""
    parts = [item.name]
    if isinstance(item, DomainLevel0):
        parts.append(item.domain_id)
        parts.append(item.area)
    if isinstance(item, JourneyLevel0 | ApplicationLevel0):
        parts.append(item.domain)
    if isinstance(item, ApplicationLevel0):
        parts.append(item.lifecycle)
    labels = {
        "subdomains": ("subdomínio", "subdomínios"),
        "applications": ("aplicação", "aplicações"),
        "journeys": ("jornada", "jornadas"),
        "data": ("dado", "dados"),
        "rules": ("regra", "regras"),
        "stages": ("etapa", "etapas"),
        "steps": ("passo", "passos"),
        "areas": ("área", "áreas"),
        "domains": ("domínio", "domínios"),
        "repositories": ("repo", "repos"),
    }
    for key, n in item.counts.items():
        one, many = labels.get(key, (key, key))
        parts.append(_plural(n, one, many))
    return " · ".join(parts)
