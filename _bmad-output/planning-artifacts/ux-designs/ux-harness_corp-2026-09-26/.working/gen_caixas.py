"""Gera .working/caixas.html: visão de arquitetura (caixas) do domínio inteiro, estilo Esmalte v4."""
import pathlib, re

here = pathlib.Path(__file__).parent
v4 = (here / "esmalte-v4.html").read_text()
style = re.search(r"<style>(.*?)</style>", v4, re.S).group(1)
rail = re.search(r'<nav class="rail".*?</nav>', v4, re.S).group(0)

TECH = {"Kt": "#C9B8F2", "Jv": "#F0B27A", "Py": "#F2D06B", "Go": "#8FD0E8", "Nd": "#9FD9B0", "Ts": "#7EA6F4"}
# subdomínio: (coluna, linha, cor, [(sistema, tech, status)])  status: ok | inf | off
GROUPS = {
    "Checkout":      (0, 0, "#C9B8F2", [("checkout-api", "Kt", "ok"), ("wallet", "Go", "ok"), ("cart-service", "Kt", "ok"), ("checkout-web", "Ts", "ok")]),
    "Autorização":   (1, 0, "#7EA6F4", [("payments-gateway", "Jv", "ok"), ("antifraude", "Py", "ok"), ("tokenizer", "Go", "ok"), ("3ds-service", "Jv", "ok"), ("risk-rules", "Py", "ok")]),
    "Assinaturas":   (2, 0, "#8FD0E8", [("subscriptions", "Kt", "ok"), ("plans", "Kt", "ok"), ("renewals", "Kt", "ok"), ("dunning", "Nd", "ok"), ("trials", "Kt", "ok"), ("coupons", "Nd", "inf"), ("entitlements", "Go", "ok")]),
    "Comunicação":   (0, 1, "#B69CF0", [("notificacoes", "Nd", "inf"), ("email-sender", "Nd", "ok"), ("sms-gateway", "Go", "ok")]),
    "Contabilidade": (1, 1, "#E2B566", [("ledger", "Jv", "ok"), ("billing-batch", "?", "off"), ("fees-engine", "Jv", "ok"), ("tax-calc", "Py", "ok"), ("journal-export", "?", "off"), ("reports", "Py", "ok")]),
    "Cobrança":      (2, 1, "#9FD9B0", [("invoices", "Kt", "ok"), ("boleto", "Go", "ok"), ("pix-charges", "Go", "ok"), ("collections", "Kt", "ok")]),
    "Conciliação":   (1, 2, "#F0B27A", [("recon-engine", "Jv", "ok"), ("acquirer-files", "Py", "ok"), ("chargebacks", "Jv", "ok"), ("settlement", "Jv", "ok"), ("disputes", "?", "off")]),
}
# integrações agregadas entre subdomínios: (origem, destino, quantidade, tipo dominante, em foco)
LINKS = [
    ("Checkout", "Autorização", 2, "API", True),
    ("Checkout", "Comunicação", 1, "evento inferido", True),
    ("Autorização", "Contabilidade", 1, "evento", False),
    ("Assinaturas", "Autorização", 1, "API", False),
    ("Assinaturas", "Cobrança", 1, "API", False),
    ("Assinaturas", "Comunicação", 1, "evento", False),
    ("Cobrança", "Contabilidade", 1, "API", False),
    ("Conciliação", "Contabilidade", 3, "arquivo", False),
]
FOCUS = "checkout-api"

COLW, GAPX, X0, Y0 = 280, 60, 30, 30
CARD_W, CARD_H, PAD, GAPC = 121, 40, 12, 8


def group_box(name):
    col, row, col_, systems = GROUPS[name]
    rows = (len(systems) + 1) // 2
    h = 44 + rows * (CARD_H + GAPC) + PAD - GAPC + 6
    y = Y0 + [0, 250, 480][row]
    x = X0 + col * (COLW + GAPX)
    return x, y, COLW, h


svg = ['<svg viewBox="0 0 1000 700" preserveAspectRatio="xMidYMid meet" aria-label="Arquitetura do domínio Pagamentos em caixas">',
       '<defs><pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#394046"/></pattern>'
       '<linearGradient id="tile" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4A525A"/><stop offset="1" stop-color="#3A4147"/></linearGradient>'
       '<filter id="glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
       '<marker id="ah" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L8,4 L0,8z" fill="#7C858D"/></marker>'
       '<marker id="ahn" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L8,4 L0,8z" fill="#46F28E"/></marker></defs>',
       '<rect width="1000" height="700" fill="url(#dots)"/>']


def anchor(a, b):
    ax, ay, aw, ah = group_box(a)
    bx, by, bw, bh = group_box(b)
    acx, acy, bcx, bcy = ax + aw / 2, ay + ah / 2, bx + bw / 2, by + bh / 2
    if abs(acx - bcx) > abs(acy - bcy):
        if bcx > acx:
            return (ax + aw, acy), (bx, bcy)
        return (ax, acy), (bx + bw, bcy)
    if bcy > acy:
        return (acx, ay + ah), (bcx, by)
    return (acx, ay), (bcx, by + bh)


labels = []
for a, b, n, kind, hot in LINKS:
    (x1, y1), (x2, y2) = anchor(a, b)
    if abs(x1 - x2) > abs(y1 - y2):
        mx = (x1 + x2) / 2
        d = f"M{x1},{y1} H{mx} V{y2} H{x2}"
        lx, ly = mx, (y1 + y2) / 2
    else:
        my = (y1 + y2) / 2
        d = f"M{x1},{y1} V{my} H{x2} V{y2}"
        lx, ly = (x1 + x2) / 2, my
    inferred = "inferido" in kind
    col = "#46F28E" if hot and not inferred else ("#EE6F7C" if inferred else "#7C858D")
    dash = ' stroke-dasharray="2 5" stroke-linecap="round"' if inferred else ""
    flt = ' filter="url(#glow)"' if hot and not inferred else ""
    mk = "ahn" if hot and not inferred else "ah"
    svg.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{2.4 if hot else 1.6}"{dash}{flt} marker-end="url(#{mk})" stroke-linejoin="round"/>')
    txt = f"{n} {'integração' if n == 1 else 'integrações'}, {kind}"
    w = 7 + len(txt) * 5.7
    labels.append(f'<rect x="{lx - w / 2:.0f}" y="{ly - 11:.0f}" width="{w:.0f}" height="22" rx="11" fill="#2A2F34" stroke="{col}" stroke-opacity=".8"/>'
                  f'<text x="{lx:.0f}" y="{ly + 4:.0f}" text-anchor="middle" font-size="11" fill="{"#C8FBDD" if hot and not inferred else "#C9C6BF"}">{txt}</text>')

for name, (colx, row, gcol, systems) in GROUPS.items():
    x, y, w, h = group_box(name)
    focus_group = any(s[0] == FOCUS for s in systems)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="rgba(255,255,255,.025)" stroke="{gcol}" stroke-opacity="{.7 if focus_group else .35}"/>')
    svg.append(f'<circle cx="{x + 18}" cy="{y + 21}" r="4" fill="{gcol}"/>'
               f'<text x="{x + 30}" y="{y + 25}" font-size="14" font-weight="600" fill="#E8E4DB" style="font-family:Optima,Avenir Next,sans-serif">{name}</text>'
               f'<text x="{x + w - 14}" y="{y + 25}" text-anchor="end" font-size="11" fill="#8D949A">{len(systems)} sistemas</text>')
    for i, (s, tech, st) in enumerate(systems):
        cx = x + PAD + (i % 2) * (CARD_W + GAPC)
        cy = y + 40 + (i // 2) * (CARD_H + GAPC)
        foc = s == FOCUS
        if st == "off":
            svg.append(f'<rect x="{cx}" y="{cy}" width="{CARD_W}" height="{CARD_H}" rx="10" fill="none" stroke="#5D656C" stroke-dasharray="4 3"/>'
                       f'<text x="{cx + CARD_W / 2}" y="{cy + 17}" text-anchor="middle" font-size="11.5" fill="#9DA3A8">{s}</text>'
                       f'<text x="{cx + CARD_W / 2}" y="{cy + 31}" text-anchor="middle" font-size="9.5" fill="#6E757B">sem acesso</text>')
            continue
        stroke = "#46F28E" if foc else ("#5A626A" if st == "ok" else "#8A5A62")
        dash = ' stroke-dasharray="1 4" stroke-linecap="round" stroke-width="1.6"' if st == "inf" else ""
        flt = ' filter="url(#glow)"' if foc else ""
        svg.append(f'<rect x="{cx}" y="{cy}" width="{CARD_W}" height="{CARD_H}" rx="10" fill="{"url(#tile)" if st == "ok" else "#30353A"}" stroke="{stroke}"{" stroke-width=\"1.8\"" if foc else ""}{dash}{flt}/>')
        svg.append(f'<rect x="{cx + 7}" y="{cy + 9}" width="22" height="22" rx="6" fill="#2F3439" stroke="#4D555C"/>'
                   f'<text x="{cx + 18}" y="{cy + 24}" text-anchor="middle" font-size="9.5" font-weight="700" fill="{TECH.get(tech, "#9DA3A8")}">{tech}</text>'
                   f'<text x="{cx + 35}" y="{cy + 25}" font-size="{11 if len(s) > 13 else 11.5}" font-weight="{600 if foc else 500}" fill="{"#46F28E" if foc else "#E8E4DB"}">{s}</text>')
        if st == "ok":
            svg.append(f'<circle cx="{cx + CARD_W - 9}" cy="{cy + 9}" r="3" fill="#46F28E" opacity=".9"/>')
svg.extend(labels)
svg.append("</svg>")

extra = """
.levels a{text-decoration:none}
.body{grid-template-columns:76px 260px 1fr 320px}
.canvas svg text{font-family:'Avenir Next','Helvetica Neue',sans-serif}
.legend2{position:absolute;left:16px;bottom:16px;display:flex;gap:14px;align-items:center;font-size:12px;color:var(--muted);background:rgba(31,35,39,.9);border:1px solid var(--line);border-radius:10px;padding:8px 12px}
.legend2 span{display:flex;align-items:center;gap:6px}
.legend2 i{width:12px;height:12px;border-radius:4px;display:inline-block}
.stat{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0 18px}
.stat div{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:10px}
.stat b{display:block;font-family:var(--display);font-size:24px;font-weight:500}
.stat span{font-size:12px;color:var(--muted)}
.stat .ok b{color:var(--neon)} .stat .bad b{color:#F2B7BE}
.sel{background:var(--surface);border:1px solid var(--neon);border-radius:12px;padding:12px;box-shadow:0 0 18px rgba(70,242,142,.15)}
.sel .k{display:block;font-size:11.5px;color:var(--neon);margin-bottom:8px}
.sel .ph h3{font-size:16px}
"""
subs = "".join(f'<div class="row{" on" if n == "Checkout" else ""}"><span class="ic" style="color:{v[2]}">■</span>{n}<em>{len(v[3])} sistemas</em></div>' for n, v in GROUPS.items())

body = f"""
<div class="note"><h1>Arquitetura em caixas</h1>
<p>Terceira visão do nível Domínio, ao lado de Mundo e Grafo: os subdomínios como caixas com os sistemas dentro, e as integrações agregadas entre subdomínios (quantidade e tipo). É a visão para ler a arquitetura como documento e para exportar. Todas as três mostram os mesmos dados.</p></div>
<div class="app">
  <div class="top">
    <span class="brand"><svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true"><circle cx="4" cy="5" r="1.6" fill="#9DA3A8"/><circle cx="8" cy="3" r="1.2" fill="#9DA3A8"/><circle cx="3" cy="10" r="1.1" fill="#9DA3A8"/><rect x="7" y="7" width="12" height="12" rx="4" fill="#46F28E"/></svg>Sinter</span>
    <span class="crumbs">Empresa<span>/</span><b>Pagamentos</b></span>
    <span class="levels"><a>Empresa</a><a class="on">Domínio</a><a>Sistema</a><a>Componente</a></span>
    <span class="levels" style="margin-left:auto"><a href="mundo.html">Mundo</a><a href="grafo.html">Grafo</a><a class="on">Caixas</a></span>
    <button>Exportar</button>
  </div>
  <div class="body">
    {rail}
    <aside class="side"><div class="list"><h5>Subdomínios</h5>{subs}</div></aside>
    <div class="canvas">
      {''.join(svg)}
      <div class="legend2"><span><i style="border:1.5px solid #46F28E"></i>Em foco</span><span><i style="background:#46F28E;width:6px;height:6px;border-radius:50%"></i>Aprovado</span><span><i style="border:1.5px dotted #EE6F7C"></i>Inferido</span><span><i style="border:1px dashed #6E757B"></i>Sem acesso</span></div>
    </div>
    <aside class="panel">
      <div class="sel"><span class="k">Selecionado</span><div class="ph"><span class="tech">Kt</span><div><h3>checkout-api</h3><p>Checkout. Fala com Autorização (2) e Comunicação (1, inferida).</p></div></div><button class="glaze" style="width:100%;margin-top:10px">Abrir no nível Sistema</button></div>
      <div class="ph" style="margin-top:18px"><span class="tech" style="color:#46F28E">Pg</span><div><h3>Pagamentos</h3><p>Dono do domínio: Rafael Nunes</p></div></div>
      <div class="stat"><div><b>34</b><span>sistemas</span></div><div><b>7</b><span>subdomínios</span></div><div class="ok"><b>88%</b><span>aprovado</span></div><div class="bad"><b>9</b><span>conflitos abertos</span></div></div>
      <h5 style="margin:0 0 6px;font-size:12px;color:var(--muted);font-weight:600">Exportar esta visão</h5>
      <div style="display:flex;gap:8px;flex-wrap:wrap"><button>C4 (Structurizr)</button><button>SVG</button><button>Markdown</button></div>
    </aside>
  </div>
</div>
"""
page = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sinter: arquitetura em caixas</title><style>{style}{extra}</style></head><body>{body}</body></html>"""
(here / "caixas.html").write_text(page, encoding="utf-8")
print("ok")
