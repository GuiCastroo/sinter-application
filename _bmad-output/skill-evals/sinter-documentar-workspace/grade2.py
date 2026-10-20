"""Critérios da v2 (6 páginas). Uso: python3 grade2.py iteration-2"""
import json, pathlib, re, sys

it = pathlib.Path(sys.argv[1])
PAGS = ["1-negocio", "2-arquitetura", "3-servicos", "4-jornadas", "5-infraestrutura", "6-referencia"]
JARGAO = r"\b(lambda|dynamodb|api gateway|kubernetes|pod|grpc|step function|eventbridge|sqs|sns|endpoint|redis|postgres|mysql)\b"

COMMON = [
    ("Tem as 6 páginas (negócio, arquitetura, serviços, jornadas, infraestrutura, referência)", "seis"),
    ("Toda página abre com 'Em resumo' e tem o índice 'Nesta página'", "indice"),
    ("Poucos arquivos: no máximo 15 Markdown escritos (fora llm/ e site/)", "poucos"),
    ("Negócio tem a parede do Event Storming (tabela com 🟧) e a seção 'Quem orquestra'", "parede"),
    ("Negócio sem jargão técnico (no máximo 3 termos como lambda, gRPC, DynamoDB)", "jargao"),
    ("Cartão para IA (llms.txt) existe e cabe em ~1.500 tokens", "cartao"),
    ("80%+ das seções de serviço abrem com 'Em resumo'", "resumo_servicos"),
    ("Jornadas têm diagrama de sequência", "sequencia"),
    ("Mapa dos serviços sai das tabelas 'Consome' (3+ ligações)", "mapa"),
    ("Referência tem 'Dúvidas e perguntas'", "duvidas"),
]
SPECIFIC = {
    1: [("A jornada de compra passa por checkout e payment", "boutique")],
    2: [("'Quem orquestra' cita Step Functions", "coffee")],
    3: [("Modelo de dados (erDiagram) em 3+ serviços", "petclinic")],
}


def raiz(out):
    for p in out.rglob("1-negocio.md"):
        return p.parent
    return None


def check(key, out):
    r = raiz(out)
    if not r:
        return False, "sem 1-negocio.md"
    txt = {n: (r / f"{n}.md").read_text(errors="ignore") if (r / f"{n}.md").exists() else "" for n in PAGS}
    if key == "seis":
        falta = [n for n in PAGS if not txt[n]]
        return not falta, "faltam: " + ", ".join(falta) if falta else "6 páginas"
    if key == "indice":
        ruins = [n for n in PAGS if txt[n] and not (re.search(r"em resumo", txt[n], re.I) and re.search(r"^## Nesta p[áa]gina", txt[n], re.M | re.I))]
        return not ruins and all(txt.values()), "sem índice/resumo: " + ", ".join(ruins) if ruins else "todas ok"
    if key == "poucos":
        n = [p for p in r.rglob("*.md") if not {"llm", "site"} & set(p.relative_to(r).parts)]
        return len(n) <= 15, f"{len(n)} arquivos"
    if key == "parede":
        ok = "🟧" in txt["1-negocio"] and re.search(r"^## Quem orquestra", txt["1-negocio"], re.M | re.I)
        return bool(ok), "parede e quem orquestra" if ok else "faltando"
    if key == "jargao":
        n = len(re.findall(JARGAO, txt["1-negocio"], re.I))
        return n <= 3, f"{n} termos técnicos"
    if key == "cartao":
        p = r / "llms.txt"
        if not p.exists():
            return False, "sem llms.txt"
        t = len(p.read_text(errors="ignore")) // 4
        return t <= 1500, f"~{t} tokens"
    if key == "resumo_servicos":
        secs = re.split(r"^## ", txt["3-servicos"], flags=re.M)[1:]
        secs = [s for s in secs if not s.lower().startswith("nesta")]
        ok = [s for s in secs if re.search(r"^>\s*\**em resumo", s.split("\n", 2)[1] if "\n" in s else "", re.I | re.M) or re.search(r"\n>\s*\**Em resumo", s[:300], re.I)]
        ratio = len(ok) / max(1, len(secs))
        return ratio >= 0.8, f"{len(ok)}/{len(secs)} seções"
    if key == "sequencia":
        n = txt["4-jornadas"].count("sequenceDiagram")
        return n >= 1, f"{n} diagramas"
    if key == "mapa":
        g = r / "llm" / "grafo.json"
        n = len(json.loads(g.read_text()).get("chamadas", [])) if g.exists() else 0
        return n >= 3, f"{n} ligações"
    if key == "duvidas":
        ok = re.search(r"^## D[úu]vidas", txt["6-referencia"], re.M | re.I)
        return bool(ok), "presente" if ok else "ausente"
    if key == "boutique":
        seqs = re.findall(r"sequenceDiagram.*?```", txt["4-jornadas"], re.S)
        ok = any(re.search("checkout", s, re.I) and re.search("payment", s, re.I) for s in seqs)
        return ok, "ok" if ok else "não encontrada"
    if key == "coffee":
        s = re.search(r"^## Quem orquestra(.*?)(^## |\Z)", txt["1-negocio"], re.S | re.M)
        ok = bool(s and re.search(r"step function", s.group(1), re.I))
        return ok, "cita Step Functions" if ok else "não cita"
    if key == "petclinic":
        n = txt["3-servicos"].count("erDiagram")
        return n >= 3, f"{n} erDiagram"


for ev in sorted(it.glob("eval-*")):
    eid = int(ev.name.split("-")[1])
    asserts = COMMON + SPECIFIC.get(eid, [])
    meta = json.loads((ev / "eval_metadata.json").read_text())
    meta["assertions"] = [a[0] for a in asserts]
    (ev / "eval_metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    for cfg in ("with_skill", "old_skill"):
        run = ev / cfg / "run-1"
        out = run / "outputs"
        if not out.exists() or not any(out.rglob("*.md")):
            continue
        exps = []
        for t, k in asserts:
            ok, evd = check(k, out)
            exps.append({"text": t, "passed": bool(ok), "evidence": evd})
        p = sum(e["passed"] for e in exps)
        (run / "grading.json").write_text(json.dumps({"expectations": exps, "summary": {"passed": p, "failed": len(exps) - p, "total": len(exps), "pass_rate": p / len(exps)}}, ensure_ascii=False, indent=2))
        print(ev.name, cfg, f"{p}/{len(exps)}")
