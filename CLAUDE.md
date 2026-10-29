# Projeto: Consulta NFSe

Página HTML offline que traduz a descrição de um serviço nos códigos da NFS-e Nacional (item LC 116, NBS, cIndOp, cClassTrib/CST), com base nos Anexos VII e VIII do Portal Nacional da NFS-e. Público: analistas fiscais e contadores (foco em Simples Nacional). Responda sempre em português do Brasil, de forma direta.

## Regras do projeto
- Os dados vêm **só** das planilhas oficiais em `dados/oficial/`. Nunca inventar nem completar de memória item, NBS, cIndOp ou cClassTrib.
- Sem IA em tempo de execução e sem chamadas de rede: a página é um arquivo único que funciona offline.
- Nunca commitar dados de clientes (notas, XMLs, PDFs, listas de atividades reais).
- O vocabulário de busca (`src/vocabulario.py`) foi feito com IA e não tem revisão fiscal. Ao adicionar termos, usar a linguagem que o usuário digitaria.
- Playwright **CLI** para testes de navegador, nunca o MCP (economia de tokens).
- Perguntas à usuária: em texto, como conversa, sem caixas de pergunta.

## Pipeline
`python3 src/atualizar.py --anexo8 <xlsx> --anexo7 <xlsx> --versao "vN - DD/MM/AAAA"` gera `dist/Consulta NFSe - vN - DD-MM-AAAA.html`.
Título da página e nome do arquivo seguem `Consulta NFSe - v2 - 27/10/2026`; a cada atualização das tabelas, subir o número e usar a data do dia.

## Armadilhas já resolvidas (não reintroduzir)
- Células mescladas no Anexo VIII: preencher a partir da célula superior esquerda; ignorar valores velhos escondidos sob mesclagem.
- Linhas de continuação sem NBS: o cIndOp pertence à última NBS do mesmo item (reiniciar o controle ao mudar de item, pois a coluna A é mesclada).
- Uma NBS pode ter várias classificações: listar todas, nunca só a primeira.
- Aba "REGRA OP NÃO ONE_EXT": adquirente no exterior e operação não onerosa mudam o cIndOp (100301 → 100302/100401, 100101 → 100102/100201, 100501 → 100502/100601).
- Busca: radical sem gênero/plural; correção de digitação só com a mesma letra inicial; avisos (NOTES) para o que é ICMS e não ISS.
- Só valem pares item × NBS presentes na tabela.

## Saúde (caso de referência)
Itens 04.xx: cClassTrib 200029 (CST 200, redução de 60%); planos 04.22/04.23 usam 820001. cIndOp 030101 para atendimento presencial no estabelecimento, 030102 em outro local, 100301 para serviço total ou parcialmente à distância.

## Pendências e ideias
- Checagem periódica de versão nova: https://www.gov.br/nfse/pt-br/biblioteca/documentacao-tecnica/rtc (o download automático costuma ser bloqueado; baixar manualmente).
- Sugerir item/NBS alternativo quando o item não estiver na lista de atividades do cliente.
- Revisão fiscal do vocabulário por quem emite as notas.
