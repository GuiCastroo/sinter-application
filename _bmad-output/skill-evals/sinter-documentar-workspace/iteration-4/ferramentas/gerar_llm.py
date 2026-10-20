"""Gera cartão de navegação, resumos explicativos e grafo estrito, sem dependências."""
import argparse, json
from pathlib import Path
from _paginas import ler, secao, tabela, grafo


def gerar(repo, nome=None):
    repo=Path(repo); pages=ler(repo); name=nome or repo.name
    graph=grafo(pages,name)
    card=[f'# {name}', '', pages['1-negocio.md']['resumo'], '', '## Onde procurar', '']
    for file,p in pages.items():
        card.append(f'- [{p["nome"]}]({file})')
    for file,title in [('3-servicos.md','Serviços'),('4-jornadas.md','Jornadas')]:
        card.extend(['', '## '+title, ''])
        for s in pages[file]['secoes']:
            card.append(f'- [{s["titulo"].replace("`", "")}]({file}#{s["slug"]})')
    pending=secao(pages['6-referencia.md'],'Pendências')
    if pending:
        card.extend(['','## Pendências','',f'Pergunta, impacto e evidência completos em [Referência](6-referencia.md#pendências).',''])
        for row in tabela(pending['corpo']):
            card.append(f'- **{row["ID"]}** ({row["Tipo"]}): {row["Assunto"]}')
    card.extend(['','[Resumos explicativos](llm/resumos.md) · [Grafo tipado](llm/grafo.json)',''])
    (repo/'llms.txt').write_text('\n'.join(card))
    summaries=[f'# {name}: resumos','', 'Explicações por página, serviço e jornada; definições completas na Referência.', '']
    for file,p in pages.items():
        summaries.extend([f'## [{p["nome"]}](../{file})', '', p['resumo'], ''])
        if file in ('3-servicos.md','4-jornadas.md'):
            for s in p['secoes']:
                summaries.extend([f'### [{s["titulo"].replace("`", "")}](../{file}#{s["slug"]})', '', s['resumo'], ''])
    (repo/'llm').mkdir(exist_ok=True)
    (repo/'llm'/'resumos.md').write_text('\n'.join(summaries))
    (repo/'llm'/'grafo.json').write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n')
    print(f'{name}: {len(graph["servicos"])} serviços, {len(graph["relacoes"])} relações, {len(graph["jornadas"])} jornadas')

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('repo'); p.add_argument('--nome'); a=p.parse_args(); gerar(a.repo,a.nome)
