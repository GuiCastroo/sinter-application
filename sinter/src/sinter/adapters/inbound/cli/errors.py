"""O único lugar que decide código de saída e monta o envelope de erro (AD-33)."""

from typing import Any

from pydantic import BaseModel

from sinter.domain.errors import SinterError
from sinter.domain.model.base import SinterModel
from sinter.ports.inbound.common import Report


class ErrorBody(SinterModel):
    code: str
    message: str
    details: dict[str, Any]


class ErrorEnvelope(SinterModel):
    error: ErrorBody


def exit_code(result: BaseModel) -> int:
    report = getattr(result, "report", None)
    if isinstance(report, Report) and report.errors:
        return 1
    return 0


def envelope(err: SinterError) -> ErrorEnvelope:
    return ErrorEnvelope(error=ErrorBody(code=err.code, message=err.message, details=err.details))


def internal_error(exc: BaseException) -> SinterError:
    return SinterError(
        "INTERNAL_ERROR",
        f"erro interno do Sinter ({type(exc).__name__}); rode de novo com --debug para detalhes",
    )


def usage_error(message: str) -> SinterError:
    return SinterError("USAGE_INVALID_OPTION", message)
