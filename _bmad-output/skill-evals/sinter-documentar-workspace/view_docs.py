"""Gera um HTML navegável (Markdown + Mermaid renderizados) para cada pasta de saída de uma iteração."""
import json, pathlib, sys, html

it = pathlib.Path(sys.argv[1])
index = []
for out in sorted(it.glob("eval-*/*/outputs")):
    files = sorted(p for p in out.rglob("*.md"))
    if not files:
        continue
    data = {str(p.relative_to(out)): p.read_text(errors="ignore") for p in files}
    label = f"{out.parent.parent.name} · {'com skill' if out.parent.name == 'with_skill' else 'sem skill'}"
    page = out.parent / "docs.html"
    page.write_text(f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>{html.escape(label)}</title>
<script src="https://cdn.jsdelivr.net/npm/marked@15/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<style>
:root{{--bg:#1F2327;--side:#1A1D20;--card:#2A2F34;--ink:#E8E4DB;--muted:#9DA3A8;--neon:#46F28E;--line:#474E55}}
body{{margin:0;display:grid;grid-template-columns:320px 1fr;height:100vh;background:var(--bg);color:var(--ink);font-family:'Avenir Next','Helvetica Neue',sans-serif}}
aside{{background:var(--side);border-right:1px solid #2E3338;overflow:auto;padding:14px}}
aside h1{{font-size:14px;margin:0 0 10px;color:var(--neon)}}
aside a{{display:block;font-size:12.5px;padding:5px 8px;border-radius:6px;color:var(--muted);text-decoration:none;word-break:break-all}}
aside a.on,aside a:hover{{background:#343A40;color:var(--ink)}}
main{{overflow:auto;padding:24px 36px}}
main .doc{{max-width:900px}}
pre{{background:#1A1D20;border:1px solid var(--line);border-radius:8px;padding:12px;overflow:auto;font-size:12.5px}}
code{{font-family:Menlo,monospace;font-size:12.5px}}
table{{border-collapse:collapse;margin:10px 0;font-size:13px}} td,th{{border:1px solid var(--line);padding:6px 9px;text-align:left}}
a{{color:#7EA6F4}} h1,h2,h3{{font-weight:600}}
.fm{{background:#26382E;border:1px solid rgba(70,242,142,.4);border-radius:8px;padding:10px;font-size:12px;white-space:pre-wrap;font-family:Menlo,monospace;color:#C8FBDD}}
.mermaid{{background:#F4F5F7;border-radius:8px;padding:12px;margin:10px 0}}
</style></head><body>
<aside><h1>{html.escape(label)}</h1><div id="nav"></div></aside>
<main><div class="doc" id="doc"></div></main>
<script>
const F = {json.dumps(data, ensure_ascii=False)};
mermaid.initialize({{startOnLoad:false, theme:'default'}});
const nav = document.getElementById('nav'), doc = document.getElementById('doc');
const keys = Object.keys(F).sort((a,b)=> (a.includes('RELATORIO')?-1:0) - (b.includes('RELATORIO')?-1:0) || a.localeCompare(b));
async function show(k){{
  document.querySelectorAll('#nav a').forEach(a=>a.classList.toggle('on', a.dataset.k===k));
  let t = F[k], fm = '';
  const m = t.match(/^---\\n([\\s\\S]*?)\\n---\\n?/);
  if (m) {{ fm = '<div class="fm">'+m[1].replace(/</g,'&lt;')+'</div>'; t = t.slice(m[0].length); }}
  let h = marked.parse(t);
  h = h.replace(/<pre><code class="language-mermaid">([\\s\\S]*?)<\\/code><\\/pre>/g, (_, c) => '<div class="mermaid">'+c+'</div>');
  doc.innerHTML = '<p style="color:var(--muted);font-size:12px">'+k+'</p>' + fm + h;
  doc.querySelectorAll('.mermaid').forEach(el => {{ el.textContent = el.textContent.replace(/&gt;/g,'>').replace(/&lt;/g,'<').replace(/&amp;/g,'&'); }});
  try {{ await mermaid.run({{nodes: doc.querySelectorAll('.mermaid')}}); }} catch(e) {{ console.warn(e); }}
}}
keys.forEach(k => {{ const a = document.createElement('a'); a.href='#'; a.textContent=k; a.dataset.k=k; a.onclick=e=>{{e.preventDefault();show(k)}}; nav.appendChild(a); }});
show(keys[0]);
</script></body></html>""", encoding="utf-8")
    index.append((label, page, len(files)))

rows = "".join(f'<li><a href="{p.relative_to(it)}">{html.escape(l)}</a> — {n} arquivos</li>' for l, p, n in index)
(it / "docs-index.html").write_text(f"""<!doctype html><meta charset="utf-8"><title>Documentações geradas</title>
<body style="background:#1F2327;color:#E8E4DB;font-family:'Avenir Next',sans-serif;padding:30px">
<h1 style="font-weight:500">Documentações geradas: iteração 1</h1><ul style="line-height:2">{rows}</ul>
<style>a{{color:#46F28E}}</style></body>""", encoding="utf-8")
print(it / "docs-index.html")
