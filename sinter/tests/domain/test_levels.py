from dataclasses import replace
from pathlib import Path

from sinter.adapters.inbound.cli.render.json import to_json
from sinter.application.load import load
from sinter.bootstrap import build
from sinter.domain.model.domain import Domain
from sinter.domain.model.subdomain import Subdomain
from sinter.domain.model.views import SubdomainLevel0
from sinter.domain.services import levels
from sinter.domain.services.tokens import count_tokens
from sinter.ports.inbound.get import GetRequest

EXAMPLE = Path(__file__).parents[1] / "fixtures" / "exemplo-catalogo"


def test_domain_summary_and_counts() -> None:
    result = build(EXAMPLE).get(GetRequest(id="dom-pagv", level=0))
    assert result.item.counts == {"subdomains": 3, "applications": 4, "journeys": 2}
    assert result.item.domain_id == "PAGV"
    assert "does" not in result.item.model_dump()


def test_children_follow_summary_order() -> None:
    container = build(EXAMPLE)
    catalog, _ = load(container._catalog_files(), container._codec)
    manifest = catalog.manifest("dom-camb")
    assert isinstance(manifest.model, Domain)
    result = levels.domain_level1(catalog, manifest)
    assert [s.id for s in result.subdomains] == manifest.model.spec.subdomains
    assert all(isinstance(s, SubdomainLevel0) for s in result.subdomains)


def test_candidate_children_not_exposed_in_counts_or_list() -> None:
    container = build(EXAMPLE)
    catalog, _ = load(container._catalog_files(), container._codec)
    sub = catalog.manifest("sub-pagv-checkout")
    assert isinstance(sub.model, Subdomain)
    candidate = sub.model.model_copy(
        update={"metadata": sub.model.metadata.model_copy(update={"status": "candidate"})}
    )
    catalog = replace(
        catalog,
        manifests=tuple(
            replace(m, model=candidate) if m.id == sub.id else m for m in catalog.manifests
        ),
    )
    view = levels.domain_level1(catalog, catalog.manifest("dom-pagv"))
    assert "sub-pagv-checkout" not in [s.id for s in view.subdomains]
    assert view.level0.counts["subdomains"] == 2


def test_empty_lists_are_gaps_not_invented_facts() -> None:
    container = build(EXAMPLE)
    catalog, _ = load(container._catalog_files(), container._codec)
    manifest = catalog.manifest("dom-camb")
    model = manifest.model
    changed = model.model_copy(
        update={"spec": model.spec.model_copy(update={"does": [], "does_not": [], "unknowns": []})}
    )
    view = levels.domain_level1(catalog, replace(manifest, model=changed))
    assert view.does == view.does_not == view.unknowns == []
    assert [g.field for g in view.gaps] == ["does", "doesNot", "unknowns"]


def test_camb_json_token_budgets() -> None:
    container = build(EXAMPLE)
    assert count_tokens(to_json(container.get(GetRequest(id="dom-camb", level=0)))) <= 300
    assert count_tokens(to_json(container.get(GetRequest(id="dom-camb", level=1)))) <= 2000


def test_query_is_byte_deterministic() -> None:
    container = build(EXAMPLE)
    request = GetRequest(id="dom-camb", level=1)
    assert to_json(container.get(request)) == to_json(container.get(request))


def test_omitted_points_to_next_level() -> None:
    assert levels.omitted("dom-pagv", 0, "Domain")[0].command.endswith("--level 1")
    assert levels.omitted("dom-pagv", 1, "Domain")[0].command.endswith("--level 2")


def test_token_heuristic_is_fixed_for_empty_and_rounding() -> None:
    assert [count_tokens(s) for s in ["", "abcd", "abcde"]] == [0, 1, 2]
