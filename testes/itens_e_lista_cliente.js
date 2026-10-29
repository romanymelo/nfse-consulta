const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
  await p.goto('file://' + process.argv[2]);
  // 1) todos os todos os itens renderizam, com NBS, cIndOp e classificação
  const codes = await p.evaluate(() => DATA.items.map(i => i.i));
  let falhas = [];
  for (const c of codes) {
    await p.fill('#q', c);
    const r = await p.evaluate(() => { const s = document.querySelector('.item'); return s ? { code: s.querySelector('.code').textContent, nbs: s.querySelectorAll('.nbs').length, ind: s.querySelectorAll('.ind li').length, cc: [...s.querySelectorAll('.row')].filter(x => x.innerText.toLowerCase().startsWith('classifica')).length } : null; });
    if (!r || r.code !== c || !r.nbs || !r.ind || !r.cc) falhas.push([c, r]);
  }
  console.log('itens testados:', codes.length, '| falhas:', falhas.length, falhas.slice(0,5));
  // 2) lista do cliente (exemplo: clínica)
  await p.fill('#q', ''); 
  await p.click('summary:has-text("Conferir com a lista")');
  await p.fill('#lista', '4.02 / 8640208 - serviços de diagnóstico por registro gráfico\n4.03 / 8640202 - laboratórios clínicos\n4.03 / 8630502 - atividade médica ambulatorial com recursos para exames complementares\n4.10 / 8650002 - atividades de profissionais da nutrição');
  for (const q of ['laboratório', 'fonoaudiologia', 'consulta', 'nutricionista']) {
    await p.fill('#q', q);
    const r = await p.evaluate(() => [...document.querySelectorAll('.item')].slice(0,3).map(s => s.querySelector('.code').textContent + ': ' + (s.querySelector('.badge.bad') ? 'NÃO cadastrado' : s.querySelector('.how').innerText.replace('Escolha em Serviço / Atividade: ','→ '))));
    console.log('cliente >', q, '=>', r);
  }
  console.log('erros:', errs);
  await b.close();
})();
