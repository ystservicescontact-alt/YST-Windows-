// Fogged-glass demo: drag across the pane to wipe the condensation away.
(function () {
  var pane = document.getElementById('pane');
  var canvas = document.getElementById('fog');
  if (!pane || !canvas) return;
  var ctx = canvas.getContext('2d');
  var dpr = Math.min(window.devicePixelRatio || 1, 2);
  var drawing = false, last = null;

  function fog() {
    var r = pane.getBoundingClientRect();
    canvas.width = Math.round(r.width * dpr);
    canvas.height = Math.round(r.height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.globalCompositeOperation = 'source-over';
    var g = ctx.createLinearGradient(0, 0, 0, r.height);
    g.addColorStop(0, 'rgba(232,238,238,.90)');
    g.addColorStop(1, 'rgba(214,224,224,.94)');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, r.width, r.height);
    for (var i = 0; i < 260; i++) {
      ctx.fillStyle = 'rgba(255,255,255,' + (Math.random() * .5 + .2) + ')';
      ctx.beginPath();
      ctx.arc(Math.random() * r.width, Math.random() * r.height, Math.random() * 2.2 + .4, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.strokeStyle = 'rgba(255,255,255,.35)';
    ctx.lineCap = 'round';
    for (var d = 0; d < 6; d++) {
      var dx = Math.random() * r.width, dy = Math.random() * r.height * .5;
      ctx.lineWidth = Math.random() * 2 + 1.5;
      ctx.beginPath(); ctx.moveTo(dx, dy); ctx.lineTo(dx + (Math.random() * 4 - 2), dy + 40 + Math.random() * 90); ctx.stroke();
    }
  }

  function wipe(x, y) {
    ctx.globalCompositeOperation = 'destination-out';
    var rad = Math.max(28, canvas.width / dpr * .09);
    var g = ctx.createRadialGradient(x, y, 0, x, y, rad);
    g.addColorStop(0, 'rgba(0,0,0,1)');
    g.addColorStop(.6, 'rgba(0,0,0,.9)');
    g.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = g;
    ctx.beginPath(); ctx.arc(x, y, rad, 0, Math.PI * 2); ctx.fill();
  }
  function pos(e) { var r = canvas.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }
  function stroke(p) {
    if (last) {
      var dx = p.x - last.x, dy = p.y - last.y, n = Math.ceil(Math.hypot(dx, dy) / 8);
      for (var i = 1; i <= n; i++) wipe(last.x + dx * i / n, last.y + dy * i / n);
    } else wipe(p.x, p.y);
    last = p;
  }
  canvas.addEventListener('pointerdown', function (e) { drawing = true; last = null; canvas.setPointerCapture(e.pointerId); stroke(pos(e)); });
  canvas.addEventListener('pointermove', function (e) { if (drawing || e.pointerType === 'mouse') stroke(pos(e)); });
  canvas.addEventListener('pointerup', function () { drawing = false; last = null; });
  canvas.addEventListener('pointerleave', function () { last = null; });
  var btn = document.getElementById('refog');
  if (btn) btn.addEventListener('click', fog);
  var t; window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(fog, 150); });
  fog();
})();
