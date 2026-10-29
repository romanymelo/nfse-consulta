"""Gera a página HTML única (offline) a partir de dados.json + vocabulário + template.
Uso: python src/montar_pagina.py <pasta_processado> <pasta_dist> "v3 - 29/10/2026"
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from vocabulario import KW
pasta, dist, versao = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.load(open(f'{pasta}/dados.json', encoding='utf-8'))
for it in d['items']: it['k'] = [x.strip() for x in KW.get(it['i'], '').split(';') if x.strip()]
t = open(os.path.join(os.path.dirname(__file__), 'template.html'), encoding='utf-8').read()
js = json.dumps(d, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
nome = 'Consulta NFSe - ' + versao.replace('/', '-') + '.html'
os.makedirs(dist, exist_ok=True)
open(os.path.join(dist, nome), 'w', encoding='utf-8').write(t.replace('/*DATA*/', js).replace('/*VERSAO*/', versao))
print('gerado:', os.path.join(dist, nome))
