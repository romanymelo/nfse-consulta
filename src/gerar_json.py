"""Junta Anexo VIII normalizado + Anexo VII e gera dados.json (item -> NBS -> cIndOp/cClassTrib).
Uso: python src/gerar_json.py <pasta_processado>
"""
import csv, json, sys, collections
pasta = sys.argv[1]
rows = list(csv.DictReader(open(f'{pasta}/anexo8_principal.csv', encoding='utf-8-sig'), delimiter=';'))
ind = {r['indop']: r for r in csv.DictReader(open(f'{pasta}/anexo7_indop.csv', encoding='utf-8-sig'), delimiter=';')}
items = collections.OrderedDict()
for r in rows:
    it = items.setdefault(r['item_lc116'], {'i': r['item_lc116'], 'd': r['descricao_item'].strip(), 'n': [], 'a': []})
    n = next((x for x in it['n'] if x['c'] == r['nbs']), None)
    if not n:
        n = {'c': r['nbs'], 'd': r['descricao_nbs'].strip(), 'o': [], 'cc': [], 'sn': None}
        it['n'].append(n)
    if r['indop'] and r['indop'] not in n['o']: n['o'].append(r['indop'])
    if r['cclasstrib'] and all(x[0] != r['cclasstrib'] for x in n['cc']): n['cc'].append([r['cclasstrib'], r['nome_cclasstrib'].strip()])
    if r.get('cod_ativ_sn') and not n['sn']: n['sn'] = [r['cod_ativ_sn'], r['desc_ativ_sn'].strip()]
usados = {o for it in items.values() for n in it['n'] for o in n['o']}
indop = {}
for k in sorted(usados):
    v = ind.get(k)
    indop[k] = {'t': v['tipo_operacao'], 'l': v['local_fornecimento_dfe']} if v else {'t': 'descrição indisponível (consultar o Anexo VII)', 'l': ''}
json.dump({'items': list(items.values()), 'indop': indop}, open(f'{pasta}/dados.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(items), 'itens;', sum(len(i['n']) for i in items.values()), 'pares item×NBS;', len(usados), 'cIndOp; sem descrição:', sorted(usados - set(ind)))
