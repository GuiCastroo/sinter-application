from sinter.adapters.outbound.memory.files import MemoryCatalogFiles
from sinter.bootstrap import build
from sinter.ports.inbound.validate import ValidateRequest, ValidateResult

BASE = {
    "organization.yaml": """apiVersion: sinter.dev/v1
kind: Organization
metadata: { id: org-acme, name: ACME, status: approved }
spec:
  schemaVersion: 1
  areas: [{ id: area-varejo, name: Varejo }]
""",
    "repositories.yaml": """apiVersion: sinter.dev/v1
kind: RepositoryList
metadata: { id: repositories, name: Repos, status: approved }
spec:
  repositories: [{ id: repo-api, url: "git@x:api.git" }]
""",
    "domains/pagv/domain.yaml": """apiVersion: sinter.dev/v1
kind: Domain
metadata: { id: dom-pagv, name: P, domainId: PAGV, area: area-varejo, status: approved }
spec:
  parent: org-acme
  purpose: Paga.
  subdomains: [sub-pagv-checkout]
  rules: [{ id: rule-pagv-x, statement: S }]
""",
    "domains/pagv/subdomains/sub-pagv-checkout.yaml": """apiVersion: sinter.dev/v1
kind: Subdomain
metadata: { id: sub-pagv-checkout, name: C, domain: dom-pagv, status: approved }
spec:
  purpose: Checkout.
  applications:
    - id: app-pagv-velho
      name: Velho
      lifecycle: legacy
      repositories: [{ repo: repo-api, role: batch, platform: mainframe }]
    - id: app-pagv-novo
      name: Novo
      lifecycle: modern
      repositories: [{ repo: repo-api, role: api, platform: java }]
""",
}

JOURNEY = """apiVersion: sinter.dev/v1
kind: Journey
metadata: {{ id: jor-pagv-pagar, name: Pagar, domain: dom-pagv, status: approved }}
spec:
  purpose: Pagar.
  trigger: Cliente clica.
  outcome: Pago.
{extra}  stages:
    - id: pagar
      steps:
{steps}"""

STEP_A = """        - id: escolher
          capability: {capability}
          action: Escolhe
          next: [{next}]
"""
STEP_B = """        - id: capturar
          capability: sub-pagv-checkout
          calls: {calls}
          action: Captura
          next: [escolher]
"""


def _journey(
    capability: str = "sub-pagv-checkout",
    next_: str = "capturar",
    calls: str = "ext-adquirente",
    extra: str = "",
) -> str:
    steps = STEP_A.format(capability=capability, next=next_) + STEP_B.format(calls=calls)
    return JOURNEY.format(extra=extra, steps=steps)


def _validate(extra_files: dict[str, str]) -> ValidateResult:
    files = {**BASE, **extra_files}
    return build(None, files=MemoryCatalogFiles(files)).validate(ValidateRequest())


def _errors(result: ValidateResult) -> set[tuple[str, str]]:
    return {(f.code, f.path) for f in result.report.errors}


JPATH = "domains/pagv/journeys/jor-pagv-pagar.yaml"


def test_jornada_valida_com_ciclo_de_retentativa() -> None:
    assert _validate({JPATH: _journey()}).report.errors == []


def test_passo_com_subdominio_inexistente() -> None:
    errors = _errors(_validate({JPATH: _journey(capability="sub-pagv-nada")}))
    assert ("JOURNEY_REF_NOT_FOUND", "spec.stages[pagar].steps[escolher].capability") in errors


def test_passo_sem_capability_e_sem_calls() -> None:
    text = _journey().replace("          capability: sub-pagv-checkout\n", "", 1)
    errors = _errors(_validate({JPATH: text}))
    assert ("SCHEMA_INVALID_VALUE", "spec.stages[pagar].steps[escolher]") in errors


def test_next_para_passo_que_nao_existe() -> None:
    errors = _errors(_validate({JPATH: _journey(next_="sumiu")}))
    assert ("JOURNEY_STEP_LINK_NOT_FOUND", "spec.stages[pagar].steps[escolher].next[0]") in errors


def test_passo_repetido_na_jornada() -> None:
    text = (
        _journey().replace("id: capturar", "id: escolher").replace("next: [escolher]", "next: []")
    )
    text = text.replace("next: [capturar]", "next: []")
    codes = {c for c, _ in _errors(_validate({JPATH: text}))}
    assert "JOURNEY_LOCAL_ID_INVALID" in codes


def test_ids_de_passo_iguais_em_jornadas_diferentes_sao_permitidos() -> None:
    other = _journey().replace("jor-pagv-pagar", "jor-pagv-outra")
    result = _validate({JPATH: _journey(), "domains/pagv/journeys/jor-pagv-outra.yaml": other})
    assert result.report.errors == []


def test_referencias_de_passo_inexistentes() -> None:
    step = """        - id: avisar
          capability: sub-pagv-checkout
          action: Avisa
          application: app-pagv-nada
          rules: [rule-pagv-nada]
          governedBy: [reg-nada]
"""
    text = JOURNEY.format(extra="  variantOf: jor-pagv-nada\n", steps=step)
    errors = _errors(_validate({JPATH: text}))
    base = "spec.stages[pagar].steps[avisar]"
    assert ("JOURNEY_REF_NOT_FOUND", f"{base}.application") in errors
    assert ("JOURNEY_REF_NOT_FOUND", f"{base}.rules[0]") in errors
    assert ("JOURNEY_REF_NOT_FOUND", f"{base}.governedBy[0]") in errors
    assert ("JOURNEY_REF_NOT_FOUND", "spec.variantOf") in errors


def test_ext_evt_agenda_so_formato() -> None:
    ok = _validate({JPATH: _journey(calls="ext-swift", extra="  orchestrator: agenda-noturna\n")})
    assert ok.report.errors == []
    bad = _errors(_validate({JPATH: _journey(calls="swift", extra="  orchestrator: cron\n")}))
    assert ("JOURNEY_REF_FORMAT_INVALID", "spec.stages[pagar].steps[capturar].calls") in bad
    assert ("JOURNEY_REF_FORMAT_INVALID", "spec.orchestrator") in bad


RELATION = """apiVersion: sinter.dev/v1
kind: Relation
metadata:
  id: {id}
  name: Velho substituído pelo novo
  domain: dom-pagv
  status: approved
spec:
  source: {source}
  type: {type}
  target: app-pagv-novo
  phase: {phase}
  evidence:
    - {{ source: conversation/2026-10-01, locator: "#msg-3", extraction: human }}
"""
REL_ID = "rel-app-pagv-velho--modernized_by--app-pagv-novo"


def _relation(
    id: str = REL_ID,
    source: str = "app-pagv-velho",
    type: str = "modernized_by",
    phase: str = "planned",
) -> dict[str, str]:
    text = RELATION.format(id=id, source=source, type=type, phase=phase)
    return {f"domains/pagv/relations/{id}.yaml": text}


def test_relacao_valida() -> None:
    assert _validate(_relation()).report.errors == []


def test_relacao_tipo_e_fase_invalidos() -> None:
    errors = _errors(_validate(_relation(type="calls", phase="feito")))
    assert ("SCHEMA_INVALID_VALUE", "spec.type") in errors
    assert ("SCHEMA_INVALID_VALUE", "spec.phase") in errors


def test_relacao_com_aplicacao_inexistente_e_id_que_nao_bate() -> None:
    errors = _errors(_validate(_relation(source="app-pagv-sumiu")))
    assert ("RELATION_ENDPOINT_NOT_FOUND", "spec.source") in errors
    assert ("RELATION_ID_MISMATCH", "metadata.id") in errors


def test_relacao_fora_do_lugar() -> None:
    files = _relation()
    text = next(iter(files.values()))
    errors = _errors(_validate({"domains/pagv/relations/outro-nome.yaml": text}))
    assert ("FILE_NOT_CANONICAL", "kind") in errors
