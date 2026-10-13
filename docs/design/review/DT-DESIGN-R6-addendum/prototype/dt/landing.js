// Drafting Table — landing flash + cross-sheet card registry (DEC-033).
// 1) On load and on hashchange, scroll the #anchor target into view (no scrollIntoView — host-safe) and flash it.
// 2) window.dtCards: a registry sheets fill with {id, sheet, title, summary, status, statusColor} so CrossRef can preview a card before you go.
(function () {
  if (window.__dtLanding) return; window.__dtLanding = true;
  function land() {
    var id = decodeURIComponent((location.hash || '').slice(1)); if (!id) return;
    var tries = 0; (function tick() {
      var el = document.getElementById(id);
      if (!el) { if (tries++ < 40) return setTimeout(tick, 150); return; }
      var r = el.getBoundingClientRect(); var y = window.scrollY + r.top - Math.max(24, (innerHeight - r.height) / 3);
      window.scrollTo({ top: Math.max(0, y), behavior: 'smooth' });
      el.classList.remove('dt-landing'); void el.offsetWidth; el.classList.add('dt-landing');
      var live = document.getElementById('dt-landing-live'); if (!live) { live = document.createElement('div'); live.id = 'dt-landing-live'; live.setAttribute('aria-live', 'polite'); live.style.cssText = 'position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)'; document.body.appendChild(live); }
      live.textContent = 'Landed on: ' + (el.getAttribute('aria-label') || (el.querySelector('h1,h2,h3,[role=heading]') || el).textContent.trim().slice(0, 120));
      setTimeout(function () { el.classList.remove('dt-landing'); }, 1800);
    })();
  }
  window.addEventListener('hashchange', land); if (document.readyState === 'complete') land(); else window.addEventListener('load', land);
  window.dtCards = window.dtCards || {};
  window.dtRegisterCards = function (sheet, cards) { cards.forEach(function (c) { window.dtCards[sheet + '#' + c.id] = Object.assign({ sheet: sheet }, c); }); };
  // Seeded previews for cross-sheet hovers (the target sheet is not loaded, so the origin sheet needs a summary). MOCK — a real host reads the manifest.
  window.dtRegisterCards('A-01', [
    { id: 'fit', title: 'Does it fit?', summary: 'Six deterministic checks against the measured tree: ring fits the table · nothing under the base · ≤10 br under the branches · right-of-way clear · sections\' track meets · grade and banking (not run).', status: '▲ 4 BLOCK · 1 PASS · 1 NOT RUN', statusColor: 'var(--dt-block-deep)' },
    { id: 'rig', title: 'MILS units in the rig', summary: 'Section NE (anchor, fixed) and Section NW (movable) — tick into the layer rig, tap to select.', status: '2 SECTIONS', statusColor: 'var(--dt-muted)' }
  ]);
  window.dtRegisterCards('C-01', [
    { id: 'parts', title: 'Parts list — what to buy, and why we think so', summary: '1 own row (16 curves arrive with the train) · 6 adapted rows from bl-741807 (3 recoloured) · ballast rows follow the choice · story rows only if the siding is accepted.', status: 'TO BUY · MOCK RANGE', statusColor: 'var(--dt-info-deep)' },
    { id: 'fit', title: 'Does it fit?', summary: 'Circle on 4 modules · ballast keeps the railhead flush · recoloured module reads as snow next to the tree.', status: '3 NOT RUN', statusColor: 'var(--dt-unres-ink)' },
    { id: 'req', title: 'In one line · the request', summary: 'The summary card carries LH’s siding request: decline / park / accept with reasons and a reply in the requester’s words.', status: 'REQUEST', statusColor: 'var(--dt-accent-deep)' },
    { id: 'choices', title: 'Choices — and how far each is worked out', summary: 'Ballast: none · single · double, each with modeled / fit state and stances. DOUBLE carries the GapCloser chip.', status: 'CHOICES', statusColor: 'var(--dt-muted)' },
    { id: 'gate', title: 'Is this list ready to spend money on?', summary: 'The procurement-release gate: what is being released, the evidence it rests on, open findings (fix · waive with a reason · defer with owner + trigger), your initials. Hands a released list to P-01.', status: 'GATE · OPENS AFTER INITIALS', statusColor: 'var(--dt-prov-deep)' }
  ]);
  window.dtRegisterCards('P-01', [ { id: '', title: 'Buying the gap', summary: 'Every shop combination priced; lowest total / fewest parcels / soonest; orders recorded after purchase.', status: 'PLAN · MOCK SHOPS', statusColor: 'var(--dt-muted)' } ]);
  window.dtRegisterCards('B-01', [ { id: '', title: 'When the AI isn’t sure', summary: 'The decision trail: each field the AI resolved, with the source wording, its reading and your confirmation.', status: 'TRAIL', statusColor: 'var(--dt-muted)' } ]);
  window.dtRegisterCards('M-01', [ { id: 'railhead-z', title: 'Railhead height above module top', summary: 'Unknown — nobody has measured this. Grade, banking and the flush check all wait on it.', status: '○ UNKNOWN', statusColor: 'var(--dt-unres-ink)' } ]);
})();
