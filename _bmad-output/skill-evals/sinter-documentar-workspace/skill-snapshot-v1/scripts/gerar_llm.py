"""Versão para LLM: gera llms.txt, llm/contexto.md e llm/grafo.json a partir do repo do domínio.

- llms.txt       índice no padrão llmstxt.org (H1, resumo, seções com links), para o agente saber o que ler
- llm/contexto.md  resumo compacto por camada: uma linha por item, sequências e contratos preservados
- llm/grafo.json   nós e arestas (realiza) para consulta estruturada

Uso: python3 gerar_llm.py <repo-do-dominio> [--nome "Pagamentos"] [--orcamento 8000]
"""
import argparse, json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _itens import ler, CAMADAS  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("repo")
ap.add_argument("--nome", default=None)
ap.add_argument("--orcamento", type=int, default=8000, help="limite aproximado de tokens do contexto.md")
a = ap.parse_args()
repo = pathlib.Path(a.repo)
itens = ler(repo)
nome = a.nome or repo.name
ordem = [2, 1, 3, 4, 5, 6, 0]
readme = next((i for i in itens if i["caminho"] == "README.md"), None)
proposito = readme["resumo"] if readme else f"Documentação do domínio {nome}."


def ext(i):
    e = set(i["extracoes"])
    return "inferido" if e == {"inferred"} else ("misto" if "inferred" in e else ("extraído" if e else "sem fonte"))


# llms.txt
linhas = [f"# {nome}", "", f"> {proposito}", "",
          "Documentação no padrão Sinter: 6 camadas (negócio → infraestrutura). Cada item tem id estável, proveniência e ligações `realiza`/`realizado-por`. Leia primeiro `llm/contexto.md`; consulte `llm/grafo.json` para navegar ligações.", ""]
for c in [x for x in ordem if x not in (5, 6)]:
    grp = [i for i in itens if i["camada"] == c and i["caminho"] != "README.md"]
    if not grp:
        continue
    linhas.append(f"## {c}. {CAMADAS[c]}" if c else f"## {CAMADAS[c]}")
    for i in grp:
        linhas.append(f"- [{i['titulo']}]({i['caminho']}): {i['resumo'][:140]}")
    linhas.append("")
# Componentes e infraestrutura ficam em "Optional" (convenção do llms.txt: pode ser pulado quando falta contexto)
opcionais = [i for i in itens if i["camada"] in (5, 6)]
if opcionais:
    linhas.append("## Optional")
    for i in opcionais:
        linhas.append(f"- [{i['titulo']}]({i['caminho']}): {CAMADAS[i['camada']]}. {i['resumo'][:120]}")
    linhas.append("")
(repo / "llms.txt").write_text("\n".join(linhas), encoding="utf-8")

# llm/contexto.md
canvas = next((i for i in itens if i["kind"] == "canvas" or i["caminho"] == "negocio/canvas.md"), None)
ctx = [f"# Contexto do domínio {nome}", "", proposito, "",
       "Legenda: `[id] título (tipo, origem) — resumo`. Origem: extraído = lido nas fontes; inferido = a confirmar.", ""]
if canvas:
    corpo = re.sub(r"^# .*\n", "", canvas["corpo"]).strip()
    ctx += ["## Canvas do negócio (resumo)", re.sub(r"^## ", "### ", corpo, flags=re.M), ""]
for c in ordem:
    grp = [i for i in itens if i["camada"] == c]
    if not grp:
        continue
    ctx.append(f"## {c}. {CAMADAS[c]}" if c else f"## {CAMADAS[c]}")
    for i in grp:
        extra = []
        if i["realiza"]:
            extra.append("realiza " + ", ".join(i["realiza"]))
        if i["conflito"]:
            extra.append("CONFLITO entre fontes")
        ctx.append(f"- [{i['id']}] {i['titulo']} ({i['kind']}, {ext(i)}) — {i['resumo'][:180]}" + (f" | {'; '.join(extra)}" if extra else ""))
    ctx.append("")
seqs = [(i, re.findall(r"```mermaid\n(sequenceDiagram.*?)```", i["corpo"], re.S)) for i in itens]
seqs = [(i, s) for i, s in seqs if s]
if seqs:
    ctx.append("## Sequências (passo a passo técnico)")
    for i, ss in seqs:
        for s in ss:
            ctx += [f"### {i['titulo']} [{i['id']}]", "```mermaid", s.strip(), "```", ""]
texto = "\n".join(ctx)
tokens = len(texto) // 4
if tokens > a.orcamento:
    texto += f"\n\n> Aviso: contexto com ~{tokens} tokens, acima do orçamento de {a.orcamento}. Priorize as camadas 1 a 4.\n"
(repo / "llm").mkdir(exist_ok=True)
(repo / "llm" / "contexto.md").write_text(texto, encoding="utf-8")

# llm/grafo.json
nos = [{k: i[k] for k in ("id", "kind", "camada", "status", "titulo", "caminho")} | {"origem": ext(i), "conflito": i["conflito"]} for i in itens]
ids = {i["id"] for i in itens}
arestas = []
for i in itens:
    for alvo in i["realiza"]:
        arestas.append({"de": i["id"], "para": alvo, "tipo": "realiza", "alvo_documentado": alvo in ids})
    for fonte in i["realizado_por"]:
        arestas.append({"de": fonte, "para": i["id"], "tipo": "realiza", "alvo_documentado": fonte in ids})
unicas = {(e["de"], e["para"]): e for e in arestas}
(repo / "llm" / "grafo.json").write_text(json.dumps({"dominio": nome, "nos": nos, "arestas": list(unicas.values())}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"llms.txt, llm/contexto.md (~{tokens} tokens), llm/grafo.json ({len(nos)} nós, {len(unicas)} arestas)")
