"""Normalização de texto num lugar só (AD-46)."""

import unicodedata


def fold(text: str) -> str:
    """Para comparar: sem diferença de maiúsculas, acentos e espaços nas pontas."""
    decomposed = unicodedata.normalize("NFKD", text.strip().casefold())
    return "".join(c for c in decomposed if not unicodedata.combining(c))


def gh_anchor(text: str) -> str:
    """Cria o anchor de heading no formato GitHub, sem acentos."""
    folded = fold(text).lower()
    chars = [c for c in folded if c.isalnum() or c in " -_"]
    return "-".join("".join(chars).split())
