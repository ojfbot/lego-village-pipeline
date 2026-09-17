// Drafting Table — shared hover-card lifecycle (DEC-032/033). One card open page-wide; body-level layer; opaque; timed fade.
// Usage from a DC logic class: const ov = window.dtOverlay.attach(component, { anchor: () => el, render: () => reactElement, width: 300 });
// ov.open() / ov.close(now) / ov.destroy(). The component's state.phase is driven by the helper via component.setState.
(function () {
  if (window.dtOverlay) return;
  var current = null;
  function host() { var h = document.getElementById('dt-overlay-layer'); if (!h) { h = document.createElement('div'); h.id = 'dt-overlay-layer'; h.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:2147483000'; document.body.appendChild(h); } return h; }
  window.dtOverlay = {
    attach: function (comp, opts) {
      var t = null, c = null, mount = null, root = null, rs = null;
      function phase() { return (comp.state && comp.state.phase) || 'closed'; }
      function set(ph, after) { comp.setState({ phase: ph }, function () { paint(); place(); if (after) after(); }); }
      function place() { var a = opts.anchor(), p = mount && mount.firstElementChild; if (!a || !p) return; var r = a.getBoundingClientRect(), W = opts.width || 300, H = Math.max(120, p.getBoundingClientRect().height); var up = innerHeight - r.bottom < H + 16 && r.top > innerHeight - r.bottom; p.style.left = Math.max(8, Math.min(r.left, innerWidth - W - 8)) + 'px'; p.style.top = (up ? Math.max(8, r.top - H - 8) : r.bottom + 8) + 'px'; }
      function teardown() { if (root) { try { root.unmount(); } catch (e) {} root = null; } else if (mount && window.ReactDOM && window.ReactDOM.unmountComponentAtNode) { try { window.ReactDOM.unmountComponentAtNode(mount); } catch (e) {} } if (mount && mount.parentNode) mount.remove(); if (rs) { removeEventListener('scroll', rs, true); removeEventListener('resize', rs); rs = null; } }
      function paint() {
        var RD = window.ReactDOM; if (!RD) return; var ph = phase();
        if (ph === 'closed') { teardown(); return; }
        if (!mount) { mount = document.createElement('div'); mount.style.cssText = 'pointer-events:auto;display:contents'; }
        if (!mount.parentNode) host().appendChild(mount);
        var el = opts.render();
        if (RD.createRoot) { if (!root) root = RD.createRoot(mount); root.render(el); } else RD.render(el, mount);
        if (!rs) { rs = place; addEventListener('scroll', rs, true); addEventListener('resize', rs); }
      }
      var api = {
        open: function () { clearTimeout(t); clearTimeout(c); if (current && current !== api) current.close(true); current = api; var ph = phase(); if (ph === 'open' || ph === 'opening') return; t = setTimeout(function () { set('opening', function () { c = setTimeout(function () { if (phase() === 'opening') set('open'); }, 40); }); }, ph === 'closing' ? 0 : 120); },
        close: function (now) { clearTimeout(t); clearTimeout(c); var go = function () { if (phase() === 'closed') return; set('closing', function () { c = setTimeout(function () { set('closed'); if (current === api) current = null; }, 150); }); }; if (now) go(); else t = setTimeout(go, 180); },
        paint: paint, place: place,
        destroy: function () { clearTimeout(t); clearTimeout(c); teardown(); if (current === api) current = null; }
      };
      return api;
    },
    style: function (open) { return { pointerEvents: open ? 'auto' : 'none', opacity: open ? 1 : 0, transform: open ? 'none' : 'translateY(-3px)', transition: 'opacity .14s ease-out, transform .14s ease-out' }; }
  };
})();
