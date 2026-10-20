import pytest

from sinter.adapters.outbound.memory.files import MemoryCatalogFiles
from sinter.bootstrap import build
from sinter.ports.inbound.validate import ValidateRequest, ValidateResult

ORG = """apiVersion: sinter.dev/v1
kind: Organization
metadata: { id: org-acme, name: ACME, status: approved }
spec:
  schemaVersion: 1
  areas:
    - { id: area-varejo, name: Varejo }
    - { id: area-atacado, name: Atacado }
"""

DOMAIN = """apiVersion: sinter.dev/v1
kind: Domain
metadata:
  id: {id}
  name: {name}
  domainId: {domain_id}
  area: {area}
  status: approved
spec:
  parent: org-acme
  purpose: Recebe e autoriza pagamentos.
  subdomains: []
{extra}"""


def _domain(
    id: str = "dom-pagv",
    name: str = "Pagamentos",
    domain_id: str = "PAGV",
    area: str = "area-varejo",
    extra: str = "",
) -> str:
    return DOMAIN.format(id=id, name=name, domain_id=domain_id, area=area, extra=extra)


def _validate(files: dict[str, str]) -> ValidateResult:
    all_files = {"organization.yaml": ORG, **files}
    return build(None, files=MemoryCatalogFiles(all_files)).validate(ValidateRequest())


def _errors(result: ValidateResult) -> set[tuple[str, str]]:
    return {(f.code, f.path) for f in result.report.errors}


def test_dominio_minimo_valido() -> None:
    result = _validate({"domains/pagv/domain.yaml": _domain()})
    assert result.report.errors == []


def test_dominio_sem_proposito() -> None:
    text = _domain().replace("  purpose: Recebe e autoriza pagamentos.\n", "")
    assert ("SCHEMA_REQUIRED_FIELD", "spec.purpose") in _errors(
        _validate({"domains/pagv/domain.yaml": text})
    )


@pytest.mark.parametrize("domain_id", ["pagv", "P", "PAGAMENTOS9", "PA-GV"])
def test_id_dominio_fora_do_formato(domain_id: str) -> None:
    folder = domain_id.lower()
    result = _validate({f"domains/{folder}/domain.yaml": _domain(domain_id=domain_id)})
    assert ("DOMAIN_ID_FORMAT_INVALID", "metadata.domainId") in _errors(result)


def test_id_dominio_repetido_cita_os_dois_arquivos() -> None:
    result = _validate(
        {
            "domains/pagv/domain.yaml": _domain(),
            "domains/pagv2/domain.yaml": _domain(id="dom-pagv2", domain_id="PAGV"),
        }
    )
    dup = next(f for f in result.report.errors if f.code == "DOMAIN_ID_DUPLICATE")
    assert dup.related[0].file in {"domains/pagv/domain.yaml", "domains/pagv2/domain.yaml"}
    assert dup.file != dup.related[0].file


def test_pasta_que_nao_bate_com_id_dominio() -> None:
    result = _validate({"domains/pagamentos/domain.yaml": _domain()})
    assert ("FILE_NOT_CANONICAL", "kind") in _errors(result)


def test_pasta_em_minusculas_bate_com_id_em_maiusculas() -> None:
    assert _validate({"domains/pagv/domain.yaml": _domain()}).report.errors == []


def test_mesmo_nome_em_areas_diferentes_e_permitido() -> None:
    result = _validate(
        {
            "domains/pagv/domain.yaml": _domain(),
            "domains/paga/domain.yaml": _domain(
                id="dom-paga", domain_id="PAGA", area="area-atacado"
            ),
        }
    )
    assert result.report.errors == []


def test_area_que_nao_existe() -> None:
    result = _validate({"domains/pagv/domain.yaml": _domain(area="area-cambio")})
    assert ("DOMAIN_AREA_NOT_FOUND", "metadata.area") in _errors(result)


def test_pai_que_nao_e_a_organizacao() -> None:
    text = _domain().replace("parent: org-acme", "parent: org-outra")
    result = _validate({"domains/pagv/domain.yaml": text})
    assert ("DOMAIN_PARENT_NOT_ORGANIZATION", "spec.parent") in _errors(result)


@pytest.mark.parametrize("campo", ["boundaries", "repositories", "journeys"])
def test_campo_calculado_escrito(campo: str) -> None:
    result = _validate({"domains/pagv/domain.yaml": _domain(extra=f"  {campo}: []\n")})
    assert _errors(result) == {("CALC_FIELD_WRITTEN", f"spec.{campo}")}


DECISION = """  decisions:
    - id: {id}
      title: T
      date: 2026-01-01
      context: C
      decision: D
"""


def test_adr_com_id_de_outro_dominio() -> None:
    extra = DECISION.format(id="ADR-CAMB-001")
    result = _validate({"domains/pagv/domain.yaml": _domain(extra=extra)})
    assert ("ADR_DOMAIN_MISMATCH", "spec.decisions[ADR-CAMB-001]") in _errors(result)


def test_adr_fora_do_formato() -> None:
    extra = DECISION.format(id="ADR-PAGV-1")
    result = _validate({"domains/pagv/domain.yaml": _domain(extra=extra)})
    assert ("ID_FORMAT_INVALID", "spec.decisions[ADR-PAGV-1]") in _errors(result)


def test_regra_repetida_entre_dominios() -> None:
    rule = "  rules:\n    - { id: rule-x-estorno, statement: S }\n"
    result = _validate(
        {
            "domains/pagv/domain.yaml": _domain(extra=rule),
            "domains/paga/domain.yaml": _domain(
                id="dom-paga", domain_id="PAGA", area="area-atacado", extra=rule
            ),
        }
    )
    assert ("DUPLICATE_ID", "spec.rules[rule-x-estorno]") in _errors(result)


def test_regra_fora_do_prefixo() -> None:
    rule = "  rules:\n    - { id: regra-estorno, statement: S }\n"
    result = _validate({"domains/pagv/domain.yaml": _domain(extra=rule)})
    assert ("ID_FORMAT_INVALID", "spec.rules[regra-estorno]") in _errors(result)


def test_operacao_e_glossario_no_formato_dos_blocos() -> None:
    extra = "  operation: { criticality: urgente }\n  glossary:\n    - { term: Boleta }\n"
    errors = _errors(_validate({"domains/pagv/domain.yaml": _domain(extra=extra)}))
    assert ("SCHEMA_INVALID_VALUE", "spec.operation.criticality") in errors
    assert ("SCHEMA_REQUIRED_FIELD", "spec.glossary[0].definition") in errors
