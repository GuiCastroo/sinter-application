"""Orçamento de contexto (NFR-1): heurística fixa, a mesma em todo lugar (AD-39)."""

import math


def count_tokens(text: str) -> int:
    """~4 caracteres por token: suficiente para vigiar o tamanho dos níveis."""
    return math.ceil(len(text) / 4)
