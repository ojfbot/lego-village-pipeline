// Shared theme preference for every Drafting Table page: blueprint (dark) by default, persisted, synced across frames/tabs.
(function () {
  var K = 'dtTheme';
  function read() { try { var v = localStorage.getItem(K); if (v === 'paper' || v === 'blueprint') return v; } catch (e) {} return 'blueprint'; }
  function apply(t) { if (document.body) document.body.classList.toggle('dt-blueprint', t === 'blueprint'); }
  var cur = read();
  function onBody() {
    apply(cur);
    new MutationObserver(function () {
      var t = document.body.classList.contains('dt-blueprint') ? 'blueprint' : 'paper';
      if (t !== cur) { cur = t; try { localStorage.setItem(K, t); } catch (e) {} }
    }).observe(document.body, { attributes: true, attributeFilter: ['class'] });
  }
  if (document.body) onBody(); else document.addEventListener('DOMContentLoaded', onBody);
  addEventListener('storage', function (e) { if (e.key === K) { cur = read(); apply(cur); } });
  window.DTTheme = { dark: function () { return read() === 'blueprint'; }, get: read, set: function (t) { cur = t; try { localStorage.setItem(K, t); } catch (e) {} apply(t); } };
})();
