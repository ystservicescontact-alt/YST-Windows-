// Interactive 3D models for /see-inside-your-window/.
// 1) A casement window with a sealed double-pane glass unit: take it apart, show fog, show what we replace.
// 2) A sliding patio door: slide it, switch worn/new rollers, X-ray the bottom rail.
import * as THREE from './three.module.min.js';
import { OrbitControls } from './OrbitControls.js';

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const COL = {
  pvc: 0xf4f6f8, pvcDark: 0xdfe4ea, glass: 0xbfe3f2, metal: 0x9aa5b4, seal: 0x1d2330,
  red: 0xe5262e, navy: 0x0f1b33, wheel: 0x2b3442, worn: 0x7a5a3a, track: 0xb9c2cd, wall: 0xe9edf2,
};

function webglOK() {
  try {
    const c = document.createElement('canvas');
    return !!(window.WebGLRenderingContext && (c.getContext('webgl2') || c.getContext('webgl')));
  } catch (e) { return false; }
}

function std(color, extra = {}) {
  return new THREE.MeshStandardMaterial({ color, roughness: 0.55, metalness: 0.05, ...extra });
}
function glassMat() {
  return new THREE.MeshStandardMaterial({ color: COL.glass, roughness: 0.05, metalness: 0.1, transparent: true, opacity: 0.28, depthWrite: false, side: THREE.DoubleSide });
}
function box(w, h, d, mat) { return new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat); }

// Four bars forming a rectangle (outer size w x h, bar width b, depth d)
function rectFrame(w, h, b, d, mat) {
  const g = new THREE.Group();
  const top = box(w, b, d, mat); top.position.y = h / 2 - b / 2;
  const bot = box(w, b, d, mat); bot.position.y = -h / 2 + b / 2;
  const l = box(b, h - 2 * b, d, mat); l.position.x = -w / 2 + b / 2;
  const r = box(b, h - 2 * b, d, mat); r.position.x = w / 2 - b / 2;
  g.add(top, bot, l, r);
  return g;
}

function anchor(parent, x, y, z) {
  const o = new THREE.Object3D(); o.position.set(x, y, z); parent.add(o); return o;
}

// Shared viewer: renderer, camera, controls, labels, render-on-demand while visible
function makeViewer(stage, { camPos, target, minDist, maxDist }) {
  const canvasWrap = stage.querySelector('.v3d-canvas');
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  canvasWrap.appendChild(renderer.domElement);
  renderer.domElement.setAttribute('aria-hidden', 'true');

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(35, 1, 0.05, 50);
  camera.position.copy(camPos);
  scene.add(new THREE.HemisphereLight(0xffffff, 0xc9d3e0, 1.6));
  const sun = new THREE.DirectionalLight(0xffffff, 1.6); sun.position.set(2, 4, 3); scene.add(sun);
  const fill = new THREE.DirectionalLight(0xdfe8ff, 0.6); fill.position.set(-3, 1, -2); scene.add(fill);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.target.copy(target);
  controls.enableDamping = true;
  controls.enablePan = false;
  controls.minDistance = minDist; controls.maxDistance = maxDist;
  controls.maxPolarAngle = Math.PI * 0.62;
  controls.update();

  const labels = [];
  const labelLayer = stage.querySelector('.v3d-labels');
  function addLabel(obj, text, cls = '') {
    const el = document.createElement('span');
    el.className = 'v3d-label ' + cls;
    el.textContent = text;
    labelLayer.appendChild(el);
    const l = { obj, el, show: false };
    labels.push(l);
    return l;
  }

  const tickers = [];
  let visible = true, last = performance.now();
  const v = new THREE.Vector3();

  function resize() {
    const w = canvasWrap.clientWidth, h = canvasWrap.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(canvasWrap);
  resize();

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(es => { visible = es[0].isIntersecting; }, { rootMargin: '100px' }).observe(stage);
  }

  function frame(now) {
    requestAnimationFrame(frame);
    if (!visible) { last = now; return; }
    const dt = Math.min((now - last) / 1000, 0.05); last = now;
    tickers.forEach(f => f(dt, now / 1000));
    controls.update();
    renderer.render(scene, camera);
    const w = canvasWrap.clientWidth, h = canvasWrap.clientHeight;
    for (const l of labels) {
      l.obj.getWorldPosition(v); v.project(camera);
      const on = l.show && v.z < 1;
      l.el.classList.toggle('on', on);
      if (on) {
        const x = (v.x * 0.5 + 0.5) * w, y = (-v.y * 0.5 + 0.5) * h;
        const flip = x + l.el.offsetWidth + 12 > w;
        l.el.classList.toggle('flip', flip);
        l.el.style.transform = `translate(${x}px, ${y}px)` + (flip ? ' translateX(-100%)' : '');
      }
    }
  }
  requestAnimationFrame(frame);

  // Smoothly move the camera to a new spot
  let camGoal = null;
  tickers.push(dt => {
    if (!camGoal) return;
    const k = reduceMotion ? 1 : 1 - Math.pow(0.002, dt);
    camera.position.lerp(camGoal.pos, k);
    controls.target.lerp(camGoal.target, k);
    if (camera.position.distanceTo(camGoal.pos) < 0.005) camGoal = null;
  });
  function flyTo(pos, tgt) { camGoal = { pos: pos.clone(), target: tgt.clone() }; }
  controls.addEventListener('start', () => { camGoal = null; });

  return { scene, camera, controls, addLabel, tickers, flyTo };
}

function damp(cur, goal, dt, speed = 0.0015) {
  if (reduceMotion) return goal;
  return cur + (goal - cur) * (1 - Math.pow(speed, dt));
}

function setOpacity(m, o) {
  const tr = o < 0.99;
  if (m.transparent !== tr) { m.transparent = tr; m.depthWrite = !tr; m.needsUpdate = true; }
  m.opacity = o;
}

function setPressed(btn, on) { btn.setAttribute('aria-pressed', on ? 'true' : 'false'); }

// ---------------------------------------------------------------- 1. Window
function fogTexture() {
  const c = document.createElement('canvas'); c.width = 256; c.height = 384;
  const g = c.getContext('2d');
  const grad = g.createLinearGradient(0, 0, 0, 384);
  grad.addColorStop(0, 'rgba(255,255,255,0.25)');
  grad.addColorStop(0.6, 'rgba(255,255,255,0.55)');
  grad.addColorStop(1, 'rgba(250,252,255,0.85)');
  g.fillStyle = grad; g.fillRect(0, 0, 256, 384);
  let seed = 7;
  const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  for (let i = 0; i < 900; i++) {
    const x = rnd() * 256, y = Math.pow(rnd(), 0.6) * 384, r = 0.8 + rnd() * 2.6;
    g.fillStyle = `rgba(255,255,255,${0.4 + rnd() * 0.5})`;
    g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill();
  }
  // a few drips running down
  g.strokeStyle = 'rgba(200,215,230,0.6)'; g.lineWidth = 2;
  for (let i = 0; i < 14; i++) {
    const x = rnd() * 256, y = 200 + rnd() * 120;
    g.beginPath(); g.moveTo(x, y); g.lineTo(x + rnd() * 3 - 1.5, y + 30 + rnd() * 40); g.stroke();
  }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

function initWindow(stage) {
  const V = makeViewer(stage, {
    camPos: new THREE.Vector3(1.7, 0.55, 2.7), target: new THREE.Vector3(0, 0, 0.1), minDist: 1.4, maxDist: 6,
  });
  const root = new THREE.Group(); V.scene.add(root);

  const W = 1.0, H = 1.4, t = 0.07, d = 0.12;
  const pvc = std(COL.pvc), pvcDark = std(COL.pvcDark);
  const fadeable = [pvc, pvcDark];

  // Frame (fixed in the wall) + crank operator on the inside sill
  const frame = new THREE.Group(); root.add(frame);
  frame.add(rectFrame(W, H, t, d, pvc));
  const crank = new THREE.Group(); frame.add(crank);
  const metal = std(COL.metal, { metalness: 0.6, roughness: 0.35 });
  const housing = box(0.16, 0.035, 0.05, metal); housing.position.set(0.18, -H / 2 + t + 0.017, d / 2 - 0.02); crank.add(housing);
  const arm = box(0.12, 0.012, 0.012, std(COL.navy)); arm.position.set(0.26, -H / 2 + t + 0.03, d / 2 + 0.02); arm.rotation.z = 0.35; crank.add(arm);
  const knob = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.05, 16), std(COL.navy));
  knob.rotation.x = Math.PI / 2; knob.position.set(0.31, -H / 2 + t + 0.05, d / 2 + 0.045); crank.add(knob);

  // Sash (the part that opens), with a dark weatherstrip
  const sash = new THREE.Group(); root.add(sash);
  const SW = W - 2 * t - 0.01, SH = H - 2 * t - 0.01, st = 0.065;
  sash.add(rectFrame(SW, SH, st, 0.07, pvcDark));
  const strip = rectFrame(SW - 0.02, SH - 0.02, 0.01, 0.075, std(COL.seal)); sash.add(strip);

  // Sealed glass unit: inside pane, spacer + seal, outside pane
  const GW = SW - 2 * st + 0.05, GH = SH - 2 * st + 0.05, gap = 0.022, pt = 0.006;
  const glassA = glassMat(), glassB = glassMat();
  const paneOut = box(GW, GH, pt, glassA); root.add(paneOut);
  const paneIn = box(GW, GH, pt, glassB); root.add(paneIn);
  const spacer = new THREE.Group(); root.add(spacer);
  const spacerMat = std(COL.metal, { metalness: 0.7, roughness: 0.3 });
  const sealMat = std(COL.seal);
  spacer.add(rectFrame(GW - 0.024, GH - 0.024, 0.012, gap - 0.002, spacerMat));
  spacer.add(rectFrame(GW, GH, 0.012, gap, sealMat));
  const fogMat = new THREE.MeshBasicMaterial({ map: fogTexture(), transparent: true, opacity: 0, depthWrite: false, side: THREE.DoubleSide });
  const fog = new THREE.Mesh(new THREE.PlaneGeometry(GW - 0.05, GH - 0.05), fogMat); spacer.add(fog);

  // The wall around the window, for scale
  const wallMat = std(COL.wall, { transparent: true, opacity: 1 });
  const wall = new THREE.Group(); frame.add(wall);
  const ww = 2.6, wh = 2.4, wd = 0.16;
  const wl = box((ww - W) / 2, wh, wd, wallMat); wl.position.x = -(W / 2 + (ww - W) / 4); wall.add(wl);
  const wr = wl.clone(); wr.position.x = -wl.position.x; wall.add(wr);
  const wt = box(W, (wh - H) / 2, wd, wallMat); wt.position.y = H / 2 + (wh - H) / 4; wall.add(wt);
  const wb = wt.clone(); wb.position.y = -wt.position.y; wall.add(wb);
  wall.position.z = -0.03;

  // Positions: assembled vs taken apart (z toward the room)
  const parts = [
    { o: frame, a: 0, e: -0.55 },
    { o: sash, a: 0.015, e: -0.2 },
    { o: paneOut, a: 0.015 - gap / 2 - pt / 2, e: 0.12 },
    { o: spacer, a: 0.015, e: 0.42 },
    { o: paneIn, a: 0.015 + gap / 2 + pt / 2, e: 0.72 },
  ];
  parts.forEach(p => { p.o.position.z = p.a; p.cur = p.a; });

  const L = [
    V.addLabel(anchor(frame, -W / 2 + 0.03, H / 2 - 0.03, d / 2), 'Frame (stays)'),
    V.addLabel(anchor(sash, -SW / 2 + 0.03, -SH / 2 + 0.2, 0.04), 'Sash (stays)'),
    V.addLabel(anchor(paneOut, GW / 2 - 0.05, GH / 2 - 0.08, 0), 'Outside pane', 'is-unit'),
    V.addLabel(anchor(spacer, GW / 2 - 0.01, 0, 0), 'Spacer + edge seal', 'is-unit'),
    V.addLabel(anchor(paneIn, GW / 2 - 0.05, -GH / 2 + 0.12, 0), 'Inside pane', 'is-unit'),
    V.addLabel(anchor(crank, 0.31, -H / 2 + t + 0.05, d / 2 + 0.07), 'Crank (stays)'),
  ];
  const fogLabel = V.addLabel(anchor(spacer, -0.12, -0.25, 0.02), 'Moisture trapped between the panes', 'is-warn');

  const state = { apart: false, fog: false, unit: false };
  const ctl = stage.closest('.v3d');
  const bApart = ctl.querySelector('[data-act="apart"]');
  const bFog = ctl.querySelector('[data-act="fog"]');
  const bUnit = ctl.querySelector('[data-act="unit"]');
  const bReset = ctl.querySelector('[data-act="reset"]');
  const note = ctl.querySelector('.v3d-note');
  const NOTES = {
    base: 'Drag to turn the window. Pinch or scroll to zoom.',
    apart: 'A double-pane window is a sealed glass unit (two panes, a spacer and an edge seal) set into a sash and frame.',
    fog: 'When the edge seal fails, damp air gets between the panes and condenses. You can’t wipe it away because it’s inside the unit.',
    unit: 'We replace only the sealed glass unit (in colour). The frame, sash, crank and your trim stay where they are.',
  };
  function refresh() {
    setPressed(bApart, state.apart); bApart.textContent = state.apart ? 'Put it back together' : 'Take it apart';
    setPressed(bFog, state.fog); setPressed(bUnit, state.unit);
    L.forEach(l => { l.show = state.apart; });
    fogLabel.show = state.fog && !state.apart;
    note.textContent = state.unit ? NOTES.unit : state.fog ? NOTES.fog : state.apart ? NOTES.apart : NOTES.base;
  }
  const views = {
    home: [new THREE.Vector3(1.7, 0.55, 2.7), new THREE.Vector3(0, 0, 0.1)],
    apart: [new THREE.Vector3(2.9, 0.7, 1.9), new THREE.Vector3(0, 0, 0.1)],
  };
  bApart.addEventListener('click', () => { state.apart = !state.apart; refresh(); V.flyTo(...(state.apart ? views.apart : views.home)); });
  bFog.addEventListener('click', () => { state.fog = !state.fog; refresh(); });
  bUnit.addEventListener('click', () => {
    state.unit = !state.unit;
    if (state.unit && !state.apart) { state.apart = true; V.flyTo(...views.apart); }
    refresh();
  });
  bReset.addEventListener('click', () => {
    Object.assign(state, { apart: false, fog: false, unit: false }); refresh();
    V.flyTo(...views.home);
  });
  refresh();

  const unitGlow = new THREE.Color(COL.red);
  let fogCur = 0, fade = 1, glow = 0;
  V.tickers.push((dt, time) => {
    parts.forEach(p => { p.cur = damp(p.cur, state.apart ? p.e : p.a, dt); p.o.position.z = p.cur; });
    fogCur = damp(fogCur, state.fog ? 0.95 : 0, dt, 0.02);
    fogMat.opacity = fogCur;
    fade = damp(fade, state.unit ? 0.25 : 1, dt, 0.01);
    fadeable.forEach(m => setOpacity(m, fade));
    setOpacity(wallMat, fade);
    glow = damp(glow, state.unit ? 1 : 0, dt, 0.01);
    const pulse = reduceMotion ? 1 : 0.75 + 0.25 * Math.sin(time * 3);
    [sealMat, spacerMat].forEach(m => m.emissive.copy(unitGlow).multiplyScalar(glow * 0.5 * pulse));
    [glassA, glassB].forEach(m => { m.emissive.copy(unitGlow).multiplyScalar(glow * 0.35 * pulse); m.opacity = 0.28 + glow * 0.17; });
  });
}

// ---------------------------------------------------------------- 2. Patio door
function initDoor(stage) {
  const home = { pos: new THREE.Vector3(1.4, 0.7, 4.6), target: new THREE.Vector3(0, -0.05, 0) };
  const V = makeViewer(stage, { camPos: home.pos, target: home.target, minDist: 0.5, maxDist: 8 });
  const root = new THREE.Group(); V.scene.add(root);

  const DW = 2.4, DH = 2.1, t = 0.08, d = 0.16;
  const pvc = std(COL.pvc), panelMat = std(COL.pvcDark);
  root.add(rectFrame(DW, DH, t, d, pvc));

  // Sill with two tracks: the sliding panel runs on the inside track (+z)
  const sillTop = -DH / 2 + t;
  const zIn = 0.04, zOut = -0.04;
  const trackMat = std(COL.track, { metalness: 0.5, roughness: 0.35 });
  const railH = 0.008;
  [zIn, zOut].forEach(z => { const r = box(DW - 2 * t, railH, 0.008, trackMat); r.position.set(0, sillTop + railH / 2, z); root.add(r); });

  const openW = DW - 2 * t, PW = openW / 2 + 0.05, PH = DH - 2 * t - 0.04, pb = 0.075, pd = 0.05;
  const wheelR = 0.024;
  const panelBottomNew = sillTop + railH + 0.012; // panel rides just above the track

  function panel(z) {
    const g = new THREE.Group();
    g.add(rectFrame(PW, PH, pb, pd, panelMat));
    const gl = box(PW - 2 * pb + 0.02, PH - 2 * pb + 0.02, 0.012, glassMat()); g.add(gl);
    g.position.z = z;
    return g;
  }
  const fixed = panel(zOut); fixed.position.set(openW / 4 - 0.025, panelBottomNew + PH / 2, zOut); root.add(fixed);
  const slider = panel(zIn); root.add(slider);
  const closedX = -openW / 4 + 0.025, openX = closedX + openW / 2 - 0.12;

  // Handle on the sliding panel
  const handle = box(0.025, 0.28, 0.03, std(COL.navy)); handle.position.set(PW / 2 - pb / 2, 0, pd / 2 + 0.02); slider.add(handle);

  // Rollers inside the bottom rail of the sliding panel
  const wheelNew = std(COL.wheel, { roughness: 0.3, metalness: 0.2 });
  const wheelWorn = std(COL.worn, { roughness: 0.95 });
  const housingMat = std(COL.metal, { metalness: 0.6, roughness: 0.35 });
  const wheels = [];
  [-1, 1].forEach(side => {
    const g = new THREE.Group();
    g.position.set(side * (PW / 2 - 0.16), -PH / 2 + wheelR - 0.012 + 0.004, 0);
    const hs = box(0.11, 0.05, pd - 0.012, housingMat); hs.position.y = 0.012; g.add(hs);
    const geo = new THREE.CylinderGeometry(wheelR, wheelR, 0.016, 28); geo.rotateX(Math.PI / 2);
    const w = new THREE.Mesh(geo, wheelNew); g.add(w);
    // a mark so you can see the wheel turn
    const dot = box(0.004, wheelR * 0.9, 0.018, std(0xffffff)); dot.position.y = wheelR * 0.45; w.add(dot);
    slider.add(g);
    wheels.push({ g, w });
  });

  const lb = [
    V.addLabel(anchor(slider, -PW / 2 + 0.16, -PH / 2 + 0.07, pd / 2), 'Roller'),
    V.addLabel(anchor(slider, PW / 2 - 0.16, -PH / 2 + 0.07, pd / 2), 'Roller'),
    V.addLabel(anchor(root, -0.6, sillTop + 0.01, zIn + 0.02), 'Track'),
    V.addLabel(anchor(slider, 0, PH / 2 - 0.25, pd / 2), 'Sliding panel'),
    V.addLabel(anchor(fixed, 0.1, PH / 2 - 0.65, 0), 'Fixed panel'),
    V.addLabel(anchor(slider, PW / 2 - pb / 2, 0.18, pd / 2 + 0.04), 'Handle + lock'),
  ];
  lb.forEach(l => { l.show = true; });
  const grind = V.addLabel(anchor(slider, -0.1, -PH / 2 - 0.09, pd / 2), 'Bottom rail dragging on the track', 'is-warn');

  const ctl = stage.closest('.v3d');
  const range = ctl.querySelector('[data-act="slide"]');
  const bWorn = ctl.querySelector('[data-act="worn"]');
  const bNew = ctl.querySelector('[data-act="new"]');
  const bXray = ctl.querySelector('[data-act="xray"]');
  const bPlay = ctl.querySelector('[data-act="play"]');
  const bReset = ctl.querySelector('[data-act="reset"]');
  const note = ctl.querySelector('.v3d-note');
  const state = { worn: true, xray: false, goal: 0, auto: false };
  const NOTES = {
    worn: 'Worn rollers: the wheels are flat and seized, so the panel drops and grinds along the track. It sticks, jumps and wears the track out.',
    nw: 'New rollers: the panel sits back up on the wheels and glides with one finger. Most hard-to-open patio doors only need this.',
  };
  function refresh() {
    setPressed(bWorn, state.worn); setPressed(bNew, !state.worn); setPressed(bXray, state.xray);
    note.textContent = state.worn ? NOTES.worn : NOTES.nw;
    wheels.forEach(({ w }) => { w.material = state.worn ? wheelWorn : wheelNew; w.scale.y = state.worn ? 0.62 : 1; });
  }
  range.addEventListener('input', () => { state.goal = range.value / 100; state.auto = false; });
  bWorn.addEventListener('click', () => { state.worn = true; refresh(); });
  bNew.addEventListener('click', () => { state.worn = false; refresh(); });
  bXray.addEventListener('click', () => {
    state.xray = !state.xray; refresh();
    const rx = slider.position.x - (PW / 2 - 0.16);
    if (state.xray) V.flyTo(new THREE.Vector3(rx + 0.35, sillTop + 0.32, 0.95), new THREE.Vector3(rx + 0.1, sillTop + 0.03, 0));
    else V.flyTo(home.pos, home.target);
  });
  bPlay.addEventListener('click', () => { state.auto = true; state.goal = state.goal > 0.5 ? 0 : 1; });
  bReset.addEventListener('click', () => {
    Object.assign(state, { worn: true, xray: false, goal: 0, auto: false }); range.value = 0; refresh();
    V.flyTo(home.pos, home.target);
  });
  refresh();

  let pos = 0, drop = 0, xr = 0, lastX = closedX;
  V.tickers.push((dt, time) => {
    // Worn rollers: slow, jerky travel. New rollers: smooth.
    const speed = state.worn ? 0.35 : 0.004;
    pos = damp(pos, state.goal, dt, speed);
    let x = closedX + (openX - closedX) * pos;
    const moving = Math.abs(state.goal - pos) > 0.004;
    if (state.worn && moving && !reduceMotion) x += Math.sin(time * 40) * 0.004;
    drop = damp(drop, state.worn ? 0.012 : 0, dt, 0.01);
    slider.position.set(x, panelBottomNew + PH / 2 - drop + (state.worn && moving && !reduceMotion ? Math.abs(Math.sin(time * 33)) * 0.003 : 0), zIn);
    if (state.auto) range.value = Math.round(pos * 100);
    // New wheels roll; worn ones are seized
    const dx = x - lastX; lastX = x;
    if (!state.worn) wheels.forEach(({ w }) => { w.rotation.z -= dx / wheelR; });
    grind.show = state.worn && moving;
    xr = damp(xr, state.xray ? 1 : 0, dt, 0.01);
    setOpacity(panelMat, 1 - xr * 0.8);
    setOpacity(housingMat, 1 - xr * 0.7);
    const glowC = new THREE.Color(COL.red).multiplyScalar(xr * 0.6);
    wheelNew.emissive.copy(glowC); wheelWorn.emissive.copy(glowC);
  });
}

// ---------------------------------------------------------------- boot
document.querySelectorAll('.v3d').forEach(v => {
  const stage = v.querySelector('.v3d-stage');
  if (!webglOK()) { v.classList.add('no-webgl'); return; }
  try {
    if (v.dataset.model === 'window') initWindow(stage);
    if (v.dataset.model === 'door') initDoor(stage);
    v.classList.add('ready');
  } catch (e) {
    v.classList.add('no-webgl');
  }
});
