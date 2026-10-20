"""Versão para humanos: gera site/index.html (arquivo único, em abas) a partir do repo do domínio.

Abas: Visão geral (negócio, arquitetura, mapa dos serviços) · Microsserviços · Fluxos · Infraestrutura · Referência.

Uso: python3 gerar_site.py <repo-do-dominio> [--nome "Pagamentos"]
"""
import argparse, html, json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _itens import ler, relatorio, CAMADAS  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("repo")
ap.add_argument("--nome", default=None)
a = ap.parse_args()
repo = pathlib.Path(a.repo)
itens = ler(repo)
nome = a.nome or repo.name
for it in itens:
    it.pop("cabecalho", None)

# ---- mapa dos serviços: arestas a partir da seção "Consome" das fichas de sistema ----
sistemas = [i for i in itens if i["kind"] == "system"]
por_nome = {i["titulo"].strip("` ").lower(): i for i in sistemas}
subs = {i["id"]: i["titulo"].replace("Subdomínio ", "") for i in itens if i["kind"] == "subdomain"}


def limpa(c):
    c = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", c)
    return c.replace("`", "").replace("*", "").strip()


def acha(nome_cel):
    n = nome_cel.lower()
    if n in por_nome:
        return por_nome[n]
    for k, v in por_nome.items():
        if k and (k in n or n in k):
            return v
    return None


arestas = []
for s in sistemas:
    m = re.search(r"^## Consome\s*\n(.*?)(?=^## |\Z)", s["corpo"], re.S | re.M)
    if not m:
        continue
    for linha in m.group(1).splitlines():
        if not linha.startswith("|") or set(linha) <= set("|- :"):
            continue
        cel = [limpa(c) for c in linha.strip("|").split("|")]
        if not cel or cel[0].lower() in ("sistema", "serviço", "servico"):
            continue
        alvo = acha(cel[0])
        rot = (cel[1] if len(cel) > 1 else "")[:28]
        arestas.append((s, alvo, cel[0], rot))


def nid(t):
    return "n_" + re.sub(r"[^A-Za-z0-9]", "_", t)


mapa = ""
if sistemas:
    linhas = ["flowchart LR"]
    grupos = {}
    for s in sistemas:
        sub = next((subs[r] for r in s["realiza"] if r in subs), None)
        grupos.setdefault(sub, []).append(s)
    for sub, ss in grupos.items():
        if sub:
            linhas.append(f'  subgraph {nid(sub)}["{sub}"]')
        for s in ss:
            linhas.append(f'    {nid(s["id"])}["{s["titulo"].strip("`")}"]')
        if sub:
            linhas.append("  end")
    vistos = set()
    for s, alvo, cru, rot in arestas:
        destino = nid(alvo["id"]) if alvo else nid("ext_" + cru)
        if not alvo:
            linhas.append(f'  {destino}(["{cru[:30]}"])')
        chave = (s["id"], destino)
        if chave in vistos:
            continue
        vistos.add(chave)
        rot = rot.replace('"', "'")
        linhas.append(f'  {nid(s["id"])} -->|"{rot}"| {destino}' if rot else f'  {nid(s["id"])} --> {destino}')
    mapa = "\n".join(linhas)

dados = {"nome": nome, "itens": itens, "relatorio": relatorio(repo), "camadas": CAMADAS, "mapa": mapa}

pagina = r"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__NOME__ · documentação do domínio</title>
<script src="https://cdn.jsdelivr.net/npm/marked@15/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<style>
:root{--chrome:#1F2327;--rail:#1A1D20;--canvas:#2A2F34;--surface:#343A40;--line:#474E55;
--ink:#E8E4DB;--muted:#9DA3A8;--faint:#6E757B;--neon:#46F28E;--api:#7EA6F4;--conf:#EE6F7C;
--ui:'Avenir Next','Helvetica Neue',sans-serif;--display:Optima,'Avenir Next',sans-serif}
*{box-sizing:border-box}
body{margin:0;background:var(--canvas);color:var(--ink);font-family:var(--ui)}
header{position:sticky;top:0;z-index:5;background:var(--chrome);border-bottom:1px solid #2E3338;display:flex;align-items:center;gap:22px;padding:0 24px;height:56px}
.brand{font-family:var(--display);font-size:19px;white-space:nowrap}
.brand small{font-family:var(--ui);font-size:12px;color:var(--muted);margin-left:8px}
nav.tabs{display:flex;gap:4px;height:100%}
nav.tabs a{display:flex;align-items:center;padding:0 14px;color:var(--muted);text-decoration:none;font-size:14px;border-bottom:2px solid transparent}
nav.tabs a.on{color:var(--ink);border-bottom-color:var(--neon)}
nav.tabs a span{font-size:11px;color:var(--faint);margin-left:6px}
#q{margin-left:auto;font:inherit;font-size:13px;padding:7px 10px;border-radius:8px;border:1px solid var(--line);background:var(--surface);color:var(--ink);width:240px}
.page{display:grid;grid-template-columns:280px 1fr;min-height:calc(100vh - 56px)}
.page.solo{grid-template-columns:1fr} .page.solo aside{display:none}
aside{background:var(--chrome);border-right:1px solid #2E3338;padding:14px 10px;overflow:auto;max-height:calc(100vh - 56px);position:sticky;top:56px}
aside .grp{margin:12px 8px 4px;font-size:11.5px;color:var(--faint)}
aside a{display:flex;gap:8px;align-items:center;padding:6px 8px;border-radius:8px;color:var(--ink);text-decoration:none;font-size:13px}
aside a:hover{background:var(--surface)} aside a.on{background:var(--surface);box-shadow:inset 0 0 0 1px rgba(70,242,142,.45)}
aside a.sub{padding-left:24px;color:var(--muted);font-size:12.5px}
.dot{width:7px;height:7px;border-radius:50%;flex:none;background:var(--faint)}
.dot.approved{background:var(--neon);box-shadow:0 0 6px var(--neon)} .dot.inf{background:transparent;border:1px dashed var(--conf)}
main{padding:28px 36px 70px;min-width:0}
.wrap{max-width:1060px;margin:0 auto}
h1{font-family:var(--display);font-weight:500;font-size:30px;margin:0 0 6px}
h2.sec{font-family:var(--display);font-weight:500;font-size:21px;margin:34px 0 4px}
p.lead{color:var(--muted);margin:0 0 14px;font-size:14px}
.crumbs{font-size:12.5px;color:var(--muted);margin-bottom:6px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 16px}
.chip{font-size:11.5px;padding:3px 9px;border-radius:10px;background:#2F3439;border:1px solid var(--line);color:var(--muted)}
.chip.ok{border-color:rgba(70,242,142,.5);color:var(--neon)} .chip.inf{border-color:rgba(238,111,124,.5);color:#F2B7BE} .chip.ext{border-color:rgba(126,166,244,.5);color:#B9C9EC}
.doc{line-height:1.6;font-size:15px}
.doc a{color:var(--api)}
.doc pre{background:var(--rail);border:1px solid #2E3338;border-radius:10px;padding:12px;overflow:auto;font-size:12.5px}
.doc code{font-family:Menlo,monospace;font-size:12.5px;background:#2F3439;padding:1px 5px;border-radius:4px} .doc pre code{background:none;padding:0}
.doc table{border-collapse:collapse;margin:12px 0;font-size:13.5px;width:100%}
.doc th,.doc td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top} .doc th{background:#2F3439;color:var(--muted);font-weight:600}
.mermaid{background:#F4F5F7;border-radius:12px;padding:16px;margin:14px 0;overflow:auto;text-align:center}
.cv{display:grid;grid-template-columns:repeat(3,1fr);grid-auto-flow:dense;gap:12px;margin:12px 0}
.cv .blk{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px 16px;font-size:14px;line-height:1.5}
.cv .blk h3{margin:0 0 8px;font-size:12.5px;font-weight:600;color:var(--muted)}
.cv .blk ul{margin:0;padding-left:18px} .cv .blk p{margin:0 0 6px} .cv .blk a{color:var(--ink)}
.cv .full{grid-column:1/-1;border-color:rgba(70,242,142,.45);font-size:16px} .cv .wide{grid-column:span 2} .cv .risk{border-color:rgba(238,111,124,.5)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin:14px 0}
.card{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px 16px;cursor:pointer}
.card:hover{border-color:var(--neon)} .card b{display:flex;gap:8px;align-items:center;font-size:15px;margin-bottom:4px} .card p{margin:0;font-size:13px;color:var(--muted);line-height:1.45}
.card .meta{font-size:11.5px;color:var(--faint);margin-top:8px}
.kpis{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}
.kpi{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:10px 14px;min-width:130px}
.kpi b{display:block;font-family:var(--display);font-size:22px;font-weight:500} .kpi span{font-size:12px;color:var(--muted)}
.links{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:22px 0}
.box{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.box h4{margin:0 0 8px;font-size:12.5px;color:var(--muted);font-weight:600}
.box a{display:block;font-size:13px;color:var(--ink);text-decoration:none;padding:3px 0} .box a:hover{color:var(--neon)}
.conf{background:rgba(238,111,124,.08);border:1px solid rgba(238,111,124,.5);border-radius:10px;padding:10px 12px;margin:12px 0;font-size:13.5px}
.empty{color:var(--faint);font-size:14px}
@media(max-width:1000px){.cv{grid-template-columns:1fr 1fr}.page{grid-template-columns:1fr}aside{position:static;max-height:none}}
</style></head><body>
<header><div class="brand">__NOME__<small>documentação do domínio</small></div>
<nav class="tabs" id="tabs"></nav><input id="q" placeholder="Buscar…"></header>
<div class="page" id="page"><aside id="side"></aside><main><div class="wrap" id="view"></div></main></div>
<script>
const D = __DADOS__;
mermaid.initialize({startOnLoad:false, securityLevel:'loose', theme:'base', themeVariables:{fontFamily:'Avenir Next, Helvetica Neue, sans-serif', primaryColor:'#E6ECEF', primaryBorderColor:'#5A626A', primaryTextColor:'#1D2433', lineColor:'#5A626A', clusterBkg:'#F4F5F7', clusterBorder:'#9DA3A8', edgeLabelBackground:'#FFFFFF', tertiaryColor:'#F4F5F7', actorBkg:'#E6ECEF', actorBorder:'#5A626A', noteBkgColor:'#FFF6DA'}});
const byId = Object.fromEntries(D.itens.map(i => [i.id, i]));
const esc = s => (s||'').replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const isCanvas = i => i.kind === 'canvas' || i.caminho === 'negocio/canvas.md';
const K = k => D.itens.filter(i => i.kind === k);
const TABS = [
  {id:'geral', nome:'Visão geral'},
  {id:'servicos', nome:'Microsserviços', n:() => K('system').length},
  {id:'fluxos', nome:'Fluxos', n:() => K('flow').length},
  {id:'infra', nome:'Infraestrutura', n:() => D.itens.filter(i => i.camada === 6).length},
  {id:'ref', nome:'Referência', n:() => D.itens.filter(i => i.camada === 0).length},
];
let tab = 'geral';
function dot(i){ const c = i.status==='approved' ? 'approved' : (i.extracoes.includes('inferred') && !i.extracoes.includes('extracted') ? 'inf' : ''); return `<span class="dot ${c}"></span>`; }
function tabs(){
  document.getElementById('tabs').innerHTML = TABS.map(t => `<a href="#" data-t="${t.id}" class="${t.id===tab?'on':''}">${t.nome}${t.n ? `<span>${t.n()}</span>` : ''}</a>`).join('');
  document.querySelectorAll('#tabs a').forEach(a => a.onclick = e => { e.preventDefault(); abrir(a.dataset.t); });
}
async function desenhar(root){
  root.querySelectorAll('pre > code.language-mermaid').forEach(c => { const d = document.createElement('div'); d.className = 'mermaid'; d.textContent = c.textContent; c.parentElement.replaceWith(d); });
  try { await mermaid.run({nodes: root.querySelectorAll('.mermaid:not([data-processed])')}); } catch(e){ console.warn(e); }
}
function md(t){ return marked.parse(t || ''); }
function canvasHTML(t){
  return '<div class="cv">' + t.split(/^## /m).slice(1).map(p => {
    const nl = p.indexOf('\n'), ti = p.slice(0, nl).trim(), k = ti.toLowerCase();
    const cls = k.startsWith('propósito') ? 'full' : (k.startsWith('fluxos') || k.startsWith('capacidades')) ? 'wide' : k.startsWith('riscos') ? 'risk' : '';
    return `<section class="blk ${cls}"><h3>${esc(ti)}</h3>${md(p.slice(nl+1))}</section>`; }).join('') + '</div>';
}
function side(grupos, ativo){
  const f = document.getElementById('q').value.toLowerCase();
  let h = '';
  for (const [g, lista] of grupos) {
    const vis = lista.filter(i => !f || (i.titulo + i.id + i.resumo).toLowerCase().includes(f));
    if (!vis.length) continue;
    if (g) h += `<div class="grp">${esc(g)}</div>`;
    for (const i of vis) h += `<a href="#" data-id="${i.id}" class="${i.id===ativo?'on':''} ${i._sub?'sub':''}">${dot(i)}${esc(i.titulo)}</a>`;
  }
  const s = document.getElementById('side'); s.innerHTML = h || '<p class="empty" style="padding:8px">Nada encontrado.</p>';
  s.querySelectorAll('a').forEach(a => a.onclick = e => { e.preventDefault(); item(a.dataset.id); });
}
function gruposServicos(){
  const subsIds = Object.fromEntries(K('subdomain').map(s => [s.id, s.titulo.replace('Subdomínio ', '')]));
  const g = new Map();
  for (const s of K('system').sort((a,b) => a.titulo.localeCompare(b.titulo))) {
    const sub = s.realiza.map(r => subsIds[r]).find(Boolean) || 'Sem subdomínio';
    if (!g.has(sub)) g.set(sub, []);
    g.get(sub).push(s);
    const pasta = s.caminho.replace(/[^/]+\.md$/, '');
    if (pasta.startsWith('sistemas/') && pasta !== 'sistemas/')
      for (const f of D.itens.filter(i => i !== s && i.caminho.startsWith(pasta))) { f._sub = true; g.get(sub).push(f); }
  }
  return [...g];
}
function gruposPara(t){
  if (t === 'servicos') return gruposServicos();
  if (t === 'fluxos') return [['Negócio', K('flow').filter(i => i.camada === 1)], ['Passo a passo técnico', K('flow').filter(i => i.camada !== 1)], ['Subdomínios', K('subdomain')]];
  if (t === 'infra') return [['Ambientes', K('environment')], ['Recursos', K('resource')], ['Outros', D.itens.filter(i => i.camada === 6 && !['resource','environment'].includes(i.kind))]];
  if (t === 'ref') return [['Glossário', K('term')], ['Regras de negócio', K('rule')], ['Decisões', K('decision')], ['Padrões', K('standard')], ['Negócio (detalhe)', D.itens.filter(i => i.camada === 1 && !isCanvas(i) && i.kind !== 'flow')]];
  return [];
}
const card = (i, meta) => `<div class="card" data-id="${i.id}"><b>${dot(i)}${esc(i.titulo)}</b><p>${esc(i.resumo.slice(0,150))}</p>${meta ? `<div class="meta">${meta}</div>` : ''}</div>`;
function abrir(t){
  tab = t; tabs(); window.scrollTo(0,0);
  const page = document.getElementById('page');
  if (t === 'geral') { page.classList.add('solo'); return geral(); }
  page.classList.remove('solo'); side(gruposPara(t));
  const v = document.getElementById('view');
  if (t === 'servicos') {
    v.innerHTML = `<h1>Microsserviços</h1><p class="lead">Cada serviço, o que faz e com quem fala. Clique para ver contratos, dados e componentes.</p><div class="cards">${
      K('system').map(s => { const pasta = s.caminho.replace(/[^/]+\.md$/, ''); const filhos = pasta !== 'sistemas/' ? D.itens.filter(i => i !== s && i.caminho.startsWith(pasta)) : [];
        return card(s, `${filhos.filter(i=>i.kind==='contract').length} contratos · ${filhos.filter(i=>i.kind==='component').length} componentes`); }).join('')}</div>`;
  } else if (t === 'fluxos') {
    v.innerHTML = `<h1>Fluxos</h1><p class="lead">Como o valor anda: primeiro em linguagem de negócio, depois o passo a passo entre os sistemas.</p><div class="cards">${
      K('flow').map(f => card(f, f.camada===1 ? 'negócio' : 'técnico')).join('') || '<p class="empty">Nenhum fluxo documentado.</p>'}</div>`;
  } else if (t === 'infra') {
    const env = K('environment'), res = K('resource');
    v.innerHTML = `<h1>Infraestrutura</h1><p class="lead">Onde tudo roda e do que depende.</p>${env.length ? '<h2 class="sec">Ambientes</h2><div class="cards">' + env.map(e => card(e)).join('') + '</div>' : ''}
      <h2 class="sec">Recursos</h2><div class="cards">${res.map(r => card(r)).join('') || '<p class="empty">Nenhum recurso documentado.</p>'}</div>`;
  } else {
    v.innerHTML = `<h1>Referência</h1><p class="lead">Termos, regras, decisões e padrões que valem para o domínio todo.</p>${D.relatorio ? `<div class="box" style="margin:14px 0"><h4>Relatório da documentação</h4><a href="#" id="rel">Abrir relatório, conflitos e perguntas para as pessoas</a></div>` : ''}${
      gruposPara('ref').filter(([,l]) => l.length).map(([g,l]) => `<h2 class="sec">${g}</h2><div class="cards">${l.map(i => card(i)).join('')}</div>`).join('')}`;
    const r = document.getElementById('rel'); if (r) r.onclick = e => { e.preventDefault(); v.innerHTML = '<p class="crumbs">Referência / Relatório</p><div class="doc">' + md(D.relatorio) + '</div>'; desenhar(v); };
  }
  v.querySelectorAll('.card').forEach(c => c.onclick = () => item(c.dataset.id));
}
function geral(){
  const v = document.getElementById('view');
  const canvas = D.itens.find(isCanvas), readme = D.itens.find(i => i.caminho === 'README.md');
  const conf = D.itens.filter(i => i.conflito);
  const inf = D.itens.filter(i => i.extracoes.includes('inferred') && !i.extracoes.includes('extracted')).length;
  const arq = readme ? readme.corpo.replace(/^# .*\n/, '') : '';
  const diag = (arq.match(/```mermaid[\s\S]*?```/) || [''])[0];
  const subsSec = (arq.match(/^## Subdom[^\n]*\n([\s\S]*?)(?=\n## |$)/) || ['',''])[1];
  v.innerHTML = `<h1>${esc(D.nome)}</h1><p class="lead">${esc(readme ? readme.resumo : '')}</p>
    <div class="kpis"><div class="kpi"><b>${K('system').length}</b><span>serviços</span></div><div class="kpi"><b>${K('subdomain').length}</b><span>subdomínios</span></div><div class="kpi"><b>${K('flow').length}</b><span>fluxos</span></div><div class="kpi"><b>${D.itens.filter(i=>i.camada===6).length}</b><span>itens de infra</span></div><div class="kpi"><b>${inf}</b><span>inferências a confirmar</span></div></div>
    ${conf.length ? `<div class="conf"><b>${conf.length} conflito(s) entre fontes:</b> ${conf.map(i => `<a href="#" data-id="${i.id}" style="color:#F7CDD2">${esc(i.titulo)}</a>`).join(', ')}</div>` : ''}
    <h2 class="sec">Negócio</h2><p class="lead">O domínio em uma página.</p>${canvas ? canvasHTML(canvas.corpo) : '<p class="empty">Canvas de negócio ainda não escrito.</p>'}
    <h2 class="sec">Arquitetura</h2><p class="lead">O domínio e o que está em volta dele.</p><div class="doc">${md(diag)}${md(subsSec)}</div>
    <h2 class="sec">Mapa dos serviços</h2><p class="lead">Quem chama quem, agrupado por subdomínio.</p>${D.mapa ? `<div class="mermaid" id="mapa"></div>` : '<p class="empty">Sem dados de integração nas fichas.</p>'}`;
  const m = document.getElementById('mapa'); if (m) m.textContent = D.mapa;
  v.querySelectorAll('.conf a').forEach(a => a.onclick = e => { e.preventDefault(); item(a.dataset.id); });
  desenhar(v);
}
function tabDoItem(i){
  if (i.kind === 'system' || i.caminho.startsWith('sistemas/')) return 'servicos';
  if (i.kind === 'flow' || i.kind === 'subdomain') return 'fluxos';
  if (i.camada === 6) return 'infra';
  return 'ref';
}
function item(id){
  const i = byId[id]; if (!i) return;
  const t = tabDoItem(i); if (t !== tab) { tab = t; tabs(); }
  document.getElementById('page').classList.remove('solo');
  side(gruposPara(tab), id);
  const link = ids => ids.map(x => byId[x] ? `<a href="#" data-id="${x}">${esc(byId[x].titulo)} <span style="color:var(--faint)">· ${D.camadas[byId[x].camada]}</span></a>` : '').join('') || '<span style="color:var(--faint);font-size:13px">—</span>';
  const desce = [...new Set([...i.realizado_por, ...D.itens.filter(o => o.realiza.includes(id)).map(o => o.id)])];
  const sobe = [...new Set([...i.realiza, ...D.itens.filter(o => o.realizado_por.includes(id)).map(o => o.id)])];
  const ex = [...new Set(i.extracoes)];
  const v = document.getElementById('view');
  v.innerHTML = `<p class="crumbs">${D.camadas[i.camada]} · ${esc(i.caminho)}</p>
    <div class="chips"><span class="chip">${esc(i.kind)}</span>${i.status ? `<span class="chip ${i.status==='approved'?'ok':''}">${i.status==='approved'?'aprovado':'proposto'}</span>` : ''}
    ${ex.map(e => `<span class="chip ${e==='inferred'?'inf':'ext'}">${e==='inferred'?'inferido':e==='extracted'?'extraído':'humano'}</span>`).join('')}${i.conflito ? '<span class="chip inf">conflito entre fontes</span>' : ''}</div>
    <div class="doc">${isCanvas(i) ? canvasHTML(i.corpo) : md(i.corpo)}</div>
    <div class="links"><div class="box"><h4>Sobe para</h4>${link(sobe)}</div><div class="box"><h4>Desce para</h4>${link(desce)}</div></div>`;
  v.querySelectorAll('.links a').forEach(a => a.onclick = e => { e.preventDefault(); item(a.dataset.id); });
  window.scrollTo(0,0); desenhar(v);
}
document.getElementById('q').oninput = () => { if (tab === 'geral') abrir('servicos'); else side(gruposPara(tab)); };
tabs(); abrir('geral');
</script></body></html>"""

saida = repo / "site"
saida.mkdir(exist_ok=True)
(saida / "index.html").write_text(
    pagina.replace("__NOME__", html.escape(nome)).replace("__DADOS__", json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")),
    encoding="utf-8")
print(saida / "index.html", f"({len(sistemas)} serviços, {len(arestas)} integrações no mapa)")
