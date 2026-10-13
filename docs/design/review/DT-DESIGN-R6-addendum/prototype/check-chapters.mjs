import {readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
const source = readFileSync(new URL('./prototypes/House World.dc.html', import.meta.url), 'utf8');
const declaration = source.match(/chapters = (\[\[.*?\]\]);/s)?.[1];
assert.ok(declaration, 'Six chapter labels and two haikus must remain declared.');
const lines = [...declaration.matchAll(/\[[\d.]+, '[^']+', '([^']+)'\]/g)].map(m => m[1]);
const approved = [
  ['Loose bricks greet the dawn', 5],
  ['Soft light slips through open doors', 7],
  ['Green leaves find their home', 5],
  ['Steps rise from the floor', 5],
  ['Small rooms gather round the tree', 7],
  ['New worlds wait for hands', 5],
];
assert.deepEqual(lines, approved.map(([line]) => line), 'Keep six subheads as the two approved haikus. Review syllables before updating the gate.');
console.log('Six chapter subheads retain the approved 5/7/5 + 5/7/5 haikus.');
