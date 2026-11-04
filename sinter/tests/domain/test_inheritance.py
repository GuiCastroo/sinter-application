from pathlib import Path

from sinter.application.load import load
from sinter.bootstrap import build
from sinter.domain.model.blocks import Operation
from sinter.domain.model.catalog import Catalog
from sinter.domain.model.domain import Domain
from sinter.domain.model.subdomain import Subdomain
from sinter.domain.services import inheritance

EXAMPLE = Path(__file__).parents[1] / "fixtures" / "exemplo-catalogo"


def items() -> tuple[Catalog, Domain, Subdomain]:
    container = build(EXAMPLE)
    catalog, _ = load(container._catalog_files(), container._codec)
    domain = catalog.manifest("dom-pagv").model
    sub = catalog.manifest("sub-pagv-conciliacao").model
    assert isinstance(domain, Domain) and isinstance(sub, Subdomain)
    return catalog, domain, sub


def test_subdomain_inherits_domain_rules_and_origin() -> None:
    catalog, domain, sub = items()
    knowledge = inheritance.subdomain_knowledge(catalog, sub, domain)
    for rule in domain.spec.rules:
        assert any(r.id == rule.id and r.origin == domain.metadata.id for r in knowledge.rules)


def test_domain_inherits_organization_glossary() -> None:
    catalog, domain, _ = items()
    knowledge = inheritance.domain_knowledge(catalog, domain)
    assert any(term.origin == "org-acme" for term in knowledge.glossary)


def test_own_and_inherited_regulations_are_not_repeated() -> None:
    catalog, domain, sub = items()
    knowledge = inheritance.subdomain_knowledge(catalog, sub, domain)
    ids = [ref.id for ref in knowledge.regulations]
    assert len(ids) == len(set(ids))
    assert set(domain.spec.regulations) <= set(ids)


def test_operation_inherits_only_undeclared_fields() -> None:
    _, domain, sub = items()
    parent = domain.model_copy(
        update={
            "spec": domain.spec.model_copy(
                update={
                    "operation": Operation(
                        hours="9–17", batch_windows=["18–20"], criticality="alta"
                    )
                }
            )
        }
    )
    child = sub.model_copy(
        update={
            "spec": sub.spec.model_copy(
                update={"operation": Operation(hours="24h", batch_windows=[])}
            )
        }
    )
    op = inheritance.operation(child, parent)
    assert op.value.hours == "24h"
    assert op.value.batch_windows == []
    assert op.value.criticality == "alta"
    assert op.inherited_fields == ["criticality"]
    assert op.inherited_from == "dom-pagv"


def test_absent_operation_inherits_whole_value() -> None:
    _, domain, sub = items()
    domain = domain.model_copy(
        update={"spec": domain.spec.model_copy(update={"operation": Operation(hours="9–17")})}
    )
    sub = sub.model_copy(update={"spec": sub.spec.model_copy(update={"operation": None})})
    op = inheritance.operation(sub, domain)
    assert op.value == domain.spec.operation
    assert op.origin == "dom-pagv"


def test_no_parent_preserves_own_knowledge() -> None:
    catalog, _, sub = items()
    knowledge = inheritance.subdomain_knowledge(catalog, sub, None)
    assert all(r.origin == sub.metadata.id for r in knowledge.rules)


def test_doc_reference_is_resolved_to_facts() -> None:
    catalog, domain, sub = items()
    docs = inheritance.catalog_docs(catalog)
    assert docs
    key = sorted(docs)[0]
    from sinter.domain.model.blocks import Doc

    sub = sub.model_copy(update={"spec": sub.spec.model_copy(update={"docs": [Doc(ref=key)]})})
    knowledge = inheritance.subdomain_knowledge(catalog, sub, domain)
    assert knowledge.docs[0].title == docs[key].title
    assert knowledge.docs[0].origin == sub.metadata.id


def test_no_operation_anywhere_returns_none() -> None:
    _, _, sub = items()
    sub = sub.model_copy(update={"spec": sub.spec.model_copy(update={"operation": None})})
    assert inheritance.operation(sub, None) is None
