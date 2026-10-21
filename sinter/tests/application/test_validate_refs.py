from sinter.adapters.outbound.memory.files import MemoryCatalogFiles
from sinter.bootstrap import build
from sinter.domain.validation.finding import Finding
from sinter.ports.inbound.validate import ValidateRequest, ValidateResult

ORG = """apiVersion: sinter.dev/v1
kind: Organization
metadata: { id: org-acme, name: ACME, status: approved }
spec:
  schemaVersion: 1
  areas: [{ id: area-varejo, name: Varejo }]
  glossary:
    - { term: "PF / PJ", definition: "Pessoa física / jurídica." }
"""

REG = """apiVersion: sinter.dev/v1
kind: Regulation
metadata: { id: reg-lgpd, name: LGPD, status: approved }
spec:
  jurisdiction: BR
  effective: { from: 2020-09-18 }
"""

DOMAIN = """apiVersion: sinter.dev/v1
kind: Domain
metadata: {{ id: dom-pagv, name: P, domainId: PAGV, area: area-varejo, status: approved }}
spec:
  parent: org-acme
  purpose: Paga.
  subdomains: [sub-pagv-checkout]
  regulations: [reg-lgpd]
{extra}"""

SUB = """apiVersion: sinter.dev/v1
kind: Subdomain
metadata: {{ id: sub-pagv-checkout, name: C, domain: dom-pagv, status: approved }}
spec:
  purpose: Checkout.
{extra}"""


def _validate(
    domain_extra: str = "", sub_extra: str = "", other: dict[str, str] | None = None
) -> ValidateResult:
    files = {
        "organization.yaml": ORG,
        "regulations/reg-lgpd.yaml": REG,
        "domains/pagv/domain.yaml": DOMAIN.format(extra=domain_extra),
        "domains/pagv/subdomains/sub-pagv-checkout.yaml": SUB.format(extra=sub_extra),
        **(other or {}),
    }
    return build(None, files=MemoryCatalogFiles(files)).validate(ValidateRequest())


def _codes(findings: list[Finding]) -> set[tuple[str, str]]:
    return {(f.code, f.path) for f in findings}


def test_referencias_internas_inexistentes() -> None:
    extra = (
        "  standards: [std-nada]\n"
        "  mainJourneys: [jor-nada]\n"
        "  sharedRepositories: [repo-nada]\n"
        "  modernization: { goal: G, decision: ADR-PAGV-009 }\n"
        "  rules:\n    - { id: rule-pagv-a, statement: S, regulations: [reg-nada] }\n"
    )
    errors = _codes(_validate(domain_extra=extra).report.errors)
    assert ("REF_NOT_FOUND", "spec.standards[0]") in errors
    assert ("REF_NOT_FOUND", "spec.mainJourneys[0]") in errors
    assert ("REF_NOT_FOUND", "spec.sharedRepositories[0]") in errors
    assert ("REF_NOT_FOUND", "spec.modernization.decision") in errors
    assert ("REF_NOT_FOUND", "spec.rules[rule-pagv-a].regulations[0]") in errors


def test_evidencia_e_supersedes_de_adr() -> None:
    extra = """  decisions:
    - id: ADR-PAGV-002
      title: T
      date: 2026-01-01
      context: C
      decision: D
      supersedes: ADR-PAGV-001
      evidence: [{ source: doc-pagv-ata, locator: "docs/a.md#x", extraction: human }]
"""
    errors = _codes(_validate(domain_extra=extra).report.errors)
    assert ("REF_NOT_FOUND", "spec.decisions[ADR-PAGV-002].supersedes") in errors
    assert ("REF_NOT_FOUND", "spec.decisions[ADR-PAGV-002].evidence[0].source") in errors


def test_dom_fora_do_catalogo_e_aviso_e_ext_so_formato() -> None:
    extra = """  boundaries:
    in:  [{ from: ext-adquirente, what: arquivo }]
    out: [{ to: dom-financeiro, what: rel }, { to: sub-pagv-nada, what: x }, { to: banco, what: y }]
"""
    result = _validate(sub_extra=extra)
    assert _codes(result.report.warnings) == {
        ("DOM_REF_NOT_IN_CATALOG", "spec.boundaries.out[0].to")
    }
    errors = _codes(result.report.errors)
    assert ("REF_NOT_FOUND", "spec.boundaries.out[1].to") in errors
    assert ("REF_FORMAT_INVALID", "spec.boundaries.out[2].to") in errors
    assert ("REF_FORMAT_INVALID", "spec.boundaries.in[0].from") not in errors


def test_docs_path_ou_url_tipo_e_arquivo() -> None:
    extra = """  docs:
    - { title: Sem nada, type: negocio }
    - { title: Os dois, type: negocio, path: docs/a.md, url: "https://x" }
    - { title: Tipo errado, type: memorando, url: "https://x" }
    - { title: Sumiu, type: runbook, path: docs/sumiu.md }
    - { title: Existe, type: runbook, path: docs/runbook.md }
    - { ref: doc-pagv-nada }
"""
    other = {"domains/pagv/docs/runbook.md": "# Runbook\n"}
    errors = _codes(_validate(domain_extra=extra, other=other).report.errors)
    assert ("DOC_PATH_OR_URL", "spec.docs[0]") in errors
    assert ("DOC_PATH_OR_URL", "spec.docs[1]") in errors
    assert ("DOC_TYPE_UNKNOWN", "spec.docs[2].type") in errors
    assert ("DOC_PATH_NOT_FOUND", "spec.docs[3].path") in errors
    assert ("DOC_PATH_NOT_FOUND", "spec.docs[4].path") not in errors
    assert ("DOC_REF_NOT_FOUND", "spec.docs[5].ref") in errors


def test_glossario_redefinido_na_mesma_linha() -> None:
    domain = "  glossary:\n    - { term: Boleta, definition: Registro da operação. }\n"
    sub = "  glossary:\n    - { term: boleta, definition: Outra coisa. }\n"
    result = _validate(domain_extra=domain, sub_extra=sub)
    finding = next(f for f in result.report.errors if f.code == "GLOSSARY_TERM_REDEFINED")
    assert finding.file == "domains/pagv/subdomains/sub-pagv-checkout.yaml"
    assert finding.related[0].file == "domains/pagv/domain.yaml"


def test_glossario_redefine_termo_da_organizacao_por_sinonimo() -> None:
    domain = "  glossary:\n    - { term: Pessoa, definition: X, synonyms: ['pf / pj'] }\n"
    codes = {f.code for f in _validate(domain_extra=domain).report.errors}
    assert "GLOSSARY_TERM_REDEFINED" in codes


def test_mesmo_termo_em_dominios_diferentes_e_permitido() -> None:
    term = "  glossary:\n    - { term: Conta, definition: X }\n"
    other_domain = (
        DOMAIN.format(extra=term)
        .replace("dom-pagv", "dom-cont")
        .replace("PAGV", "CONT")
        .replace("subdomains: [sub-pagv-checkout]", "subdomains: []")
    )
    result = _validate(domain_extra=term, other={"domains/cont/domain.yaml": other_domain})
    assert result.report.errors == []


def test_subdominio_repete_o_que_herda_e_aviso() -> None:
    result = _validate(sub_extra="  regulations: [reg-lgpd]\n")
    assert result.report.errors == []
    assert _codes(result.report.warnings) == {("INHERITED_REPEATED", "spec.regulations[0]")}
