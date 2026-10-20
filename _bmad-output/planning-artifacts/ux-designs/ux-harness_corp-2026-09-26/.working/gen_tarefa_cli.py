"""Gera .working/tarefa.html (pacote de contexto, UJ-4) e .working/cli.html (CLI do dev, UJ-4 e UJ-5)."""
import pathlib, re

here = pathlib.Path(__file__).parent
v4 = (here / "esmalte-v4.html").read_text()
style = re.search(r"<style>(.*?)</style>", v4, re.S).group(1)
rail = re.search(r'<nav class="rail".*?</nav>', v4, re.S).group(0)
rail = rail.replace('<a class="on">', "<a>", 1)
rail = rail.replace('<a><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="14" height="14" rx="3"/>',
                    '<a class="on"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="14" height="14" rx="3"/>', 1)
BRAND = '<span class="brand"><svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true"><circle cx="4" cy="5" r="1.6" fill="#9DA3A8"/><circle cx="8" cy="3" r="1.2" fill="#9DA3A8"/><circle cx="3" cy="10" r="1.1" fill="#9DA3A8"/><rect x="7" y="7" width="12" height="12" rx="4" fill="#46F28E"/></svg>Sinter</span>'

# ---------------- tarefa.html ----------------
extra_t = """
.body{grid-template-columns:76px 270px 1fr 360px}
.work{background:var(--canvas);padding:22px 28px;overflow:auto}
.work h2{margin:0;font-size:22px;font-weight:600}
.work .lede{color:var(--muted);font-size:14px;margin:6px 0 22px}
.chain{position:relative;padding-left:34px}
.chain::before{content:"";position:absolute;left:13px;top:8px;bottom:8px;width:2px;background:linear-gradient(var(--neon) 0 62%,#474E55 62% 100%)}
.layer{position:relative;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin-bottom:14px}
.layer .dot{position:absolute;left:-29px;top:18px;width:16px;height:16px;border-radius:50%;background:var(--chrome);border:2px solid #5D656C}
.layer.done .dot{background:var(--neon);border-color:var(--neon);box-shadow:0 0 10px var(--neon)}
.layer.now{border-color:rgba(70,242,142,.55)}
.layer.now .dot{border-color:var(--neon);background:var(--chrome);box-shadow:0 0 0 4px rgba(70,242,142,.15)}
.layer.todo{opacity:.6}
.lh{display:flex;align-items:center;gap:10px}
.lh b{font-size:15px;font-weight:600}
.lh .who{font-size:12.5px;color:var(--muted)}
.lh em{margin-left:auto;font-style:normal;font-size:11.5px;padding:2px 9px;border-radius:9px}
.ok{background:rgba(70,242,142,.12);color:var(--neon)} .wip{background:rgba(226,181,102,.14);color:var(--arquivo)} .wait{background:#30353A;color:var(--muted)}
.items{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.it{font-size:12.5px;padding:5px 9px;border-radius:8px;background:#2F3439;border:1px solid #4D555C}
.it i{font-style:normal;font-size:10px;font-weight:700;margin-right:6px;color:var(--muted)}
.note2{font-size:13px;line-height:1.5;margin:10px 0 0;padding:10px 12px;border-radius:10px;background:#2A2F34;border:1px dashed #5A626A}
.pack{background:var(--chrome);border-left:1px solid #2E3338;padding:18px;overflow:auto}
.pack h4{margin:0 0 10px;font-size:13px;color:var(--muted);font-weight:600}
.tree{font-family:Menlo,monospace;font-size:12px;line-height:1.75;background:#1A1D20;border:1px solid #2E3338;border-radius:10px;padding:12px 14px;margin-bottom:18px;color:#C9C6BF}
.tree .n{color:var(--neon)} .tree .d{color:var(--faint)}
.budget{margin-bottom:18px}
.bar{height:8px;border-radius:5px;background:#30353A;overflow:hidden;display:flex}
.bar i{display:block;height:100%}
.bl{display:flex;justify-content:space-between;font-size:12px;color:var(--muted);margin-top:6px}
.cmd{display:flex;align-items:center;gap:8px;font-family:Menlo,monospace;font-size:12.5px;background:#1A1D20;border:1px solid var(--neon);border-radius:10px;padding:10px 12px;box-shadow:0 0 14px rgba(70,242,142,.15)}
.cmd span{flex:1;color:#C8FBDD}
.side .trow{padding:10px;border-radius:9px;margin-bottom:4px;font-size:13px}
.side .trow b{display:block;font-weight:600}
.side .trow span{display:block;font-size:12px;color:var(--muted);margin-top:2px}
.side .trow.on{background:var(--surface);box-shadow:inset 0 0 0 1px rgba(70,242,142,.45)}
.pips{display:flex;gap:3px;margin-top:6px}.pips i{width:18px;height:4px;border-radius:2px;background:#474E55}.pips i.d{background:var(--neon)}
"""
tarefa = f"""
<div class="note"><h1>Pacote de contexto da tarefa</h1>
<p>UJ-4: a tarefa passa de mão em mão e cada papel só adiciona a sua camada. A linha à esquerda mostra onde o bastão está. À direita, exatamente o que vai para o .sinter/ do repo e quanto isso custa em contexto para o agente.</p></div>
<div class="app">
  <div class="top">{BRAND}
    <span class="crumbs">Pagamentos<span>/</span>Tarefas<span>/</span><b>PAG-231</b></span>
    <button style="margin-left:auto">Abrir conversa de origem</button>
  </div>
  <div class="body">
    {rail}
    <aside class="side">
      <div class="list"><h5>Tarefas do domínio</h5></div>
      <div class="trow on"><b>PAG-231 Parcelamento no checkout</b><span>Com Diego, camada do repo</span><div class="pips"><i class="d"></i><i class="d"></i><i></i><i></i></div></div>
      <div class="trow"><b>PAG-232 installment-policy</b><span>Com Rafael, camada de solução</span><div class="pips"><i class="d"></i><i></i><i></i><i></i></div></div>
      <div class="trow"><b>PAG-219 Estorno parcial</b><span>Pronta para o dev</span><div class="pips"><i class="d"></i><i class="d"></i><i class="d"></i><i></i></div></div>
      <div class="trow"><b>PAG-214 Timeout do gateway</b><span>Implementada</span><div class="pips"><i class="d"></i><i class="d"></i><i class="d"></i><i class="d"></i></div></div>
    </aside>
    <main class="work">
      <h2>PAG-231 Parcelamento no checkout</h2>
      <p class="lede">checkout-api. Nasceu da conversa "Parcelamento no checkout" em 26 set.</p>
      <div class="chain">
        <section class="layer done"><span class="dot"></span>
          <div class="lh"><b>Negócio</b><span class="who">Carla Mendes, PM</span><em class="ok">aprovada</em></div>
          <div class="items"><span class="it"><i>REGRA</i>Até 12x, sem juros até 6x</span><span class="it"><i>REGRA</i>Parcela mínima R$ 20</span><span class="it"><i>REGRA</i>Só no crédito</span><span class="it"><i>PRD</i>Parcelamento no checkout</span></div>
        </section>
        <section class="layer done"><span class="dot"></span>
          <div class="lh"><b>Solução</b><span class="who">Rafael Nunes, arquiteto</span><em class="ok">aprovada</em></div>
          <div class="items"><span class="it"><i>ADR</i>ADR-013 Idempotência com parcelas</span><span class="it"><i>SYS</i>installment-policy (novo)</span><span class="it"><i>EVT</i>PaymentAuthorized + installments</span><span class="it"><i>API</i>POST /score + installments</span></div>
        </section>
        <section class="layer now"><span class="dot"></span>
          <div class="lh"><b>Repo</b><span class="who">Diego Almeida, tech lead</span><em class="wip">em edição</em></div>
          <div class="items"><span class="it"><i>PADRÃO</i>Usar InstallmentPolicyClient</span><span class="it"><i>PADRÃO</i>Nunca calcular juros no front</span></div>
          <p class="note2">Testes de contrato com o antifraude ficam em src/test/contract. Não mexer no fluxo de 3DS nesta tarefa.</p>
          <div style="display:flex;gap:8px;margin-top:12px"><button>Adicionar item</button><button class="glaze">Aprovar camada e passar para o dev</button></div>
        </section>
        <section class="layer todo"><span class="dot"></span>
          <div class="lh"><b>Dev</b><span class="who">Bia Souza</span><em class="wait">aguardando</em></div>
          <p class="note2" style="border-style:solid">Recebe o pacote com <b>sinter task pull PAG-231</b>.</p>
        </section>
      </div>
    </main>
    <aside class="pack">
      <h4>O que vai para o .sinter/ do checkout-api</h4>
      <div class="tree">.sinter/<br>├─ tasks/<span class="n">PAG-231.md</span> <span class="d">novo</span><br>├─ context/<br>│  ├─ domain.md<br>│  ├─ neighbors/<span class="n">installment-policy.md</span> <span class="d">novo</span><br>│  ├─ neighbors/antifraude.md <span class="d">alterado</span><br>│  ├─ business-rules.md <span class="d">+3 regras</span><br>│  └─ decisions.md <span class="d">+ADR-013</span><br>└─ flows/nova-feature.md<br><br>AGENTS.md, CLAUDE.md, .cursor/rules <span class="d">regerados</span></div>
      <div class="budget"><h4>Orçamento de contexto da tarefa</h4>
        <div class="bar"><i style="width:22%;background:#B69CF0"></i><i style="width:34%;background:#7EA6F4"></i><i style="width:18%;background:#46F28E"></i></div>
        <div class="bl"><span>3,7 mil de 5 mil tokens</span><span>negócio, solução, repo</span></div></div>
      <h4>Comando para o dev</h4>
      <div class="cmd"><span>sinter task pull PAG-231</span><button>Copiar</button></div>
      <p style="font-size:12px;color:var(--muted);line-height:1.5;margin-top:10px">Disponível quando a camada do repo for aprovada. A Bia recebe um aviso.</p>
    </aside>
  </div>
</div>"""
(here / "tarefa.html").write_text(f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sinter: pacote de contexto</title><style>{style}{extra_t}</style></head><body>{tarefa}</body></html>""", encoding="utf-8")

# ---------------- cli.html ----------------
cli_css = """
body{background:#151719}
.term{max-width:1100px;margin:0 auto 40px;border-radius:12px;overflow:hidden;border:1px solid #2E3338;box-shadow:0 20px 60px rgba(0,0,0,.5)}
.tbar{background:#23272B;padding:10px 14px;display:flex;align-items:center;gap:8px;font-size:12.5px;color:var(--muted)}
.tbar i{width:11px;height:11px;border-radius:50%;background:#474E55;display:inline-block}
.tbar span{margin-left:10px}
pre{margin:0;background:#1A1D20;color:#D6D2CA;font-family:Menlo,'SF Mono',monospace;font-size:13px;line-height:1.7;padding:18px 20px;white-space:pre-wrap}
.p{color:#46F28E}.c{color:#E8E4DB;font-weight:600}.m{color:#8D949A}.ok{color:#46F28E}.w{color:#E2B566}.b{color:#7EA6F4}.v{color:#B69CF0}.r{color:#EE6F7C}
.caption{max-width:1100px;margin:0 auto 10px;padding:0 4px;color:#C9C6BF;font-size:14px}
.caption b{color:#EEE}
"""
cli = """
<div class="note"><h1>CLI do dev</h1>
<p>UJ-4 e UJ-5: a Bia recebe o pacote da tarefa e o Diego cria um serviço que já nasce com o .sinter/. A CLI usa as mesmas cores do app: neon para o que foi aplicado, âmbar para o que pede atenção. Toda saída tem versão em JSON para agentes (--json).</p></div>

<p class="caption"><b>Bia puxa a tarefa</b> no checkout-api</p>
<div class="term"><div class="tbar"><i></i><i></i><i></i><span>bia@mac: ~/code/checkout-api</span></div>
<pre><span class="p">❯</span> <span class="c">sinter task pull PAG-231</span>

  <span class="c">PAG-231 Parcelamento no checkout</span>   <span class="m">domínio Pagamentos</span>

  Camadas
  <span class="ok">●</span> Negócio   Carla Mendes     aprovada   <span class="m">3 regras, 1 PRD</span>
  <span class="ok">●</span> Solução   Rafael Nunes     aprovada   <span class="m">ADR-013, installment-policy, 2 contratos</span>
  <span class="ok">●</span> Repo      Diego Almeida    aprovada   <span class="m">2 padrões, 1 nota</span>

  Gravado em .sinter/
  <span class="ok">+</span> tasks/PAG-231.md
  <span class="ok">+</span> context/neighbors/installment-policy.md
  <span class="w">~</span> context/neighbors/antifraude.md          <span class="m">POST /score + installments</span>
  <span class="w">~</span> context/business-rules.md               <span class="m">+3 regras</span>
  <span class="w">~</span> context/decisions.md                    <span class="m">+ADR-013</span>

  Exports regerados: <span class="b">AGENTS.md</span>, <span class="b">CLAUDE.md</span>, <span class="b">.cursor/rules</span>, <span class="b">.github/copilot-instructions.md</span>
  Contexto da tarefa: <span class="c">3,7 mil</span> de 5 mil tokens

  <span class="ok">Pronto.</span> Peça ao seu agente: <span class="c">implemente a PAG-231 seguindo .sinter/flows/nova-feature.md</span>

<span class="p">❯</span> <span class="c">sinter status</span>

  .sinter/ sincronizado com o domínio Pagamentos   <span class="m">há 1 min</span>
  <span class="w">!</span> CLAUDE.md foi editado à mão; a próxima exportação sobrescreve. Mova a edição para .sinter/standards/
</pre></div>

<p class="caption" style="margin-top:28px"><b>Diego cria um serviço novo</b></p>
<div class="term"><div class="tbar"><i></i><i></i><i></i><span>diego@mac: ~/code</span></div>
<pre><span class="p">❯</span> <span class="c">sinter init --domain pagamentos --name installment-policy</span>

  Novo sistema no subdomínio <span class="v">Checkout</span>, definido na ADR-013

  Vizinhos previstos
  <span class="m">←</span> checkout-api        chama GET /installments/options
  <span class="m">→</span> ledger              publica InstallmentPlanCreated   <span class="w">contrato em rascunho</span>

  <span class="ok">Criado</span> installment-policy/
  ├─ .sinter/
  │  ├─ sinter.yaml
  │  ├─ context/domain.md, neighbors/ (2), business-rules.md, decisions.md
  │  ├─ standards/          <span class="m">Kotlin, padrões da empresa</span>
  │  ├─ skills/             <span class="m">6 do catálogo: dev-kotlin, testes-de-contrato, adr-reader…</span>
  │  ├─ agents/             <span class="m">tech-lead, dev</span>
  │  └─ flows/              <span class="m">nova-feature.md, bugfix.md</span>
  ├─ AGENTS.md
  ├─ CLAUDE.md
  ├─ .cursor/rules/
  └─ .github/copilot-instructions.md

  <span class="ok">Pronto em 4 s.</span> O repo foi registrado no mapa de Pagamentos como <span class="w">aguardando primeiro commit</span>.
</pre></div>
"""
(here / "cli.html").write_text(f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sinter: CLI</title><style>{style}{cli_css}</style></head><body>{cli}</body></html>""", encoding="utf-8")
print("ok")
