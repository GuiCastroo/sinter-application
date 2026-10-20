"""Gera .working/directions-1.html: 4 direções visuais do mapa do domínio (Sinter)."""
import pathlib, html

OUT = pathlib.Path(__file__).parent / "directions-1.html"

NODES = {
    "wallet": (150, 150, "wallet"),
    "checkout-api": (380, 200, "checkout-api"),
    "payments-gateway": (610, 150, "payments-gateway"),
    "antifraude": (610, 330, "antifraude"),
    "notificacoes": (150, 360, "notificacoes"),
    "ledger": (380, 440, "ledger"),
    "billing-batch": (610, 500, "billing-batch"),
}
# (origem, destino, tipo, rótulo, inferida)
EDGES = [
    ("wallet", "checkout-api", "api", "GET /balance", False),
    ("checkout-api", "payments-gateway", "api", "POST /authorize", False),
    ("checkout-api", "antifraude", "api", "POST /score", False),
    ("payments-gateway", "ledger", "evento", "PaymentAuthorized", False),
    ("checkout-api", "notificacoes", "evento", "PaymentAuthorized", True),
    ("ledger", "billing-batch", "arquivo", "conciliação diária", False),
]
FOCUS = "checkout-api"
NOACCESS = "billing-batch"

DIRS = [
    dict(
        slug="prancheta", name="Prancheta",
        why="O mapa como desenho técnico de arquiteto: papel de desenho azul-acinzentado, traço de grafite, "
            "cotas e anotações em serifa. Calmo e preciso; transmite rigor e autoria.",
        bg="#E6ECEF", surface="#F2F5F6", ink="#26323B", muted="#5E6D78", line="#9FB0BA",
        api="#1F6F8B", evento="#4B6A2E", arquivo="#8A5A1F", accent="#1F6F8B", conflict="#B03A2E",
        font="'Iowan Old Style', Charter, Georgia, serif", ui="'Avenir Next', 'Helvetica Neue', sans-serif",
        node="drafting", edge="straight", radius=2,
    ),
    dict(
        slug="metro", name="Metrô",
        why="O domínio como mapa de metrô: cada tipo de integração é uma linha colorida, cada sistema é uma estação. "
            "Lê-se de longe, em reunião, na tela grande. A ousadia está nas linhas; o resto é branco e silencioso.",
        bg="#FFFFFF", surface="#F4F5F7", ink="#14213D", muted="#5A6478", line="#D5D9E0",
        api="#0057B8", evento="#00965E", arquivo="#F2A900", accent="#0057B8", conflict="#D52B1E",
        font="'Avenir Next Condensed', 'Avenir Next', 'Helvetica Neue', sans-serif",
        ui="'Avenir Next', 'Helvetica Neue', sans-serif",
        node="station", edge="ortho", radius=6,
    ),
    dict(
        slug="esmalte", name="Esmalte",
        why="Vem do próprio nome: sinterizar é fundir partículas soltas em peça sólida. O conhecimento aprovado aparece "
            "como cerâmica esmaltada (sólido, brilhante); o inferido aparece como partículas ainda soltas.",
        bg="#33383D", surface="#3D4349", ink="#E4E1DA", muted="#A3A7AB", line="#5B6268",
        api="#6F9BE8", evento="#9CC5A1", arquivo="#E0B36A", accent="#6F9BE8", conflict="#E0735A",
        font="Optima, 'Gill Sans', 'Avenir Next', sans-serif", ui="Optima, 'Avenir Next', sans-serif",
        node="tile", edge="curve", radius=14,
    ),
    dict(
        slug="sobrio", name="Sóbrio",
        why="A opção segura para o comprador corporativo: claro, denso, familiar a quem usa Jira e Confluence. "
            "Incluída para comparação honesta; é a que mais se parece com qualquer ferramenta SaaS.",
        bg="#F6F7F9", surface="#FFFFFF", ink="#1D2433", muted="#667085", line="#D0D5DD",
        api="#0F7C86", evento="#6941C6", arquivo="#B54708", accent="#0F7C86", conflict="#C4320A",
        font="'Helvetica Neue', Helvetica, Arial, sans-serif", ui="'Helvetica Neue', Helvetica, Arial, sans-serif",
        node="card", edge="straight", radius=8,
    ),
]


def edge_path(d, a, b):
    (x1, y1, _), (x2, y2, _) = NODES[a], NODES[b]
    if d["edge"] == "ortho":
        mx = (x1 + x2) / 2
        return f"M{x1},{y1} H{mx} V{y2} H{x2}", (mx, (y1 + y2) / 2)
    if d["edge"] == "curve":
        cx, cy = (x1 + x2) / 2 + (y2 - y1) * 0.2, (y1 + y2) / 2 - (x2 - x1) * 0.2
        return f"M{x1},{y1} Q{cx},{cy} {x2},{y2}", ((x1 + 2 * cx + x2) / 4, (y1 + 2 * cy + y2) / 4)
    return f"M{x1},{y1} L{x2},{y2}", ((x1 + x2) / 2, (y1 + y2) / 2)


def render_map(d):
    s = []
    s.append(f'<svg viewBox="0 0 760 600" class="map" role="img" aria-label="Mapa do domínio Pagamentos">')
    if d["node"] == "drafting":
        s.append(f'<defs><pattern id="g-{d["slug"]}" width="20" height="20" patternUnits="userSpaceOnUse">'
                 f'<path d="M20 0H0V20" fill="none" stroke="{d["line"]}" stroke-width=".4" opacity=".6"/></pattern></defs>'
                 f'<rect width="760" height="600" fill="url(#g-{d["slug"]})"/>')
    labels = []
    SHIFT = {3: (0, 70), 1: (0, -16), 2: (0, 8)}
    for i, (a, b, t, label, inf) in enumerate(EDGES):
        p, (lx, ly) = edge_path(d, a, b)
        lx, ly = lx + SHIFT.get(i, (0, 0))[0], ly + SHIFT.get(i, (0, 0))[1]
        col = d[t]
        noacc = b == NOACCESS
        if d["node"] == "station":
            w = 9
        elif d["node"] == "tile":
            w = 3
        else:
            w = 1.6
        dash = ""
        if inf:
            dash = 'stroke-dasharray="1 7" stroke-linecap="round"' if d["node"] == "tile" else 'stroke-dasharray="6 5"'
            if d["node"] == "tile":
                w = 4
        if noacc:
            dash = 'stroke-dasharray="3 4"'
        op = ".55" if noacc else "1"
        s.append(f'<path d="{p}" fill="none" stroke="{col}" stroke-width="{w}" {dash} opacity="{op}" '
                 f'stroke-linejoin="round"/>')
        tcol = d["ink"]
        labels.append(f'<g class="elabel"><rect x="{lx-62}" y="{ly-11}" width="124" height="20" rx="{min(d["radius"],10)}" '
                 f'fill="{d["surface"]}" stroke="{col if not inf else d["conflict"]}" stroke-width="{1 if not inf else 1.2}" '
                 f'{"stroke-dasharray=\"3 3\"" if inf else ""}/>'
                 f'<text x="{lx}" y="{ly+4}" text-anchor="middle" fill="{tcol}" font-size="11">{html.escape(label)}'
                 f'{" (inferida)" if inf else ""}</text></g>')
    s.extend(labels)
    for key, (x, y, label) in NODES.items():
        focus = key == FOCUS
        noacc = key == NOACCESS
        stroke = d["accent"] if focus else d["ink"]
        if d["node"] == "station":
            r = 16 if focus else 12
            fill = d["accent"] if focus else "#FFFFFF"
            s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{d["ink"]}" stroke-width="4" '
                     f'{"stroke-dasharray=\"4 4\" opacity=\".6\"" if noacc else ""}/>')
            s.append(f'<text x="{x}" y="{y-24}" text-anchor="middle" fill="{d["ink"]}" font-size="{17 if focus else 15}" '
                     f'font-weight="{700 if focus else 600}" style="font-family:{d["font"]}">{label}</text>')
            if noacc:
                s.append(f'<text x="{x}" y="{y+34}" text-anchor="middle" fill="{d["muted"]}" font-size="11">sem acesso</text>')
        else:
            w, h = 150, 46
            rx = d["radius"]
            if d["node"] == "tile":
                fill = f"url(#glaze-{d['slug']})" if not noacc else d["bg"]
                if key == list(NODES)[0]:
                    s.insert(1, f'<defs><linearGradient id="glaze-{d["slug"]}" x1="0" y1="0" x2="0" y2="1">'
                                f'<stop offset="0" stop-color="#57606A"/><stop offset="1" stop-color="#434A51"/></linearGradient></defs>')
            elif d["node"] == "drafting":
                fill = d["surface"]
            else:
                fill = d["surface"]
            sw = 2.2 if focus else 1
            s.append(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
                     f'stroke="{stroke}" stroke-width="{sw}" {"stroke-dasharray=\"4 4\"" if noacc else ""}/>')
            if d["node"] == "drafting":
                for cx, cy in [(x-w/2, y-h/2), (x+w/2, y-h/2), (x-w/2, y+h/2), (x+w/2, y+h/2)]:
                    s.append(f'<path d="M{cx-5},{cy} h10 M{cx},{cy-5} v10" stroke="{d["muted"]}" stroke-width=".8"/>')
            if d["node"] == "tile" and focus:
                s.append(f'<rect x="{x-w/2-5}" y="{y-h/2-5}" width="{w+10}" height="{h+10}" rx="{rx+4}" fill="none" '
                         f'stroke="{d["accent"]}" stroke-width="1" opacity=".5"/>')
            s.append(f'<text x="{x}" y="{y+5 if not noacc else y}" text-anchor="middle" fill="{d["ink"]}" '
                     f'font-size="14" font-weight="{600 if focus else 500}" style="font-family:{d["font"]}"'
                     f'{" font-style=\"italic\"" if d["node"]=="drafting" else ""}>{label}</text>')
            if noacc:
                s.append(f'<text x="{x}" y="{y+15}" text-anchor="middle" fill="{d["muted"]}" font-size="10.5">sem acesso de leitura</text>')
    if d["node"] == "tile":
        # partículas soltas em volta da aresta inferida
        import random
        random.seed(3)
        for _ in range(26):
            px = 150 + random.random() * 230 + random.uniform(-10, 10)
            py = 200 + (px - 150) / 230 * 160 + random.uniform(-26, 26)
            s.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{random.uniform(1,2.4):.1f}" fill="{d["evento"]}" opacity=".55"/>')
    s.append("</svg>")
    return "\n".join(s)


def legend(d):
    items = [("API", d["api"], ""), ("Evento", d["evento"], ""), ("Arquivo", d["arquivo"], ""),
             ("Inferida, confirmar", d["conflict"], "dash")]
    out = []
    for name, c, st in items:
        style = f"border-top:3px {'dashed' if st else 'solid'} {c}"
        out.append(f'<span class="lg"><i style="{style}"></i>{name}</span>')
    return "".join(out)


def panel(d):
    return f"""
<aside class="panel">
  <h3>checkout-api</h3>
  <p class="resp">Recebe o pedido de pagamento do site e orquestra a autorização e o antifraude.</p>
  <dl>
    <dt>Dono</dt><dd>Squad Checkout, Diego Almeida</dd>
    <dt>Stack</dt><dd>Kotlin, Spring Boot, PostgreSQL</dd>
    <dt>Expõe</dt><dd>POST /payments<br>GET /payments/{{id}}</dd>
    <dt>Consome</dt><dd>payments-gateway, antifraude, wallet</dd>
  </dl>
  <div class="infer">
    <strong>Publica PaymentAuthorized?</strong>
    <p>Inferido a partir de <code>NotificationPublisher.kt:42</code>. Nenhum contrato documentado.</p>
    <div class="btns"><button class="primary">Confirmar integração</button><button>Descartar</button></div>
  </div>
  <p class="links">3 regras de negócio. ADR-012 Idempotência no checkout</p>
</aside>"""


def mock(d):
    css = f"""
#{d['slug']} {{ --bg:{d['bg']}; --surface:{d['surface']}; --ink:{d['ink']}; --muted:{d['muted']}; --line:{d['line']};
  --accent:{d['accent']}; --conflict:{d['conflict']}; font-family:{d['ui']}; }}
#{d['slug']} .display {{ font-family:{d['font']}; }}
"""
    tabs = ["Mapa", "Curadoria", "Conversas", "Tarefas", "Catálogo"]
    tabhtml = "".join(
        f'<a class="tab{" on" if t=="Mapa" else ""}">{t}{" <b class=badge>9 conflitos</b>" if t=="Curadoria" else ""}</a>'
        for t in tabs)
    return f"""
<section class="dir" id="{d['slug']}">
<style>{css}</style>
<header class="dirhead"><h2>{d['name']}</h2><p>{d['why']}</p>
<p class="hex">Fundo {d['bg']}, texto {d['ink']}, API {d['api']}, evento {d['evento']}, arquivo {d['arquivo']}, conflito {d['conflict']}</p></header>
<div class="frame">
  <div class="chrome"><span></span><span></span><span></span><em>localhost:4317/dominios/pagamentos/mapa</em></div>
  <div class="app">
    <nav class="top">
      <span class="brand display">Sinter</span>
      <span class="domain display">Pagamentos <small>34 sistemas, 212 integrações</small></span>
      <span class="tabs">{tabhtml}</span>
      <button class="primary">Adicionar fonte</button>
    </nav>
    <div class="body">
      <div class="canvas">
        <div class="tools"><input value="Buscar sistema ou contrato" readonly><span class="legend">{legend(d)}</span></div>
        {render_map(d)}
        <p class="more">Mostrando checkout-api e vizinhos. 27 sistemas ocultos.</p>
      </div>
      {panel(d)}
    </div>
  </div>
</div>
</section>"""


BASE = """
*{box-sizing:border-box} body{margin:0;background:#EDEDED;color:#222;font-family:'Helvetica Neue',sans-serif}
.intro{max-width:1180px;margin:32px auto 8px;padding:0 16px} .intro h1{font-size:26px;margin:0 0 6px}
.intro p{max-width:72ch;line-height:1.5;color:#444}
.dir{max-width:1180px;margin:40px auto;padding:0 16px}
.dirhead h2{font-size:22px;margin:0 0 4px} .dirhead p{margin:0 0 6px;max-width:80ch;line-height:1.5;color:#333}
.dirhead .hex{font-size:12px;color:#666}
.frame{border-radius:10px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.18);margin-top:12px}
.chrome{background:#D9D9D9;padding:8px 12px;display:flex;gap:6px;align-items:center}
.chrome span{width:11px;height:11px;border-radius:50%;background:#BDBDBD} .chrome em{font-style:normal;font-size:12px;color:#555;margin-left:12px}
.app{background:var(--bg);color:var(--ink)}
.top{display:flex;align-items:center;gap:20px;padding:12px 18px;border-bottom:1px solid var(--line)}
.brand{font-weight:700;font-size:18px;letter-spacing:.01em}
.domain{font-size:18px} .domain small{font-size:12px;color:var(--muted);margin-left:6px}
.tabs{display:flex;gap:4px;margin-left:auto}
.tab{padding:6px 10px;border-radius:6px;font-size:14px;color:var(--muted);cursor:default}
.tab.on{color:var(--ink);background:var(--surface);font-weight:600}
.badge{font-weight:600;font-size:11px;color:#fff;background:var(--conflict);border-radius:9px;padding:1px 7px;margin-left:4px}
button{font:inherit;font-size:13px;padding:7px 12px;border-radius:6px;border:1px solid var(--line);background:var(--surface);color:var(--ink)}
button.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.body{display:grid;grid-template-columns:1fr 320px;min-height:640px}
.canvas{position:relative;padding:12px 16px}
.tools{display:flex;gap:16px;align-items:center;flex-wrap:wrap}
.tools input{font:inherit;font-size:13px;padding:7px 10px;border:1px solid var(--line);border-radius:6px;background:var(--surface);color:var(--muted);width:240px}
.legend{display:flex;gap:14px;font-size:12px;color:var(--muted)} .lg{display:flex;align-items:center;gap:6px} .lg i{display:inline-block;width:22px}
.map{width:100%;height:auto;display:block;margin-top:6px} .map text{font-family:inherit}
.more{font-size:12px;color:var(--muted);margin:0}
.panel{border-left:1px solid var(--line);background:var(--surface);padding:18px}
.panel h3{margin:0 0 6px;font-size:18px} .resp{margin:0 0 14px;line-height:1.45;font-size:14px}
dl{display:grid;grid-template-columns:78px 1fr;gap:6px 10px;font-size:13px;margin:0 0 16px} dt{color:var(--muted)} dd{margin:0}
.infer{border:1px dashed var(--conflict);border-radius:8px;padding:12px;font-size:13px}
.infer p{margin:6px 0 10px;line-height:1.4;color:var(--muted)} .infer code{color:var(--ink)}
.btns{display:flex;gap:8px;flex-wrap:wrap} .links{font-size:12px;color:var(--muted);margin-top:16px}
@media (max-width:900px){.body{grid-template-columns:1fr}.panel{border-left:0;border-top:1px solid var(--line)}.tabs{display:none}}
"""

page = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sinter: direções visuais</title><style>{BASE}</style></head><body>
<div class="intro"><h1>Sinter: quatro direções para o mapa do domínio</h1>
<p>A mesma tela nas quatro: o domínio Pagamentos com foco em checkout-api, uma integração inferida esperando confirmação
e um sistema sem acesso de leitura. Compare a personalidade, não só a cor. Pode misturar: "linhas do Metrô com a paleta do Esmalte".</p></div>
{''.join(mock(d) for d in DIRS)}
</body></html>"""
OUT.write_text(page, encoding="utf-8")
print(OUT)
