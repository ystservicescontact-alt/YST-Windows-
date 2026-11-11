// Lead tracking: sends Google Analytics events for calls, texts and quote forms.
// Works only when GA4 is enabled in build.py (SITE["ga4"]); otherwise does nothing.
(function () {
  function track(name, params) {
    if (typeof window.gtag === 'function') window.gtag('event', name, params || {});
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href');
    var where = a.getAttribute('data-where') || 'link';
    if (href.indexOf('tel:') === 0) track('phone_call_click', { where: where, page: location.pathname });
    else if (href.indexOf('sms:') === 0) track('text_click', { where: where, page: location.pathname });
    else if (href.indexOf('https://wa.me/') === 0) track('whatsapp_click', { where: where, page: location.pathname });
  });
  document.querySelectorAll('form[data-netlify]').forEach(function (f) {
    f.addEventListener('submit', function () {
      var p = f.querySelector('input[name="problem"]:checked, select[name="problem"]');
      track('generate_lead', { form: f.getAttribute('data-where') || 'form', problem: p ? p.value : '', page: location.pathname });
    });
  });
})();

// Close the mobile menu when tapping outside it or pressing Escape.
(function () {
  var menu = document.querySelector('.mnav');
  if (!menu) return;
  document.addEventListener('click', function (e) { if (menu.open && !menu.contains(e.target)) menu.open = false; });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && menu.open) { menu.open = false; menu.querySelector('summary').focus(); } });
})();

// Window style cards: tap to open/close; on phones, each card opens once as it scrolls into view.
(function () {
  var cards = document.querySelectorAll('.wstyle');
  if (!cards.length) return;
  cards.forEach(function (c) {
    c.addEventListener('click', function () { c.classList.toggle('open'); });
    c.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); c.classList.toggle('open'); } });
  });
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var touch = window.matchMedia && window.matchMedia('(hover: none)').matches;
  if (still || !touch || !('IntersectionObserver' in window)) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      var c = en.target; io.unobserve(c);
      setTimeout(function () { c.classList.add('open'); }, 300);
      setTimeout(function () { c.classList.remove('open'); }, 2100);
    });
  }, { threshold: 0.6 });
  cards.forEach(function (c) { io.observe(c); });
})();

// Price estimator on the cost guide: size band from width x height, plus glass options and quantity.
(function () {
  var box = document.querySelector('.calc[data-cost]');
  if (!box) return;
  var d = JSON.parse(box.getAttribute('data-cost'));
  var out = box.querySelector('[data-out]'), note = box.querySelector('[data-note]');
  function fmt(n) { n = Math.round(n / 5) * 5; return '$' + n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function calc() {
    var w = parseFloat(box.querySelector('[name=w]').value), h = parseFloat(box.querySelector('[name=h]').value);
    var q = Math.max(1, parseInt(box.querySelector('[name=q]').value, 10) || 1);
    if (!(w > 0 && h > 0)) { out.textContent = '—'; note.textContent = 'Enter the width and height.'; return; }
    var sq = w * h / 144;
    if (sq > 50) { out.textContent = 'Custom quote'; note.textContent = sq.toFixed(1) + ' sq ft: send us a photo for an exact price.'; return; }
    var i = sq <= 10 ? 0 : sq <= 20 ? 1 : sq <= 30 ? 2 : 3;
    var t = d.tiers[i], pct = 0;
    box.querySelectorAll('.opt input:checked').forEach(function (c) {
      d.addons.forEach(function (a) { if (a[0] === c.value) pct += a[2]; });
    });
    var lo = t[0] * (1 + pct / 100) * q, hi = t[1] ? t[1] * (1 + pct / 100) * q : null;
    out.textContent = hi ? fmt(lo) + '–' + fmt(hi) : fmt(lo) + '+';
    note.textContent = sq.toFixed(1) + ' sq ft per unit' + (q > 1 ? ' × ' + q + ' units' : '') + ' · before HST';
  }
  box.addEventListener('input', calc);
  box.addEventListener('change', calc);
  calc();
})();
