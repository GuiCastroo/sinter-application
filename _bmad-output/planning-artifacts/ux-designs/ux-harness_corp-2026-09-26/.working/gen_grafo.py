"""Gera .working/grafo.html: visão Domínio (constelação) no estilo Esmalte v4."""
import pathlib, re, random, math

here = pathlib.Path(__file__).parent
v4 = (here / "esmalte-v4.html").read_text()
style = re.search(r"<style>(.*?)</style>", v4, re.S).group(1)
rail = re.search(r'<nav class="rail".*?</nav>', v4, re.S).group(0)

random.seed(11)
# subdomínio: (centro x, centro y, raio, cor do esmalte, sistemas)
CLUSTERS = {
    "Checkout":      (330, 250, 70, "#C9B8F2", ["checkout-api", "wallet", "cart-service", "checkout-web"]),
    "Autorização":   (560, 190, 80, "#7EA6F4", ["payments-gateway", "antifraude", "tokenizer", "3ds-service", "risk-rules"]),
    "Contabilidade": (640, 430, 85, "#E2B566", ["ledger", "billing-batch", "fees-engine", "tax-calc", "journal-export", "reports"]),
    "Comunicação":   (230, 470, 55, "#B69CF0", ["notificacoes", "email-sender", "sms-gateway"]),
    "Assinaturas":   (860, 250, 85, "#8FD0E8", ["subscriptions", "plans", "renewals", "dunning", "trials", "coupons", "entitlements"]),
    "Conciliação":   (430, 610, 70, "#F0B27A", ["recon-engine", "acquirer-files", "chargebacks", "settlement", "disputes"]),
    "Cobrança":      (880, 560, 60, "#9FD9B0", ["invoices", "boleto", "pix-charges", "collections"]),
}
NOACCESS = {"billing-batch", "journal-export", "disputes"}
INFERRED_TARGETS = {"notificacoes", "coupons"}
FOCUS = "checkout-api"

pos = {}
for name, (cx, cy, r, col, systems) in CLUSTERS.items():
    n = len(systems)
    for i, s in enumerate(systems):
        a = 2 * math.pi * i / n + random.uniform(-.3, .3)
        rr = r * (0.35 + 0.65 * random.random()) if i else r * 0.15
        pos[s] = (cx + rr * math.cos(a), cy + rr * math.sin(a), col, name)

EDGES = [
    ("checkout-api", "payments-gateway"), ("checkout-api", "antifraude"), ("checkout-api", "wallet"),
    ("checkout-web", "checkout-api"), ("cart-service", "checkout-api"), ("payments-gateway", "tokenizer"),
    ("payments-gateway", "3ds-service"), ("antifraude", "risk-rules"), ("payments-gateway", "ledger"),
    ("ledger", "fees-engine"), ("ledger", "tax-calc"), ("ledger", "billing-batch"), ("ledger", "reports"),
    ("ledger", "journal-export"), ("ledger", "settlement"), ("recon-engine", "acquirer-files"),
    ("recon-engine", "ledger"), ("chargebacks", "disputes"), ("chargebacks", "ledger"), ("settlement", "recon-engine"),
    ("subscriptions", "plans"), ("subscriptions", "renewals"), ("renewals", "dunning"), ("subscriptions", "entitlements"),
    ("renewals", "payments-gateway"), ("trials", "subscriptions"), ("dunning", "email-sender"),
    ("invoices", "ledger"), ("invoices", "boleto"), ("invoices", "pix-charges"), ("collections", "invoices"),
    ("notificacoes", "email-sender"), ("notificacoes", "sms-gateway"), ("renewals", "invoices"),
    ("checkout-api", "notificacoes"), ("subscriptions", "coupons"),
]
deg = {}
for a, b in EDGES:
    deg[a] = deg.get(a, 0) + 1
    deg[b] = deg.get(b, 0) + 1

svg = ['<svg viewBox="150 90 860 620" preserveAspectRatio="xMidYMid meet" aria-label="Visão Domínio: 34 sistemas de Pagamentos">',
       '<defs><filter id="blur"><feGaussianBlur stdDeviation="28"/></filter>'
       '<filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
       '<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#353B41"/></pattern>']
for name, (cx, cy, r, col, _) in CLUSTERS.items():
    k = name.replace("ç", "c").replace("ã", "a")
    svg.append(f'<radialGradient id="sph-{k}" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".55"/>'
               f'<stop offset=".35" stop-color="{col}"/><stop offset="1" stop-color="#2A2F34"/></radialGradient>')
svg.append('<radialGradient id="sph-focus" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".7"/>'
           '<stop offset=".35" stop-color="#46F28E"/><stop offset="1" stop-color="#11402A"/></radialGradient></defs>')
svg.append('<rect width="1060" height="720" fill="url(#dots)"/>')

# halos dos subdomínios
for name, (cx, cy, r, col, systems) in CLUSTERS.items():
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r+40}" fill="{col}" opacity=".07" filter="url(#blur)"/>')
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r+34}" fill="none" stroke="{col}" stroke-opacity=".18" stroke-dasharray="2 5"/>')

# arestas
for a, b in EDGES:
    x1, y1, c1, g1 = pos[a]
    x2, y2, c2, g2 = pos[b]
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    qx, qy = mx - dy * .15, my + dx * .15
    inferred = b in INFERRED_TARGETS
    focus = FOCUS in (a, b)
    if inferred:
        for t in [i / 14 for i in range(1, 14)]:
            px = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * qx + t ** 2 * x2 + random.uniform(-4, 4)
            py = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * qy + t ** 2 * y2 + random.uniform(-4, 4)
            svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{random.uniform(1,2):.1f}" fill="#EE6F7C" opacity=".75"/>')
        continue
    col = "#46F28E" if focus else ("#7C858D" if g1 != g2 else c1)
    op = ".9" if focus else (".35" if g1 != g2 else ".45")
    w = 1.8 if focus else 1.1
    flt = ' filter="url(#glow)"' if focus else ""
    dash = ' stroke-dasharray="3 4"' if (a in NOACCESS or b in NOACCESS) else ""
    svg.append(f'<path d="M{x1:.1f},{y1:.1f} Q{qx:.1f},{qy:.1f} {x2:.1f},{y2:.1f}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{w}"{dash}{flt}/>')

# nós
for s, (x, y, col, g) in pos.items():
    k = g.replace("ç", "c").replace("ã", "a")
    r = 6 + 2.2 * deg.get(s, 0)
    r = min(r, 22)
    if s in NOACCESS:
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="none" stroke="#6E757B" stroke-dasharray="3 3"/>')
    elif s == FOCUS:
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r+9:.1f}" fill="none" stroke="#46F28E" stroke-opacity=".4"/>')
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="url(#sph-focus)" filter="url(#glow)"/>')
    else:
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="url(#sph-{k})"/>')
    big = deg.get(s, 0) >= 4 or s == FOCUS or s in NOACCESS or s in INFERRED_TARGETS
    if big:
        fill = "#46F28E" if s == FOCUS else "#C9C6BF"
        svg.append(f'<text x="{x:.1f}" y="{y + r + 14:.1f}" text-anchor="middle" font-size="{12.5 if s == FOCUS else 11.5}" '
                   f'font-weight="{600 if s == FOCUS else 500}" fill="{fill}">{s}</text>'.replace(f'y="{y + r + 14:.1f}"', f'y="{y + r + (24 if s == FOCUS else 14):.1f}"'))

# rótulos de subdomínio
for name, (cx, cy, r, col, systems) in CLUSTERS.items():
    svg.append(f'<text x="{cx}" y="{cy - r - 44}" text-anchor="middle" font-size="14" font-weight="600" fill="{col}" '
               f'style="font-family:Optima,Avenir Next,sans-serif">{name}</text>'
               f'<text x="{cx}" y="{cy - r - 28}" text-anchor="middle" font-size="11" fill="#8D949A">{len(systems)} sistemas</text>')
svg.append("</svg>")

rail2 = rail  # Mapa já está ativo
subs = "".join(
    f'<div class="row{" on" if n == "Checkout" else ""}"><span class="ic" style="color:{c[3]}">●</span>{n}<em>{len(c[4])} sistemas</em></div>'
    for n, c in CLUSTERS.items())

extra = """
.levels a{text-decoration:none}
.body{grid-template-columns:76px 260px 1fr 320px}
.canvas svg text{font-family:'Avenir Next','Helvetica Neue',sans-serif}
.legend2{position:absolute;left:16px;bottom:16px;display:flex;gap:14px;align-items:center;font-size:12px;color:var(--muted);background:rgba(31,35,39,.9);border:1px solid var(--line);border-radius:10px;padding:8px 12px}
.legend2 span{display:flex;align-items:center;gap:6px}
.legend2 i{width:10px;height:10px;border-radius:50%;display:inline-block}
.stat{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:14px 0 18px}
.stat div{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:10px}
.stat b{display:block;font-family:var(--display);font-size:24px;font-weight:500}
.stat span{font-size:12px;color:var(--muted)}
.stat .ok b{color:var(--neon)} .stat .bad b{color:#F2B7BE}
.hub{display:flex;justify-content:space-between;font-size:13px;padding:7px 0;border-bottom:1px solid #2E3338}
.hub em{font-style:normal;color:var(--muted);font-size:12px}
.sel{background:var(--surface);border:1px solid var(--neon);border-radius:12px;padding:12px;box-shadow:0 0 18px rgba(70,242,142,.15)}
.sel .k{display:block;font-size:11.5px;color:var(--neon);margin-bottom:8px}
.sel .ph h3{font-size:16px}
.tip{position:absolute;background:rgba(31,35,39,.96);border:1px solid var(--neon);border-radius:10px;padding:10px 12px;font-size:12.5px;line-height:1.45;box-shadow:0 0 18px rgba(70,242,142,.2);width:220px}
.tip b{font-size:13.5px}
.tip p{margin:4px 0 8px;color:var(--muted)}
"""

body = f"""
<div class="note"><h1>Grafo do domínio</h1>
<p>Nível Domínio: os 34 sistemas de Pagamentos como constelação, agrupados por subdomínio. O tamanho da esfera é o número de integrações; linhas cinza cruzam subdomínios; partículas vermelhas são integrações inferidas; contornos tracejados são sistemas sem acesso. Clicar em um subdomínio aproxima para o nível Sistema.</p></div>
<div class="app">
  <div class="top">
    <span class="brand"><svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true"><circle cx="4" cy="5" r="1.6" fill="#9DA3A8"/><circle cx="8" cy="3" r="1.2" fill="#9DA3A8"/><circle cx="3" cy="10" r="1.1" fill="#9DA3A8"/><rect x="7" y="7" width="12" height="12" rx="4" fill="#46F28E"/></svg>Sinter</span>
    <span class="crumbs"><b>Pagamentos</b></span>
    <span class="levels"><a>Empresa</a><a class="on">Domínio</a><a>Sistema</a><a>Componente</a></span>
    <span class="levels" style="margin-left:auto"><a href="mundo.html">Mundo</a><a class="on" href="grafo.html">Grafo</a><a href="caixas.html">Caixas</a></span>
    <button>Compartilhar</button>
  </div>
  <div class="body">
    {rail2}
    <aside class="side">
      <div class="list"><h5>Subdomínios</h5>{subs}</div>
    </aside>
    <div class="canvas">
      {''.join(svg)}
      <div class="search"><input value="Buscar sistema, contrato ou regra" readonly></div>
      <div class="layers"><span class="chip on">Subdomínios</span><span class="chip on">Status</span><span class="chip">Donos</span><span class="chip">Fluxos</span></div>
      <div class="legend2"><span><i style="background:#46F28E;box-shadow:0 0 6px #46F28E"></i>Em foco</span><span><i style="background:#7C858D"></i>Entre subdomínios</span><span><i style="background:#EE6F7C"></i>Inferida</span><span><i style="border:1px dashed #6E757B"></i>Sem acesso</span></div>
    </div>
    <aside class="panel">
      <div class="sel"><span class="k">Selecionado</span><div class="ph"><span class="tech">Kt</span><div><h3>checkout-api</h3><p>Checkout. 6 integrações: 4 aprovadas, 1 inferida.</p></div></div><button class="glaze" style="width:100%;margin-top:10px">Abrir no nível Sistema</button></div>
      <div class="ph" style="margin-top:18px"><span class="tech" style="color:#46F28E">Pg</span><div><h3>Pagamentos</h3><p>Dono do domínio: Rafael Nunes</p></div></div>
      <div class="stat" style="margin-top:12px">
        <div><b>34</b><span>sistemas</span></div><div><b>212</b><span>integrações</span></div>
        <div class="ok"><b>88%</b><span>aprovado</span></div><div class="bad"><b>9</b><span>conflitos abertos</span></div>
      </div>
      <h5 style="margin:0 0 6px;font-size:12px;color:var(--muted);font-weight:600">Mais conectados</h5>
      <div class="hub">ledger<em>10 integrações</em></div>
      <div class="hub">payments-gateway<em>6 integrações</em></div>
      <div class="hub">checkout-api<em>6 integrações</em></div>
      <div class="hub">subscriptions<em>5 integrações</em></div>
      <div class="infer" style="margin-top:16px"><strong>3 sistemas sem acesso</strong><p>billing-batch, journal-export e disputes não aparecem no .sinter/ dos vizinhos até alguém com acesso conectar a fonte.</p><div class="btns"><button class="glaze">Pedir acesso</button></div></div>
    </aside>
  </div>
</div>
"""
page = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sinter: Grafo do domínio</title><style>{style}{extra}</style></head><body>{body}</body></html>"""
(here / "grafo.html").write_text(page, encoding="utf-8")
print("ok")
