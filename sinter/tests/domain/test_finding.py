from sinter.domain.validation.finding import Finding, format_path, line_for, sort_key

DATA = {
    "spec": {
        "areas": [{"id": "area-varejo", "name": "Varejo"}, {"name": "sem id"}],
        "docTypes": ["ata"],
    }
}


def test_path_usa_id_do_item_quando_tem() -> None:
    assert format_path(DATA, ("spec", "areas", 0, "name")) == "spec.areas[area-varejo].name"


def test_path_usa_indice_quando_item_nao_tem_id() -> None:
    assert format_path(DATA, ("spec", "areas", 1, "name")) == "spec.areas[1].name"
    assert format_path(DATA, ("spec", "docTypes", 0)) == "spec.docTypes[0]"


def test_linha_do_trecho_mais_especifico() -> None:
    positions = {(): 1, ("spec",): 5, ("spec", "areas", 0): 7}
    assert line_for(positions, ("spec", "areas", 0, "name")) == 7
    assert line_for(positions, ("spec", "outro")) == 5


def _f(path: str) -> Finding:
    return Finding(code="X", severity="error", file="a.yaml", path=path, message="m")


def test_ordem_natural_dos_indices() -> None:
    paths = ["spec.x[10]", "spec.x[2]", "spec.a"]
    ordered = [f.path for f in sorted((_f(p) for p in paths), key=sort_key)]
    assert ordered == ["spec.a", "spec.x[2]", "spec.x[10]"]
