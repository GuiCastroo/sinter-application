"""Leitura das 6 páginas do domínio. Sem dependências externas."""
import pathlib, re, unicodedata

PAGINAS = [
    ("1-negocio.md", "Negócio"), ("2-arquitetura.md", "Arquitetura"), ("3-servicos.md", "Serviços"),
    ("4-jornadas.md", "Jornadas"), ("5-infraestrutura.md", "Infraestrutura"), ("6-referencia.md", "Referência"),
]


def slug(t):
    """Âncora no estilo GitHub: minúsculas, sem pontuação, espaços viram hífen (acentos mantidos)."""
    t = re.sub(r"[`*_\[\]()]", "", t.strip().lower())
    t = re.sub(r"[^\w\- ]", "", t, flags=re.UNICODE)
    return t.replace(" ", "-")


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def limpa(t):
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t or "")
    return t.replace("`", "").replace("**", "").strip()


def _resumo(bloco):
    linhas = []
    for l in bloco.splitlines():
        if l.startswith(">"):
            linhas.append(l.lstrip("> ").strip())
        elif linhas:
            break
    r = " ".join(linhas)
    return re.sub(r"^\**Em resumo:?\**:?\s*", "", r, flags=re.I).strip()


def ler_pagina(path):
    texto = path.read_text(errors="ignore")
    titulo = next((l[2:].strip() for l in texto.splitlines() if l.startswith("# ")), path.stem)
    partes = re.split(r"^## ", texto, flags=re.M)
    cabeca = partes[0]
    secoes, nesta = [], []
    for p in partes[1:]:
        nl = p.find("\n")
        t, corpo = p[:nl].strip(), p[nl + 1:]
        if sem_acento(t.lower()) == "nesta pagina":
            nesta = tabela(corpo)
            continue
        corpo_sem_fontes = re.split(r"^\*\*Fontes:?\*\*", corpo, flags=re.M)[0]
        secoes.append({"titulo": t, "slug": slug(t), "corpo": corpo_sem_fontes, "resumo": _resumo(corpo_sem_fontes.lstrip())})
    fontes = ""
    m = re.search(r"^\*\*Fontes:?\*\*:?(.*)", texto, flags=re.M | re.S)
    if m:
        fontes = m.group(1).strip()
    return {"arquivo": path.name, "titulo": titulo, "resumo": _resumo(cabeca.split("\n", 1)[1] if "\n" in cabeca else ""),
            "nesta": nesta, "secoes": secoes, "texto": texto, "fontes": fontes}


def ler(repo):
    repo = pathlib.Path(repo)
    paginas = {}
    for arq, nome in PAGINAS:
        p = repo / arq
        pasta = repo / arq.removesuffix(".md")
        if p.exists():
            pg = ler_pagina(p)
        elif pasta.is_dir():  # página dividida por subdomínio
            partes = [ler_pagina(f) for f in sorted(pasta.glob("*.md"))]
            pg = {"arquivo": pasta.name + "/", "titulo": nome, "resumo": " ".join(x["resumo"] for x in partes)[:600],
                  "nesta": sum((x["nesta"] for x in partes), []), "secoes": sum((x["secoes"] for x in partes), []),
                  "texto": "\n\n".join(x["texto"] for x in partes), "fontes": ""}
        else:
            continue
        pg["nome"] = nome
        paginas[arq] = pg
    return paginas


# v3: matching is exact; tables end at the first non-table line.
def tabela(texto):
    lines = []
    for line in texto.splitlines():
        if line.strip().startswith('|'):
            lines.append(line.strip())
        elif lines:
            break
    if len(lines) < 2:
        return []
    cells = lambda line: [x.strip() for x in re.split(r'(?<!\\)\|', line.strip('|'))]
    headers = cells(lines[0])
    if not all(re.fullmatch(r':?-+:?', x.replace(' ', '')) for x in cells(lines[1])):
        return []
    return [dict(zip(headers, cells(line))) for line in lines[2:]]


def secao(pg, titulo):
    target = sem_acento(titulo.strip().lower())
    return next((s for s in (pg or {}).get('secoes', []) if sem_acento(s['titulo'].lower()) == target), None)


def subsecao(corpo, titulo):
    target = sem_acento(titulo.strip().lower())
    for part in re.split(r'^### ', corpo, flags=re.M)[1:]:
        heading, _, body = part.partition('\n')
        if sem_acento(heading.strip().lower()) == target:
            return body
    return ''


def inventario(paginas):
    result = []
    for s in paginas['3-servicos.md']['secoes']:
        ident = re.search(r'^\*\*ID:\*\* `([^`]+)`$', s['corpo'], re.M)
        state = re.search(r'^\*\*Estado:\*\* (ativo|opcional|inativo)$', s['corpo'], re.M)
        if not ident or not state:
            raise ValueError('Serviço sem ID/Estado: ' + s['titulo'])
        result.append({'id': ident[1], 'nome': limpa(s['titulo']), 'estado': state[1], 'origem': '3-servicos.md#'+s['slug'], 'resumo': s['resumo']})
    if len({s['id'] for s in result}) != len(result):
        raise ValueError('IDs de serviço duplicados')
    return result


def relacoes(paginas):
    services = inventario(paginas)
    known = {s['id']: s for s in services}
    result = []
    for s, meta in zip(paginas['3-servicos.md']['secoes'], services):
        for row in tabela(subsecao(s['corpo'], 'Consome')):
            vals = list(row.values())
            if not vals:
                continue
            target = limpa(vals[0])
            if target in ('', '—', '-', 'Nenhum'):
                continue
            contract = limpa(vals[1]) if len(vals)>1 else ''
            typ = limpa(row.get('Tipo', 'não declarado'))
            allowed = {'chama_api','consome_evento','acessa_dado','callback','inicializacao','configuracao'}
            if typ not in allowed:
                raise ValueError('Tipo não declarado/permitido: '+typ)
            kind = typ
            lowered = contract.lower()
            result.append({'de':meta['id'], 'para':target, 'contrato':contract, 'tipo':kind, 'tipo_declarado':typ, 'interno':target in known, 'estado_origem':meta['estado'], 'estado_destino':known.get(target, {}).get('estado','externo'), 'evidencia':'a confirmar' if 'a confirmar' in lowered else 'declarada', 'origem':meta['origem']})
    return result


def arestas_servicos(paginas):
    return [s['id'] for s in inventario(paginas)], [(r['de'],r['para'],r['tipo']+': '+r['contrato'],r['interno']) for r in relacoes(paginas)]


def grafo(paginas, nome):
    services = inventario(paginas)
    known = {s['id'] for s in services}
    journeys, uses = [], []
    for s in paginas['4-jornadas.md']['secoes']:
        m = re.search(r'^\*\*Participantes:\*\* (.+)$', s['corpo'], re.M)
        if not m:
            raise ValueError('Jornada sem participantes explícitos: '+s['titulo'])
        participants = re.findall(r'`([^`]+)`', m[1])
        if not participants or set(participants)-known:
            raise ValueError('Participantes desconhecidos: '+str(set(participants)-known))
        journeys.append({'id':s['slug'], 'nome':s['titulo'], 'participantes':participants, 'origem':'4-jornadas.md#'+s['slug']})
        uses.extend({'jornada':s['slug'], 'servico':p} for p in participants)
    return {'versao':4, 'dominio':nome, 'semantica':'Aresta de dependência: consumidor → fornecedor; tipo preserva evento, dado, callback, API e inicialização. Não representa cronologia de execução.', 'servicos':services, 'jornadas':journeys, 'relacoes':relacoes(paginas), 'jornada_usa_servico':uses}
