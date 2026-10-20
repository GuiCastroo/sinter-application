"""Verifica contratos do gerador, links, grafo, preservação e determinismo sem rede."""
import hashlib,json,re,sys
from pathlib import Path
from _paginas import ler,slug,grafo,tabela,subsecao,secao
from gerar_tudo import ROOT,DOMINIOS,gerar

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def snapshot(root):return {p.relative_to(root).as_posix():sha(p) for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
def anchors(text):
    result=set();count={}
    for title in re.findall(r'^#{1,6} (.+)$',text,re.M):
        s=slug(title); n=count.get(s,0);count[s]=n+1;result.add(s+('-'+str(n) if n else ''))
    result.update(re.findall(r'<a id="([^"]+)"',text))
    return result

def main():
    errors=[];details=[];links=0
    # Regression cases exercise strict boundaries and no implicit entity matching.
    assert len(tabela('| A | B |\n|---|---|\n| x | y |\n\n| C |\n|---|\n| z |'))==1
    assert subsecao('### Consome extra\nincorreto\n### Consome\ncorreto\n### Dados\nnão incluir','Consome').strip()=='correto'
    assert secao({'secoes':[{'titulo':'Regras extras'}]},'Regras') is None
    for domain in DOMINIOS:
        pages=ler(domain);assert len(pages)==6
        graph=grafo(pages,domain.name)
        assert all(r['para'] not in ('','—','-') for r in graph['relacoes'])
        assert all(r['tipo'] in {'chama_api','consome_evento','acessa_dado','callback','inicializacao','configuracao'} for r in graph['relacoes'])
        for p in [*domain.glob('*.md'),domain/'llms.txt',domain/'llm'/'resumos.md']:
            text=p.read_text();body=re.sub(r'```[\s\S]*?```','',text)
            for href in re.findall(r'\[[^\]]+\]\(([^)]+)\)',body):
                if re.match(r'^[a-z]+:',href):continue
                file,_,anchor=href.partition('#');dest=(p.parent/file).resolve() if file else p
                links+=1
                if not dest.exists():errors.append(f'{p.relative_to(ROOT)}: arquivo ausente {href}')
                elif anchor and anchor not in anchors(dest.read_text()):errors.append(f'{p.relative_to(ROOT)}: âncora ausente {href}')
        site=(domain/'site'/'index.html').read_text();payload=json.loads(re.search(r'const D = (.*);\nconst esc',site).group(1))
        ids=[]
        for p in payload['paginas']:
            assert p['texto']==pages[p['arquivo']]['texto']
            for section in p['secoes']:
                ids.append(p['arquivo']+'#'+section['slug'])
                ids.extend(p['arquivo']+'#'+s['slug'] for s in section['subs'])
        assert len(ids)==len(set(ids)), 'IDs duplicados'
        assert pages['2-arquitetura.md']['texto'].count('<!-- MAPA-PRINCIPAL -->')==1
        assert 'curto(' not in (ROOT/'ferramentas'/'gerar_llm.py').read_text()
        pending=tabela(secao(pages['6-referencia.md'],'Pendências')['corpo']);assert pending
        for row in pending:assert row['ID'] in (domain/'llms.txt').read_text() and row['Assunto'] in (domain/'llms.txt').read_text()
        # v4: removed sections must not come back.
        for f,p in pages.items():
            for gone in ('Em uma frase','Linguagem','Dúvidas e perguntas','Dúvidas de contexto','Perguntas para decisão','Evidências da revisão v3','Decisões'):
                assert secao(p,gone) is None, f'{domain.name}/{f}: seção removida voltou: {gone}'
            assert 'consulte também as [dúvidas]' not in p['texto']
        # Domain regressions independent of parser's own expected output.
        rel={(r['de'],r['para']) for r in graph['relacoes']}
        if domain.name=='dominio-online-boutique':
            assert 'shoppingassistantservice' in graph['jornadas'][2]['participantes']
            assert not any('SearchProducts' in r['contrato'] for r in graph['relacoes'] if r['de']=='frontend')
        if domain.name=='dominio-serverlesspresso':assert all(r['para']!='counting-service' for r in graph['relacoes'])
        if domain.name=='dominio-clinica-veterinaria':
            assert ('api-gateway','genai-service') in rel
            assert 'customers-service' not in graph['jornadas'][1]['participantes']
            assert 'config-server' not in graph['jornadas'][3]['participantes']
        details.append({'dominio':domain.name,'paginas':len(pages),'servicos':len(graph['servicos']),'relacoes':len(graph['relacoes']),'jornadas':len(graph['jornadas']),'ids_arvore_unicos':len(ids),'pendencias':len(pending)})
    baseline=json.loads((ROOT/'ferramentas'/'baseline-v3.json').read_text())
    actual=snapshot(ROOT.parent/'iteration-3')
    preserved=baseline==actual
    if not preserved:errors.append('iteration-3 difere do baseline')
    generated=lambda:{str(p.relative_to(ROOT)):sha(p) for d in DOMINIOS for p in [d/'llms.txt',d/'llm'/'resumos.md',d/'llm'/'grafo.json',d/'site'/'index.html']}|{'index.html':sha(ROOT/'index.html')}
    first=generated();gerar();second=generated();deterministic=first==second
    if not deterministic:errors.append('Geração não determinística')
    report={'ok':not errors,'dominios':details,'links_markdown_verificados':links,'erros':errors,'preservacao_v3':{'ok':preserved,'arquivos':len(baseline),'baseline':'ferramentas/baseline-v3.json'},'determinismo':{'ok':deterministic,'saidas':len(first),'sha256':second},'fixtures_sha256':snapshot(ROOT.parent/'fixtures'),'limites':['Conferência factual amostral; aplicações não executadas.','HTML usa CDN para Marked/Mermaid; requer rede no primeiro carregamento.','Smoke do navegador relatado separadamente; esta verificação é estática.']}
    (ROOT/'verificacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'ok':not errors,'links':links,'erros':errors,'preservados':len(baseline),'determinismo':deterministic},ensure_ascii=False,indent=2))
    return bool(errors)
if __name__=='__main__':sys.exit(main())
