from sinter.adapters.outbound.memory.files import MemoryCatalogFiles
from sinter.bootstrap import build
from sinter.ports.inbound.validate import ValidateRequest, ValidateResult

ORG = """apiVersion: sinter.dev/v1
kind: Organization
metadata: { id: org-acme, name: ACME, status: approved }
spec:
  schemaVersion: 1
  areas: [{ id: area-varejo, name: Varejo }]
  dataLayers: [{ id: raw, name: Raw }, { id: refined, name: Refined }]
"""

REPOS = """apiVersion: sinter.dev/v1
kind: RepositoryList
metadata: { id: repositories, name: Repos, status: approved }
spec:
  repositories:
    - { id: repo-api, url: "git@x:api.git" }
    - { id: repo-mainframe, url: "git@x:mf.git" }
"""

DOMAIN = """apiVersion: sinter.dev/v1
kind: Domain
metadata: {{ id: dom-pagv, name: Pagamentos, domainId: PAGV, area: area-varejo, status: approved }}
spec:
  parent: org-acme
  purpose: Paga.
  subdomains: [{summary}]
"""

SUB = """apiVersion: sinter.dev/v1
kind: Subdomain
metadata: {{ id: {id}, name: S, domain: {domain}, status: approved }}
spec:
  purpose: Faz uma parte.
{extra}"""

APP = """  applications:
    - id: {app_id}
      name: App
      lifecycle: {lifecycle}
      repositories:
        - {{ repo: {repo}, role: {role}, platform: java }}
"""


def _sub(id: str = "sub-pagv-checkout", domain: str = "dom-pagv", extra: str = "") -> str:
    return SUB.format(id=id, domain=domain, extra=extra)


def _app(
    app_id: str = "app-pagv-checkout",
    lifecycle: str = "modern",
    repo: str = "repo-api",
    role: str = "api",
) -> str:
    return APP.format(app_id=app_id, lifecycle=lifecycle, repo=repo, role=role)


def _validate(summary: str, subs: dict[str, str]) -> ValidateResult:
    files = {
        "organization.yaml": ORG,
        "repositories.yaml": REPOS,
        "domains/pagv/domain.yaml": DOMAIN.format(summary=summary),
        **{f"domains/pagv/subdomains/{k}.yaml": v for k, v in subs.items()},
    }
    return build(None, files=MemoryCatalogFiles(files)).validate(ValidateRequest())


def _errors(result: ValidateResult) -> set[tuple[str, str]]:
    return {(f.code, f.path) for f in result.report.errors}


def test_subdominio_com_aplicacao_valido() -> None:
    result = _validate("sub-pagv-checkout", {"sub-pagv-checkout": _sub(extra=_app())})
    assert result.report.errors == []


def test_dominio_do_subdominio_nao_existe() -> None:
    result = _validate("", {"sub-pagv-checkout": _sub(domain="dom-nada")})
    assert ("SUBDOMAIN_DOMAIN_NOT_FOUND", "metadata.domain") in _errors(result)


def test_sumario_com_subdominio_sem_arquivo() -> None:
    result = _validate("sub-pagv-checkout, sub-pagv-fantasma", {"sub-pagv-checkout": _sub()})
    finding = next(f for f in result.report.errors if f.code == "SUBDOMAIN_SUMMARY_MISMATCH")
    assert finding.path == "spec.subdomains[1]"
    assert "sub-pagv-fantasma" in finding.message


def test_sumario_sem_um_subdominio_que_existe() -> None:
    result = _validate("", {"sub-pagv-checkout": _sub()})
    finding = next(f for f in result.report.errors if f.code == "SUBDOMAIN_SUMMARY_MISMATCH")
    assert "falta 'sub-pagv-checkout'" in finding.message


def test_sumario_com_subdominio_repetido() -> None:
    result = _validate("sub-pagv-checkout, sub-pagv-checkout", {"sub-pagv-checkout": _sub()})
    assert ("SUBDOMAIN_SUMMARY_MISMATCH", "spec.subdomains[1]") in _errors(result)


def test_subdominio_invalido_nao_gera_erro_falso_no_sumario() -> None:
    broken = _sub(extra="  does: [x]\n").replace("  purpose: Faz uma parte.\n", "")
    codes = {c for c, _ in _errors(_validate("sub-pagv-checkout", {"sub-pagv-checkout": broken}))}
    assert codes == {"SCHEMA_REQUIRED_FIELD"}


def test_subdominio_fora_da_pasta_do_dominio() -> None:
    files = {
        "organization.yaml": ORG,
        "repositories.yaml": REPOS,
        "domains/pagv/domain.yaml": DOMAIN.format(summary="sub-pagv-checkout"),
        "domains/outro/subdomains/sub-pagv-checkout.yaml": _sub(),
    }
    result = build(None, files=MemoryCatalogFiles(files)).validate(ValidateRequest())
    assert ("FILE_NOT_CANONICAL", "kind") in _errors(result)


def test_aplicacao_sem_lifecycle_valido() -> None:
    result = _validate(
        "sub-pagv-checkout", {"sub-pagv-checkout": _sub(extra=_app(lifecycle="antigo"))}
    )
    assert (
        "SCHEMA_INVALID_VALUE",
        "spec.applications[app-pagv-checkout].lifecycle",
    ) in _errors(result)


def test_aplicacao_com_id_de_outro_dominio() -> None:
    result = _validate(
        "sub-pagv-checkout", {"sub-pagv-checkout": _sub(extra=_app(app_id="app-camb-x"))}
    )
    assert ("APP_ID_DOMAIN_MISMATCH", "spec.applications[app-camb-x].id") in _errors(result)


def test_repo_que_nao_existe_e_papel_invalido() -> None:
    extra = _app(repo="repo-nada", role="servico")
    errors = _errors(_validate("sub-pagv-checkout", {"sub-pagv-checkout": _sub(extra=extra)}))
    assert (
        "SCHEMA_INVALID_VALUE",
        "spec.applications[app-pagv-checkout].repositories[0].role",
    ) in errors
    extra = _app(repo="repo-nada")
    errors = _errors(_validate("sub-pagv-checkout", {"sub-pagv-checkout": _sub(extra=extra)}))
    assert (
        "APP_REPO_NOT_FOUND",
        "spec.applications[app-pagv-checkout].repositories[0].repo",
    ) in errors


def test_mesmo_repo_em_duas_aplicacoes_e_permitido() -> None:
    extra = _app() + _app(app_id="app-pagv-checkout-2").replace("  applications:\n", "")
    result = _validate("sub-pagv-checkout", {"sub-pagv-checkout": _sub(extra=extra)})
    assert result.report.errors == []


def test_aplicacao_repetida_em_dois_subdominios() -> None:
    result = _validate(
        "sub-pagv-checkout, sub-pagv-outro",
        {
            "sub-pagv-checkout": _sub(extra=_app()),
            "sub-pagv-outro": _sub(id="sub-pagv-outro", extra=_app()),
        },
    )
    dup = next(f for f in result.report.errors if f.code == "DUPLICATE_ID")
    assert dup.related[0].file != dup.file


DATA = """  data:
    - id: dat-pagv-vendas
      name: Vendas
      producedBy: {producer}
      personalData: true
      layers:
        {layer}: {{ location: "s3://x" }}
"""


def test_dado_com_camada_e_produtor_validos() -> None:
    extra = _app() + DATA.format(producer="app-pagv-checkout", layer="raw")
    result = _validate("sub-pagv-checkout", {"sub-pagv-checkout": _sub(extra=extra)})
    assert result.report.errors == []


def test_dado_com_camada_e_produtor_inexistentes() -> None:
    extra = DATA.format(producer="app-pagv-nada", layer="gold")
    errors = _errors(_validate("sub-pagv-checkout", {"sub-pagv-checkout": _sub(extra=extra)}))
    assert ("DATA_LAYER_NOT_FOUND", "spec.data[dat-pagv-vendas].layers.gold") in errors
    assert ("DATA_PRODUCER_NOT_FOUND", "spec.data[dat-pagv-vendas].producedBy") in errors
