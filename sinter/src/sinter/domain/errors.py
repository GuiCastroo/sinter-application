"""Tabela fechada de erros: cada código com o seu código de saída (AD-33, AD-37).

Código novo exige linha aqui. Problema no conteúdo do catálogo NÃO é erro: é Finding.
"""

from typing import Any

ERROR_TABLE: dict[str, int] = {
    # pré-condição de ambiente ou uso errado → 2
    "USAGE_INVALID_OPTION": 2,
    "USAGE_NOT_A_CATALOG": 2,
    "USAGE_INIT_NOT_EMPTY": 2,
    "USAGE_NOT_A_GIT_REPO": 2,
    "USAGE_GIT_NOT_FOUND": 2,
    # item ou recurso pedido não pode ser atendido → 1
    "CATALOG_VERSION_UNSUPPORTED": 1,
    "ITEM_NOT_FOUND": 1,
    "ANCHOR_NOT_FOUND": 1,
    "FILE_DIRTY": 1,
    "ID_ALREADY_EXISTS": 1,
    "AREA_NOT_FOUND": 1,
    "SKILL_FILE_MODIFIED": 1,
    # bug → 3
    "INTERNAL_ERROR": 3,
}


class SinterError(Exception):
    def __init__(self, code: str, message: str, details: dict[str, Any] | None = None) -> None:
        if code not in ERROR_TABLE:
            raise ValueError(f"código de erro fora da tabela: {code}")
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}

    @property
    def exit_code(self) -> int:
        return ERROR_TABLE[self.code]
