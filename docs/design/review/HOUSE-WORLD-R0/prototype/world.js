// PROTOTYPE: local navigation experiment; no production topology is implied.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import metadata from './house-metadata.json';
import modelUrl from './house.glb?url';
import previewUrl from './house-preview.png?url';
import { sampleFlight, assemblyEase } from './flight-path.js';
import { moduleByBlock } from './modules.js';

// Supplied tree connection axes: stacked parts seat downward; the side leaf
// attaches along the branch from the outside. Each has a final stud stroke.
const treeSeats = [
  {axis:'y',gap:.07,finish:.24}, {axis:'y',gap:.07,finish:.25},
  {axis:'y',gap:.23,finish:.39}, {axis:'y',gap:.28,finish:.34},
  {axis:'y',gap:.46,finish:.445}, {axis:'x',gap:-.34,finish:.48},
  {axis:'y',gap:.48,finish:.475}, {axis:'y',gap:.72,finish:.505},
];
function seatingOffset(progress, seat) {
  const stroke = Math.sign(seat.gap)*.035;
  const pressStart = seat.finish-.025;
  return (seat.gap-stroke)*(1-assemblyEase(progress,pressStart)) + stroke*(1-THREE.MathUtils.smootherstep(progress,pressStart,seat.finish));
}

export class HouseWorld {
  constructor(stage, onSelect, announce) {
    this.stage = stage;
    this.onSelect = onSelect;
    this.announce = announce;
    this.blocks = new Map();
    this.treePieces = [];
    this.stairPieces = [];
    this.buildingCourses = [];
    this.hoveredBlock = null;
    this.pickStats = { candidates:0, total:0 };
    this.mode = 'exploded';
    this.journeyProgress = 0;
    this.still = matchMedia('(prefers-reduced-motion: reduce)').matches;
    this.lite = false;
    this.motion = true;
    this.sequence = 0;
    this.frames = 0;
    this.renderRequests = 0;
    this.raycaster = new THREE.Raycaster();
    this.pointer = new THREE.Vector2();
    this.status = document.querySelector('#model-status');
    if (new URLSearchParams(location.search).has('no3d')) {
      this.showFallback();
      this.status.textContent = '2D mode · every destination is available in the list.';
      return;
    }
    try {
      this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      this.renderer.setPixelRatio(Math.min(devicePixelRatio, 1.25));
      this.renderer.setClearColor(0x000000, 0);
      this.renderer.outputColorSpace = THREE.SRGBColorSpace;
      this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
      this.renderer.toneMappingExposure = 1;
      stage.prepend(this.renderer.domElement);
      this.scene = new THREE.Scene();
      this.camera = new THREE.PerspectiveCamera(38, 1, .01, 100);
      this.camera.position.set(5.6, 4.7, 6.8);
      this.controls = new OrbitControls(this.camera, this.renderer.domElement);
      this.controls.target.set(.15, .65, .2);
      this.controls.minDistance = .08;
      this.controls.maxDistance = 22;
      this.controls.maxPolarAngle = Math.PI * .85;
      this.controls.enableDamping = false;
      this.controls.enableZoom = false;
      this.renderer.domElement.style.touchAction = 'pan-y';
      this.controls.addEventListener('change', () => this.render());
      this.scene.add(new THREE.HemisphereLight(0xfaf9f3, 0x89908b, 1.7));
      const key = new THREE.DirectionalLight(0xffffff, 2.6);
      key.position.set(-3, 8, 5);
      this.scene.add(key);
      const fill = new THREE.DirectionalLight(0xe0eafa, 1.1);
      fill.position.set(5, 3, -5);
      this.scene.add(fill);
      this.outline = new THREE.BoxHelper(undefined, 0xb84f2b);
      this.outline.material.depthTest = false;
      this.outline.material.transparent = true;
      this.outline.renderOrder = 100;
      this.outline.visible = false;
      this.scene.add(this.outline);
      this.resizeObserver = new ResizeObserver(() => this.resize());
      this.resizeObserver.observe(stage);
      const canvas = this.renderer.domElement;
      canvas.setAttribute('aria-hidden', 'true');
      canvas.addEventListener('pointerdown', (event) => { this.down = [event.clientX, event.clientY]; });
      canvas.addEventListener('pointermove', (event) => this.hover(event));
      canvas.addEventListener('pointerleave', () => this.highlight(null));
      canvas.addEventListener('pointerup', (event) => {
        if (this.down && Math.hypot(event.clientX - this.down[0], event.clientY - this.down[1]) < 7 && event.button === 0) {
          const block = this.pick(event);
          if (block) this.onSelect(moduleByBlock.get(block.userData.block));
        }
        this.down = null;
      });
      canvas.addEventListener('webglcontextlost', (event) => {
        event.preventDefault();
        this.sequence++;
        this.status.hidden = false;
        this.status.textContent = '3D paused. The page list still works. Reload to restore the model.';
        this.showFallback();
      });
      this.proxy = this.makeProxy();
      this.scene.add(this.proxy);
      this.activate(this.proxy);
      document.querySelector('#stage-fallback').hidden = true;
      this.resize();
      this.status.textContent = 'Lite house ready · loading the supplied brick model…';
      if (!new URLSearchParams(location.search).has('lite')) this.loadFull();
      else { this.lite = true; this.status.textContent = 'Lite house · simplified blocks, same destinations'; }
    } catch (error) {
      this.showFallback();
      this.status.textContent = '3D unavailable · use the page list to enter every room.';
      this.announce('3D unavailable. All pages remain available in the page list.');
      console.info('House fallback:', error.message);
    }
  }
  showFallback() {
    const image = document.querySelector('#stage-fallback');
    image.src = previewUrl;
    image.hidden = false;
  }
  async loadFull() {
    if (this.full || this.loading || !this.renderer) return;
    this.loading = true;
    try {
      const startLoad = performance.now();
      const draco = new DRACOLoader().setDecoderPath('/draco/').setWorkerLimit(2);
      const gltf = await new GLTFLoader().setDRACOLoader(draco).loadAsync(modelUrl);
      draco.dispose();
      this.modelReadyMs = Math.round(performance.now() - startLoad);
      this.full = gltf.scene;
      this.full.scale.setScalar(.01);
      this.full.traverse((object) => {
        const match = object.name.match(/^Block_(\d+)$|^Block (\d+)$/);
        if (match && object.type !== 'Mesh') object.userData.block = Number(match[1] || match[2]);
        const tree = object.name.match(/^Tree_piece_(\d+)$/);
        if (tree) object.userData.treeOrder = Number(tree[1])-1;
        const stair = object.name.match(/^Stair_piece_(\d+)$/);
        if (stair) object.userData.stairOrder = Number(stair[1])-1;
        const course = object.name.match(/^Block_(\d+)_course_(\d+)$/);
        if (course) {object.userData.courseBlock = Number(course[1]);object.userData.courseOrder = Number(course[2]);}
        if (object.isMesh) {
          object.frustumCulled = true;
          const materials = Array.isArray(object.material) ? object.material : [object.material];
          materials.forEach((material) => {
            material.roughness = .72; material.metalness = 0;
            if (material.name === 'Material_47_c') {
              material.transparent = true; material.opacity = .18;
              material.depthWrite = false; material.forceSinglePass = true;
            }
          });
        }
      });
      this.scene.add(this.full);
      if (!this.lite && !this.returnView) this.activate(this.full);
      this.status.textContent = this.lite ? 'Lite house · simplified blocks, same destinations' : 'Supplied LEGO model · 21 selectable blocks';
      this.render();
    } catch (error) {
      this.lite = true;
      document.querySelector('#quality-toggle').setAttribute('aria-pressed','true');
      this.status.textContent = 'Brick model unavailable · lite house and page list are ready';
      this.announce('The brick model could not load. The lite house has the same destinations.');
      console.info('GLB fallback:', error.message);
    } finally { this.loading = false; }
  }
  makeProxy() {
    const root = new THREE.Group();
    const white = new THREE.MeshStandardMaterial({ color: 0xf7f5ed, roughness: .85 });
    const roofs = [0xdc5528, 0xedaf27, 0x357aab, 0x72a245, 0xdb4d33];
    const base = new THREE.Mesh(new THREE.BoxGeometry(5.6, .12, 4.8), new THREE.MeshStandardMaterial({ color: 0x393c39 }));
    base.position.set(.2, .08, .2);
    root.add(base);
    for (const item of metadata.groups.filter((group) => /^Block /.test(group.name))) {
      const number = Number(item.name.split(' ')[1]);
      const block = new THREE.Group();
      block.userData.block = number;
      block.position.set(item.center[0] * .01, item.center[2] * .01, -item.center[1] * .01);
      const courses = metadata.building_courses.filter(part=>part.block===number);
      const roofMaterial = new THREE.MeshStandardMaterial({color:number===22?0xf5f3ec:roofs[number%roofs.length]});
      for (const [index,part] of courses.entries()) {
        const mesh = new THREE.Mesh(new THREE.BoxGeometry(part.size[0]*.01,part.size[2]*.01,part.size[1]*.01),index===courses.length-1?roofMaterial:white);
        mesh.position.set(part.center[0]*.01-block.position.x,part.center[2]*.01-block.position.y,-part.center[1]*.01-block.position.z);
        mesh.userData.courseBlock = number;
        mesh.userData.courseOrder = part.order;
        block.add(mesh);
      }
      root.add(block);
    }
    const green = new THREE.MeshStandardMaterial({color:0x167a38,roughness:.8});
    const brown = new THREE.MeshStandardMaterial({color:0x684027,roughness:.8});
    const leafGeometry = new THREE.CylinderGeometry(.13,.13,.075,12);
    const baseGeometry = new THREE.CylinderGeometry(.085,.085,.055,12);
    const stemGeometry = new THREE.CylinderGeometry(.045,.045,.24,12);
    for (const part of metadata.tree_pieces || []) {
      const leaf = part.faces === 316;
      const mesh = new THREE.Mesh(leaf ? leafGeometry : part.faces === 160 ? baseGeometry : stemGeometry, leaf ? green : brown);
      mesh.position.set(part.center[0]*.01,part.center[2]*.01,-part.center[1]*.01);
      if (part.order === 5) mesh.rotation.z = Math.PI/2;
      mesh.userData.treeOrder = part.order;
      root.add(mesh);
    }
    for (const part of metadata.stair_pieces || []) {
      const material = part.transparent ? new THREE.MeshStandardMaterial({color:0xd9e3e8,transparent:true,opacity:.18,depthWrite:false,roughness:.72}) : white;
      const mesh = new THREE.Mesh(new THREE.BoxGeometry(part.size[0]*.01,part.size[2]*.01,part.size[1]*.01),material);
      mesh.position.set(part.center[0]*.01,part.center[2]*.01,-part.center[1]*.01);
      mesh.userData.stairOrder = part.order;
      root.add(mesh);
    }
    return root;
  }
  activate(root) {
    this.sequence++;
    if (this.active) this.active.visible = false;
    this.active = root;
    root.visible = true;
    this.blocks.clear();
    this.treePieces = [];
    this.stairPieces = [];
    this.buildingCourses = [];
    root.updateMatrixWorld(true);
    root.traverse((object) => {
      if (object.userData.block && moduleByBlock.has(object.userData.block)) {
        if (!object.userData.home) object.userData.home = object.position.clone();
        this.blocks.set(object.userData.block, object);
      }
      if (Number.isInteger(object.userData.treeOrder)) {
        if (!object.userData.treeHome) object.userData.treeHome = object.position.clone();
        this.treePieces.push(object);
      }
      if (Number.isInteger(object.userData.courseOrder)) {
        if (!object.userData.courseHome) object.userData.courseHome = object.position.clone();
        this.buildingCourses.push(object);
      }
      if (Number.isInteger(object.userData.stairOrder)) {
        if (!object.userData.stairHome) object.userData.stairHome = object.position.clone();
        this.stairPieces.push(object);
      }
    });
    if (!root.userData.markers) { this.addMarkers(root); root.userData.markers = true; }
    root.updateMatrixWorld(true);
    for (const block of this.blocks.values()) {
      if (!block.userData.pickBounds) {
        block.userData.pickBounds = new THREE.Box3();
        block.userData.localPickBounds = new THREE.Box3().setFromObject(block).applyMatrix4(block.matrixWorld.clone().invert()).expandByScalar(.4*(root===this.full?100:1));
      }
    }
    this.setMode(this.mode);
  }
  addMarkers(root) {
    for (const [number, block] of this.blocks) {
      if (!moduleByBlock.get(number).marker) continue;
      const scale = root === this.full ? 100 : 1;
      const box = new THREE.Box3().setFromObject(block);
      const location = box.getCenter(new THREE.Vector3());
      location.y = box.max.y + .015;
      root.worldToLocal(location);
      const marker = new THREE.Group();
      marker.userData.minifigBlock = number;
      const ink = new THREE.MeshStandardMaterial({ color: 0x344c5a, roughness: .7 });
      const yellow = new THREE.MeshStandardMaterial({ color: 0xf5bc34, roughness: .7 });
      const head = new THREE.Mesh(new THREE.CylinderGeometry(.035, .035, .065, 10), yellow);
      head.position.y = .155;
      const body = new THREE.Mesh(new THREE.BoxGeometry(.095, .09, .055), ink);
      body.position.y = .085;
      const legs = new THREE.Mesh(new THREE.BoxGeometry(.085, .055, .045), ink);
      legs.position.y = .025;
      marker.add(head, body, legs);
      marker.scale.setScalar(scale);
      const roof = this.buildingCourses.filter(piece=>piece.userData.courseBlock===number).sort((a,b)=>b.userData.courseOrder-a.userData.courseOrder)[0] || block;
      roof.worldToLocal(root.localToWorld(location));
      marker.position.copy(location);
      // Imported roof courses retain Blender's axes. Keep the figure world-up.
      roof.getWorldQuaternion(marker.quaternion).invert();
      roof.add(marker);
    }
  }
  setMode(mode) {
    this.mode = mode;
    this.highlight(null);
    this.setJourney(this.journeyProgress);
  }
  setJourney(progress) {
    this.journeyProgress = progress;
    if (!this.renderer) return;
    const sceneProgress = this.still ? (this.frozenProgress || 0) : progress;
    const sample = sampleFlight(sceneProgress);
    const modeAmount = (this.mode === 'house' ? .35 + .65 * sample.interior : 1)*sample.openingSpread;
    for (const [number, block] of this.blocks) {
      const scale = this.active === this.full ? 100 : 1;
      const home = block.userData.home;
      const finish = .74 + (number % 4)*.027;
      const rear = home.z < -.5*scale ? sample.rearSeparation : 0;
      const horizontal = Math.max(1-assemblyEase(sceneProgress,finish),rear)*modeAmount;
      const depth = Math.max(1-assemblyEase(sceneProgress,finish*.98),rear)*modeAmount;
      const height = Math.max(1-assemblyEase(sceneProgress,finish*1.015),rear)*modeAmount;
      block.position.copy(home);
      block.position.x += Math.sign(home.x || 1) * 1.1 * scale * horizontal;
      block.position.z += Math.sign(home.z || 1) * .9 * scale * depth;
      block.position.y += (.65 + (number % 4) * .42) * scale * height;
    }
    const scale = this.active === this.full ? 100 : 1;
    const treeProgress = sceneProgress;
    for (const piece of this.treePieces) {
      const order = piece.userData.treeOrder;
      const seat = treeSeats[order];
      const offset = seatingOffset(treeProgress,seat);
      piece.position.copy(piece.userData.treeHome);
      piece.position[seat.axis] += offset*scale;
      piece.userData.assembled = 1-offset/seat.gap;
    }
    for (const piece of this.stairPieces) {
      const order = piece.userData.stairOrder;
      const separation = 1-assemblyEase(treeProgress,.35+order*.008);
      piece.position.copy(piece.userData.stairHome);
      // Lift toward the stair's far side, leaving the low tree passage clear.
      piece.position.x -= (.08+order*.004)*scale*separation;
      piece.position.y += (.12+order*.007)*scale*separation;
      piece.position.z += (.06+order*.003)*scale*separation;
      piece.userData.assembled = 1-separation;
    }
    for (const piece of this.buildingCourses) {
      const order = piece.userData.courseOrder, number = piece.userData.courseBlock;
      const separation = (1-assemblyEase(sceneProgress,.4+order*.055+(number%3)*.01))*sample.courseSpread;
      const angle = number*2.4;
      piece.position.copy(piece.userData.courseHome);
      piece.position.x += Math.cos(angle)*(.04+order*.018)*scale*separation;
      piece.position.y += (.12+order*.08)*scale*separation;
      piece.position.z += Math.sin(angle)*(.04+order*.018)*scale*separation;
      piece.userData.assembled = 1-separation;
    }
    this.active?.updateMatrixWorld(true);
    for (const block of this.blocks.values()) block.userData.pickBounds.copy(block.userData.localPickBounds).applyMatrix4(block.matrixWorld);
    if (!this.still || !this.poseInitialized) {
      this.camera.fov = sample.fov;
      this.camera.position.copy(sample.position);
      if (this.camera.aspect<.72) {
        const openingDistance = 1+(.72/this.camera.aspect-1)*(1-assemblyEase(sceneProgress,.18));
        this.camera.position.sub(sample.target).multiplyScalar(openingDistance).add(sample.target);
      }
      this.controls.target.copy(sample.target);
      this.camera.lookAt(sample.target);
    }
    this.poseInitialized = true;
    this.applyFraming(sample.posterOffset);
    this.outline.visible = false;
    this.hoveredBlock = null;
    this.stage.style.cursor = 'grab';
    document.querySelector('#hover-label').style.display = 'none';
    this.render();
  }
  applyFraming(offset) {
    if (!this.renderer) return;
    const {width,height} = this.viewport || this.stage.getBoundingClientRect();
    const key = `${width}:${height}:${offset}:${this.camera.fov}:${this.camera.aspect}`;
    if (key === this.framingKey) return;
    this.framingKey = key;
    if (width < 740) this.camera.clearViewOffset();
    else this.camera.setViewOffset(width,height,-width*offset,0,width,height);
  }
  setStill(still) {
    if (still) this.frozenProgress = this.journeyProgress;
    this.still = still;
    if (!still) this.setJourney(this.journeyProgress);
  }
  toggleLite(lite) {
    if (!this.renderer || !this.proxy) { this.announce('3D unavailable. Use the page list.'); return; }
    this.restore();
    this.lite = lite;
    if (lite) this.activate(this.proxy);
    else if (this.full) this.activate(this.full);
    else this.loadFull();
    this.status.textContent = lite ? 'Lite house · simplified blocks, same destinations' : this.full ? 'Supplied LEGO model · 21 selectable blocks' : 'Loading the supplied brick model…';
  }
  resize() {
    if (!this.renderer) return;
    const { width, height } = this.stage.getBoundingClientRect();
    if (!width || !height) return;
    this.viewport = {width,height};
    this.renderer.setSize(width, height, false);
    this.camera.aspect = width / height;
    this.applyFraming(sampleFlight(this.still ? (this.frozenProgress || 0) : this.journeyProgress).posterOffset);
    this.render();
  }
  render() {
    if (!this.renderer || document.hidden) return;
    this.renderRequests++;
    if (this.pendingFrame) return;
    this.pendingFrame = requestAnimationFrame(() => {
      this.pendingFrame = null;
      if (document.hidden) return;
      const start = performance.now();
      this.renderer.render(this.scene, this.camera);
      this.lastRenderCpuMs = performance.now()-start;
      this.frames++;
    });
  }
  pick(event) {
    if (!this.renderer || !this.controls.enabled) return null;
    const bounds = this.renderer.domElement.getBoundingClientRect();
    this.pointer.set(((event.clientX - bounds.left) / bounds.width) * 2 - 1, -((event.clientY - bounds.top) / bounds.height) * 2 + 1);
    this.raycaster.setFromCamera(this.pointer, this.camera);
    const candidates = [...this.blocks.values()].filter(block=>this.raycaster.ray.intersectsBox(block.userData.pickBounds));
    this.pickStats = {candidates:candidates.length,total:this.blocks.size};
    const hits = this.raycaster.intersectObjects(candidates, true);
    for (const hit of hits) {
      let object = hit.object;
      while (object && !object.userData.block) object = object.parent;
      if (object && moduleByBlock.has(object.userData.block)) return object;
    }
    return null;
  }
  hover(event) {
    const block = this.pick(event);
    this.highlight(block?.userData.block);
    const label = document.querySelector('#hover-label');
    if (block) {
      const bounds = this.stage.getBoundingClientRect();
      label.style.left = `${Math.min(event.clientX - bounds.left + 14, bounds.width - 190)}px`;
      label.style.top = `${Math.min(event.clientY - bounds.top + 14, bounds.height - 55)}px`;
    }
  }
  highlight(number) {
    if (!this.renderer) return;
    if (this.hoveredBlock === (number || null)) return;
    this.hoveredBlock = number || null;
    const block = this.blocks.get(number);
    const label = document.querySelector('#hover-label');
    this.outline.visible = !!block;
    if (block) {
      this.outline.setFromObject(block);
      const item = moduleByBlock.get(number);
      label.textContent = `${item.code} · ${item.title}`;
      label.style.display = 'block';
    } else label.style.display = 'none';
    this.stage.style.cursor = block ? 'pointer' : 'grab';
    this.render();
  }
  async enter(number) {
    if (!this.renderer || !this.blocks.has(number) || this.mode === 'landscape') return;
    this.restore();
    this.returnView = { position: this.camera.position.clone(), target: this.controls.target.clone() };
    this.controls.enabled = false;
    this.selected = this.blocks.get(number);
    this.beforeLift = this.selected.position.clone();
    this.selected.position.y += this.active === this.full ? 24 : .24;
    this.selected.updateMatrixWorld(true);
    this.highlight(number);
    document.querySelector('#hover-label').style.display = 'none';
    const bounds = new THREE.Box3().setFromObject(this.selected);
    const target = bounds.getCenter(new THREE.Vector3());
    const direction = this.camera.position.clone().sub(this.controls.target).normalize();
    const distance = Math.max(1.8, bounds.getSize(new THREE.Vector3()).length() * 1.5);
    const position = target.clone().addScaledVector(direction, distance);
    await this.fly(position, target, this.motion && !matchMedia('(prefers-reduced-motion: reduce)').matches ? 750 : 0);
  }
  fly(position, target, duration) {
    const token = ++this.sequence;
    const startPosition = this.camera.position.clone();
    const startTarget = this.controls.target.clone();
    return new Promise((resolve) => {
      const start = performance.now();
      const frame = (time) => {
        if (token !== this.sequence) { resolve(); return; }
        const progress = duration ? Math.min(1, (time - start) / duration) : 1;
        const ease = progress * progress * (3 - 2 * progress);
        this.camera.position.lerpVectors(startPosition, position, ease);
        this.controls.target.lerpVectors(startTarget, target, ease);
        this.controls.update();
        this.render();
        if (progress < 1) requestAnimationFrame(frame); else resolve();
      };
      requestAnimationFrame(frame);
    });
  }
  restore() {
    this.sequence++;
    if (!this.renderer) return;
    if (this.selected && this.beforeLift) this.selected.position.copy(this.beforeLift);
    if (this.returnView) {
      this.camera.position.copy(this.returnView.position);
      this.controls.target.copy(this.returnView.target);
    }
    this.returnView = null;
    this.selected = null;
    if (this.full && !this.lite && this.active !== this.full) this.activate(this.full);
    this.controls.enabled = true;
    this.controls.update();
    this.highlight(null);
    this.render();
  }
  reset() {
    this.restore();
    if (!this.renderer) return;
    this.setJourney(this.journeyProgress);
    this.announce('House view reset.');
    this.render();
  }
  diagnostics() {
    const rect = this.stage.getBoundingClientRect();
    const minifigs = [];
    this.active?.traverse(object=>{
      if (object.userData.minifigBlock) minifigs.push({
        block:object.userData.minifigBlock,
        up:new THREE.Vector3(0,1,0).applyQuaternion(object.getWorldQuaternion(new THREE.Quaternion())).toArray(),
        feet:object.getWorldPosition(new THREE.Vector3()).toArray(),
        head:object.children[0].getWorldPosition(new THREE.Vector3()).toArray(),
      });
    });
    const points = [...this.blocks].map(([block, object]) => {
      const bounds = new THREE.Box3().setFromObject(object);
      const roof = bounds.getCenter(new THREE.Vector3());
      roof.y = bounds.max.y;
      roof.project(this.camera);
      return { block, x: rect.left + (roof.x + 1) * rect.width / 2, y: rect.top + (1 - roof.y) * rect.height / 2 };
    });
    return this.renderer ? { minifigs, mode: this.mode, journeyProgress: this.journeyProgress, still: this.still, lite: this.active === this.proxy, blocks: this.blocks.size, treePieces: this.treePieces.map(piece=>({order:piece.userData.treeOrder,assembled:piece.userData.assembled,position:piece.position.toArray(),home:piece.userData.treeHome.toArray()})), stairPieces:this.stairPieces.map(piece=>({order:piece.userData.stairOrder,assembled:piece.userData.assembled,position:piece.position.toArray(),home:piece.userData.stairHome.toArray()})), buildingCourses:this.buildingCourses.map(piece=>({block:piece.userData.courseBlock,order:piece.userData.courseOrder,assembled:piece.userData.assembled,position:piece.position.toArray(),home:piece.userData.courseHome.toArray()})), picking:this.pickStats, lastRenderCpuMs:this.lastRenderCpuMs, points, renderRequests:this.renderRequests, frames: this.frames, drawCalls: this.renderer.info.render.calls, triangles: this.renderer.info.render.triangles, pixelRatio: this.renderer.getPixelRatio(), modelReadyMs: this.modelReadyMs, camera: this.camera.position.toArray(), target: this.controls.target.toArray() } : { fallback: true };
  }
}
