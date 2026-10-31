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
