const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
  await p.goto('file://' + process.argv[2]);
  for (const q of process.argv.slice(3)) {
    await p.fill('#q', q);
    const r = await p.evaluate(() => [...document.querySelectorAll('.item')].map(s => s.querySelector('.code').textContent + (s.querySelector('.badge.ok')&&s.querySelector('h2').innerText.includes('boa')?'*':'')));
    const note = await p.textContent('#count');
    console.log('>', q, '=>', r.slice(0,14).join(' '), '| total', r.length, '|', note.includes('Buscando') ? note.slice(note.indexOf('Buscando')) : '');
  }
  console.log('erros:', errs);
  await b.close();
})();
