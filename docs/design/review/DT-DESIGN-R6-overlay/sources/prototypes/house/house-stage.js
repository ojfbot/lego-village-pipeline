// <house-stage>: the LEGO House built from house-metadata.json (schematic stand-in), upgraded in place to the
// supplied house.glb when prototypes/house/house.glb is present. R0 scroll flight path + explicit room flights.
// Camera has ONE owner at a time: 'tour' | 'flight' | 'threshold' | 'blend'.
(function () {
  if (customElements.get('house-stage')) return;
  const S = 0.01, PITCH = .2, CDN = 'https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/';
  const W = (c) => [c[0] * S, c[2] * S, -c[1] * S];
  const ROOF = { 1: '#8c1d1d', 2: '#f2b23a', 3: '#2d7fc1', 4: '#1f3a6e', 5: '#8dc3e8', 6: '#f0c94a', 7: '#e9a23b', 9: '#6fbf5a', 10: '#e3261a', 11: '#e9a23b', 12: '#2d7fc1', 13: '#f26a28', 14: '#8c1d1d', 15: '#f0c94a', 16: '#2d7fc1', 17: '#f4f2ec', 18: '#8dc3e8', 19: '#6fbf5a', 20: '#e3261a', 21: '#8c1d1d', 22: '#f4f2ec' };
  const MARKERS = [3, 7, 19];
  const GREY = '#cfcbc1', WHITE = '#f4f2ec';
  const ease = (t) => t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
  const loadScript = (src) => new Promise((res) => { if (document.querySelector('script[src="' + src + '"]')) return res(true); const s = document.createElement('script'); s.src = src; s.onload = () => res(true); s.onerror = () => res(false); document.head.appendChild(s); setTimeout(() => res(false), 9000); });

  class HouseStage extends HTMLElement {
    constructor() {
      super();
      this.progress = 0; this.owner = 'tour'; this.frozen = false; this.roofMode = 'model'; this.posterOffset = 0;
      this.hover = null; this.highlighted = []; this.blocks = new Map(); this.courses = []; this.ready = false; this.model = 'schematic';
    }
    connectedCallback() {
      this.style.cssText += 'display:block;position:absolute;inset:0;overflow:hidden;';
      this.wrap = document.createElement('div'); this.wrap.style.cssText = 'position:absolute;inset:0;'; this.appendChild(this.wrap);
      this.boot();
    }
    disconnectedCallback() { this.alive = false; if (this.renderer) this.renderer.dispose(); }
    async boot(tries) {
      if (!window.THREE) { if ((tries || 0) < 80) return setTimeout(() => this.boot((tries || 0) + 1), 120); return this.fail('three'); }
      const src = this.getAttribute('data-src') || 'house/house-metadata.json', dir = src.replace(/[^/]*$/, '');
      try { this.data = await (await fetch(src)).json(); } catch (e) { return this.fail('data'); }
      await Promise.all([loadScript(CDN + 'geometries/RoundedBoxGeometry.js'), loadScript(CDN + 'environments/RoomEnvironment.js')]);
      try { this.init(); } catch (e) { console.error(e); return this.fail('webgl'); }
      this.loadGlb(dir + 'house.glb');
    }
    fail(why) { this.dispatchEvent(new CustomEvent('stagefail', { detail: { why } })); }
    init() {
      const T = window.THREE;
      const renderer = new T.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
      renderer.setPixelRatio(Math.min(devicePixelRatio, 2)); renderer.outputEncoding = T.sRGBEncoding;
      renderer.toneMapping = T.ACESFilmicToneMapping; renderer.toneMappingExposure = 1;
      renderer.shadowMap.enabled = true; renderer.shadowMap.type = T.PCFSoftShadowMap;
      renderer.domElement.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;display:block;touch-action:pan-y;';
      this.wrap.appendChild(renderer.domElement); this.renderer = renderer;
      const scene = new T.Scene(); this.scene = scene;
      const camera = new T.PerspectiveCamera(38, 1, .03, 80); this.camera = camera;
      // Image-based light makes the plastic read as plastic; direct lights only shape it.
      if (T.RoomEnvironment && T.PMREMGenerator) { try { const pm = new T.PMREMGenerator(renderer); scene.environment = pm.fromScene(new T.RoomEnvironment(), .04).texture; pm.dispose(); this.envOn = true; } catch (e) { console.info('env skipped', e); } }
      scene.add(new T.HemisphereLight(0xfaf9f3, 0x6d7580, this.envOn ? .35 : .95));
      const sun = new T.DirectionalLight(0xffffff, this.envOn ? .9 : 1.15); sun.position.set(-3, 8, 5); sun.castShadow = true;
      sun.shadow.mapSize.set(2048, 2048); sun.shadow.camera.left = -4.5; sun.shadow.camera.right = 4.5; sun.shadow.camera.top = 4.5; sun.shadow.camera.bottom = -4.5; sun.shadow.camera.near = 1; sun.shadow.camera.far = 20; sun.shadow.bias = -.002; sun.shadow.normalBias = .03; sun.shadow.radius = 3;
      scene.add(sun); scene.add(sun.target);
      const fill = new T.DirectionalLight(0xe0eafa, this.envOn ? .25 : .5); fill.position.set(5, 3, -5); scene.add(fill);
      this.house = new T.Group(); scene.add(this.house);
      this.studGeo = new T.CylinderGeometry(.048, .048, .017, 24);
      this.buildHouse();
      this.ro = new ResizeObserver(() => this.resize()); this.ro.observe(this);
      this.resize();
      this.ray = new T.Raycaster(); this.ptr = new T.Vector2();
      renderer.domElement.addEventListener('pointermove', (e) => this.onMove(e));
      renderer.domElement.addEventListener('pointerleave', () => { this.lastPtr = null; this.pending = null; this.setHover(null); });
      renderer.domElement.addEventListener('pointerdown', (e) => { this.down = [e.clientX, e.clientY]; });
      renderer.domElement.addEventListener('pointerup', (e) => { if (this.down && Math.hypot(e.clientX - this.down[0], e.clientY - this.down[1]) < 7) { const b = this.pick(e); if (b) this.dispatchEvent(new CustomEvent('roomactivate', { detail: { block: b } })); } this.down = null; });
      this.alive = true; this.ready = true;
      this.dispatchEvent(new CustomEvent('ready'));
      this._raf = requestAnimationFrame((t) => this.frame(t));
    }
    geo(w, h, d, r) { const T = window.THREE; return T.RoundedBoxGeometry ? new T.RoundedBoxGeometry(w, h, d, 2, Math.min(r || .008, w / 4, h / 4, d / 4)) : new T.BoxGeometry(w, h, d); }
    box(sz, mat, inset, r) {
      const T = window.THREE, e = inset || 0;
      const mesh = new T.Mesh(this.geo(Math.max(.02, sz[0] * S - e), Math.max(.02, sz[2] * S - e), Math.max(.02, sz[1] * S - e), r), mat);
      mesh.castShadow = true; mesh.receiveShadow = true; return mesh;
    }
    mat(color, opts) { const m = new window.THREE.MeshStandardMaterial(Object.assign({ roughness: .55, metalness: 0, envMapIntensity: .9 }, opts || {})); m.color.set(color).convertSRGBToLinear(); return m; }
    studs(mesh, sz, mat, e) {
      const T = window.THREE, nx = Math.max(1, Math.round(sz[0] * S / PITCH)), nz = Math.max(1, Math.round(sz[1] * S / PITCH)), top = (sz[2] * S - (e || 0)) / 2;
      const inst = new T.InstancedMesh(this.studGeo, mat, nx * nz); const m = new T.Matrix4(); let i = 0;
      for (let x = 0; x < nx; x++) for (let z = 0; z < nz; z++) { m.makeTranslation((x - (nx - 1) / 2) * PITCH, top + .0085, (z - (nz - 1) / 2) * PITCH); inst.setMatrixAt(i++, m); }
      inst.castShadow = true; inst.receiveShadow = true; mesh.add(inst); return inst;
    }
    // "LEGO House" on the front edge of the base, as on the supplied model.
    label() {
      const T = window.THREE, c = document.createElement('canvas'); c.width = 1024; c.height = 128; const g = c.getContext('2d');
      g.clearRect(0, 0, 1024, 128); g.font = '600 italic 78px "Libre Franklin", "Helvetica Neue", Arial, sans-serif'; g.textBaseline = 'middle';
      g.fillStyle = 'rgba(0,0,0,.35)'; g.fillText('LEGO House', 22, 70); g.fillStyle = '#e9e6dc'; g.fillText('LEGO House', 18, 64);
      const tex = new T.CanvasTexture(c); tex.encoding = T.sRGBEncoding; tex.anisotropy = 8;
      const m = new T.Mesh(new T.PlaneGeometry(1.4, .175), new T.MeshStandardMaterial({ map: tex, transparent: true, roughness: .5, metalness: 0 }));
      m.position.set(-1.5, .105, 2.6 + .002); m.renderOrder = 2; return m;
    }
    buildHouse() {
      const T = window.THREE, d = this.data;
      const base = this.box([560, 480, 20], this.mat('#2b2e33', { roughness: .45 }), 0, .02); base.position.set(...W([20, -20, 10])); this.house.add(base);
      this.labelMesh = this.label(); this.house.add(this.labelMesh);
      const pave = this.box([520, 440, 12], this.mat('#d6d2c8', { roughness: .8 }), .002, .006); pave.position.set(...W([20, -20, 22])); this.house.add(pave); this.pave = pave;
      const glass = this.box([320, 280, 56], this.mat('#d9e8f2', { transparent: true, opacity: .14, depthWrite: false, roughness: .15 }), .03); glass.position.set(...W([20, -20, 52])); glass.castShadow = false; this.house.add(glass); this.glass = glass;
      const byBlock = {};
      d.building_courses.forEach((c) => { (byBlock[c.block] = byBlock[c.block] || []).push(c); });
      Object.keys(byBlock).forEach((k, bi) => {
        const n = +k, list = byBlock[k].sort((a, b) => a.order - b.order), top = list.length - 1;
        const g = d.groups.find((x) => x.name === 'Block ' + n);
        const center = new T.Vector3(...W(g.center));
        const wall = this.mat(WHITE, { roughness: .5 }), roof = this.mat(ROOF[n] || GREY, { roughness: .42 });
        const group = new T.Group(); group.position.copy(center); this.house.add(group);
        const dir = new T.Vector3(center.x - .1, 0, center.z + .2); if (dir.length() < .05) dir.set(0, 0, 1); dir.normalize();
        const entry = { n, group, center, dir, k: 1, mats: [{ m: wall, roof: false }, { m: roof, roof: true, color: ROOF[n] || GREY }], courses: [], idx: bi, lift: 0 };
        list.forEach((c, i) => {
          // course bounds interpenetrate; a per-order inset keeps coplanar faces from z-fighting
          const mesh = this.box(c.size, i === top ? roof : wall, .006 + i * .004, .007);
          mesh.position.copy(new T.Vector3(...W(c.center)).sub(center)); mesh.userData.base = mesh.position.clone(); mesh.userData.order = c.order; mesh.userData.block = n;
          // studs wherever a top is exposed: the roof, and any course wider than the one above it
          const above = list[i + 1], exposed = i === top || (above && (above.size[0] < c.size[0] - 10 || above.size[1] < c.size[1] - 10));
          if (exposed) this.studs(mesh, c.size, i === top ? roof : wall, .006 + i * .004);
          if (i === top && MARKERS.includes(n)) mesh.add(this.minifig(c.size));
          group.add(mesh); entry.courses.push(mesh); this.courses.push(mesh);
        });
        this.blocks.set(n, entry);
      });
      const glassStair = this.mat('#d9e3e8', { transparent: true, opacity: .2, depthWrite: false, roughness: .25 }), white = this.mat(WHITE, { roughness: .5 });
      this.stairs = d.stair_pieces.map((s) => { const m = this.box(s.size, s.transparent ? glassStair : white, .004, .005); if (s.transparent) m.castShadow = false; m.position.set(...W(s.center)); m.userData.base = m.position.clone(); m.userData.order = s.order; this.house.add(m); return m; });
      const green = this.mat('#2f8f45', { roughness: .6 }), brown = this.mat('#684027', { roughness: .7 });
      const leafG = new T.CylinderGeometry(.13, .13, .075, 20), baseG = new T.CylinderGeometry(.085, .085, .055, 16), stemG = new T.CylinderGeometry(.045, .045, .24, 14);
      this.tree = d.tree_pieces.map((p, i) => {
        const leaf = p.faces === 316; const m = new T.Mesh(leaf ? leafG : p.faces === 160 ? baseG : stemG, leaf ? green : brown); m.castShadow = true; m.receiveShadow = true;
        if (p.order === 5) m.rotation.z = Math.PI / 2;
        m.position.set(...W(p.center)); m.userData.base = m.position.clone(); m.userData.spread = new T.Vector3(Math.cos(i * 2.3) * .3, .5 + i * .1, Math.sin(i * 2.3) * .3); this.house.add(m); return m;
      });
    }
    // ---- supplied model (house.glb beside the metadata) ----
    async loadGlb(url) {
      const T = window.THREE;
      let buf; try { const r = await fetch(url); if (!r.ok) return; buf = await r.arrayBuffer(); } catch (e) { return; }
      const ok = await loadScript(CDN + 'loaders/GLTFLoader.js'); await loadScript(CDN + 'loaders/DRACOLoader.js');
      if (!ok || !T.GLTFLoader) return;
      const loader = new T.GLTFLoader();
      if (T.DRACOLoader) { const d = new T.DRACOLoader(); d.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.4.1/'); loader.setDRACOLoader(d); }
      loader.parse(buf, '', (gltf) => { try { this.adoptGlb(gltf.scene); } catch (e) { console.error('house.glb could not be adopted; schematic stays', e); } }, (e) => console.info('house.glb failed to parse; schematic stays', e));
    }
    adoptGlb(root) {
      const T = window.THREE, k = 100;
      root.scale.setScalar(S);
      const blocks = new Map(), courses = [], stairs = [], tree = [];
      root.traverse((o) => {
        let m;
        if ((m = o.name.match(/^Block[_ ](\d+)$/)) && !o.isMesh) blocks.set(+m[1], { n: +m[1], group: o, center: o.position.clone(), k, mats: [], courses: [], lift: 0 });
        if ((m = o.name.match(/^Tree_piece_(\d+)$/))) { o.userData.base = o.position.clone(); const i = +m[1] - 1; o.userData.spread = new T.Vector3(Math.cos(i * 2.3) * .3, .5 + i * .1, Math.sin(i * 2.3) * .3).multiplyScalar(k); tree.push(o); }
        if ((m = o.name.match(/^Stair_piece_(\d+)$/))) { o.userData.base = o.position.clone(); o.userData.order = +m[1] - 1; stairs.push(o); }
        if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; o.frustumCulled = true; }
      });
      root.traverse((o) => {
        const m = o.name.match(/^Block_(\d+)_course_(\d+)$/); if (!m) return;
        const b = blocks.get(+m[1]); if (!b) return;
        o.userData.base = o.position.clone(); o.userData.order = +m[2]; o.userData.block = b.n; b.courses.push(o); courses.push(o);
        o.traverse((c) => { if (!c.isMesh) return; c.userData.block = b.n; courses.push(c); const list = Array.isArray(c.material) ? c.material : [c.material]; c.material = list.map((mt) => { const cl = mt.clone(); cl.roughness = .5; cl.metalness = 0; cl.envMapIntensity = .9; if (mt.name === 'Material_47_c') { cl.transparent = true; cl.opacity = .18; cl.depthWrite = false; } b.mats.push({ m: cl, roof: false, color: '#' + cl.color.clone().convertLinearToSRGB().getHexString(), glass: mt.name === 'Material_47_c' }); return cl; }); if (!Array.isArray(c.material) || c.material.length === 1) c.material = c.material[0]; });
      });
      if (!blocks.size || !courses.length) throw new Error('no Block_N_course_M meshes');
      blocks.forEach((b) => {
        b.courses.sort((a, c) => a.userData.order - c.userData.order);
        const top = b.courses[b.courses.length - 1];
        top.traverse((c) => { if (c.isMesh) [].concat(c.material).forEach((mt) => { const e = b.mats.find((x) => x.m === mt); if (e && !e.glass) e.roof = true; }); });
        const wc = b.group.getWorldPosition(new T.Vector3());
        b.dir = new T.Vector3(wc.x - .1, 0, wc.z + .2); if (b.dir.length() < .05) b.dir.set(0, 0, 1); b.dir.normalize();
        if (MARKERS.includes(b.n)) { const bb = new T.Box3().setFromObject(top); const p = bb.getCenter(new T.Vector3()); p.y = bb.max.y; const fig = this.minifig(); fig.position.copy(top.worldToLocal(p.clone())); fig.scale.setScalar(k); top.getWorldQuaternion(fig.quaternion).invert(); top.add(fig); }
      });
      root.traverse((o) => { if (o.isMesh && !o.userData.block) [].concat(o.material).forEach((mt) => { mt.roughness = .55; mt.metalness = 0; mt.envMapIntensity = .9; if (mt.name === 'Material_47_c') { mt.transparent = true; mt.opacity = .18; mt.depthWrite = false; } }); });
      this.house.visible = false; this.scene.add(root); this.glbRoot = root;
      this.blocks = blocks; this.courses = courses; this.stairs = stairs; this.tree = tree; this.glass = null; this.pave = null; this.model = 'glb';
      this.setRoofMode(this.roofMode);
      this.dispatchEvent(new CustomEvent('model', { detail: { model: 'glb' } }));
    }
    minifig(sz) {
      const T = window.THREE, g = new T.Group(), ink = this.mat('#344c5a'), yellow = this.mat('#f5bc34');
      const head = new T.Mesh(new T.CylinderGeometry(.035, .035, .065, 12), yellow); head.position.y = .155;
      const body = new T.Mesh(this.geo(.095, .09, .055, .006), ink); body.position.y = .085;
      const legs = new T.Mesh(this.geo(.085, .055, .045, .005), ink); legs.position.y = .025;
      [head, body, legs].forEach((m) => { m.castShadow = true; g.add(m); });
      if (sz) g.position.set(sz[0] * S * .25, sz[2] * S / 2 + .017, sz[1] * S * .2);
      g.rotation.y = .6; return g;
    }
    resize() { const w = this.clientWidth || 800, h = this.clientHeight || 600; this.renderer.setSize(w, h, false); this.camera.aspect = w / h; this.vw = w; this.vh = h; this.camera.updateProjectionMatrix(); }
    // ---- flight path (R0 flight-path.js) ----
    sampleFlight(progress) {
      const T = window.THREE, M = T.MathUtils;
      if (!this._curves) {
        const curve = (pts) => new T.CatmullRomCurve3(pts.map((p) => new T.Vector3(...p)), false, 'centripetal');
        this._curves = {
          pos: curve([[5.6, 4.7, 6.8], [4, 3.5, 5.5], [2.2, 2.3, 4.2], [.85, 1.25, 2.7], [.36, .58, 1.8], [.36, .55, 1.1], [.48, .58, .78], [.9, .59, .43], [.95, .6, -.12], [.64, .6, -.67], [.16, .62, -1.05], [.12, .65, -1.55], [.25, .8, -2.2], [.65, 1.3, -3.3], [1.3, 2.3, -5], [4.2, 2.8, -4.5], [5.8, 3.2, -1.8], [6.1, 3.8, 1.8], [4.8, 4.35, 5.2], [3.6, 4.15, 6.3]]),
          gaze: curve([[.15, .65, .2], [.15, .65, .2], [.05, .6, .05], [-.1, .5, 0], [-.23, .49, 0], [-.23, .49, 0], [-.23, .49, 0], [-.23, .5, 0], [-.23, .5, 0], [-.23, .5, 0], [-.23, .5, 0], [-.18, .6, .05], [.1, .65, .2], [.15, .65, .2], [.15, .65, .2], [.15, .7, .2], [.15, .75, .2], [.15, .75, .2], [.15, .7, .2], [.15, .65, .2]]),
        };
        const beats = [[0, 0], [.28, 6 / 19], [.54, 10 / 19], [.69, 14 / 19], [1, 1]];
        const slopes = beats.slice(1).map(([x, y], i) => (y - beats[i][1]) / (x - beats[i][0]));
        const tangents = beats.map((_, i) => i === 0 ? slopes[0] : i === beats.length - 1 ? slopes[slopes.length - 1] : 2 / (1 / slopes[i - 1] + 1 / slopes[i]));
        this._routeTime = (p) => {
          let i = beats.findIndex((b, j) => j > 0 && p <= b[0]) - 1; i = Math.max(0, Math.min(beats.length - 2, i));
          const a = beats[i], b = beats[i + 1], d = b[0] - a[0], t = (p - a[0]) / d, t2 = t * t, t3 = t2 * t;
          return (2 * t3 - 3 * t2 + 1) * a[1] + (t3 - 2 * t2 + t) * d * tangents[i] + (-2 * t3 + 3 * t2) * b[1] + (t3 - t2) * d * tangents[i + 1];
        };
      }
      const aE = (p, f) => .5 - .5 * Math.cos(Math.PI * M.clamp(p / f, 0, 1));
      const p = M.clamp(progress, 0, 1), o = p / .16;
      const cp = p < .16 ? .16 * (2 * o * o - o * o * o) : p;
      const t = M.clamp(this._routeTime(cp), 0, 1), ov = 1 - aE(p, .18);
      const position = this._curves.pos.getPoint(t); position.x += 3 * ov; position.y += 2.5 * ov; position.z += 3.4 * ov;
      const target = this._curves.gaze.getPoint(t); target.y += .55 * ov;
      return {
        position, target, aE,
        fov: 38 + 20 * M.smoothstep(p, .16, .28) * (1 - M.smoothstep(p, .57, .8)),
        separation: 1 - aE(p, .82),
        rearSeparation: 1 - .035 * aE(p, .58) - .965 * M.smootherstep(p, .58, .84),
        interior: M.smoothstep(p, .08, .22) * (1 - M.smoothstep(p, .72, .95)),
        openingSpread: .4 + .6 * aE(p, .16),
        courseSpread: .2 + .8 * aE(p, .16),
        posterOffset: .22 * (1 - M.smoothstep(p, 0, .2)),
      };
    }
    // ---- public API ----
    setProgress(p) { const prev = this.progress; this.progress = p; if (this.owner === 'threshold' && Math.abs(p - prev) > .002) this.startBlend(); }
    setRoofMode(mode) { this.roofMode = mode; this.blocks.forEach((b) => b.mats.forEach((e) => { if (e.roof) e.m.color.set(mode === 'grey' ? GREY : (e.color || ROOF[b.n] || GREY)).convertSRGBToLinear(); })); }
    setTheme(dark) { this.dark = dark; if (this.pave) this.pave.material.color.set(dark ? '#c9c6bd' : '#d6d2c8').convertSRGBToLinear(); if (this.renderer) this.renderer.toneMappingExposure = dark ? 1.08 : 1; }
    highlight(blocks) { this.highlighted = blocks == null ? [] : [].concat(blocks); }
    freeze(on) { this.frozen = on; if (!on && this.alive) { if (this._raf) cancelAnimationFrame(this._raf); this._raf = requestAnimationFrame((t) => this.frame(t)); } }
    pose() { return { position: this.camera.position.clone(), target: this.target ? this.target.clone() : new window.THREE.Vector3(), fov: this.camera.fov }; }
    bookmark() { this.mark = Object.assign(this.pose(), { progress: this.progress }); return this.mark; }
    blockWorld(b) { return b.group.getWorldPosition(new window.THREE.Vector3()); }
    roomPose(block, style) {
      const T = window.THREE, b = this.blocks.get(block); if (!b) return null;
      const c = this.blockWorld(b); c.y += .15;
      if (style === 'liftoff') return { position: c.clone().add(new T.Vector3(.1, 3.8, 1.5)), target: c, fov: 36 };
      if (style === 'lobby') return { position: c.clone().add(b.dir.clone().multiplyScalar(1.6)).add(new T.Vector3(0, .8, 0)), target: c, fov: 46 };
      return { position: c.clone().add(b.dir.clone().multiplyScalar(2.4)).add(new T.Vector3(0, 1.8, 0)), target: c, fov: 40 };
    }
    lobbyPose() { const T = window.THREE; return { position: new T.Vector3(.48, .58, .78), target: new T.Vector3(-.23, .49, 0), fov: 52 }; }
    flyTo(block, opts) {
      const T = window.THREE, o = Object.assign({ style: 'liftoff', seconds: 1.4, slide: true }, opts || {});
      if (!this.ready) return Promise.resolve(false);
      if (this.flight) this.cancelFlight(true);
      if (this.owner === 'tour' || this.owner === 'blend') this.bookmark();
      const b = this.blocks.get(block); if (!b) return Promise.resolve(false);
      this.lastStyle = o.style;
      const to = o.pose || this.roomPose(block, o.style === 'direct' ? 'liftoff' : o.style);
      const from = this.pose();
      const points = [from.position];
      if (o.pose) { points.push(new T.Vector3(.85, 1.25, 2.7), new T.Vector3(.36, .58, 1.8)); }
      else if (o.style === 'exterior') { const mid = from.position.clone().lerp(to.position, .5); mid.setLength(Math.max(5.5, mid.length())); mid.y = Math.max(mid.y, 4.2); points.push(mid); }
      if (!o.pose && o.style === 'lobby') points.push(new T.Vector3(.36, .58, 1.8), new T.Vector3(.36, .55, 1.1));
      if (!o.pose && o.style === 'liftoff') { const up = from.position.clone().lerp(to.position, .45); up.y = Math.max(up.y, to.position.y + .6); points.push(up); }
      points.push(to.position);
      const curve = new T.CatmullRomCurve3(points, false, 'centripetal');
      return new Promise((resolve) => {
        this.owner = 'flight'; this.activeBlock = o.pose ? null : block;
        this.flight = { t0: performance.now(), dur: o.style === 'direct' ? 10 : o.seconds * 1000, curve, from, to, slide: o.slide, block, resolve, phase: 'move' };
      });
    }
    cancelFlight(silent) {
      const f = this.flight; if (!f) return false;
      this.flight = null; this.slideTo(0, 350);
      if (!silent && this.mark) this.tweenTo(this.mark, 600, () => { this.owner = 'tour'; });
      f.resolve(false); return true;
    }
    slideTo(amount, ms) { const b = this.blocks.get(this.activeBlock); if (!b) return; this.slide = { b, from: b.lift, to: amount, t0: performance.now(), dur: ms }; }
    tweenTo(pose, ms, done) {
      const T = window.THREE, from = this.pose();
      this.owner = 'flight'; this.flight = { t0: performance.now(), dur: ms, curve: new T.CatmullRomCurve3([from.position, pose.position], false), from, to: pose, slide: false, resolve: () => { if (done) done(); }, phase: 'move', plain: true };
    }
    returnFrom(mode, ms) {
      return new Promise((resolve) => {
        this.slideTo(0, 420);
        if (mode === 'bookmark' && this.mark) this.tweenTo(this.mark, ms || 900, () => { this.owner = 'tour'; this.activeBlock = null; resolve(true); });
        else { this.owner = 'threshold'; this.held = this.pose(); setTimeout(() => resolve(true), 420); }
      });
    }
    // Put the camera (and the lifted block) outside `block` without animating — used when the sheet on the table
    // is not the room we flew to, so Back lands you where the open sheet actually lives.
    landAt(block, pose) {
      this.flight = null; this.slide = null; this.blend = null;
      this.blocks.forEach((b) => { b.lift = 0; });
      this.activeBlock = pose ? null : (this.blocks.has(block) ? block : null);
      if (this.activeBlock) this.blocks.get(block).lift = 1;
      this.held = pose || this.roomPose(block, this.lastStyle === 'direct' ? 'liftoff' : (this.lastStyle || 'liftoff')) || this.pose();
      this.owner = 'threshold';
      this.camera.position.copy(this.held.position); this.target = this.held.target.clone(); this.camera.fov = this.held.fov;
    }
    startBlend() { this.held = this.pose(); this.blend = { t0: performance.now(), dur: 700 }; this.owner = 'blend'; this.activeBlock = null; }
    // ---- picking ----
    pick(e) {
      const r = this.renderer.domElement.getBoundingClientRect();
      this.ptr.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
      this.ray.setFromCamera(this.ptr, this.camera);
      const hits = this.ray.intersectObjects(this.courses, false);
      if (!hits.length) return null;
      // the hovered block is lifted/scaled, so prefer it whenever it is anywhere under the ray — it can't un-hover itself by moving
      if (this.hover != null) { for (let i = 0; i < Math.min(hits.length, 4); i++) if (hits[i].object.userData.block === this.hover) return this.hover; }
      return hits[0].object.userData.block;
    }
    onMove(e) { if (this.owner === 'flight') return; this.lastPtr = [e.clientX, e.clientY]; if (this.suspendHover) return; if (this.hover != null) this.dispatchEvent(new CustomEvent('roomhover', { detail: { block: this.hover, x: e.clientX, y: e.clientY } })); this.propose(this.pick(e), e.clientX, e.clientY, performance.now()); }
    // camera moved under a still pointer (scroll, blend): re-pick so hover tracks what is really under it
    repick() { if (!this.lastPtr || this.owner === 'flight' || this.suspendHover) return; const [x, y] = this.lastPtr; this.propose(this.pick({ clientX: x, clientY: y }), x, y, performance.now()); }
    // hysteresis: a change must be seen continuously for a short while before it is committed (longer to clear than to switch)
    propose(b, x, y, now) {
      if (b === this.hover) { this.pending = null; return; }
      if (!this.pending || this.pending.b !== b) { this.pending = { b, t0: now }; if (this.hover == null && b != null) { this.pending = null; this.setHover(b, x, y); } return; }
      if (now - this.pending.t0 >= (b == null ? 110 : 45)) { this.pending = null; this.setHover(b, x, y); }
    }
    setHover(b, x, y) { if (b !== this.hover || b) { this.hover = b; this.renderer.domElement.style.cursor = b ? 'pointer' : ''; this.dispatchEvent(new CustomEvent('roomhover', { detail: { block: b, x, y } })); } }
    // ---- frame ----
    frame(now) {
      if (!this.alive || this.frozen) { this._raf = null; return; }
      this._raf = requestAnimationFrame((t) => this.frame(t));
      const T = window.THREE, M = T.MathUtils, cam = this.camera;
      const s = this.sampleFlight(this.progress), p = this.progress;
      if (this.owner === 'tour') { cam.position.copy(s.position); this.target = s.target.clone(); cam.fov = s.fov; }
      else if (this.owner === 'blend' && this.blend) {
        const k = ease(M.clamp((now - this.blend.t0) / this.blend.dur, 0, 1));
        cam.position.copy(this.held.position).lerp(s.position, k); this.target = this.held.target.clone().lerp(s.target, k); cam.fov = M.lerp(this.held.fov, s.fov, k);
        if (k >= 1) { this.owner = 'tour'; this.blend = null; }
      } else if (this.owner === 'flight' && this.flight) {
        const f = this.flight, k = ease(M.clamp((now - f.t0) / f.dur, 0, 1));
        cam.position.copy(f.curve.getPoint(k)); this.target = f.from.target.clone().lerp(f.to.target, k); cam.fov = M.lerp(f.from.fov, f.to.fov, k);
        if (k >= 1) {
          if (f.phase === 'move' && f.slide) { f.phase = 'slide'; this.slideTo(1, 520); f.t1 = now; }
          else if (f.phase === 'slide' && now - f.t1 < 520) { /* settle */ }
          else { this.flight = null; if (!f.plain) this.owner = 'threshold'; this.held = this.pose(); f.resolve(true); }
        }
      } else if (this.owner === 'threshold' && this.held) { cam.position.copy(this.held.position); this.target = this.held.target.clone(); cam.fov = this.held.fov; }
      // poster framing: push the house right while the wordmark owns the left (tour only)
      const off = this.owner === 'tour' || this.owner === 'blend' ? s.posterOffset : 0;
      if (this.vw && this.vw >= 740 && off > .001) cam.setViewOffset(this.vw, this.vh, -this.vw * off, 0, this.vw, this.vh); else if (cam.view && cam.view.enabled) cam.clearViewOffset();
      cam.up.set(0, 1, 0); cam.lookAt(this.target || new T.Vector3()); cam.updateProjectionMatrix();
      // hover follows the camera: re-pick a few times a second whenever the view is moving
      if (this.lastPtr && (this.owner !== 'threshold') && now - (this._lastRepick || 0) > 32) { this._lastRepick = now; this.repick(); }
      // assembly (R0 choreography); `k` converts metre offsets into the model's own units (cm for the glb)
      if (this.slide) { const sl = this.slide, kk = ease(M.clamp((now - sl.t0) / sl.dur, 0, 1)); sl.b.lift = M.lerp(sl.from, sl.to, kk); if (kk >= 1) this.slide = null; }
      const camDir = new T.Vector3(), interior = s.interior, lifted = this.activeBlock && this.blocks.get(this.activeBlock) ? this.blocks.get(this.activeBlock).lift : 0;
      this.blocks.forEach((b) => {
        const n = b.n, home = b.center, k = b.k || 1, finish = .74 + (n % 4) * .027, rear = home.z < -.5 * k ? s.rearSeparation : 0;
        const hz = Math.max(1 - s.aE(p, finish), rear) * s.openingSpread, dp = Math.max(1 - s.aE(p, finish * .98), rear) * s.openingSpread, ht = Math.max(1 - s.aE(p, finish * 1.015), rear) * s.openingSpread;
        const pos = home.clone(); pos.x += Math.sign(home.x || 1) * 1.1 * k * hz; pos.z += Math.sign(home.z || 1) * .9 * k * dp; pos.y += (.65 + (n % 4) * .42) * k * ht;
        if (b.lift > 0) { camDir.copy(cam.position).sub(pos.clone().multiplyScalar(1 / k)).normalize().multiplyScalar(.5 * b.lift * k); pos.add(camDir); }
        b.group.position.copy(pos); const sc = 1 + .1 * b.lift; b.group.scale.set(sc, sc, sc);
        b.courses.forEach((m) => { const o = m.userData.order, sepc = (1 - s.aE(p, .4 + o * .055 + (n % 3) * .01)) * s.courseSpread, a = n * 2.4; m.position.copy(m.userData.base); m.position.x += Math.cos(a) * (.04 + o * .018) * k * sepc; m.position.y += (.12 + o * .08) * k * sepc; m.position.z += Math.sin(a) * (.04 + o * .018) * k * sepc; });
        const isActive = this.activeBlock === n, dim = this.activeBlock && !isActive ? 1 - .5 * lifted : 1;
        const hot = (this.hover === n || this.highlighted.indexOf(n) >= 0) ? 1 : 0;
        const anyHot = this.hover != null || this.highlighted.length > 0;
        b.hot = b.hot === undefined ? 0 : b.hot + ((hot ? 1 : 0) - b.hot) * (hot ? .35 : .25);
        if (b.hot > .002) { b.group.position.y += .06 * b.hot; const hs = 1 + .03 * b.hot; b.group.scale.multiplyScalar(hs); }
        const cool = anyHot && !hot ? .72 : 1;
        b.mats.forEach((e) => {
          if (e.glass) return;
          e.m.opacity = (1 - (e.roof ? .3 : .55) * interior) * dim * cool;
          const tr = e.m.opacity < .995; if (e.m.transparent !== tr) { e.m.transparent = tr; e.m.needsUpdate = true; }
          e.m.emissive.set(0xff533d); e.m.emissiveIntensity = (e.roof ? .55 : .3) * b.hot;
        });
      });
      if (this.glass) this.glass.material.opacity = .14 * (1 - .6 * interior);
      this.stairs.forEach((m) => { const o = m.userData.order, k = this.model === 'glb' ? 100 : 1, sp = 1 - s.aE(p, .35 + o * .008); m.position.copy(m.userData.base); m.position.x -= (.08 + o * .004) * k * sp; m.position.y += (.12 + o * .007) * k * sp; m.position.z += (.06 + o * .003) * k * sp; });
      this.tree.forEach((m, i) => { const sp = 1 - s.aE(p, .24 + i * .04); m.position.copy(m.userData.base).add(m.userData.spread.clone().multiplyScalar(sp)); });
      this.renderer.render(this.scene, cam);
    }
  }
  customElements.define('house-stage', HouseStage);
})();
