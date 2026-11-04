import pytest
from pydantic import TypeAdapter, ValidationError

from sinter.domain.model.views import (
    DomainLevel0,
    DomainLevel1,
    Inherited,
    Level0View,
    SubdomainLevel0,
)


def domain() -> DomainLevel0:
    return DomainLevel0(id="dom-x", name="X", domain_id="XX", area="area-x")


def test_level0_discriminates_domain() -> None:
    view = TypeAdapter(Level0View).validate_python(domain().model_dump())
    assert isinstance(view, DomainLevel0)
    assert view.domain_id == "XX"


def test_domain_requires_identity_fields() -> None:
    with pytest.raises(ValidationError):
        DomainLevel0(id="dom-x", name="X")


def test_subdomain_has_only_its_level0_fields() -> None:
    view = SubdomainLevel0(id="sub-x", name="Parte", counts={"applications": 0})
    assert "domainId" not in view.model_dump(by_alias=True)
    assert view.counts == {"applications": 0}


def test_unknown_fields_are_rejected() -> None:
    with pytest.raises(ValidationError):
        SubdomainLevel0.model_validate({"id": "sub-x", "name": "X", "area": "area-x"})


def test_level1_fields_are_not_emitted_by_level0() -> None:
    assert "does" not in domain().model_dump()
    view = DomainLevel1(
        **domain().model_dump(),
        does=[],
        does_not=[],
        unknowns=[],
        gaps=[],
        subdomains=[],
        main_journeys=[],
    )
    assert view.model_dump(by_alias=True)["doesNot"] == []
    assert view.level0 == domain()
    assert view.knowledge.rules == []


def test_inherited_value_keeps_origin() -> None:
    value = Inherited[str](value="reg-x", origin="dom-x")
    assert value.model_dump() == {"value": "reg-x", "origin": "dom-x"}


def test_discriminator_rejects_unknown_kind() -> None:
    with pytest.raises(ValidationError):
        TypeAdapter(Level0View).validate_python({"kind": "Typo", "id": "x", "name": "X"})
