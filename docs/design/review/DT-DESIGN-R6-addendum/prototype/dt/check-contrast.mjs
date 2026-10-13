// Contrast assertion for dt/tokens.css — run: node dt/check-contrast.mjs
// Fails (exit 1) if any text token reads below 4.5:1 on --dt-sheet in either theme. Contract text lives at the top of tokens.css.
import { readFileSync } from 'node:fs';
const css = readFileSync(new URL('./tokens.css', import.meta.url), 'utf8');
const TEXT = ['ink','muted','accent','accent-deep','pass','prov','prov-deep','block','block-deep','info','info-deep','unres','unres-ink'];
const block = (name) => { const i = css.indexOf(name); return css.slice(i, css.indexOf('}', i)); };
const vars = (b) => Object.fromEntries([...b.matchAll(/--dt-([\w-]+):(#[0-9A-Fa-f]{6})\b/g)].map(m => [m[1], m[2]]));
const lum = (hex) => { const c = [1,3,5].map(i => parseInt(hex.slice(i,i+2),16)/255).map(v => v <= .03928 ? v/12.92 : ((v+.055)/1.055)**2.4); return .2126*c[0]+.7152*c[1]+.0722*c[2]; };
const ratio = (a,b) => { const [l1,l2] = [lum(a),lum(b)].sort((x,y)=>y-x); return (l1+.05)/(l2+.05); };
let fail = 0;
for (const [theme, b] of [['paper', block(':root{')], ['blueprint', block('body.dt-blueprint{')]]) {
  const v = vars(b), sheet = v.sheet;
  for (const t of TEXT) { if (!v[t]) continue; const r = ratio(v[t], sheet); const ok = r >= 4.5; if (!ok) fail++; console.log(`${ok ? 'pass' : 'FAIL'} ${theme} --dt-${t} ${v[t]} on ${sheet} = ${r.toFixed(2)}:1`); }
}
if (fail) { console.error(fail + ' contrast failure(s)'); process.exit(1); }
