"""Jornadas: passos ligados a subdomínios e grafo de passos fechado (FR-11, FR-12)."""

from collections import Counter
from collections.abc import Iterable

from sinter.domain.model.catalog import Catalog, ParsedManifest
from sinter.domain.model.journey import Journey
from sinter.domain.model.registry import (
    EVENT_ID,
    EXTERNAL_ID,
    ID_SLUG,
    SCHEDULER_ID,
)
from sinter.domain.validation.engine import FileFacts, Problem, problem, rule
from sinter.domain.validation.finding import ERROR, Segment


def _journeys(catalog: Catalog) -> Iterable[tuple[ParsedManifest, Journey]]:
    for m in catalog.valid_manifests("Journey"):
        assert isinstance(m.model, Journey)
        yield m, m.model


def _ids(catalog: Catalog, kind: str) -> set[str]:
    return {e.id for e in catalog.entries if e.kind == kind}


def _steps(j: Journey) -> Iterable[tuple[tuple[Segment, ...], int, object]]:
    for si, stage in enumerate(j.spec.stages):
        for pi, step in enumerate(stage.steps):
            yield ("spec", "stages", si, "steps", pi), pi, step


@rule(code="JOURNEY_LOCAL_ID_INVALID", severity=ERROR)
def local_ids(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    """Etapas e passos têm id curto, único dentro da jornada (AD-41)."""
    for m, j in _journeys(catalog):
        stage_ids = Counter(s.id for s in j.spec.stages)
        step_ids = Counter(p.id for s in j.spec.stages for p in s.steps)
        for si, stage in enumerate(j.spec.stages):
            if not ID_SLUG.match(stage.id) or stage_ids[stage.id] > 1:
                yield problem(
                    m,
                    "spec",
                    "stages",
                    si,
                    "id",
                    message=f"etapa '{stage.id}' inválida ou repetida",
                )
            for pi, step in enumerate(stage.steps):
                if not ID_SLUG.match(step.id) or step_ids[step.id] > 1:
                    yield problem(
                        m,
                        "spec",
                        "stages",
                        si,
                        "steps",
                        pi,
                        "id",
                        message=f"passo '{step.id}' inválido ou repetido na jornada",
                    )


@rule(code="JOURNEY_STEP_LINK_NOT_FOUND", severity=ERROR)
def step_links(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    """`next` e `parallelWith` apontam para passos da MESMA jornada (ciclos são permitidos)."""
    for m, j in _journeys(catalog):
        steps = {p.id for s in j.spec.stages for p in s.steps}
        for si, stage in enumerate(j.spec.stages):
            for pi, step in enumerate(stage.steps):
                for field_name, targets in (
                    ("next", step.next),
                    ("parallelWith", step.parallel_with),
                ):
                    for ti, target in enumerate(targets):
                        if target not in steps:
                            yield problem(
                                m,
                                "spec",
                                "stages",
                                si,
                                "steps",
                                pi,
                                field_name,
                                ti,
                                message=f"passo '{target}' não existe nesta jornada",
                            )


@rule(code="JOURNEY_REF_NOT_FOUND", severity=ERROR)
def references(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    subdomains = _ids(catalog, "Subdomain")
    apps = _ids(catalog, "Application")
    rules = _ids(catalog, "Rule")
    regulations = _ids(catalog, "Regulation")
    journeys = _ids(catalog, "Journey")
    for m, j in _journeys(catalog):
        if j.spec.variant_of is not None and j.spec.variant_of not in journeys:
            yield problem(
                m, "spec", "variantOf", message=f"jornada '{j.spec.variant_of}' não existe"
            )
        orch = j.spec.orchestrator
        if orch is not None and orch.startswith("app-") and orch not in apps:
            yield problem(m, "spec", "orchestrator", message=f"aplicação '{orch}' não existe")
        for si, stage in enumerate(j.spec.stages):
            for pi, step in enumerate(stage.steps):
                base: tuple[Segment, ...] = ("spec", "stages", si, "steps", pi)
                if step.capability is not None and step.capability not in subdomains:
                    yield problem(
                        m,
                        *base,
                        "capability",
                        message=f"subdomínio '{step.capability}' não existe no catálogo",
                    )
                if step.application is not None and step.application not in apps:
                    yield problem(
                        m,
                        *base,
                        "application",
                        message=f"aplicação '{step.application}' não existe no catálogo",
                    )
                for ri, rule_id in enumerate(step.rules):
                    if rule_id not in rules:
                        yield problem(
                            m, *base, "rules", ri, message=f"regra '{rule_id}' não existe"
                        )
                for gi, reg in enumerate(step.governed_by):
                    if reg not in regulations:
                        yield problem(
                            m, *base, "governedBy", gi, message=f"regulação '{reg}' não existe"
                        )


@rule(code="JOURNEY_REF_FORMAT_INVALID", severity=ERROR)
def formats(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
    """`ext-`, `evt-`, `agenda-` não têm arquivo: só o formato é conferido (FR-17)."""
    for m, j in _journeys(catalog):
        orch = j.spec.orchestrator
        is_free = orch is not None and orch != "none" and not orch.startswith("app-")
        if is_free and orch is not None and not SCHEDULER_ID.match(orch):
            yield problem(
                m,
                "spec",
                "orchestrator",
                message="orquestrador deve ser 'app-…', 'agenda-…' ou 'none'",
            )
        for si, stage in enumerate(j.spec.stages):
            for pi, step in enumerate(stage.steps):
                base: tuple[Segment, ...] = ("spec", "stages", si, "steps", pi)
                calls = step.calls
                if calls is not None and not (calls.startswith("dom-") or EXTERNAL_ID.match(calls)):
                    yield problem(
                        m, *base, "calls", message="'calls' deve ser 'ext-<slug>' ou 'dom-<slug>'"
                    )
                if step.event is not None and not EVENT_ID.match(step.event):
                    yield problem(m, *base, "event", message="evento deve ser 'evt-<slug>'")
