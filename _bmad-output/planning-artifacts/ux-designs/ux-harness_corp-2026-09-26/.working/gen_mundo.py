"""Gera .working/mundo.html: o domínio como um mundo 3D com constelações (subdomínios)."""
import pathlib, re, json

here = pathlib.Path(__file__).parent
v4 = (here / "esmalte-v4.html").read_text()
style = re.search(r"<style>(.*?)</style>", v4, re.S).group(1)
rail = re.search(r'<nav class="rail".*?</nav>', v4, re.S).group(0)

# subdomínio: latitude, longitude (graus), cor, sistemas
CLUSTERS = {
    "Checkout":      (28, -20, "#C9B8F2", ["checkout-api", "wallet", "cart-service", "checkout-web"]),
    "Autorização":   (40, 45, "#7EA6F4", ["payments-gateway", "antifraude", "tokenizer", "3ds-service", "risk-rules"]),
    "Contabilidade": (-8, 30, "#E2B566", ["ledger", "billing-batch", "fees-engine", "tax-calc", "journal-export", "reports"]),
    "Comunicação":   (-5, -70, "#B69CF0", ["notificacoes", "email-sender", "sms-gateway"]),
    "Assinaturas":   (18, 120, "#8FD0E8", ["subscriptions", "plans", "renewals", "dunning", "trials", "coupons", "entitlements"]),
    "Conciliação":   (-42, -10, "#F0B27A", ["recon-engine", "acquirer-files", "chargebacks", "settlement", "disputes"]),
    "Cobrança":      (-35, 95, "#9FD9B0", ["invoices", "boleto", "pix-charges", "collections"]),
}
EDGES = [
    ["checkout-api", "payments-gateway"], ["checkout-api", "antifraude"], ["checkout-api", "wallet"],
    ["checkout-web", "checkout-api"], ["cart-service", "checkout-api"], ["payments-gateway", "tokenizer"],
    ["payments-gateway", "3ds-service"], ["antifraude", "risk-rules"], ["payments-gateway", "ledger"],
    ["ledger", "fees-engine"], ["ledger", "tax-calc"], ["ledger", "billing-batch"], ["ledger", "reports"],
    ["ledger", "journal-export"], ["ledger", "settlement"], ["recon-engine", "acquirer-files"],
    ["recon-engine", "ledger"], ["chargebacks", "disputes"], ["chargebacks", "ledger"], ["settlement", "recon-engine"],
    ["subscriptions", "plans"], ["subscriptions", "renewals"], ["renewals", "dunning"], ["subscriptions", "entitlements"],
    ["renewals", "payments-gateway"], ["trials", "subscriptions"], ["dunning", "email-sender"],
    ["invoices", "ledger"], ["invoices", "boleto"], ["invoices", "pix-charges"], ["collections", "invoices"],
    ["notificacoes", "email-sender"], ["notificacoes", "sms-gateway"], ["renewals", "invoices"],
    ["checkout-api", "notificacoes", "inferida"], ["subscriptions", "coupons", "inferida"],
]
DATA = {
    "clusters": {k: {"lat": v[0], "lon": v[1], "color": v[2], "systems": v[3]} for k, v in CLUSTERS.items()},
    "edges": EDGES,
    "noaccess": ["billing-batch", "journal-export", "disputes"],
    "focus": "checkout-api",
}

subs = "".join(
    f'<div class="row{" on" if n == "Checkout" else ""}" data-c="{n}"><span class="ic" style="color:{v[2]}">✦</span>{n}<em>{len(v[3])} sistemas</em></div>'
    for n, v in CLUSTERS.items())

extra = """
.levels a{text-decoration:none}
.body{grid-template-columns:76px 260px 1fr 320px}
.canvas{background:radial-gradient(ellipse at 50% 45%,#2F353B 0%,#23272B 55%,#1C1F22 100%)}
#world{position:absolute;inset:0;width:100%;height:100%;cursor:grab}
#world:active{cursor:grabbing}
.legend2{position:absolute;left:16px;bottom:16px;display:flex;gap:14px;align-items:center;font-size:12px;color:var(--muted);background:rgba(31,35,39,.9);border:1px solid var(--line);border-radius:10px;padding:8px 12px}
.legend2 span{display:flex;align-items:center;gap:6px}
.legend2 i{width:10px;height:10px;border-radius:50%;display:inline-block}
.hint{position:absolute;right:16px;bottom:16px;font-size:12px;color:var(--muted);background:rgba(31,35,39,.9);border:1px solid var(--line);border-radius:10px;padding:8px 12px}
.stat{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0 18px}
.stat div{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:10px}
.stat b{display:block;font-family:var(--display);font-size:24px;font-weight:500}
.stat span{font-size:12px;color:var(--muted)}
.stat .ok b{color:var(--neon)} .stat .bad b{color:#F2B7BE}
.sel{background:var(--surface);border:1px solid var(--neon);border-radius:12px;padding:12px;box-shadow:0 0 18px rgba(70,242,142,.15)}
.sel .k{display:block;font-size:11.5px;color:var(--neon);margin-bottom:8px}
.sel .ph h3{font-size:16px}
.row{cursor:pointer}
"""

js = """
const D = %s;
const cv = document.getElementById('world'), ctx = cv.getContext('2d');
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
let W, H, R, cx, cy, rotY = -0.35, rotX = 0.32, drag = null, auto = !reduce, selected = D.focus;
const rad = d => d * Math.PI / 180;
// posições dos sistemas: espalhados em volta do centro da constelação
const nodes = {}; let seed = 7; const rnd = () => (seed = (seed * 16807) %% 2147483647) / 2147483647;
for (const [name, c] of Object.entries(D.clusters)) {
  c.systems.forEach((s, i) => {
    const a = 2 * Math.PI * i / c.systems.length + rnd() * .5, r = i ? 5 + rnd() * 9 : 1.5;
    nodes[s] = {lat: c.lat + r * Math.sin(a), lon: c.lon + r * Math.cos(a) / Math.cos(rad(c.lat)), color: c.color, cluster: name, deg: 0};
  });
}
D.edges.forEach(e => { nodes[e[0]].deg++; nodes[e[1]].deg++; });
const vec = (lat, lon) => [Math.cos(rad(lat)) * Math.sin(rad(lon)), Math.sin(rad(lat)), Math.cos(rad(lat)) * Math.cos(rad(lon))];
function proj(v) {
  let [x, y, z] = v;
  const cyr = Math.cos(rotY), syr = Math.sin(rotY);
  [x, z] = [x * cyr + z * syr, -x * syr + z * cyr];
  const cxr = Math.cos(rotX), sxr = Math.sin(rotX);
  [y, z] = [y * cxr - z * sxr, y * sxr + z * cxr];
  return [cx + x * R, cy - y * R, z];
}
function slerp(a, b, t) {
  const d = Math.acos(Math.min(1, a[0]*b[0] + a[1]*b[1] + a[2]*b[2])) || 1e-6, s = Math.sin(d);
  const k1 = Math.sin((1 - t) * d) / s, k2 = Math.sin(t * d) / s;
  const v = [a[0]*k1 + b[0]*k2, a[1]*k1 + b[1]*k2, a[2]*k1 + b[2]*k2];
  const lift = 1 + .06 * Math.sin(Math.PI * t);
  return v.map(c => c * lift);
}
function resize() {
  const r = cv.getBoundingClientRect(), dpr = devicePixelRatio || 1;
  cv.width = r.width * dpr; cv.height = r.height * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  W = r.width; H = r.height; R = Math.min(W, H) * .36; cx = W / 2; cy = H / 2 + 6;
}
function draw() {
  ctx.clearRect(0, 0, W, H); ctx.shadowBlur = 0;
  // estrelas de fundo
  ctx.fillStyle = 'rgba(232,228,219,.35)';
  for (let i = 0; i < 90; i++) { const x = (i * 97.3) %% W, y = (i * 57.7 + i * i * .3) %% H; ctx.fillRect(x, y, i %% 7 ? .8 : 1.4, i %% 7 ? .8 : 1.4); }
  // atmosfera
  const g = ctx.createRadialGradient(cx - R * .3, cy - R * .35, R * .1, cx, cy, R * 1.08);
  g.addColorStop(0, 'rgba(78,88,97,.6)'); g.addColorStop(.8, 'rgba(40,45,50,.92)'); g.addColorStop(1, 'rgba(34,38,42,.95)');
  ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.fill();
  ctx.strokeStyle = 'rgba(70,242,142,.18)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.arc(cx, cy, R + 1, 0, Math.PI * 2); ctx.stroke();
  // malha do mundo
  ctx.lineWidth = .6;
  for (let lat = -75; lat <= 75; lat += 15) line(Array.from({length: 73}, (_, i) => vec(lat, i * 5 - 180)), 'rgba(157,163,168,');
  for (let lon = -180; lon < 180; lon += 20) line(Array.from({length: 37}, (_, i) => vec(i * 5 - 90, lon)), 'rgba(157,163,168,');
  // arestas
  for (const e of D.edges) {
    const a = nodes[e[0]], b = nodes[e[1]], va = vec(a.lat, a.lon), vb = vec(b.lat, b.lon);
    const hot = e.includes(selected), inferred = e[2] === 'inferida', cross = a.cluster !== b.cluster;
    const pts = Array.from({length: 25}, (_, i) => proj(slerp(va, vb, i / 24)));
    if (inferred) {
      pts.forEach(([x, y, z], i) => { if (z < -0.05 || i %% 2) return; ctx.fillStyle = `rgba(238,111,124,${.4 + .5 * Math.max(0, z)})`;
        ctx.beginPath(); ctx.arc(x + Math.sin(i * 3) * 1.5, y + Math.cos(i * 5) * 1.5, 1.6, 0, 7); ctx.fill(); });
      continue;
    }
    ctx.lineWidth = hot ? 2 : 1;
    ctx.shadowBlur = hot ? 10 : 0; ctx.shadowColor = '#46F28E';
    for (let i = 1; i < pts.length; i++) {
      const z = (pts[i][2] + pts[i-1][2]) / 2; if (z < -0.08) continue;
      const al = (hot ? .95 : cross ? .28 : .5) * (.35 + .65 * Math.max(0, z));
      ctx.strokeStyle = hot ? `rgba(70,242,142,${al})` : cross ? `rgba(160,168,175,${al})` : hex(a.color, al);
      ctx.beginPath(); ctx.moveTo(pts[i-1][0], pts[i-1][1]); ctx.lineTo(pts[i][0], pts[i][1]); ctx.stroke();
    }
    ctx.shadowBlur = 0;
  }
  // nós (de trás para frente)
  const list = Object.entries(nodes).map(([k, n]) => [k, n, proj(vec(n.lat, n.lon))]).sort((p, q) => p[2][2] - q[2][2]);
  window._hit = [];
  for (const [k, n, [x, y, z]] of list) {
    if (z < -0.15) continue;
    const vis = .25 + .75 * Math.max(0, z), r = Math.min(4 + n.deg * 1.4, 16) * (.7 + .3 * z);
    const noacc = D.noaccess.includes(k), sel = k === selected;
    ctx.globalAlpha = vis;
    if (noacc) { ctx.setLineDash([3, 3]); ctx.strokeStyle = '#8D949A'; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.stroke(); ctx.setLineDash([]); }
    else {
      const col = sel ? '#46F28E' : n.color, gg = ctx.createRadialGradient(x - r * .35, y - r * .35, r * .1, x, y, r);
      gg.addColorStop(0, 'rgba(255,255,255,.85)'); gg.addColorStop(.35, col); gg.addColorStop(1, 'rgba(20,24,27,.9)');
      ctx.shadowBlur = sel ? 22 : 10; ctx.shadowColor = col; ctx.fillStyle = gg; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill(); ctx.shadowBlur = 0;
      if (sel) { ctx.strokeStyle = 'rgba(70,242,142,.5)'; ctx.beginPath(); ctx.arc(x, y, r + 7, 0, 7); ctx.stroke(); }
    }
    if ((n.deg >= 4 || sel || noacc) && z > .15) {
      ctx.font = `${sel ? 600 : 500} ${sel ? 13 : 11.5}px 'Avenir Next', sans-serif`; ctx.textAlign = 'center';
      ctx.fillStyle = sel ? '#46F28E' : '#D6D2CA'; ctx.fillText(k, x, y + r + (sel ? 20 : 14));
    }
    ctx.globalAlpha = 1; window._hit.push([k, x, y, r + 4, z]);
  }
  // nomes das constelações
  for (const [name, c] of Object.entries(D.clusters)) {
    const [x, y, z] = proj(vec(c.lat + 13, c.lon)); if (z < .2) continue;
    ctx.globalAlpha = Math.min(1, z * 1.4); ctx.textAlign = 'center';
    ctx.font = "600 14px Optima, 'Avenir Next', sans-serif"; ctx.fillStyle = c.color; ctx.fillText(name, x, y);
    ctx.font = "11px 'Avenir Next', sans-serif"; ctx.fillStyle = '#9DA3A8'; ctx.fillText(`${c.systems.length} sistemas`, x, y + 14);
    ctx.globalAlpha = 1;
  }
}
function line(vs, base) {
  const p = vs.map(proj);
  for (let i = 1; i < p.length; i++) { const z = (p[i][2] + p[i-1][2]) / 2; if (z < 0) continue;
    ctx.strokeStyle = base + (.05 + .14 * z) + ')'; ctx.beginPath(); ctx.moveTo(p[i-1][0], p[i-1][1]); ctx.lineTo(p[i][0], p[i][1]); ctx.stroke(); }
}
function hex(h, a) { const n = parseInt(h.slice(1), 16); return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${a})`; }
function loop() { if (auto && !drag) rotY += .0016; draw(); requestAnimationFrame(loop); }
cv.addEventListener('pointerdown', e => { drag = [e.clientX, e.clientY, rotY, rotX, false]; cv.setPointerCapture(e.pointerId); });
cv.addEventListener('pointermove', e => { if (!drag) return; const dx = e.clientX - drag[0], dy = e.clientY - drag[1];
  if (Math.abs(dx) + Math.abs(dy) > 3) drag[4] = true; rotY = drag[2] + dx * .006; rotX = Math.max(-1.2, Math.min(1.2, drag[3] + dy * .006)); });
cv.addEventListener('pointerup', e => { const moved = drag && drag[4]; drag = null; if (moved) return;
  const r = cv.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top;
  const hit = (window._hit || []).filter(h => h[4] > 0 && Math.hypot(h[1] - x, h[2] - y) < h[3]).pop();
  if (hit) select(hit[0]); });
function select(k) {
  selected = k; const n = nodes[k];
  document.getElementById('sel-name').textContent = k;
  document.getElementById('sel-sub').textContent = `${n.cluster}. ${n.deg} integrações.`;
  document.querySelectorAll('.side .row').forEach(r => r.classList.toggle('on', r.dataset.c === n.cluster));
}
document.querySelectorAll('.side .row').forEach(r => r.addEventListener('click', () => {
  const c = D.clusters[r.dataset.c]; auto = false; const t0 = rotY, t1 = -rad(c.lon), x0 = rotX, x1 = rad(c.lat) * .8; let t = 0;
  (function ease() { t = Math.min(1, t + .05); const k = 1 - Math.pow(1 - t, 3); rotY = t0 + (t1 - t0) * k; rotX = x0 + (x1 - x0) * k; if (t < 1) requestAnimationFrame(ease); })();
  select(c.systems[0]);
}));
document.getElementById('spin').addEventListener('click', e => { auto = !auto; e.target.textContent = auto ? 'Pausar rotação' : 'Girar'; });
addEventListener('resize', resize); resize(); loop();
""" % json.dumps(DATA, ensure_ascii=False)

body = f"""
<div class="note"><h1>O mundo do domínio</h1>
<p>Pagamentos como um mundo: cada subdomínio é uma constelação na superfície, cada sistema é uma estrela (o tamanho é o número de integrações). Arraste para girar, clique numa estrela para selecionar, clique num subdomínio à esquerda para voar até ele. No nível Empresa, cada domínio seria um mundo diferente.</p></div>
<div class="app">
  <div class="top">
    <span class="brand"><svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true"><circle cx="4" cy="5" r="1.6" fill="#9DA3A8"/><circle cx="8" cy="3" r="1.2" fill="#9DA3A8"/><circle cx="3" cy="10" r="1.1" fill="#9DA3A8"/><rect x="7" y="7" width="12" height="12" rx="4" fill="#46F28E"/></svg>Sinter</span>
    <span class="crumbs">Empresa<span>/</span><b>Pagamentos</b></span>
    <span class="levels"><a>Empresa</a><a class="on">Domínio</a><a>Sistema</a><a>Componente</a></span>
    <span class="levels" style="margin-left:auto"><a class="on" href="mundo.html">Mundo</a><a href="grafo.html">Grafo</a><a href="caixas.html">Caixas</a></span>
    <button id="spin">Pausar rotação</button>
  </div>
  <div class="body">
    {rail}
    <aside class="side"><div class="list"><h5>Constelações</h5>{subs}</div></aside>
    <div class="canvas">
      <canvas id="world" aria-label="Mundo do domínio Pagamentos com 34 sistemas em 7 constelações"></canvas>
      <div class="search"><input value="Buscar sistema, contrato ou regra" readonly></div>
      <div class="layers"><span class="chip on">Constelações</span><span class="chip on">Status</span><span class="chip">Donos</span><span class="chip">Fluxos</span></div>
      <div class="legend2"><span><i style="background:#46F28E;box-shadow:0 0 6px #46F28E"></i>Selecionado</span><span><i style="background:#A0A8AF"></i>Entre constelações</span><span><i style="background:#EE6F7C"></i>Inferida</span><span><i style="border:1px dashed #8D949A"></i>Sem acesso</span></div>
      <div class="hint">Arraste para girar</div>
    </div>
    <aside class="panel">
      <div class="sel"><span class="k">Selecionado</span><div class="ph"><span class="tech">Kt</span><div><h3 id="sel-name">checkout-api</h3><p id="sel-sub">Checkout. 6 integrações.</p></div></div><button class="glaze" style="width:100%;margin-top:10px">Abrir no nível Sistema</button></div>
      <div class="ph" style="margin-top:18px"><span class="tech" style="color:#46F28E">Pg</span><div><h3>Pagamentos</h3><p>Dono do domínio: Rafael Nunes</p></div></div>
      <div class="stat"><div><b>34</b><span>sistemas</span></div><div><b>212</b><span>integrações</span></div><div class="ok"><b>88%</b><span>aprovado</span></div><div class="bad"><b>9</b><span>conflitos abertos</span></div></div>
      <div class="infer"><strong>3 estrelas apagadas</strong><p>billing-batch, journal-export e disputes estão sem acesso de leitura. Sem fonte, não entram no .sinter/ dos vizinhos.</p><div class="btns"><button class="glaze">Pedir acesso</button></div></div>
    </aside>
  </div>
</div>
<script>{js}</script>
"""
page = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sinter: mundo do domínio</title><style>{style}{extra}</style></head><body>{body}</body></html>"""
(here / "mundo.html").write_text(page, encoding="utf-8")
print("ok")
