"""Gera .working/curadoria.html reaproveitando o CSS do esmalte-v4.html."""
import pathlib, re

here = pathlib.Path(__file__).parent
v4 = (here / "esmalte-v4.html").read_text()
style = re.search(r"<style>(.*?)</style>", v4, re.S).group(1)
rail = re.search(r'<nav class="rail".*?</nav>', v4, re.S).group(0)
rail = rail.replace('<a class="on">', "<a>", 1).replace("<a><svg viewBox=\"0 0 20 20\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"><path d=\"M4 5h12M4 10h8M4 15h10\"/>",
                                                    "<a class=\"on\"><svg viewBox=\"0 0 20 20\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"><path d=\"M4 5h12M4 10h8M4 15h10\"/>", 1)

extra = """
.body{grid-template-columns:76px 300px 1fr 330px}
.qtabs{display:flex;gap:4px;margin:0 6px 12px;background:var(--canvas);border:1px solid var(--line);border-radius:8px;padding:2px}
.qtabs a{flex:1;text-align:center;font-size:12.5px;padding:6px 0;border-radius:6px;color:var(--muted)}
.qtabs a.on{background:var(--tile);color:var(--ink)}
.qrow{display:block;padding:10px;border-radius:9px;margin-bottom:4px}
.qrow.on{background:var(--surface);box-shadow:inset 0 0 0 1px rgba(238,111,124,.55)}
.qrow b{display:block;font-size:13.5px;font-weight:600}
.qrow span{display:block;font-size:12px;color:var(--muted);margin-top:3px}
.qrow .k{display:inline-block;font-size:11px;padding:1px 7px;border-radius:9px;margin-top:6px;border:1px solid var(--line);color:var(--muted)}
.qrow .k.c{border-color:rgba(238,111,124,.6);color:#F2B7BE}
.qrow .k.d{border-color:#5A626A}
.qhead{display:flex;align-items:baseline;justify-content:space-between;margin:14px 10px 6px;font-size:12px;color:var(--muted)}
.work{background:var(--canvas);padding:22px 26px;overflow:auto}
.work h2{font-size:22px;font-weight:600;margin:0}
.work .lede{color:var(--muted);font-size:14px;margin:6px 0 20px;max-width:70ch;line-height:1.5}
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.src-card{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px;position:relative}
.src-card.pick{border-color:var(--neon);box-shadow:0 0 0 1px var(--neon),0 0 18px rgba(70,242,142,.18)}
.src-card .from{display:flex;align-items:center;gap:10px;font-size:12.5px;color:var(--muted)}
.src-card .from i{width:28px;height:28px;border-radius:8px;display:grid;place-items:center;font-style:normal;font-weight:700;font-size:11px;background:#2F3439;border:1px solid #4D555C}
.claim{font-family:var(--display);font-size:30px;margin:16px 0 4px}
.claim small{font-family:var(--ui);font-size:13px;color:var(--muted);margin-left:6px}
.quote{font-size:13px;line-height:1.55;background:#2A2F34;border:1px solid #3E454C;border-radius:10px;padding:12px;margin:12px 0}
.quote mark{background:rgba(238,111,124,.18);color:#F7CDD2;padding:0 3px;border-radius:3px}
.quote code, .quote pre{font-family:Menlo,monospace;font-size:12px}
.quote pre{margin:0;white-space:pre-wrap;color:#C9C6BF}
.meta{font-size:12px;color:var(--muted);line-height:1.6}
.meta b{color:var(--ink);font-weight:500}
.age{display:inline-block;font-size:11px;padding:1px 8px;border-radius:9px;background:rgba(226,181,102,.14);color:var(--arquivo);margin-left:6px}
.fresh{background:rgba(70,242,142,.12);color:var(--neon)}
.pickbtn{margin-top:12px;width:100%}
.vs{position:absolute;left:50%;top:50%}
.impact{margin-top:20px;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px}
.impact h4{margin:0 0 10px;font-size:14px}
.chips2{display:flex;flex-wrap:wrap;gap:8px}
.chip2{display:flex;align-items:center;gap:8px;font-size:12.5px;padding:6px 10px;border-radius:9px;background:#2F3439;border:1px solid #4D555C}
.chip2 i{font-style:normal;font-weight:700;font-size:10px}
.decide{background:var(--chrome);border-left:1px solid #2E3338;padding:20px;overflow:auto}
.decide h3{margin:0 0 4px;font-size:16px}
.decide p.s{font-size:12.5px;color:var(--muted);margin:0 0 16px;line-height:1.5}
.opt{display:flex;gap:10px;align-items:flex-start;padding:12px;border-radius:10px;border:1px solid var(--line);margin-bottom:8px;font-size:13px;line-height:1.45}
.opt.on{border-color:var(--neon);background:rgba(70,242,142,.06)}
.opt .radio{flex:none;width:16px;height:16px;border-radius:50%;border:1.5px solid #6E757B;margin-top:2px}
.opt.on .radio{border-color:var(--neon);box-shadow:inset 0 0 0 4px var(--chrome);background:var(--neon)}
.opt b{display:block;font-weight:600}
.opt span{color:var(--muted);font-size:12.5px}
textarea{width:100%;min-height:78px;font:inherit;font-size:13px;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:10px;resize:none;margin:6px 0 14px}
label.l{font-size:12.5px;color:var(--muted)}
.foot{display:flex;gap:8px;margin-top:4px}
.foot button{flex:1}
.after{font-size:12px;color:var(--muted);margin-top:14px;line-height:1.5;border-top:1px solid #2E3338;padding-top:12px}
"""

body = f"""
<div class="note">
<h1>Curadoria</h1>
<p>UJ-2: Rafael transforma documentação espalhada em padrão. À esquerda, a fila; no centro, as duas versões do mesmo fato lado a lado, com a fonte e a idade de cada uma; à direita, a decisão. Nada vira oficial sem aprovação.</p>
</div>
<div class="app">
  <div class="top">
    <span class="brand"><svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true"><circle cx="4" cy="5" r="1.6" fill="#9DA3A8"/><circle cx="8" cy="3" r="1.2" fill="#9DA3A8"/><circle cx="3" cy="10" r="1.1" fill="#9DA3A8"/><rect x="7" y="7" width="12" height="12" rx="4" fill="#46F28E"/></svg>Sinter</span>
    <span class="crumbs">Pagamentos<span>/</span><b>Curadoria</b></span>
    <button style="margin-left:auto">Reprocessar fontes</button>
  </div>
  <div class="body">
    {rail}
    <aside class="side">
      <div class="qtabs"><a class="on">Conflitos 9</a><a>Propostas 131</a><a>Segredos 2</a></div>
      <div class="qhead"><span>Regras de negócio</span><span>4</span></div>
      <div class="qrow on"><b>Timeout da autorização</b><span>Confluence diz 30 s, código usa 10 s</span><em class="k c">conflito</em></div>
      <div class="qrow"><b>Parcelas máximas sem juros</b><span>3 fontes discordam: 6, 10 e 12</span><em class="k c">conflito</em></div>
      <div class="qrow"><b>Retentativa no antifraude</b><span>Doc antigo diz 3 tentativas; código não retenta</span><em class="k c">conflito</em></div>
      <div class="qrow"><b>Arredondamento de juros</b><span>PDF de 2021 e ADR-007</span><em class="k c">conflito</em></div>
      <div class="qhead"><span>Integrações</span><span>3</span></div>
      <div class="qrow"><b>Formato do evento PaymentAuthorized</b><span>Schema no repo difere do Confluence</span><em class="k c">conflito</em></div>
      <div class="qrow"><b>Versão da API do gateway</b><span>v2 no código, v1 no diagrama</span><em class="k c">conflito</em></div>
      <div class="qrow"><b>Dono do billing-batch</b><span>Duas squads se declaram donas</span><em class="k c">conflito</em></div>
      <div class="qhead"><span>Padrões</span><span>2</span></div>
      <div class="qrow"><b>Nome de tópicos Kafka</b><span>Guia de 2022 vs uso real</span><em class="k c">conflito</em></div>
    </aside>

    <main class="work">
      <h2>Timeout da autorização</h2>
      <p class="lede">Duas fontes descrevem o tempo máximo que o checkout-api espera pela resposta do payments-gateway. Escolha a que vale, escreva uma nova ou registre uma decisão.</p>
      <div class="cmp">
        <section class="src-card">
          <div class="from"><i style="color:#8FD0E8">Cf</i>Confluence PAG, página "Limites do checkout"<span class="age">editada há 26 meses</span></div>
          <p class="claim">30 s<small>de espera pela autorização</small></p>
          <div class="quote">"O checkout deve aguardar até <mark>30 segundos</mark> pela resposta do adquirente antes de considerar a transação pendente."</div>
          <p class="meta">Autor: <b>Marina Costa</b> (saiu da empresa)<br>Citado por 2 outros documentos</p>
          <button class="pickbtn">Usar esta versão</button>
        </section>
        <section class="src-card pick">
          <div class="from"><i style="color:#C9B8F2">Kt</i>checkout-api, GatewayClient.kt:27<span class="age fresh">commit de 3 semanas</span></div>
          <p class="claim">10 s<small>de espera pela autorização</small></p>
          <div class="quote"><pre>private val authorizeTimeout =
    Duration.ofSeconds(<mark>10</mark>) // ver ADR-012</pre></div>
          <p class="meta">Autor do commit: <b>Diego Almeida</b><br>Em produção desde 3 de setembro</p>
          <button class="pickbtn glaze">Versão escolhida</button>
        </section>
      </div>
      <div class="impact">
        <h4>Quem depende desta regra</h4>
        <div class="chips2">
          <span class="chip2"><i style="color:#C9B8F2">Kt</i>checkout-api</span>
          <span class="chip2"><i style="color:#F0B27A">Jv</i>payments-gateway</span>
          <span class="chip2"><i>ADR</i>ADR-012 Idempotência no checkout</span>
          <span class="chip2"><i>.s</i>.sinter/ de 2 repos será atualizado</span>
        </div>
      </div>
    </main>

    <aside class="decide">
      <h3>Decisão</h3>
      <p class="s">O Sinter sugere a versão do código: é mais recente, está em produção e cita a ADR-012.</p>
      <div class="opt on"><span class="radio"></span><div><b>Usar a versão do código (10 s)</b><span>O Confluence será marcado como desatualizado.</span></div></div>
      <div class="opt"><span class="radio"></span><div><b>Usar a versão do Confluence (30 s)</b><span>Abre uma tarefa para ajustar o código.</span></div></div>
      <div class="opt"><span class="radio"></span><div><b>Escrever uma nova regra</b><span>Nenhuma das duas está certa.</span></div></div>
      <div class="opt"><span class="radio"></span><div><b>Registrar como decisão (ADR)</b><span>Quando a escolha precisa de contexto.</span></div></div>
      <label class="l" for="just">Justificativa (vai para o histórico)</label>
      <textarea id="just">Reduzido para 10 s em set/2026 para liberar threads do checkout; ver ADR-012.</textarea>
      <div class="foot"><button>Pular</button><button class="glaze">Aprovar e próximo</button></div>
      <p class="after">Ao aprovar: a regra entra em <b>regras-de-negocio/timeout-autorizacao.md</b> com as duas fontes, e o PR no repo do domínio recebe esta alteração. Faltam 8 conflitos.</p>
    </aside>
  </div>
</div>
"""

page = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sinter: Curadoria</title><style>{style}{extra}</style></head><body>{body}</body></html>"""
(here / "curadoria.html").write_text(page, encoding="utf-8")
print("ok")
