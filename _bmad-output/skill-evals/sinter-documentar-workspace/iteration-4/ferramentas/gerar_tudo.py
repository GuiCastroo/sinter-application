"""Regenera todas as projeções a partir das 18 páginas canônicas, sem rede."""
from pathlib import Path
import subprocess, sys, html
ROOT=Path(__file__).resolve().parents[1]
DOMINIOS=sorted(ROOT.glob('eval-*/with_skill/run-1/outputs/dominio-*'))

def gerar():
    links=[]
    for domain in DOMINIOS:
        name=(domain/'1-negocio.md').read_text().splitlines()[0].split(': ',1)[-1]
        for script in ('gerar_llm.py','gerar_site.py'):
            subprocess.run([sys.executable,str(ROOT/'ferramentas'/script),str(domain),'--nome',name],check=True)
        relative=domain.relative_to(ROOT).as_posix()
        links.append(f'<li><a href="{relative}/site/index.html">{html.escape(name)}</a><p><a href="{relative}/llms.txt">Cartão IA</a> · <a href="{relative}/llm/resumos.md">Resumos</a> · <a href="{relative}/llm/grafo.json">Grafo</a></p></li>')
    (ROOT/'index.html').write_text('''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Documentação Sinter v3</title><style>body{font-family:system-ui;background:#f4f6f8;color:#1b2430;max-width:800px;margin:64px auto;padding:24px}h1{font-weight:500}li{background:white;padding:24px;margin:16px 0;border:1px solid #d8dee4;border-radius:12px}ul{padding:0;list-style:none}a{color:#1f5fd1}p{line-height:1.6}</style><h1>Documentação Sinter v3</h1><p>Três domínios, seis perspectivas por domínio. Regras, linguagem e dúvidas têm uma referência única; infraestrutura conserva o inventário.</p><ul>'''+''.join(links)+'''</ul><p><a href="README.md">Mudanças, reprodução e limites</a> · <a href="verificacao.json">Verificação</a></p></html>\n''')
if __name__=='__main__':gerar()
