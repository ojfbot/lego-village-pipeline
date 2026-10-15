# N-05 — Blueprint / paper is one shared preference

`dt/theme.js` (new, copied in `sources/dt/theme.js`) is loaded by the house and should be loaded by every sheet. It reads `localStorage.dtTheme` (`blueprint` default), toggles `body.dt-blueprint`, watches the body class so any page's own toggle persists, and listens for `storage` so the house and the sheets in its iframes (and other tabs) flip together. API: `DTTheme.dark()`, `DTTheme.get()`, `DTTheme.set('blueprint'|'paper')`.

Consequence for the house: the BLUEPRINT / PAPER control in the header writes the shared preference; the 3D stage re-exposes (`setTheme`) and the studio palette inverts (HW-04 §3). The `theme` tweak only seeds; the user's choice wins.

Importer: sheets that still carry their own un-synced toggle should add the script; nothing else changes.
