"""Gera .working/conversa.html: conversa guiada (UJ-3) no estilo Esmalte v4."""
import pathlib, re

here = pathlib.Path(__file__).parent
v4 = (here / "esmalte-v4.html").read_text()
style = re.search(r"<style>(.*?)</style>", v4, re.S).group(1)
rail = re.search(r'<nav class="rail".*?</nav>', v4, re.S).group(0)
rail = rail.replace('<a class="on">', "<a>", 1)
rail = rail.replace('<a><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 5a2',
                    '<a class="on"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 5a2', 1)

extra = """

.att{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.doc{display:flex;align-items:center;gap:8px;padding:7px 10px;border-radius:9px;background:#2F3439;border:1px solid #4D555C;font-size:12.5px}
.doc .ty{font-size:9.5px;font-weight:700;padding:2px 5px;border-radius:4px;background:#3A4148}
.doc span{color:var(--muted);font-size:11.5px}
.doc.proc{border-color:rgba(70,242,142,.5)}
.composer{border-top:1px solid #353B41;padding:12px 22px 14px}
.composer .pending{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px}
.composer .pending .doc{background:var(--surface)}
.composer .pending .doc b{font-weight:500}
.composer .pending .x{color:var(--faint);margin-left:4px}
.composer .row2{display:flex;gap:8px;align-items:center}
.composer input{flex:1;font:inherit;font-size:14px;padding:11px 12px;border-radius:10px;border:1px solid var(--line);background:var(--surface);color:var(--muted)}
.iconbtn{width:40px;height:40px;display:grid;place-items:center;padding:0;border-radius:10px}
.iconbtn svg{width:18px;height:18px}
.menu{position:absolute;bottom:150px;left:22px;width:360px;background:#262B30;border:1px solid var(--line);border-radius:12px;padding:6px;box-shadow:0 12px 30px rgba(0,0,0,.45)}
.menu a{display:flex;gap:10px;align-items:center;padding:9px 10px;border-radius:8px;font-size:13px}
.menu a:first-child{background:var(--surface)}
.menu .ty{font-style:normal;font-size:9.5px;font-weight:700;padding:3px 5px;border-radius:4px;background:#3A4148;color:var(--muted);min-width:30px;text-align:center}
.menu a span{margin-left:auto;font-size:11px;color:var(--faint)}
.conv{position:relative}
.drop{font-size:11.5px;color:var(--faint);margin-top:8px}
.body{grid-template-columns:76px 250px 1fr 380px}
.conv{background:var(--canvas);display:flex;flex-direction:column;overflow:hidden}
.chead{display:flex;align-items:center;gap:14px;padding:14px 22px;border-bottom:1px solid #353B41}
.chead h2{margin:0;font-size:17px;font-weight:600}
.chead .who{margin-left:auto;display:flex;align-items:center}
.av{width:28px;height:28px;border-radius:50%;display:grid;place-items:center;font-size:11px;font-weight:700;border:2px solid var(--canvas);margin-left:-8px}
.thread{flex:1;overflow:auto;padding:20px 22px;display:flex;flex-direction:column;gap:16px}
.msg{display:flex;gap:12px;max-width:760px}
.msg .body2{flex:1}
.msg .name{font-size:12.5px;color:var(--muted);margin-bottom:4px}
.msg .name b{color:var(--ink);font-weight:600;margin-right:6px}
.msg p{margin:0;font-size:14px;line-height:1.55}
.agent .av{background:linear-gradient(#56E59A,#2FBF6F);color:#0B2A17;border-color:transparent}
.bubble{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.agent .bubble{background:#2C3337;border-color:#3E4A44}
.cite{display:flex;gap:10px;align-items:flex-start;margin-top:10px;background:rgba(238,111,124,.07);border:1px solid rgba(238,111,124,.45);border-radius:10px;padding:10px 12px;font-size:13px;line-height:1.45}
.cite b{display:block}
.cite span{color:var(--muted)}
.cite i{font-style:normal;flex:none;font-size:11px;font-weight:700;padding:3px 6px;border-radius:6px;background:#3A2A2E;color:#F2B7BE}
.touch{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.touch span{font-size:12px;padding:4px 9px;border-radius:8px;background:#2F3439;border:1px solid #4D555C}
.touch span.new{border-color:var(--neon);color:var(--neon)}
.opts{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}
.opts button{font-size:12.5px}
.compose{border-top:1px solid #353B41;padding:14px 22px;display:flex;gap:10px;align-items:center}
.compose input{flex:1;font:inherit;font-size:14px;padding:11px 12px;border-radius:10px;border:1px solid var(--line);background:var(--surface);color:var(--muted)}
.modes{display:flex;background:var(--canvas);border:1px solid var(--line);border-radius:8px;padding:2px}
.modes a{font-size:12.5px;padding:5px 10px;border-radius:6px;color:var(--muted)}
.modes a.on{background:var(--tile);color:var(--ink)}
.out{background:var(--chrome);border-left:1px solid #2E3338;padding:16px;overflow:auto}
.out h4{margin:0 0 10px;font-size:13px;color:var(--muted);font-weight:600}
.delta{background:var(--canvas);border:1px solid var(--line);border-radius:12px;padding:8px;margin-bottom:18px}
.delta svg{width:100%;height:auto;display:block}
.dl{display:flex;gap:12px;font-size:11.5px;color:var(--muted);padding:6px 4px 2px}
.dl span{display:flex;gap:5px;align-items:center}
.dl i{width:9px;height:9px;border-radius:2px;display:inline-block}
.art{display:flex;gap:10px;align-items:flex-start;padding:10px;border-radius:10px;border:1px solid var(--line);margin-bottom:8px;font-size:13px}
.art .t{flex:none;width:32px;height:32px;border-radius:8px;display:grid;place-items:center;font-size:10.5px;font-weight:700;background:#2F3439;border:1px solid #4D555C}
.art b{display:block;font-weight:600}
.art span{color:var(--muted);font-size:12px}
.art em{margin-left:auto;font-style:normal;font-size:11px;padding:2px 8px;border-radius:9px;white-space:nowrap}
.art em.draft{background:rgba(226,181,102,.14);color:var(--arquivo)}
.art em.ready{background:rgba(70,242,142,.12);color:var(--neon)}
.side .conv-row{padding:10px;border-radius:9px;margin-bottom:4px;font-size:13px}
.side .conv-row b{display:block;font-weight:600}
.side .conv-row span{font-size:12px;color:var(--muted)}
.side .conv-row.on{background:var(--surface);box-shadow:inset 0 0 0 1px rgba(70,242,142,.45)}
"""

delta_svg = """
<svg viewBox="0 0 340 220" aria-label="Mapa atual e proposto">
  <defs><marker id="a1" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8z" fill="#7C858D"/></marker>
  <marker id="a2" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8z" fill="#46F28E"/></marker>
  <filter id="gl"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
  <g font-family="Avenir Next, sans-serif" font-size="11">
  <rect x="14" y="20" width="104" height="36" rx="9" fill="#3E454C" stroke="#46F28E" stroke-width="1.5"/><text x="66" y="42" text-anchor="middle" fill="#E8E4DB">checkout-api</text>
  <text x="66" y="68" text-anchor="middle" fill="#46F28E" font-size="10">alterado</text>
  <rect x="218" y="20" width="110" height="36" rx="9" fill="#3E454C" stroke="#5D656C"/><text x="273" y="42" text-anchor="middle" fill="#E8E4DB">payments-gateway</text>
  <rect x="218" y="92" width="110" height="36" rx="9" fill="#3E454C" stroke="#5D656C"/><text x="273" y="114" text-anchor="middle" fill="#E8E4DB">antifraude</text>
  <rect x="14" y="150" width="120" height="40" rx="9" fill="#26382E" stroke="#46F28E" stroke-dasharray="4 3" filter="url(#gl)"/><text x="74" y="168" text-anchor="middle" fill="#C8FBDD">installment-policy</text><text x="74" y="182" text-anchor="middle" fill="#46F28E" font-size="10">novo</text>
  <rect x="218" y="162" width="110" height="36" rx="9" fill="#3E454C" stroke="#5D656C"/><text x="273" y="184" text-anchor="middle" fill="#E8E4DB">ledger</text>
  <path d="M118,38 H218" stroke="#7C858D" marker-end="url(#a1)"/><text x="168" y="32" text-anchor="middle" fill="#9DA3A8" font-size="10">POST /authorize</text>
  <path d="M118,48 C170,48 170,110 218,110" stroke="#46F28E" fill="none" marker-end="url(#a2)"/><text x="176" y="86" text-anchor="middle" fill="#46F28E" font-size="10">+ parcelas no score</text>
  <path d="M66,56 V150" stroke="#46F28E" stroke-dasharray="4 3" marker-end="url(#a2)"/>
  <path d="M273,56 V162" stroke="#7C858D" marker-end="url(#a1)" opacity=".7"/><text x="266" y="146" text-anchor="end" fill="#B69CF0" font-size="10">PaymentAuthorized</text>
  <text x="266" y="158" text-anchor="end" fill="#46F28E" font-size="10">+ campo installments</text>
  </g>
</svg>"""

body = f"""
<div class="note"><h1>Conversa guiada</h1>
<p>UJ-3: Carla (PM) e Rafael (arquiteto) desenham o parcelamento no checkout. O facilitador já conhece o domínio: cita a ADR que conflita, mostra quais sistemas mudam e, à direita, o mapa atual contra o proposto e os documentos que a conversa está produzindo. Nada vira oficial sem aprovação.</p></div>
<div class="app">
  <div class="top">
    <span class="brand"><svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true"><circle cx="4" cy="5" r="1.6" fill="#9DA3A8"/><circle cx="8" cy="3" r="1.2" fill="#9DA3A8"/><circle cx="3" cy="10" r="1.1" fill="#9DA3A8"/><rect x="7" y="7" width="12" height="12" rx="4" fill="#46F28E"/></svg>Sinter</span>
    <span class="crumbs">Pagamentos<span>/</span>Conversas<span>/</span><b>Parcelamento no checkout</b></span>
    <span class="modes" style="margin-left:auto"><a>Processo</a><a>Funcionalidade</a><a class="on">Solução</a></span>
  </div>
  <div class="body">
    {rail}
    <aside class="side">
      <div class="list"><h5>Conversas</h5></div>
      <div class="conv-row on"><b>Parcelamento no checkout</b><span>Solução. Carla, Rafael. Agora</span></div>
      <div class="conv-row"><b>Estorno parcial</b><span>Funcionalidade. Carla. Ontem</span></div>
      <div class="conv-row"><b>Processo de chargeback</b><span>Processo. Rafael. 22 set</span></div>
      <div class="conv-row"><b>Migração do tokenizer</b><span>Solução. Diego. 19 set</span></div>
      <button class="glaze" style="width:calc(100% - 12px);margin:14px 6px 0">Nova conversa</button>
    </aside>

    <section class="conv">
      <div class="chead"><h2>Parcelamento no checkout</h2><span class="chip">Modo solução</span>
        <span class="who"><span class="av" style="background:#B69CF0;color:#1F1635">CA</span><span class="av" style="background:#7EA6F4;color:#10203F">RN</span><span class="av" style="background:linear-gradient(#56E59A,#2FBF6F);color:#0B2A17">S</span></span></div>
      <div class="thread">
        <div class="msg"><span class="av" style="background:#B69CF0;color:#1F1635;margin:0">CA</span><div class="body2"><div class="name"><b>Carla Mendes</b>PM, 10:02</div>
          <div class="bubble"><p>Queremos parcelar em até 12x no cartão, sem juros até 6x. O cliente escolhe as parcelas no checkout. Anexei a proposta comercial e o print da tela nova.</p><div class="att"><span class="doc proc"><em class="ty" style="color:#EE6F7C;font-style:normal">PDF</em>Proposta parcelamento v3.pdf<span>8 páginas</span></span><span class="doc proc"><em class="ty" style="color:#8FD0E8;font-style:normal">PNG</em>tela-checkout-parcelas.png</span></div></div></div></div>
        <div class="msg agent"><span class="av" style="margin:0">S</span><div class="body2"><div class="name"><b>Facilitador de solução</b>Sinter, 10:02</div><div class="bubble"><p>Li os dois anexos. Da proposta saíram <b>3 regras de negócio</b> (juros a partir de 7x, parcela mínima de R$ 20, parcelamento só no crédito). Elas entram na conversa agora e vão para a curadoria no fim.</p></div></div></div>

        <div class="msg agent"><span class="av" style="margin:0">S</span><div class="body2"><div class="name"><b>Facilitador de solução</b>Sinter, 10:02</div>
          <div class="bubble"><p>Entendi. Pelo mapa de Pagamentos, a decisão das parcelas passa por três sistemas. Antes de desenhar, um ponto de atenção:</p>
          <div class="cite"><i>ADR-012</i><div><b>Idempotência no checkout</b><span>A chave de idempotência é calculada sobre valor e cartão. Com parcelas, o mesmo valor pode gerar duas autorizações diferentes. A chave precisa incluir o número de parcelas?</span></div></div>
          <div class="touch"><span>checkout-api</span><span>antifraude</span><span>payments-gateway</span><span class="new">+ installment-policy</span></div></div></div></div>

        <div class="msg"><span class="av" style="background:#7EA6F4;color:#10203F;margin:0">RN</span><div class="body2"><div class="name"><b>Rafael Nunes</b>Arquiteto, 10:05</div>
          <div class="bubble"><p>Sim, inclui. E a regra de parcelas não deve ficar no checkout: cria um serviço pequeno, installment-policy, que o checkout consulta.</p></div></div></div>

        <div class="msg agent"><span class="av" style="margin:0">S</span><div class="body2"><div class="name"><b>Facilitador de solução</b>Sinter, 10:05</div>
          <div class="bubble"><p>Registrei as duas decisões. Última pergunta para fechar o contrato: o antifraude precisa saber o número de parcelas para calcular o score?</p>
          <div class="opts"><button>Sim, enviar no POST /score</button><button>Não precisa</button><button>Perguntar ao dono do antifraude</button></div></div></div></div>
      </div>
      <div class="menu" role="menu" aria-label="Adicionar ao contexto"><a><em class="ty">ARQ</em>Arquivo do computador<span>PDF, DOCX, MD, imagem</span></a><a><em class="ty">DOC</em>Confluence ou Google Docs<span>link da página</span></a><a><em class="ty">REU</em>Transcrição de reunião<span>em breve</span></a><a><em class="ty">@</em>Item do domínio<span>sistema, ADR, regra</span></a><a><em class="ty">WEB</em>Link da web</a></div><div class="composer"><div class="pending"><span class="doc"><em class="ty" style="color:#8FD0E8;font-style:normal">DOCX</em><b>Regras antifraude 2025.docx</b><span>lendo…</span><span class="x">✕</span></span><span class="doc"><em class="ty" style="color:#46F28E;font-style:normal">ADR</em><b>@ADR-007 Arredondamento</b><span class="x">✕</span></span></div><div class="row2"><button class="iconbtn" aria-label="Adicionar documento ou referência"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M10 4v12M4 10h12"/></svg></button><input value="Responder, citar com @ ou arrastar arquivos para cá" readonly><button class="glaze">Enviar</button></div><p class="drop">Anexos entram como fonte desta conversa. O que virar conhecimento passa pela curadoria antes de ficar oficial.</p></div>
    </section>

    <aside class="out">
      <h4>Mapa atual e proposto</h4>
      <div class="delta">{delta_svg}
        <div class="dl"><span><i style="background:#46F28E"></i>Novo ou alterado</span><span><i style="background:#7C858D"></i>Sem mudança</span></div></div>
      <h4>O que esta conversa está produzindo</h4>
      <div class="art"><span class="t" style="color:#7EA6F4">ADR</span><div><b>ADR-013 Chave de idempotência com parcelas</b><span>Atualiza ADR-012</span></div><em class="ready">pronta</em></div>
      <div class="art"><span class="t" style="color:#46F28E">SYS</span><div><b>installment-policy</b><span>Novo sistema no subdomínio Checkout</span></div><em class="ready">pronta</em></div>
      <div class="art"><span class="t" style="color:#B69CF0">EVT</span><div><b>Contrato PaymentAuthorized</b><span>Novo campo installments</span></div><em class="draft">rascunho</em></div>
      <div class="art"><span class="t" style="color:#E2B566">PRD</span><div><b>PRD Parcelamento no checkout</b><span>3 tarefas propostas</span></div><em class="draft">rascunho</em></div>
      <button class="glaze" style="width:100%;margin-top:8px">Enviar para curadoria</button>
    </aside>
  </div>
</div>
"""
page = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sinter: Conversa guiada</title><style>{style}{extra}</style></head><body>{body}</body></html>"""
(here / "conversa.html").write_text(page, encoding="utf-8")
print("ok")
