// Player for realistic 3D explainers: loads the scene only when it comes near the screen,
// then drives it on the same caption timeline as the 2D explainers.
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const LOADERS = {
  crank3d: () => import('./3d/crank-scene.js').then(m => m.createCrankScene),
};

function webglOK() {
  try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) { return false; }
}

async function setup(root) {
  const load = LOADERS[root.dataset.scene];
  if (!load || !webglOK()) { root.classList.add('ex-failed'); return; }
  const create = await load();
  const stage = root.querySelector('.ex-canvas');
  const update = create(stage, root.querySelector('.ex-labels'), root.dataset.view);
  const steps = [...root.querySelectorAll('.ex-steps li')];
  const starts = steps.map(li => parseFloat(li.dataset.start));
  const dur = parseFloat(root.dataset.duration);
  const cap = root.querySelector('.ex-caption');
  const btn = root.querySelector('.ex-play');
  let t = reduce ? starts[3] + 2 : 0, playing = !reduce, visible = true, last = performance.now() / 1000, active = -1;
  const stepAt = x => starts.reduce((i, s, k) => (x >= s ? k : i), 0);
  function render(time) {
    update(t, time);
    const i = stepAt(t);
    if (i !== active) {
      active = i;
      steps.forEach((li, k) => { li.classList.toggle('on', k === i); li.classList.toggle('done', k < i); });
      cap.textContent = steps[i].querySelector('.ex-text').textContent;
      cap.classList.remove('in'); void cap.offsetWidth; cap.classList.add('in');
    }
    root.style.setProperty('--ex-progress', (t / dur).toFixed(4));
  }
  function setPlaying(p) { playing = p; btn.setAttribute('aria-pressed', String(p)); btn.querySelector('span').textContent = p ? 'Pause' : 'Play'; }
  setPlaying(playing);
  btn.addEventListener('click', () => { if (!playing && t >= dur) t = 0; setPlaying(!playing); });
  steps.forEach((li, k) => {
    li.tabIndex = 0;
    const go = () => { t = starts[k] + 0.01; render(performance.now() / 1000); };
    li.addEventListener('click', go);
    li.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
  });
  new IntersectionObserver(es => { visible = es[0].isIntersecting; }, { threshold: 0.15 }).observe(root);
  function frame(now) {
    requestAnimationFrame(frame);
    const time = now / 1000, dt = Math.min(time - last, 0.1); last = time;
    if (!visible) return;
    if (playing) { t += dt; if (t > dur + 2) t = 0; }
    render(time);
  }
  root.exSeek = x => { t = x; setPlaying(false); render(performance.now() / 1000); };
  render(last);
  requestAnimationFrame(frame);
  root.classList.add('ready');
}

document.querySelectorAll('.explainer[data-render="3d"]').forEach(root => {
  const io = new IntersectionObserver(es => {
    if (!es[0].isIntersecting) return;
    io.disconnect();
    setup(root).catch(() => root.classList.add('ex-failed'));
  }, { rootMargin: '400px' });
  io.observe(root);
});
