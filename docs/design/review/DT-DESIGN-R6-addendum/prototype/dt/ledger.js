/* DTLedger — one append-only store every sheet reads. Gates (tasks) close here; facts (measurements) land here.
   localStorage stand-in for the Task / Measurement tables. Same-tab and cross-tab subscribers. */
(function () {
  const KEY = 'dtLedger', CANON_KEYS = ['dtLedger', 'dtI03Canon', 'dtHubNow', 'dtQueueState'];
  const read = () => { try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { return {}; } };
  const write = (v) => { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {} window.dispatchEvent(new CustomEvent('dt-ledger', { detail: v })); };
  const norm = (v) => Object.assign({ gates: {}, facts: {}, log: [] }, v);
  // Task ids → which gates they close; a gate id is shared vocabulary across sheets.
  const UNBLOCKS = { 'hub-1': ['fit', 'stand-fit'], 'hub-2': ['fit'] };
  // Backfill: touches recorded on I-03 before the ledger existed still count. Read once from the I-03 canon and write the gate + fact so every sheet agrees.
  const backfill = (v) => {
    if (v.gates['hub-1']) return v;
    let canon; try { canon = JSON.parse(localStorage.getItem('dtI03Canon') || '{}'); } catch (e) { return v; }
    const c = canon['41843'], mo = c && c.measOverride && c.measOverride.base;
    if (!mo || mo.status !== 'measured') return v;
    const m = /(\d+) × (\d+) st room(?: · (\d+) × (\d+) st solid)? · (\d+) br(?: \+ (\d+) pl)?/.exec(mo.value || '');
    const meta = (mo.meta || '').split(' · '), by = meta[1] || 'jfo', tool = meta[0] || 'counted studs';
    const at = new Date().toISOString(), ev = 'I-03 touch #' + (c.touchCount || '?') + ' (backfilled)';
    if (m) { const w = +m[1], d = +m[2], hb = +m[5], hp = +(m[6] || 0); v.facts.treeBase = v.facts.treeBase || { at, reservedStuds: { w, d }, height: { bricks: hb, plates: hp }, ldu: { w: w * 20, d: d * 20, h: hb * 24 + hp * 8 }, tool, by, touch: c.touchCount, summary: 'Tree 41843 base: ' + w + ' × ' + d + ' studs of room, ' + hb + ' bricks' + (hp ? ' and ' + hp + ' plate' + (hp === 1 ? '' : 's') : '') + ' tall · ' + tool + ' · ' + by, backfilled: true }; }
    v.gates['hub-1'] = { closedAt: at, by, evidence: ev, summary: 'Tree base measured — ' + (mo.value || ''), backfilled: true };
    v.log.unshift({ at, kind: 'GATE CLOSED', id: 'hub-1', summary: v.gates['hub-1'].summary + ' · ' + ev });
    try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {}
    return v;
  };
  const L = {
    KEY, UNBLOCKS,
    get() { return backfill(norm(read())); },
    isClosed(id) { return !!this.get().gates[id]; },
    gate(id) { return this.get().gates[id] || null; },
    close(id, rec) { const v = this.get(); v.gates[id] = Object.assign({ closedAt: new Date().toISOString(), by: 'jfo' }, rec || {}); v.log.unshift({ at: v.gates[id].closedAt, kind: 'GATE CLOSED', id, summary: (rec && rec.summary) || id }); write(v); return v.gates[id]; },
    reopen(id, why) { const v = this.get(); if (!v.gates[id]) return; v.log.unshift({ at: new Date().toISOString(), kind: 'GATE REOPENED', id, summary: why || '' }); delete v.gates[id]; write(v); },
    fact(k) { return this.get().facts[k] || null; },
    setFact(k, val) { const v = this.get(); const prev = v.facts[k] || null; v.facts[k] = Object.assign({ at: new Date().toISOString(), supersedes: prev }, val); v.log.unshift({ at: v.facts[k].at, kind: 'FACT', id: k, summary: val.summary || k }); write(v); return v.facts[k]; },
    unblocked(taskId) { const v = this.get(); return Object.keys(UNBLOCKS).filter(g => v.gates[g] && UNBLOCKS[g].indexOf(taskId) >= 0); },
    reset() { CANON_KEYS.forEach(k => { try { localStorage.removeItem(k); } catch (e) {} }); window.dispatchEvent(new CustomEvent('dt-ledger', { detail: norm({}) })); },
    subscribe(fn) { const a = () => fn(this.get()); const b = (e) => { if (!e.key || CANON_KEYS.indexOf(e.key) >= 0) fn(this.get()); }; window.addEventListener('dt-ledger', a); window.addEventListener('storage', b); return () => { window.removeEventListener('dt-ledger', a); window.removeEventListener('storage', b); }; }
  };
  window.DTLedger = L;
})();
