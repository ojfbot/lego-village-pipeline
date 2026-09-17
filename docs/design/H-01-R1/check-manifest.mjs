// Cross-artifact check — run from archive root: node handoff/check-manifest.mjs
// Fails if any manifest path is missing, a sheet status contradicts J-01 aliases, or the state-screenshot list disagrees with STATES.md.
import { readFileSync, existsSync, statSync } from 'node:fs';
const ix = JSON.parse(readFileSync('handoff/index.json', 'utf8')); let fail = 0;
const need = (p, why) => { if (p && !existsSync(p)) { fail++; console.log('MISSING', p, '←', why); } };
need(ix.tokens, 'tokens'); ix.brief.forEach(b => need(b, 'brief')); Object.values(ix.ledgers).forEach(l => need(l, 'ledger'));
for (const s of ix.sheets) { need(s.file, s.id); need(s.spec, s.id); need(s.standalone, s.id); (s.screenshots || []).forEach(p => need(p, s.id)); }
ix.state_screenshots.forEach(s => need(s.file, 'state'));
const states = readFileSync('handoff/screenshots/STATES.md', 'utf8'); const listed = [...states.matchAll(/states\/(\d\d-\w+\.jpg)/g)].map(m => m[1]);
const inIx = ix.state_screenshots.map(s => s.file.split('/').pop());
for (const f of listed) if (!inIx.includes(f)) { fail++; console.log('STATES.md lists', f, 'but index.json does not'); }
for (const f of inIx) if (!listed.includes(f)) { fail++; console.log('index.json lists', f, 'but STATES.md does not'); }
if (ix.components.length !== ix.component_count) { fail++; console.log('component_count drift'); }
for (const f of ['A-01', 'C-01', 'P-01']) need('handoff/a11y/' + f + '.tree.json', 'a11y baseline');
if (ix.review_round) need(ix.review_round.brief, 'review brief');
for (const s of ix.sheets) if (s.standalone && s.file) { const a = statSync(s.file).mtimeMs, b = statSync(s.standalone).mtimeMs; if (a > b) { fail++; console.log('STALE standalone', s.standalone, '← source newer'); } }
const j01 = readFileSync(ix.sheets.find(s => s.id === 'J-01').file, 'utf8');
for (const j of ix.journeys) { const m = j01.match(new RegExp("id: '" + j.id + "'[^\\n]*?status: '(\\w+)'")); if (m && m[1] !== j.status) { fail++; console.log('J-01 says', j.id, m[1], 'but index.json says', j.status); } }
console.log(fail ? fail + ' problem(s)' : 'manifest consistent'); process.exit(fail ? 1 : 0);
