"""Leitura dos itens do repo do domínio (Markdown com cabeçalho YAML simples). Sem dependências externas."""
import pathlib, re

CAMADAS = {
    1: "Negócio", 2: "Domínio", 3: "Subdomínio", 4: "Sistema",
    5: "Componente", 6: "Infraestrutura", 0: "Transversal",
}
KIND_CAMADA = {
    "canvas": 1, "capability": 1, "flow": 1, "domain": 2, "event": 2, "subdomain": 3,
    "system": 4, "contract": 4, "entity": 4, "integration": 3,
    "component": 5, "resource": 6, "environment": 6,
    "rule": 0, "decision": 0, "standard": 0, "term": 0,
}
IGNORAR = {"RELATORIO.md"}


def _lista(v):
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        return [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
    return [v.strip("'\"")] if v else []


def ler(repo):
    repo = pathlib.Path(repo)
    itens = []
    for p in sorted(repo.rglob("*.md")):
        rel = p.relative_to(repo).as_posix()
        if rel.startswith(("site/", "llm/")) or p.name in IGNORAR:
            continue
        texto = p.read_text(errors="ignore")
        m = re.match(r"^---\n(.*?)\n---\n?", texto, re.S)
        cab, corpo = (m.group(1), texto[m.end():]) if m else ("", texto)
        campos = {}
        for linha in cab.splitlines():
            mm = re.match(r"^([A-Za-z_-]+):\s*(.*)$", linha)
            if mm:
                campos[mm.group(1)] = mm.group(2).split(" #")[0].strip()
        extracoes = re.findall(r"extraction:\s*(\w+)", cab)
        titulo = next((l[2:].strip() for l in corpo.splitlines() if l.startswith("# ")), p.stem)
        kind = campos.get("kind", "")
        camada = campos.get("camada")
        camada = int(camada) if camada and camada.isdigit() else KIND_CAMADA.get(kind, 2 if p.name == "README.md" else 0)
        resumo = ""
        for l in corpo.splitlines():
            l = l.strip()
            if l and not l.startswith(("#", "|", "```", "-", "<", ">")):
                resumo = l
                break
        itens.append({
            "id": campos.get("id") or rel.removesuffix(".md").replace("/", "-"),
            "kind": kind or ("domain" if p.name == "README.md" else "doc"),
            "camada": camada,
            "status": campos.get("status", ""),
            "titulo": titulo,
            "resumo": resumo[:240],
            "caminho": rel,
            "realiza": _lista(campos.get("realiza", "")),
            "realizado_por": _lista(campos.get("realizado-por", "")),
            "extracoes": extracoes,
            "conflito": campos.get("conflito", "").lower() == "true",
            "corpo": corpo,
            "cabecalho": cab,
        })
    return itens


def relatorio(repo):
    p = pathlib.Path(repo) / "RELATORIO.md"
    return p.read_text(errors="ignore") if p.exists() else ""
