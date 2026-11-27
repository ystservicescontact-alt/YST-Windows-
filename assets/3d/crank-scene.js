// Realistic 3D render: a white vinyl casement window with a crank operator whose gears are stripped.
// Fixed camera moves (no free orbit). Driven by update(t) from the explainer player.
import * as THREE from './three.module.min.js';
import { RoomEnvironment } from './RoomEnvironment.js';
import { RoundedBoxGeometry } from './RoundedBoxGeometry.js';

const V = (x, y, z) => new THREE.Vector3(x, y, z);
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const ramp = (t, a, b) => clamp((t - a) / (b - a), 0, 1);
const ease = x => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const lerp = (a, b, k) => a + (b - a) * k;
const DEG = Math.PI / 180;

function rbox(w, h, d, r, mat) {
  const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 3, Math.min(r, w / 2, h / 2, d / 2)), mat);
  m.castShadow = true; m.receiveShadow = true;
  return m;
}
// Four rounded bars forming a rectangle (outer w x h, bar b, depth d)
function rectFrame(w, h, b, d, r, mat) {
  const g = new THREE.Group();
  const top = rbox(w, b, d, r, mat); top.position.y = h / 2 - b / 2;
  const bot = rbox(w, b, d, r, mat); bot.position.y = -h / 2 + b / 2;
  const l = rbox(b, h - 2 * b + 0.002, d, r, mat); l.position.x = -w / 2 + b / 2;
  const rr = rbox(b, h - 2 * b + 0.002, d, r, mat); rr.position.x = w / 2 - b / 2;
  g.add(top, bot, l, rr);
  return g;
}

// ---------------------------------------------------------------- textures (painted in canvas)
function plasterTexture() {
  const c = document.createElement('canvas'); c.width = c.height = 512;
  const g = c.getContext('2d');
  g.fillStyle = '#e6ddcf'; g.fillRect(0, 0, 512, 512);
  const img = g.getImageData(0, 0, 512, 512), d = img.data;
  for (let i = 0; i < d.length; i += 4) { const n = (Math.random() - 0.5) * 10; d[i] += n; d[i + 1] += n; d[i + 2] += n; }
  g.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(4, 3);
  return t;
}

function softDot() {
  const c = document.createElement('canvas'); c.width = c.height = 64;
  const g = c.getContext('2d'), gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
  return new THREE.CanvasTexture(c);
}

// Spur gear outline (teeth listed in `worn` are ground down)
function gearGeometry(r, n, th, depth, worn) {
  const s = new THREE.Shape();
  for (let i = 0; i < n; i++) {
    const a = (i / n) * Math.PI * 2, da = (Math.PI * 2) / n;
    const h = worn && worn(i) ? th * (0.04 + 0.08 * ((i * 7) % 3) / 2) : th;
    const p = (rr, ang) => [Math.cos(ang) * rr, Math.sin(ang) * rr];
    const pts = [p(r, a), p(r, a + da * 0.22), p(r + h, a + da * 0.36), p(r + h, a + da * 0.64), p(r, a + da * 0.78)];
    pts.forEach(([x, y], k) => (i === 0 && k === 0 ? s.moveTo(x, y) : s.lineTo(x, y)));
  }
  s.closePath();
  const hole = new THREE.Path(); hole.absarc(0, 0, r * 0.28, 0, Math.PI * 2, true); s.holes.push(hole);
  const geo = new THREE.ExtrudeGeometry(s, { depth, bevelEnabled: true, bevelSize: 0.0004, bevelThickness: 0.0004, bevelSegments: 2, curveSegments: 24 });
  geo.translate(0, 0, -depth / 2); geo.rotateX(-Math.PI / 2);
  return geo;
}

class Helix extends THREE.Curve {
  constructor(r, len, turns) { super(); this.r = r; this.len = len; this.turns = turns; }
  getPoint(t, target = new THREE.Vector3()) {
    const a = t * this.turns * Math.PI * 2;
    return target.set(Math.cos(a) * this.r, Math.sin(a) * this.r, -this.len / 2 + this.len * t);
  }
}

export function createCrankScene(container, labelLayer, viewUrl) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  container.appendChild(renderer.domElement);
  renderer.domElement.setAttribute('aria-hidden', 'true');

  const scene = new THREE.Scene();
  scene.background = new THREE.Color('#d8cfc2');
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(renderer), 0.04).texture;

  const camera = new THREE.PerspectiveCamera(34, 16 / 10, 0.01, 40);

  // ---------------- materials
  const plaster = new THREE.MeshStandardMaterial({ map: plasterTexture(), roughness: 0.92, envMapIntensity: 0.25 });
  const trim = new THREE.MeshPhysicalMaterial({ color: '#f4f2ec', roughness: 0.42, clearcoat: 0.25, clearcoatRoughness: 0.5, envMapIntensity: 0.35 });
  const pvc = new THREE.MeshPhysicalMaterial({ color: '#f7f7f4', roughness: 0.3, clearcoat: 0.4, clearcoatRoughness: 0.35, envMapIntensity: 0.45 });
  const gasket = new THREE.MeshStandardMaterial({ color: '#1b1d20', roughness: 0.8 });
  const glass = new THREE.MeshPhysicalMaterial({ color: '#f2fbf8', metalness: 0, roughness: 0.02, transmission: 1, thickness: 0.006, ior: 1.52, envMapIntensity: 1.2, specularIntensity: 1 });
  const spacerMat = new THREE.MeshStandardMaterial({ color: '#5d6168', metalness: 0.7, roughness: 0.4 });
  const steel = new THREE.MeshStandardMaterial({ color: '#b8bdc4', metalness: 1, roughness: 0.28 });
  const zinc = new THREE.MeshStandardMaterial({ color: '#9ea4ab', metalness: 0.9, roughness: 0.38 });
  const brassNew = new THREE.MeshStandardMaterial({ color: '#d9ad55', metalness: 1, roughness: 0.25 });
  const brassOld = new THREE.MeshStandardMaterial({ color: '#8f6a35', metalness: 0.85, roughness: 0.62 });
  const handleMat = new THREE.MeshPhysicalMaterial({ color: '#f2f0ea', roughness: 0.38, clearcoat: 0.3 });
  const coverMat = new THREE.MeshPhysicalMaterial({ color: '#f5f4f0', roughness: 0.32, clearcoat: 0.35, transparent: true, opacity: 1 });

  // ---------------- wall with an opening
  const OW = 1.0, OH = 1.3, WT = 0.17; // rough opening and wall thickness
  const wall = new THREE.Group(); scene.add(wall);
  const WW = 5, WH = 3.4;
  const wbox = (w, h, x, y) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, WT), plaster); m.position.set(x, y, -WT / 2); m.receiveShadow = true; m.castShadow = true; wall.add(m); };
  wbox((WW - OW) / 2, WH, -(OW / 2 + (WW - OW) / 4), 0);
  wbox((WW - OW) / 2, WH, OW / 2 + (WW - OW) / 4, 0);
  wbox(OW, (WH - OH) / 2, 0, OH / 2 + (WH - OH) / 4);
  wbox(OW, (WH - OH) / 2, 0, -(OH / 2 + (WH - OH) / 4));
  // white jamb returns lining the opening
  const jd = 0.11;
  [[OW, 0.012, 0, OH / 2 - 0.006], [0.012, OH, -OW / 2 + 0.006, 0], [0.012, OH, OW / 2 - 0.006, 0]].forEach(([w, h, x, y]) => {
    const m = rbox(w, h, jd, 0.002, trim); m.position.set(x, y, -jd / 2); wall.add(m);
  });
  // casing around the opening
  const cw = 0.075, cz = 0.012;
  const casing = rectFrame(OW + 2 * cw, OH + cw, cw, cz, 0.004, trim);
  casing.position.set(0, cw / 2, cz / 2); wall.add(casing);
  // stool (inside sill) and apron
  const stool = rbox(OW + 0.24, 0.026, 0.17, 0.006, trim); stool.position.set(0, -OH / 2 - 0.013, -0.03); wall.add(stool);
  const apron = rbox(OW + 2 * cw, 0.08, 0.014, 0.003, trim); apron.position.set(0, -OH / 2 - 0.066, 0.007); wall.add(apron);

  // ---------------- window frame (sits in the opening)
  const FW = OW - 0.02, FH = OH - 0.02, fb = 0.065, fd = 0.075, fz = -0.105;
  const frame = rectFrame(FW, FH, fb, fd, 0.006, pvc); frame.position.set(0, 0, fz); scene.add(frame);

  // ---------------- sash (hinged on the left, opens outward)
  const SW = FW - 2 * fb - 0.004, SH = FH - 2 * fb - 0.004, sb = 0.058, sd = 0.055;
  const pivot = new THREE.Group(); pivot.position.set(-SW / 2, 0, fz - 0.012); scene.add(pivot);
  const sash = new THREE.Group(); sash.position.x = SW / 2; pivot.add(sash);
  sash.add(rectFrame(SW, SH, sb, sd, 0.006, pvc));
  const gk = rectFrame(SW - 2 * sb + 0.01, SH - 2 * sb + 0.01, 0.006, sd + 0.004, 0.001, gasket); sash.add(gk);
  const GW = SW - 2 * sb + 0.006, GH = SH - 2 * sb + 0.006;
  [-0.011, 0.011].forEach(z => { const p = new THREE.Mesh(new THREE.BoxGeometry(GW, GH, 0.004), glass); p.position.z = z; sash.add(p); });
  const sp = rectFrame(GW - 0.004, GH - 0.004, 0.01, 0.016, 0.001, spacerMat); sash.add(sp);

  // ---------------- operator on the frame sill
  const yb = -FH / 2 + fb; // top of the frame's bottom bar
  const O = V(0.2, yb + 0.019, fz + fd / 2 + 0.026);
  const opBase = rbox(0.13, 0.006, 0.07, 0.002, zinc); opBase.position.set(O.x, yb + 0.003, O.z); scene.add(opBase);
  const cover = rbox(0.13, 0.034, 0.07, 0.012, coverMat); cover.position.copy(O); scene.add(cover);
  // gears inside the housing
  const gearR = 0.017, gearC = V(O.x - 0.018, O.y - 0.002, O.z - 0.008);
  const oldGear = new THREE.Mesh(gearGeometry(gearR, 18, 0.0042, 0.006, i => i >= 14 || i <= 1), brassOld);
  const newGear = new THREE.Mesh(gearGeometry(gearR, 18, 0.0042, 0.006, null), brassNew);
  [oldGear, newGear].forEach(g => { g.position.copy(gearC); g.castShadow = true; scene.add(g); });
  newGear.visible = false;
  const hubPin = new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.004, 0.016, 20), steel); hubPin.position.copy(gearC); scene.add(hubPin);
  const worm = new THREE.Group(); worm.position.set(gearC.x + gearR + 0.0105, gearC.y, O.z); scene.add(worm);
  const wormCore = new THREE.Mesh(new THREE.CylinderGeometry(0.0046, 0.0046, 0.056, 24), steel); wormCore.rotation.x = Math.PI / 2; worm.add(wormCore);
  worm.add(new THREE.Mesh(new THREE.TubeGeometry(new Helix(0.0056, 0.044, 9), 360, 0.0014, 8, false), steel));
  // shaft through the front to the handle
  const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.003, 0.003, 0.05, 16), steel); shaft.rotation.x = Math.PI / 2; shaft.position.set(worm.position.x, worm.position.y, O.z + 0.045); scene.add(shaft);
  // folding T-handle on the front
  const handle = new THREE.Group(); handle.position.set(worm.position.x, worm.position.y, O.z + 0.068); scene.add(handle);
  const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.011, 0.012, 0.018, 28), handleMat); hub.rotation.x = Math.PI / 2; handle.add(hub);
  const lever = rbox(0.075, 0.014, 0.01, 0.004, handleMat); lever.position.set(0.034, 0, 0.006); handle.add(lever);
  const knob = new THREE.Mesh(new THREE.CylinderGeometry(0.0075, 0.0085, 0.032, 24), handleMat); knob.rotation.x = Math.PI / 2; knob.position.set(0.068, 0, 0.022); knob.castShadow = true; handle.add(knob);
  // arm from the gear to the sash
  const arm = rbox(1, 0.006, 0.014, 0.002, zinc); scene.add(arm);
  const armEnd = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.01, 20), zinc); scene.add(armEnd);

  // ---------------- outside: backdrop, sun
  // real photo of a Toronto backyard, seen through the glass
  const viewTex = new THREE.TextureLoader().load(viewUrl); viewTex.colorSpace = THREE.SRGBColorSpace;
  const back = new THREE.Mesh(new THREE.PlaneGeometry(1.9, 2.71), new THREE.MeshBasicMaterial({ map: viewTex }));
  back.material.color.setScalar(1.12);
  back.position.set(-0.08, 0.05, -1.25); scene.add(back);
  const sun = new THREE.DirectionalLight('#ffe9cc', 5.5);
  sun.position.set(-1.6, 2.6, -3.0); sun.target.position.set(0.1, -0.6, 0.05);
  sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -1.2, right: 1.2, top: 1.2, bottom: -1.2, near: 0.5, far: 8 });
  sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.015; sun.shadow.radius = 4;
  scene.add(sun, sun.target);
  scene.add(new THREE.HemisphereLight('#eef4ff', '#b9a892', 0.35));
  const fill = new THREE.DirectionalLight('#fff4e6', 0.4); fill.position.set(-2, 1.5, 3); scene.add(fill);
  const rim = new THREE.PointLight('#ffffff', 0, 0.6); rim.position.set(O.x + 0.05, O.y + 0.12, O.z + 0.12); scene.add(rim);

  // ---------------- cold air through the gap
  const N = 160;
  const airGeo = new THREE.BufferGeometry();
  const airPos = new Float32Array(N * 3); airGeo.setAttribute('position', new THREE.BufferAttribute(airPos, 3));
  const air = new THREE.Points(airGeo, new THREE.PointsMaterial({ map: softDot(), color: '#bfe0ff', size: 0.022, transparent: true, opacity: 0, depthWrite: false }));
  scene.add(air);
  const seeds = Array.from({ length: N }, (_, i) => ({ h: Math.random(), ph: Math.random(), sp: 0.5 + Math.random() * 0.6, dx: (Math.random() - 0.5) * 0.06 }));

  // ---------------- labels (HTML, projected)
  const labels = [];
  function label(text, cls) {
    const el = document.createElement('span'); el.className = 'ex-label ' + (cls || ''); el.textContent = text;
    labelLayer.appendChild(el); const l = { el, p: V(0, 0, 0), k: 0 }; labels.push(l); return l;
  }
  const lGap = label('Gap', 'is-red'), lAir = label('Cold air', 'is-blue'), lTeeth = label('Stripped teeth', 'is-red'), lNew = label('New gears', 'is-green'), lHandle = label('Handle turning', '');

  // ---------------- timeline
  function sashAngle(t) {
    if (t < 3.5) return lerp(30, 14, ease(ramp(t, 0, 3.5))) * DEG;
    if (t < 17.2) return (14 + (t > 3.5 && t < 7.5 ? Math.sin(t * 28) * 0.25 : 0)) * DEG;
    return lerp(14, 0, ease(ramp(t, 17.2, 20.6))) * DEG;
  }
  const turned = t => Math.min(t, 14.5) + Math.max(0, Math.min(t, 20.6) - 17.2);
  const CW = { p: V(0.55, -0.02, 3.15), q: V(0.06, -0.14, -0.1) };
  const CG = { p: V(1.05, -0.08, 1.95), q: V(0.36, -0.14, -0.12) };
  const CC = { p: V(O.x + 0.035, O.y + 0.2, O.z + 0.1), q: V(O.x - 0.006, O.y - 0.004, O.z - 0.008) };
  const keys = [[0, CW], [6.5, CW], [8.3, CG], [10.2, CG], [12, CC], [16.6, CC], [18.6, CW], [30, CW]];
  function camAt(t) {
    let i = 0; while (i < keys.length - 2 && t >= keys[i + 1][0]) i++;
    const [t0, a] = keys[i], [t1, b] = keys[i + 1];
    const k = ease(ramp(t, t0, t1));
    const drift = Math.sin(t * 0.25) * 0.02;
    return { p: a.p.clone().lerp(b.p, k).add(V(drift, 0, 0)), q: a.q.clone().lerp(b.q, k) };
  }

  const tmp = V(0, 0, 0), S = V(0, 0, 0), up = V(1, 0, 0);
  let w = 1, h = 1;
  function resize() {
    w = container.clientWidth; h = container.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(container); resize();

  function place(l, pos, k) {
    tmp.copy(pos).project(camera);
    const on = k > 0.02 && tmp.z < 1;
    l.el.style.opacity = on ? k : 0;
    if (on) l.el.style.transform = `translate(${((tmp.x * 0.5 + 0.5) * w).toFixed(1)}px, ${((-tmp.y * 0.5 + 0.5) * h).toFixed(1)}px)`;
  }

  return function update(t, time) {
    const th = sashAngle(t);
    pivot.rotation.y = th;
    // handle + worm turn together
    const ang = turned(t) * 5.5;
    handle.rotation.z = -ang; worm.rotation.z = -ang;
    // gear swap and rotation
    const fixed = t >= 14.9;
    oldGear.visible = !fixed; newGear.visible = fixed;
    newGear.rotation.y = -Math.max(0, Math.min(t, 20.6) - 17.2) * 0.9;
    // arm: gear centre to a point under the sash's bottom rail
    sash.localToWorld(S.set(SW * 0.32, -SH / 2 + 0.012, 0));
    const from = gearC.clone().add(V(0, 0.006, 0));
    const dir = S.clone().sub(from), len = dir.length();
    arm.scale.set(len, 1, 1); arm.position.copy(from).addScaledVector(dir, 0.5);
    arm.quaternion.setFromUnitVectors(up, dir.normalize());
    armEnd.position.copy(S);
    // cover comes off for the close-up, goes back on after
    const off = ramp(t, 11.2, 12.4) * (1 - ramp(t, 17, 18.2));
    cover.position.set(O.x + off * 0.2, O.y + off * 0.03, O.z - off * 0.03);
    cover.rotation.z = -off * 0.4;
    coverMat.opacity = 1 - off * 0.85; coverMat.depthWrite = off < 0.5;
    rim.intensity = off * 0.25;
    // cold air
    const airK = ramp(t, 7.5, 8.3) * (1 - ramp(t, 16.5, 17.5));
    air.material.opacity = airK * 0.55;
    sash.localToWorld(tmp.set(SW / 2, 0, 0));
    const gx = (tmp.x + FW / 2 - fb) / 2, gz = tmp.z;
    for (let i = 0; i < N; i++) {
      const s = seeds[i], life = (time * 0.35 * s.sp + s.ph) % 1;
      airPos[i * 3] = gx + s.dx + life * 0.25;
      airPos[i * 3 + 1] = -SH / 2 + 0.08 + s.h * (SH - 0.2) - life * 0.25;
      airPos[i * 3 + 2] = gz + life * 0.9;
    }
    airGeo.attributes.position.needsUpdate = true;
    // camera
    const c = camAt(t); camera.position.copy(c.p); camera.lookAt(c.q);
    renderer.render(scene, camera);
    // labels
    place(lGap, V(gx, 0.15, gz + 0.02), ramp(t, 4.2, 4.8) * (1 - ramp(t, 10.5, 11)));
    place(lAir, V(gx + 0.12, -0.2, gz + 0.45), airK * (1 - ramp(t, 10.5, 11)));
    place(lHandle, handle.position.clone().add(V(0.05, -0.03, 0.02)), ramp(t, 3.6, 4.2) * (1 - ramp(t, 7.5, 8)));
    place(lTeeth, gearC.clone().add(V(0.012, 0.004, 0.014)), ramp(t, 12.4, 13) * (1 - ramp(t, 14.6, 14.9)));
    place(lNew, gearC.clone().add(V(0.012, 0.004, 0.014)), ramp(t, 15, 15.5) * (1 - ramp(t, 16.8, 17.3)));
  };
}
