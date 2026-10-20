"""Versão para pessoas: site/index.html (arquivo único).

Navegação só à esquerda, em árvore: página › seção › subseção, acompanhando a rolagem.
Tema claro por padrão, com opção escura. A parede do Event Storming vira post-its;
o mapa dos serviços é montado a partir das tabelas "Consome".

Uso: python3 gerar_site.py <repo-do-dominio> [--nome "Pagamentos"]
"""
import argparse, html, json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _paginas import ler, arestas_servicos, slug, inventario  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("repo")
ap.add_argument("--nome", default=None)
a = ap.parse_args()
repo = pathlib.Path(a.repo)
P = ler(repo)
if not P:
    sys.exit("Nenhuma das 6 páginas encontrada em " + str(repo))
nome = a.nome or repo.name

# ---- mapa dos serviços (Mermaid) a partir de 3-servicos ----
nomes, ares = arestas_servicos(P)
estados = {s["id"]:s["estado"] for s in inventario(P)}
nid = lambda t: "n_" + re.sub(r"[^A-Za-z0-9]", "_", t)
mapa = ""
if nomes:
    L = ["flowchart LR"]
    sub_de = {}
    for r in (P.get("3-servicos.md") or {}).get("nesta", []):
        v = list(r.values())
        if len(v) > 1:
            sub_de[re.sub(r"[`\[\]]|\(.*?\)", "", v[0]).strip().lower()] = re.sub(r"[`*]", "", v[1]).strip()
    grupos = {}
    for n in nomes:
        grupos.setdefault(sub_de.get(n.lower()), []).append(n)
    for g, ns in grupos.items():
        if g:
            L.append(f'  subgraph {nid("g_" + g)}["{g}"]')
        L += [f'    {nid(n)}["{n} ({estados[n]})"]' for n in ns]
        if g:
            L.append("  end")
    vistos = set()
    for o, d, ct, interno in ares:
        if (o, d) in vistos:
            continue
        vistos.add((o, d))
        if not interno:
            L.append(f'  {nid(d)}(["{d}"])')
        rot = ct.replace('"', "'")
        L.append(f'  {nid(o)} -->|"{rot}"| {nid(d)}' if rot else f"  {nid(o)} --> {nid(d)}")
    mapa = "\n".join(L)

paginas = []
for k, v in P.items():
    secs = []
    for s in v["secoes"]:
        subs = [t.strip() for t in re.findall(r"^### (.+)$", s["corpo"], flags=re.M)]
        secs.append({"titulo": s["titulo"].replace("`", ""), "slug": s["slug"], "subs": [{"titulo": t, "slug": s["slug"] + "--" + slug(t)} for t in subs]})
    paginas.append({"arquivo": k, "nome": v["nome"], "resumo": v["resumo"], "texto": v["texto"], "secoes": secs})
cartao = (repo / "llms.txt").read_text(errors="ignore") if (repo / "llms.txt").exists() else ""
dados = {"nome": nome, "paginas": paginas, "mapa": mapa, "cartao": cartao}

pagina = r"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__NOME__ · documentação do domínio</title>
<script src="https://cdn.jsdelivr.net/npm/marked@15/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<style>
:root{--bg:#F4F6F8;--surface:#FFFFFF;--panel:#EBEFF3;--hover:#E1E7ED;--ink:#1B2430;--muted:#566372;--faint:#8793A0;--line:#D8DEE4;
--accent:#0E8A4F;--accent-soft:#E3F4EA;--link:#1F5FD1;--quote:#F7FAF8;--code:#EEF1F4;--pre:#F7F8FA;--wall:#F1EEE6;
--ui:'Avenir Next','Helvetica Neue',sans-serif;--display:Optima,'Avenir Next',sans-serif}
[data-tema="escuro"]{--bg:#2A2F34;--surface:#343A40;--panel:#1F2327;--hover:#2C3237;--ink:#E8E4DB;--muted:#9DA3A8;--faint:#6E757B;--line:#474E55;
--accent:#46F28E;--accent-soft:rgba(70,242,142,.12);--link:#7EA6F4;--quote:#30363B;--code:#2F3439;--pre:#1A1D20;--wall:#3A3F44}
*{box-sizing:border-box} aside,#q{min-width:0}.doc{overflow-wrap:anywhere}.table-scroll{max-width:100%;overflow-x:auto}.wrap{min-width:0}.doc pre{max-width:100%} html{scroll-padding-top:24px}
body{margin:0;display:grid;grid-template-columns:300px 1fr;background:var(--bg);color:var(--ink);font-family:var(--ui)}
aside{background:var(--panel);border-right:1px solid var(--line);height:100vh;position:sticky;top:0;overflow:auto;display:flex;flex-direction:column}
.topo{padding:18px 16px 12px;border-bottom:1px solid var(--line)}
.brand{font-family:var(--display);font-size:20px;line-height:1.2}
.brand small{display:block;font-family:var(--ui);font-size:12px;color:var(--muted);margin-top:2px}
.ferr{display:flex;gap:8px;margin-top:12px}
#q{flex:1;font:inherit;font-size:13px;padding:7px 10px;border-radius:8px;border:1px solid var(--line);background:var(--surface);color:var(--ink)}
#tema{font:inherit;font-size:12.5px;padding:0 10px;border-radius:8px;border:1px solid var(--line);background:var(--surface);color:var(--muted);cursor:pointer}
nav{padding:10px 8px 40px;font-size:13.5px}
details{margin:1px 0} summary{list-style:none;cursor:pointer} summary::-webkit-details-marker{display:none}
.no{display:flex;align-items:center;gap:6px;padding:6px 8px;border-radius:7px;color:var(--ink);text-decoration:none}
.no:hover{background:var(--hover)}
.seta{width:14px;flex:none;color:var(--faint);font-size:10px;transition:transform .15s}
details[open]>summary .seta{transform:rotate(90deg)}
.pag>summary .no{font-weight:600}
.pag .n{margin-left:auto;font-size:11px;color:var(--faint);font-weight:400}
.nivel2{padding-left:14px;border-left:1px solid var(--line);margin-left:15px}
.nivel3{padding-left:12px;border-left:1px solid var(--line);margin-left:15px}
.nivel3 .no{color:var(--muted);font-size:12.5px;padding:4px 8px}
.no.ativo{background:var(--accent-soft);color:var(--ink);box-shadow:inset 3px 0 0 var(--accent)}
.vazio{width:14px;flex:none}
main{min-width:0;padding:34px 48px 120px}
.wrap{max-width:960px;margin:0 auto}
.trilha{font-size:12.5px;color:var(--muted);margin-bottom:6px;min-height:18px}
.doc{line-height:1.65;font-size:15.5px}
.doc h1{font-family:var(--display);font-weight:500;font-size:34px;margin:0 0 14px}
.doc h2{font-family:var(--display);font-weight:500;font-size:23px;margin:42px 0 10px;padding-top:14px;border-top:1px solid var(--line)}
.doc h3{font-size:15px;font-weight:600;color:var(--muted);margin:24px 0 6px}
.doc blockquote{margin:0 0 18px;padding:12px 16px;border-left:3px solid var(--accent);background:var(--quote);border-radius:0 10px 10px 0}
.doc blockquote p{margin:0}
.doc a{color:var(--link)}
.doc code{font-family:Menlo,monospace;font-size:12.5px;background:var(--code);padding:1px 5px;border-radius:4px}
.doc pre{background:var(--pre);border:1px solid var(--line);border-radius:10px;padding:12px;overflow:auto} .doc pre code{background:none;padding:0}
.doc table{border-collapse:collapse;margin:10px 0 16px;font-size:14px;width:100%;background:var(--surface)}
.doc th,.doc td{border:1px solid var(--line);padding:8px 11px;text-align:left;vertical-align:top}
.doc th{background:var(--panel);color:var(--muted);font-weight:600;font-size:13px}
.mermaid{background:#FFFFFF;border:1px solid var(--line);border-radius:12px;padding:16px;margin:14px 0;overflow:auto;text-align:center}
.wall{display:flex;gap:14px;overflow-x:auto;padding:16px;background:var(--wall);border-radius:14px;margin:12px 0}
.wall .step{min-width:170px;display:flex;flex-direction:column;gap:6px}
.wall .num{font-size:11px;color:var(--faint);font-weight:600}
.note{border-radius:4px;padding:8px 10px;font-size:12.5px;line-height:1.35;color:#1D2433;box-shadow:0 1px 3px rgba(0,0,0,.15)}
.note.ator{background:#FFE9A8} .note.cmd{background:#B9D3FF} .note.evt{background:#FFB36B;font-weight:600} .note.pol{background:#DCC4F7}
.legend{display:flex;gap:12px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin:6px 0}
.legend span::before{content:"";display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:-1px;background:var(--c)}
.gen{font-size:12px;color:var(--faint);margin:0}
.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:14px 0}
.card pre{white-space:pre-wrap;font-size:12.5px;margin:0}
@media(max-width:900px){body{grid-template-columns:1fr}aside{position:static;height:auto}main{padding:24px 18px 80px}}
</style></head><body>
<aside><div class="topo"><div class="brand">__NOME__<small>documentação do domínio</small></div>
<div class="ferr"><input id="q" placeholder="Buscar…"><button id="tema" title="Alternar tema">Escuro</button></div></div>
<nav id="arvore"></nav></aside>
<main><div class="wrap"><div class="trilha" id="trilha"></div><div class="doc" id="doc"></div></div></main>
<script>
const D = __DADOS__;
const esc = s => (s||'').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const slug = t => t.trim().toLowerCase().replace(/[`*_\[\]()]/g,'').replace(/[^\p{L}\p{N}\- ]/gu,'').replace(/ /g,'-');
let tema = 'claro'; try { tema = localStorage.getItem('sinter-tema') || 'claro'; } catch(e) {}
let atual = null;
function aplicaTema(){ document.documentElement.dataset.tema = tema; document.getElementById('tema').textContent = tema === 'claro' ? 'Escuro' : 'Claro';
  mermaid.initialize({startOnLoad:false, securityLevel:'loose', theme:'base', themeVariables:{fontFamily:'Avenir Next, Helvetica Neue, sans-serif', primaryColor:'#E8EEF3', primaryBorderColor:'#5A626A', primaryTextColor:'#1D2433', lineColor:'#5A626A', clusterBkg:'#F6F8FA', clusterBorder:'#AEB6BE', edgeLabelBackground:'#FFFFFF', actorBkg:'#E8EEF3', actorBorder:'#5A626A', noteBkgColor:'#FFF6DA'}}); }
document.getElementById('tema').onclick = () => { tema = tema === 'claro' ? 'escuro' : 'claro'; try { localStorage.setItem('sinter-tema', tema); } catch(e) {} aplicaTema(); if (atual) mostrar(atual, null, true); };

function arvore(){
  let h = '';
  for (const p of D.paginas) {
    h += `<details class="pag" data-p="${p.arquivo}"><summary><a class="no" href="#" data-p="${p.arquivo}"><span class="seta">▶</span>${esc(p.nome)}<span class="n">${p.secoes.length}</span></a></summary><div class="nivel2">`;
    for (const s of p.secoes) {
      if (s.subs.length) {
        h += `<details data-busca="${esc((s.titulo + ' ' + s.subs.map(x=>x.titulo).join(' ')).toLowerCase())}"><summary><a class="no" href="#" data-p="${p.arquivo}" data-a="${s.slug}"><span class="seta">▶</span>${esc(s.titulo)}</a></summary><div class="nivel3">`;
        for (const t of s.subs) h += `<a class="no" href="#" data-p="${p.arquivo}" data-a="${t.slug}" data-pai="${s.slug}"><span class="vazio"></span>${esc(t.titulo)}</a>`;
        h += `</div></details>`;
      } else h += `<a class="no" href="#" data-p="${p.arquivo}" data-a="${s.slug}" data-busca="${esc(s.titulo.toLowerCase())}"><span class="vazio"></span>${esc(s.titulo)}</a>`;
    }
    h += `</div></details>`;
  }
  if (D.cartao) h += `<details class="pag" data-p="_ia"><summary><a class="no" href="#" data-p="_ia"><span class="seta">▶</span>Para IA<span class="n">1</span></a></summary><div class="nivel2"><a class="no" href="#" data-p="_ia"><span class="vazio"></span>Cartão do domínio</a></div></details>`;
  const nav = document.getElementById('arvore'); nav.innerHTML = h;
  nav.querySelectorAll('a.no').forEach(a => a.onclick = e => { e.preventDefault(); mostrar(a.dataset.p, a.dataset.a || null); });
}
function parede(table){
  const ths = [...table.querySelectorAll('th')].map(t => t.textContent);
  if (!ths.some(t => t.includes('🟧'))) return;
  const idx = k => ths.findIndex(t => t.includes(k));
  const cols = {ator: idx('🟨'), cmd: idx('🟦'), evt: idx('🟧'), pol: idx('🟪')};
  const w = document.createElement('div'); w.className = 'wall';
  [...table.querySelectorAll('tbody tr')].forEach((tr, i) => {
    const td = [...tr.children].map(c => c.innerHTML);
    let h = `<div class="step"><div class="num">${i+1}</div>`;
    for (const [k, j] of Object.entries(cols)) if (j >= 0 && td[j] && td[j].replace(/<[^>]+>/g,'').trim() && td[j].trim() !== '—') h += `<div class="note ${k}">${td[j]}</div>`;
    w.innerHTML += h + '</div>';
  });
  const leg = document.createElement('div'); leg.className = 'legend';
  leg.innerHTML = '<span style="--c:#FFE9A8">Quem</span><span style="--c:#B9D3FF">Faz</span><span style="--c:#FFB36B">Acontece</span><span style="--c:#DCC4F7">Regra ou reação</span>';
  table.replaceWith(leg); leg.after(w);
}
async function mostrar(arq, ancora, forcar){
  const doc = document.getElementById('doc');
  if (arq !== atual || forcar) {
    atual = arq;
    if (arq === '_ia') {
      doc.innerHTML = `<h1>Para IA</h1><blockquote><p>O que um agente lê primeiro: ~${Math.round(D.cartao.length/4)} tokens. Resumos completos em <code>llm/resumos.md</code>; ligações em <code>llm/grafo.json</code>.</p></blockquote><div class="card"><pre>${esc(D.cartao)}</pre></div>`;
    } else {
      const p = D.paginas.find(x => x.arquivo === arq);
      doc.innerHTML = marked.parse(p.texto.replace(/^## Nesta p[áa]gina[\s\S]*?(?=^## )/m, ''));
      let parent = ''; const used = new Map(); const githubCounts = new Map(); p.aliases = {};
      doc.querySelectorAll('h1, h2, h3').forEach(h => {
        let id = slug(h.textContent); const plain = id; const seen = githubCounts.get(plain) || 0; githubCounts.set(plain, seen + 1); const nativeAnchor = plain + (seen ? '-' + seen : '');
        if (h.tagName === 'H2') parent = id;
        if (h.tagName === 'H3') id = parent + '--' + id;
        const count = used.get(id) || 0; used.set(id, count + 1);
        if (count) id += '-' + count;
        p.aliases[nativeAnchor] = id; h.dataset.anchor = id; h.id = arq.replace('.md','') + '--' + id;
      });
      doc.querySelectorAll('a[href]').forEach(a => {
        const raw = a.getAttribute('href');
        const [file, anchor] = raw.split('#');
        const target = file.replace(/^\.\//,'');
        if ((!file && anchor) || D.paginas.some(x => x.arquivo === target)) {
          const dest = file ? target : arq;
          a.href = '#' + encodeURIComponent(dest) + (anchor ? '#' + anchor : '');
          a.onclick = e => { e.preventDefault(); mostrar(dest, anchor ? decodeURIComponent(anchor) : null); };
        } else if (!/^(?:[a-z]+:|\/)/i.test(raw)) a.setAttribute('href', '../' + raw);
      });
      doc.querySelectorAll('table').forEach(parede);
      doc.querySelectorAll('table').forEach(table => { const wrapper = document.createElement('div'); wrapper.className = 'table-scroll'; table.replaceWith(wrapper); wrapper.append(table); });
      if (arq === '2-arquitetura.md' && D.mapa) {
        const walker = document.createTreeWalker(doc, NodeFilter.SHOW_COMMENT);
        let marker; while (marker = walker.nextNode()) {
          if (marker.textContent.trim() !== 'MAPA-PRINCIPAL') continue;
          const box = document.createElement('div'); box.className = 'mapa-principal';
          box.innerHTML = '<p class="gen">Mapa de dependências gerado das relações declaradas em Serviços; estados preservados.</p><div class="mermaid"></div>';
          box.querySelector('.mermaid').textContent = D.mapa; marker.replaceWith(box); break;
        }
      }
      doc.querySelectorAll('pre > code.language-mermaid').forEach(c => { const d = document.createElement('div'); d.className = 'mermaid'; d.textContent = c.textContent; c.parentElement.replaceWith(d); });
      try { await mermaid.run({nodes: doc.querySelectorAll('.mermaid')}); } catch(e){ console.warn(e); }
      observar();
    }
  }
  document.querySelectorAll('details.pag').forEach(d => d.open = d.dataset.p === arq || (d.open && !!document.getElementById('q').value));
  if (ancora) { const p = D.paginas.find(x => x.arquivo === arq); ancora = (p && p.aliases && p.aliases[ancora]) || ancora; const el = document.getElementById(arq.replace('.md','') + '--' + ancora); if (el) el.scrollIntoView(); } else window.scrollTo(0, 0);
  marcar(arq, ancora);
}
function marcar(arq, ancora){
  document.querySelectorAll('#arvore a.no').forEach(a => a.classList.remove('ativo'));
  const sel = ancora ? `#arvore a.no[data-p="${arq}"][data-a="${ancora}"]` : `#arvore details.pag[data-p="${arq}"] > summary a.no`;
  const a = document.querySelector(sel); if (!a) return;
  a.classList.add('ativo');
  let d = a.closest('details'); while (d) { d.open = true; d = d.parentElement.closest('details'); }
  const pg = D.paginas.find(x => x.arquivo === arq);
  const partes = [pg ? pg.nome : 'Para IA'];
  if (ancora && a.dataset.pai) { const pai = document.querySelector(`#arvore a.no[data-p="${arq}"][data-a="${a.dataset.pai}"]`); if (pai) partes.push(pai.textContent.trim()); }
  if (ancora) partes.push(a.textContent.trim());
  document.getElementById('trilha').textContent = partes.join('  ›  ');
}
let obs;
function observar(){
  if (obs) obs.disconnect();
  obs = new IntersectionObserver(es => { const vis = es.filter(e => e.isIntersecting); if (vis.length) marcar(atual, vis[0].target.dataset.anchor); }, {rootMargin:'0px 0px -75% 0px'});
  document.querySelectorAll('#doc h2, #doc h3').forEach(h => obs.observe(h));
}
document.getElementById('q').oninput = e => {
  const f = e.target.value.toLowerCase().trim();
  document.querySelectorAll('#arvore [data-busca]').forEach(el => { const ok = !f || el.dataset.busca.includes(f); el.style.display = ok ? '' : 'none'; if (f && ok && el.tagName === 'DETAILS') el.open = true; });
  document.querySelectorAll('#arvore .nivel3 a.no').forEach(a => { if (f) { const ok = a.textContent.toLowerCase().includes(f) || a.closest('details').dataset.busca.split(' ')[0].includes(f); a.style.display = ok || a.closest('details').dataset.busca.includes(f) ? '' : 'none'; } else a.style.display = ''; });
  if (f) document.querySelectorAll('details.pag').forEach(d => d.open = !![...d.querySelectorAll('[data-busca]')].some(x => x.style.display !== 'none'));
};
function abrirHash(){
  const [file, anchor] = location.hash.slice(1).split('#');
  const decoded = decodeURIComponent(file || '');
  mostrar(D.paginas.some(p => p.arquivo === decoded) ? decoded : D.paginas[0].arquivo, anchor ? decodeURIComponent(anchor) : null);
}
aplicaTema(); arvore(); abrirHash(); window.addEventListener('hashchange', abrirHash);
</script></body></html>"""

saida = repo / "site"
saida.mkdir(exist_ok=True)
(saida / "index.html").write_text(pagina.replace("__NOME__", html.escape(nome)).replace("__DADOS__", json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")), encoding="utf-8")
print(saida / "index.html", f"({len(P)} páginas, {len(nomes)} serviços, {len(ares)} chamadas no mapa)")
