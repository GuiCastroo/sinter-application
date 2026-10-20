"""Avalia as saídas de uma iteração contra as asserções e grava grading.json em cada run."""
import json, pathlib, re, sys

it = pathlib.Path(sys.argv[1])

COMMON = [
    ("Usa as gavetas do padrão (5+ de: capacidades, fluxos, sistemas, infraestrutura, subdominios, glossario, regras-de-negocio, decisoes, padroes)", "folders"),
    ("80%+ dos itens têm cabeçalho YAML com proveniência e tipo de extração", "provenance"),
    ("Itens nascem como proposta (status: proposed) e nenhum como approved", "proposed"),
    ("Itens ligam camadas com realiza / realizado-por", "links"),
    ("Tem ao menos um diagrama de sequência Mermaid", "sequence"),
    ("Tem RELATORIO.md com perguntas para as pessoas", "report"),
    ("Marca inferências na camada de negócio (extraction: inferred em capacidades ou fluxos)", "inferred_business"),
    ("Documenta infraestrutura como itens próprios (1+ arquivo em infraestrutura/recursos)", "infra"),
]
SPECIFIC = {
    1: [("A sequência de compra passa por checkoutservice e paymentservice", "boutique_seq")],
    2: [("Um item de componente por lambda (5+ arquivos em componentes/)", "coffee_components")],
    3: [("Modelo de dados com erDiagram em 3+ serviços", "petclinic_erd"),
        ("2+ capacidades de negócio documentadas", "petclinic_caps")],
}


def mds(out):
    return [p for p in out.rglob("*.md")]


def check(key, out):
    files = mds(out)
    text = {p: p.read_text(errors="ignore") for p in files}
    alltext = "\n".join(text.values())
    items = [p for p in files if p.name not in ("RELATORIO.md", "README.md") and not p.name.startswith("_")]
    fm = {p: re.match(r"^---\n(.*?)\n---", text[p], re.S) for p in items}
    if key == "folders":
        names = {d.name for d in out.rglob("*") if d.is_dir()}
        want = {"capacidades", "fluxos", "sistemas", "infraestrutura", "subdominios", "glossario", "regras-de-negocio", "decisoes", "padroes"}
        hit = names & want
        return len(hit) >= 5, f"gavetas encontradas: {sorted(hit)}"
    if key == "provenance":
        ok = [p for p, m in fm.items() if m and "provenance" in m.group(1) and "extraction" in m.group(1)]
        ratio = len(ok) / max(1, len(items))
        return ratio >= 0.8, f"{len(ok)}/{len(items)} itens com proveniência ({ratio:.0%})"
    if key == "proposed":
        prop = sum(1 for m in fm.values() if m and re.search(r"status:\s*proposed", m.group(1)))
        appr = sum(1 for m in fm.values() if m and re.search(r"status:\s*approved", m.group(1)))
        return prop > 0 and appr == 0, f"proposed={prop}, approved={appr}"
    if key == "links":
        n = sum(1 for m in fm.values() if m and ("realiza" in m.group(1)))
        return n >= max(3, len(items) // 3), f"{n} itens com realiza/realizado-por"
    if key == "sequence":
        n = alltext.count("sequenceDiagram")
        return n >= 1, f"{n} diagramas de sequência"
    if key == "report":
        r = next((p for p in files if p.name == "RELATORIO.md"), None)
        ok = bool(r) and re.search(r"pergunt", text[r], re.I) is not None
        return ok, "RELATORIO.md com perguntas" if ok else "sem RELATORIO.md ou sem perguntas"
    if key == "inferred_business":
        n = sum(1 for p, m in fm.items() if m and p.parent.name in ("capacidades", "fluxos") and "inferred" in m.group(1))
        return n >= 1, f"{n} itens de negócio marcados como inferidos"
    if key == "infra":
        n = sum(1 for p in files if "infraestrutura" in p.parts and "recursos" in p.parts)
        return n >= 1, f"{n} recursos de infraestrutura"
    if key == "boutique_seq":
        seqs = [t for t in text.values() if "sequenceDiagram" in t]
        ok = any(re.search(r"checkout", t, re.I) and re.search(r"payment", t, re.I) for t in seqs)
        return ok, "sequência com checkout e payment" if ok else "não encontrada"
    if key == "coffee_components":
        n = sum(1 for p in files if "componentes" in p.parts)
        return n >= 5, f"{n} arquivos de componente"
    if key == "petclinic_erd":
        n = sum(1 for t in text.values() if "erDiagram" in t)
        return n >= 3, f"{n} arquivos com erDiagram"
    if key == "petclinic_caps":
        n = sum(1 for p in files if "capacidades" in p.parts)
        return n >= 2, f"{n} capacidades"
    return False, "chave desconhecida"


for ev in sorted(it.glob("eval-*")):
    eid = int(ev.name.split("-")[1])
    asserts = COMMON + SPECIFIC.get(eid, [])
    meta = json.loads((ev / "eval_metadata.json").read_text())
    meta["assertions"] = [a[0] for a in asserts]
    (ev / "eval_metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    for cfg in ("with_skill", "without_skill"):
        out = ev / cfg / "outputs"
        if not out.exists():
            continue
        exps = []
        for textual, key in asserts:
            ok, ev_txt = check(key, out)
            exps.append({"text": textual, "passed": bool(ok), "evidence": ev_txt})
        passed = sum(e["passed"] for e in exps)
        grading = {"expectations": exps, "summary": {"passed": passed, "failed": len(exps) - passed, "total": len(exps), "pass_rate": passed / len(exps)}}
        (ev / cfg / "grading.json").write_text(json.dumps(grading, ensure_ascii=False, indent=2))
        print(ev.name, cfg, f"{passed}/{len(exps)}")
