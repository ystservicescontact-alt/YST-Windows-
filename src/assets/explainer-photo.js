/* Photo explainers: a real (or AI) photo with timed effects, a slow camera, a zoom bubble and captions.
   Each scene's data comes from <script type="application/json" class="ex-config"> next to the stage.
   Stage coordinates are 1200 x 750. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var C = { navy: '#0F1B33', red: '#E5262E', green: '#1FA35F', blue: '#3D9BE0', amber: '#F2A900', white: '#ffffff', line: '#22304A' };
  var TONE = { red: C.red, green: C.green, blue: C.blue, navy: C.navy, amber: C.amber, white: C.white };

  function el(tag, attrs, parent) {
    var n = document.createElementNS(NS, tag);
    if (attrs) for (var k in attrs) if (attrs[k] != null) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }
  function clamp(x, a, b) { return Math.max(a, Math.min(b, x)); }
  function ramp(t, a, b) { return clamp((t - a) / (b - a), 0, 1); }
  function ease(x) { return x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2; }
  function lerp(a, b, k) { return a + (b - a) * k; }
  // visibility of an effect with a [t0, t1] window and soft edges
  function win(t, w, fade) { if (!w) return 1; fade = fade || 0.35; return ramp(t, w[0], w[0] + fade) * (1 - ramp(t, w[1] - fade, w[1])); }
  function keyed(keys, t) { // [[t, v], ...] -> eased value
    if (t <= keys[0][0]) return keys[0][1];
    for (var i = 0; i < keys.length - 1; i++) {
      if (t < keys[i + 1][0]) return lerp(keys[i][1], keys[i + 1][1], ease(ramp(t, keys[i][0], keys[i + 1][0])));
    }
    return keys[keys.length - 1][1];
  }
  function pts(list) { return list.map(function (p) { return p[0] + ',' + p[1]; }).join(' '); }
  var uid = 0;

  // ------------------------------------------------------------ bubble diagrams (crisp, technical)
  // Each returns function(time, fixed) for animation; drawn around (cx, cy) inside a ~130px radius.
  var DIAGRAMS = {
    gear: function (g, cx, cy) {
      var parts = {};
      function gear(color, worn) {
        var gg = el('g', null, g);
        for (var i = 0; i < 16; i++) {
          if (worn && (i < 3 || i > 13)) { el('rect', { x: cx - 4, y: cy - 58, width: 8, height: 4, fill: C.red, transform: 'rotate(' + i * 22.5 + ' ' + cx + ' ' + (cy + 10) + ')' }, gg); continue; }
          el('rect', { x: cx - 7, y: cy - 66, width: 14, height: 16, rx: 2, fill: color, stroke: C.line, transform: 'rotate(' + i * 22.5 + ' ' + cx + ' ' + (cy + 10) + ')' }, gg);
        }
        el('circle', { cx: cx, cy: cy + 10, r: 58, fill: color, stroke: C.line, 'stroke-width': 1.5 }, gg);
        el('circle', { cx: cx, cy: cy + 10, r: 14, fill: '#fff', stroke: C.line, 'stroke-width': 1.5 }, gg);
        return gg;
      }
      parts.old = gear('#C9A86A', true); parts.nw = gear('#9FD9B6', false);
      el('rect', { x: cx - 100, y: cy - 98, width: 200, height: 30, rx: 14, fill: '#C3C9D2', stroke: C.line, 'stroke-width': 1.5 }, g);
      var th = el('g', null, g), clip = 'cg' + (++uid);
      var cp = el('clipPath', { id: clip }, g); el('rect', { x: cx - 100, y: cy - 98, width: 200, height: 30, rx: 14 }, cp);
      th.setAttribute('clip-path', 'url(#' + clip + ')');
      for (var k = -14; k < 16; k++) el('line', { x1: cx + k * 16, y1: cy - 100, x2: cx + k * 16 - 10, y2: cy - 66, stroke: C.line, 'stroke-width': 2.5 }, th);
      return function (time, fixed) {
        parts.old.setAttribute('opacity', fixed ? 0 : 1); parts.nw.setAttribute('opacity', fixed ? 1 : 0);
        th.setAttribute('transform', 'translate(' + ((time * 40) % 16) + ' 0)');
        parts.nw.setAttribute('transform', 'rotate(' + (fixed ? time * 25 : 0) + ' ' + cx + ' ' + (cy + 10) + ')');
      };
    },
    fapim: function (g, cx, cy) { // handle spindle drives a toothed rack that moves the arm
      el('rect', { x: cx - 105, y: cy - 10, width: 210, height: 22, fill: '#B9C0CA', stroke: C.line, 'stroke-width': 1.5 }, g);
      var teeth = el('g', null, g), broken = el('g', null, g);
      for (var i = 0; i < 13; i++) {
        var x = cx - 96 + i * 16, bad = i >= 5 && i <= 7;
        el('rect', { x: x, y: cy - 22, width: 9, height: 13, fill: bad ? 'none' : '#B9C0CA', stroke: bad ? 'none' : C.line, 'stroke-width': 1 }, teeth);
        if (bad) el('path', { d: 'M' + x + ' ' + (cy - 10) + 'l3 -4l3 3l3 -3', stroke: C.red, 'stroke-width': 2.5, fill: 'none' }, broken);
      }
      var newTeeth = el('g', { opacity: 0 }, g);
      for (var j = 5; j <= 7; j++) el('rect', { x: cx - 96 + j * 16, y: cy - 22, width: 9, height: 13, fill: '#9FD9B6', stroke: C.green, 'stroke-width': 1.5 }, newTeeth);
      var pinion = el('g', null, g);
      for (var k = 0; k < 10; k++) el('rect', { x: cx - 5, y: cy - 84, width: 10, height: 12, fill: '#D7DCE3', stroke: C.line, transform: 'rotate(' + k * 36 + ' ' + cx + ' ' + (cy - 50) + ')' }, pinion);
      el('circle', { cx: cx, cy: cy - 50, r: 25, fill: '#D7DCE3', stroke: C.line, 'stroke-width': 1.5 }, pinion);
      el('circle', { cx: cx, cy: cy - 50, r: 7, fill: C.navy }, pinion);
      el('rect', { x: cx + 105, y: cy - 4, width: 0, height: 0 }, g);
      var arm = el('path', { d: 'M' + (cx + 70) + ' ' + (cy + 12) + 'L' + (cx + 40) + ' ' + (cy + 80), stroke: '#8E97A4', 'stroke-width': 12, 'stroke-linecap': 'round' }, g);
      return function (time, fixed) {
        broken.setAttribute('opacity', fixed ? 0 : 1); newTeeth.setAttribute('opacity', fixed ? 1 : 0);
        var a = fixed ? Math.sin(time * 1.4) * 60 : Math.sin(time * 9) * 12;
        pinion.setAttribute('transform', 'rotate(' + a + ' ' + cx + ' ' + (cy - 50) + ')');
        var shift = fixed ? Math.sin(time * 1.4) * 22 : 0;
        teeth.setAttribute('transform', 'translate(' + shift + ' 0)'); newTeeth.setAttribute('transform', 'translate(' + shift + ' 0)');
        arm.setAttribute('transform', 'translate(' + shift + ' 0)');
      };
    },
    hinge: function (g, cx, cy) { // casement 4-bar hinge seen from above
      el('rect', { x: cx - 110, y: cy + 30, width: 220, height: 12, rx: 3, fill: '#B9C0CA', stroke: C.line, 'stroke-width': 1.5 }, g);
      var bad = el('g', null, g), good = el('g', { opacity: 0 }, g);
      el('path', { d: 'M' + (cx - 90) + ' ' + (cy + 30) + 'Q' + (cx - 30) + ' ' + (cy - 30) + ' ' + (cx + 20) + ' ' + (cy - 40), stroke: '#8E97A4', 'stroke-width': 10, fill: 'none', 'stroke-linecap': 'round' }, bad);
      el('path', { d: 'M' + (cx - 10) + ' ' + (cy + 30) + 'L' + (cx + 60) + ' ' + (cy - 55), stroke: '#8E97A4', 'stroke-width': 10, 'stroke-linecap': 'round' }, bad);
      el('path', { d: 'M' + (cx - 40) + ' ' + (cy - 12) + 'q10 -6 18 0', stroke: C.red, 'stroke-width': 4, fill: 'none' }, bad);
      el('rect', { x: cx - 10, y: cy - 78, width: 120, height: 14, rx: 3, fill: '#D7DCE3', stroke: C.line, transform: 'rotate(-18 ' + (cx + 50) + ' ' + (cy - 70) + ')' }, bad);
      el('path', { d: 'M' + (cx - 90) + ' ' + (cy + 30) + 'L' + (cx + 20) + ' ' + (cy - 40), stroke: '#7FC49D', 'stroke-width': 10, 'stroke-linecap': 'round' }, good);
      el('path', { d: 'M' + (cx - 10) + ' ' + (cy + 30) + 'L' + (cx + 60) + ' ' + (cy - 55), stroke: '#7FC49D', 'stroke-width': 10, 'stroke-linecap': 'round' }, good);
      el('rect', { x: cx - 30, y: cy - 66, width: 140, height: 14, rx: 3, fill: '#BFE8CF', stroke: C.green, transform: 'rotate(-12 ' + (cx + 40) + ' ' + (cy - 60) + ')' }, good);
      return function (time, fixed) { bad.setAttribute('opacity', fixed ? 0 : 1); good.setAttribute('opacity', fixed ? 1 : 0); };
    },
    lock: function (g, cx, cy) { // cam lock on the sash, keeper on the frame
      el('rect', { x: cx - 110, y: cy + 4, width: 220, height: 50, fill: '#E9ECF0', stroke: C.line, 'stroke-width': 1.5 }, g);
      el('rect', { x: cx - 110, y: cy - 70, width: 220, height: 50, fill: '#F6F7F9', stroke: C.line, 'stroke-width': 1.5 }, g);
      var keeper = el('path', { d: 'M' + (cx + 10) + ' ' + (cy + 4) + 'v-18h56v18', fill: '#C3C9D2', stroke: C.line, 'stroke-width': 1.5 }, g);
      var cam = el('g', null, g);
      el('path', { d: 'M' + (cx - 20) + ' ' + (cy - 20) + 'a40 40 0 0 1 70 18', stroke: '#8E97A4', 'stroke-width': 12, fill: 'none', 'stroke-linecap': 'round' }, cam);
      el('circle', { cx: cx - 20, cy: cy - 30, r: 12, fill: '#C3C9D2', stroke: C.line, 'stroke-width': 1.5 }, cam);
      var miss = el('path', { d: 'M' + (cx + 70) + ' ' + (cy - 40) + 'l12 12m0 -12l-12 12', stroke: C.red, 'stroke-width': 4 }, g);
      return function (time, fixed) {
        var a = fixed ? 0 : -24 + Math.sin(time * 3) * 4;
        cam.setAttribute('transform', 'rotate(' + a + ' ' + (cx - 20) + ' ' + (cy - 30) + ')');
        keeper.setAttribute('fill', fixed ? '#BFE8CF' : '#C3C9D2'); keeper.setAttribute('stroke', fixed ? C.green : C.line);
        keeper.setAttribute('transform', fixed ? '' : 'translate(14 6)');
        miss.setAttribute('opacity', fixed ? 0 : 1);
      };
    },
    spline: function (g, cx, cy) { // handle socket: stripped splines vs new
      var bad = el('g', null, g), good = el('g', { opacity: 0 }, g);
      function star(parent, color, stroke, worn) {
        var d = '';
        for (var i = 0; i < 24; i++) {
          var a = i / 24 * Math.PI * 2, r = (i % 2 ? 34 : (worn ? 36 : 44));
          d += (i ? 'L' : 'M') + (cx + Math.cos(a) * r).toFixed(1) + ' ' + (cy + Math.sin(a) * r).toFixed(1);
        }
        el('circle', { cx: cx, cy: cy, r: 70, fill: '#D7DCE3', stroke: C.line, 'stroke-width': 1.5 }, parent);
        el('path', { d: d + 'Z', fill: color, stroke: stroke, 'stroke-width': 2 }, parent);
        el('circle', { cx: cx, cy: cy, r: 12, fill: '#fff', stroke: C.line }, parent);
      }
      star(bad, '#C9A86A', C.red, true); star(good, '#9FD9B6', C.green, false);
      return function (time, fixed) {
        bad.setAttribute('opacity', fixed ? 0 : 1); good.setAttribute('opacity', fixed ? 1 : 0);
        bad.setAttribute('transform', 'rotate(' + (time * 120 % 360) + ' ' + cx + ' ' + cy + ')');
        good.setAttribute('transform', 'rotate(' + (Math.sin(time * 1.5) * 45) + ' ' + cx + ' ' + cy + ')');
      };
    },
    latch: function (g, cx, cy) { // spring latch tongue and strike plate
      el('rect', { x: cx - 110, y: cy - 60, width: 120, height: 120, fill: '#F6F7F9', stroke: C.line, 'stroke-width': 1.5 }, g);
      el('rect', { x: cx + 30, y: cy - 60, width: 80, height: 120, fill: '#E9ECF0', stroke: C.line, 'stroke-width': 1.5 }, g);
      var strike = el('path', { d: 'M' + (cx + 30) + ' ' + (cy - 16) + 'h26v32h-26', fill: '#fff', stroke: C.line, 'stroke-width': 1.5 }, g);
      var tongue = el('path', { d: 'M' + (cx + 10) + ' ' + (cy - 12) + 'h22l10 12l-10 12h-22z', fill: '#C3C9D2', stroke: C.line, 'stroke-width': 1.5 }, g);
      var spring = el('path', { d: 'M' + (cx - 80) + ' ' + cy + 'l8 -10l8 20l8 -20l8 20l8 -20l8 20l8 -10', stroke: '#8E97A4', 'stroke-width': 3, fill: 'none' }, g);
      var x = el('path', { d: 'M' + (cx - 72) + ' ' + (cy + 24) + 'l14 14m0 -14l-14 14', stroke: C.red, 'stroke-width': 4 }, g);
      return function (time, fixed) {
        var out = fixed ? 22 * (0.5 + 0.5 * Math.sin(time * 2)) + 4 : 0;
        tongue.setAttribute('transform', 'translate(' + out + ' 0)');
        tongue.setAttribute('fill', fixed ? '#9FD9B6' : '#C3C9D2'); spring.setAttribute('stroke', fixed ? C.green : C.red);
        x.setAttribute('opacity', fixed ? 0 : 1);
      };
    },
    roller: function (g, cx, cy) {
      el('rect', { x: cx - 110, y: cy + 40, width: 220, height: 14, fill: '#B9C0CA', stroke: C.line, 'stroke-width': 1.5 }, g);
      el('rect', { x: cx - 100, y: cy - 60, width: 200, height: 70, fill: '#E9ECF0', stroke: C.line, 'stroke-width': 1.5 }, g);
      var bad = el('g', null, g), good = el('g', { opacity: 0 }, g);
      el('path', { d: 'M' + (cx - 30) + ' ' + (cy + 40) + 'a30 30 0 1 1 60 0z', fill: '#8C6A45', stroke: C.red, 'stroke-width': 2.5 }, bad);
      el('rect', { x: cx - 100, y: cy + 4, width: 200, height: 36, fill: '#E9ECF0', stroke: C.red, 'stroke-width': 2, 'stroke-dasharray': '6 4' }, bad);
      var wheel = el('g', null, good);
      el('circle', { cx: cx, cy: cy + 14, r: 26, fill: '#3A4556', stroke: C.green, 'stroke-width': 3 }, wheel);
      el('line', { x1: cx, y1: cy - 6, x2: cx, y2: cy + 34, stroke: '#fff', 'stroke-width': 3 }, wheel);
      return function (time, fixed) {
        bad.setAttribute('opacity', fixed ? 0 : 1); good.setAttribute('opacity', fixed ? 1 : 0);
        wheel.setAttribute('transform', 'rotate(' + (time * 160) + ' ' + cx + ' ' + (cy + 14) + ')');
      };
    },
    caulk: function (g, cx, cy) { // wall / frame joint with a caulk bead
      el('rect', { x: cx - 110, y: cy - 80, width: 110, height: 160, fill: '#B3846A', stroke: C.line, 'stroke-width': 1.5 }, g);
      el('rect', { x: cx + 10, y: cy - 80, width: 100, height: 160, fill: '#F2F2EE', stroke: C.line, 'stroke-width': 1.5 }, g);
      var bad = el('g', null, g), good = el('g', { opacity: 0 }, g);
      el('path', { d: 'M' + cx + ' ' + (cy - 80) + 'q12 20 0 40q-10 18 4 30M' + cx + ' ' + (cy + 10) + 'q10 30 0 70', stroke: '#8A8173', 'stroke-width': 9, fill: 'none' }, bad);
      el('path', { d: 'M' + (cx + 2) + ' ' + (cy - 10) + 'l8 4l-6 8l8 4', stroke: C.red, 'stroke-width': 3, fill: 'none' }, bad);
      el('path', { d: 'M' + (cx + 5) + ' ' + (cy - 80) + 'V' + (cy + 80), stroke: '#FAFAF7', 'stroke-width': 16, 'stroke-linecap': 'round' }, good);
      el('path', { d: 'M' + (cx + 5) + ' ' + (cy - 80) + 'V' + (cy + 80), stroke: C.green, 'stroke-width': 2, fill: 'none', 'stroke-dasharray': '6 5' }, good);
      var drops = [];
      for (var i = 0; i < 5; i++) drops.push(el('path', { d: 'M0 -7Q5 0 0 5Q-5 0 0 -7Z', fill: C.blue }, bad));
      return function (time, fixed) {
        bad.setAttribute('opacity', fixed ? 0 : 1); good.setAttribute('opacity', fixed ? 1 : 0);
        drops.forEach(function (d, i) { var k = (time * 0.7 + i / 5) % 1; d.setAttribute('transform', 'translate(' + (cx - 60 + k * 70) + ' ' + (cy - 20 + i * 8) + ')'); d.setAttribute('opacity', k < 0.9 ? 1 : 0); });
      };
    },
    drain: function (g, cx, cy) { // sill cross-section with a weep hole
      el('path', { d: 'M' + (cx - 110) + ' ' + (cy - 20) + 'h150v60h70v24h-220z', fill: '#E9ECF0', stroke: C.line, 'stroke-width': 1.5 }, g);
      var water = el('rect', { x: cx - 100, y: cy - 10, width: 130, height: 0, fill: C.blue, opacity: 0.7 }, g);
      var plug = el('rect', { x: cx + 30, y: cy + 24, width: 26, height: 14, fill: '#6B5A45' }, g);
      var dripG = el('g', null, g), drips = [];
      for (var i = 0; i < 4; i++) drips.push(el('circle', { r: 5, fill: C.blue }, dripG));
      return function (time, fixed) {
        water.setAttribute('height', fixed ? 6 : 34 + Math.sin(time * 2) * 3);
        water.setAttribute('y', fixed ? cy + 38 - 6 : cy + 4 - Math.sin(time * 2) * 3);
        plug.setAttribute('opacity', fixed ? 0 : 1);
        drips.forEach(function (d, k) { var p = (time * 0.8 + k / 4) % 1; d.setAttribute('cx', cx + 44 + p * 60); d.setAttribute('cy', cy + 32 + p * p * 60); d.setAttribute('opacity', fixed ? 1 : 0); });
      };
    },
    screen: function (g, cx, cy) {
      var clip = 'sc' + (++uid), cp = el('clipPath', { id: clip }, g);
      el('rect', { x: cx - 100, y: cy - 90, width: 200, height: 170 }, cp);
      var mesh = el('g', { 'clip-path': 'url(#' + clip + ')' }, g);
      for (var i = -100; i <= 100; i += 8) { el('line', { x1: cx + i, y1: cy - 90, x2: cx + i, y2: cy + 80, stroke: '#5E6773', 'stroke-width': 1.2 }, mesh); }
      for (var j = -90; j <= 80; j += 8) { el('line', { x1: cx - 100, y1: cy + j, x2: cx + 100, y2: cy + j, stroke: '#5E6773', 'stroke-width': 1.2 }, mesh); }
      el('rect', { x: cx - 100, y: cy - 90, width: 200, height: 170, fill: 'none', stroke: '#3B424C', 'stroke-width': 8 }, g);
      var hole = el('path', { d: 'M' + (cx - 30) + ' ' + (cy - 20) + 'q20 -30 50 -6q20 30 -8 48q-34 10 -42 -42z', fill: '#F7FAFE', stroke: C.red, 'stroke-width': 3 }, g);
      var bug = el('g', null, g);
      el('ellipse', { cx: 0, cy: 0, rx: 7, ry: 4, fill: '#222' }, bug);
      el('path', { d: 'M-2 -3l-6 -8M2 -3l6 -8', stroke: '#222', 'stroke-width': 1.5 }, bug);
      return function (time, fixed) {
        hole.setAttribute('opacity', fixed ? 0 : 1);
        var k = (time * 0.4) % 1;
        bug.setAttribute('transform', 'translate(' + (cx - 60 + k * 120) + ' ' + (cy - 60 + Math.sin(k * 9) * 20 + (fixed ? -30 : 0)) + ')');
        bug.setAttribute('opacity', fixed ? (k < 0.45 ? 1 : 0) : 1);
      };
    },
    closer: function (g, cx, cy) { // storm / commercial door closer cylinder
      el('rect', { x: cx - 100, y: cy - 20, width: 150, height: 34, rx: 17, fill: '#C3C9D2', stroke: C.line, 'stroke-width': 1.5 }, g);
      var rod = el('rect', { x: cx + 50, y: cy - 6, width: 50, height: 8, fill: '#8E97A4', stroke: C.line }, g);
      var leak = el('g', null, g);
      for (var i = 0; i < 3; i++) el('path', { d: 'M' + (cx - 40 + i * 30) + ' ' + (cy + 16) + 'q4 10 0 16q-4 -6 0 -16z', fill: '#6B4F2A' }, leak);
      var label = el('text', { x: cx - 25, y: cy + 4, 'text-anchor': 'middle', class: 'exp-chip-t', fill: C.navy }, g);
      return function (time, fixed) {
        leak.setAttribute('opacity', fixed ? 0 : 1);
        rod.setAttribute('width', fixed ? 30 + 20 * (0.5 + 0.5 * Math.sin(time * 1.5)) : 50);
        label.textContent = fixed ? 'NEW CLOSER' : 'LEAKING';
        label.setAttribute('fill', fixed ? C.green : C.red);
      };
    },
    crack: function (g, cx, cy) { // pane with a spreading crack, then a new pane
      el('rect', { x: cx - 100, y: cy - 90, width: 200, height: 170, fill: '#DDEFF8', stroke: C.line, 'stroke-width': 2 }, g);
      var cr = el('g', { stroke: C.navy, 'stroke-width': 2, fill: 'none' }, g);
      var lines = [[0, -80], [70, -40], [80, 50], [-10, 80], [-90, 30], [-70, -60]];
      lines.forEach(function (p) { el('path', { d: 'M' + (cx + 10) + ' ' + (cy - 5) + 'l' + p[0] * 0.5 + ' ' + p[1] * 0.4 + 'l' + p[0] * 0.5 + ' ' + p[1] * 0.6, 'stroke-dasharray': 200, 'stroke-dashoffset': 200 }, cr); });
      var shine = el('path', { d: 'M' + (cx - 80) + ' ' + (cy + 60) + 'l60 -130M' + (cx - 50) + ' ' + (cy + 70) + 'l40 -90', stroke: '#fff', 'stroke-width': 6, opacity: 0 }, g);
      return function (time, fixed, k) {
        [].forEach.call(cr.childNodes, function (n) { n.setAttribute('stroke-dashoffset', 200 * (1 - clamp(k * 1.5, 0, 1))); });
        cr.setAttribute('opacity', fixed ? 0 : 1); shine.setAttribute('opacity', fixed ? 0.8 : 0);
      };
    },
    rot: function (g, cx, cy) { // wood sill cross-section
      el('rect', { x: cx - 110, y: cy - 50, width: 220, height: 100, fill: '#C89B6D', stroke: C.line, 'stroke-width': 1.5 }, g);
      for (var i = 0; i < 6; i++) el('path', { d: 'M' + (cx - 110) + ' ' + (cy - 35 + i * 15) + 'q110 ' + (i % 2 ? 8 : -8) + ' 220 0', stroke: '#A97E55', fill: 'none' }, g);
      var rot = el('path', { d: 'M' + (cx - 10) + ' ' + (cy + 50) + 'q-30 -60 20 -80q60 -10 70 40q10 30 -10 40z', fill: '#5A3E28', stroke: C.red, 'stroke-width': 3 }, g);
      var patch = el('path', { d: 'M' + (cx - 10) + ' ' + (cy + 50) + 'q-30 -60 20 -80q60 -10 70 40q10 30 -10 40z', fill: '#D9B58C', stroke: C.green, 'stroke-width': 3, 'stroke-dasharray': '6 4' }, g);
      return function (time, fixed) { rot.setAttribute('opacity', fixed ? 0 : 1); patch.setAttribute('opacity', fixed ? 1 : 0); };
    },
    weatherstrip: function (g, cx, cy) { // door edge and jamb, gap with cold air
      el('rect', { x: cx - 110, y: cy - 90, width: 110, height: 180, fill: '#7A4B32', stroke: C.line, 'stroke-width': 1.5 }, g);
      el('rect', { x: cx + 20, y: cy - 90, width: 90, height: 180, fill: '#F2F2EE', stroke: C.line, 'stroke-width': 1.5 }, g);
      var strip = el('rect', { x: cx, y: cy - 90, width: 20, height: 180, fill: '#2A2D33' }, g);
      var air = el('g', null, g), arrows = [];
      for (var i = 0; i < 3; i++) arrows.push(el('path', { d: 'M0 0h40', stroke: C.blue, 'stroke-width': 4, 'stroke-linecap': 'round' }, air));
      return function (time, fixed) {
        strip.setAttribute('width', fixed ? 20 : 6); strip.setAttribute('fill', fixed ? '#1F6B43' : '#2A2D33');
        air.setAttribute('opacity', fixed ? 0 : 1);
        arrows.forEach(function (a, k) { var p = (time * 0.8 + k / 3) % 1; a.setAttribute('transform', 'translate(' + (cx + 40 - p * 140) + ' ' + (cy - 50 + k * 50) + ')'); a.setAttribute('opacity', 1 - p); });
      };
    },
    seal: function (g, cx, cy) { // glass edge cross-section (for broken-seal style scenes)
      var p1 = el('rect', { x: cx - 62, y: cy - 110, width: 24, height: 180, fill: '#CDE8F6', stroke: C.line, 'stroke-width': 1.5 }, g);
      var p2 = el('rect', { x: cx + 38, y: cy - 110, width: 24, height: 180, fill: '#CDE8F6', stroke: C.line, 'stroke-width': 1.5 }, g);
      el('rect', { x: cx - 34, y: cy + 24, width: 68, height: 30, fill: '#B8BFC9', stroke: C.line, 'stroke-width': 1.5 }, g);
      var seal = el('rect', { x: cx - 62, y: cy + 54, width: 124, height: 26, fill: '#1F242D', stroke: C.line }, g);
      var dots = [];
      for (var i = 0; i < 12; i++) dots.push(el('circle', { r: 4, fill: '#8B6CD9' }, g));
      return function (time, fixed) {
        [p1, p2].forEach(function (p) { p.setAttribute('fill', fixed ? '#BFEBD2' : '#CDE8F6'); p.setAttribute('stroke', fixed ? C.green : C.line); });
        dots.forEach(function (d, k) { d.setAttribute('cx', cx - 25 + (k % 4) * 17 + Math.sin(time + k) * 3); d.setAttribute('cy', cy - 90 + Math.floor(k / 4) * 35 + Math.cos(time * 1.2 + k) * 4); d.setAttribute('fill', fixed ? '#8B6CD9' : C.blue); });
      };
    },
  };

  // ------------------------------------------------------------ scene
  function build(root, cfg) {
    var svg = root.querySelector('svg.exp-svg');
    var id = 'xp' + (++uid);
    var defs = el('defs', null, svg);
    var fx = cfg.photo, PX = fx.x, PY = fx.y || 0, PW = fx.w, PH = fx.h || 750;
    var arrowM = function (color) {
      var mid = id + 'm' + color.replace('#', '');
      if (!defs.querySelector('#' + mid)) { var m = el('marker', { id: mid, viewBox: '0 0 10 10', refX: 6, refY: 5, markerWidth: 4.5, markerHeight: 4.5, orient: 'auto-start-reverse' }, defs); el('path', { d: 'M0 0L10 5L0 10z', fill: color }, m); }
      return 'url(#' + mid + ')';
    };
    var grid = el('pattern', { id: id + 'g', width: 16, height: 16, patternUnits: 'userSpaceOnUse' }, defs);
    el('path', { d: 'M16 0H0V16', fill: 'none', stroke: '#9DB7D8', 'stroke-width': 0.6, opacity: 0.55 }, grid);
    // backdrop + photo layer (camera zooms this layer)
    if (cfg.bg) el('image', { href: cfg.bg, x: 0, y: 0, width: 1200, height: 750, preserveAspectRatio: 'xMidYMid slice' }, svg);
    else el('rect', { x: 0, y: 0, width: 1200, height: 750, fill: '#1B2433' }, svg);
    var pc = el('clipPath', { id: id + 'pc' }, defs); el('rect', { x: PX, y: PY, width: PW, height: PH }, pc);
    var frame = el('g', { 'clip-path': 'url(#' + id + 'pc)' }, svg);
    var cam = el('g', null, frame);
    el('image', { href: fx.src, x: PX, y: PY, width: PW, height: PH, preserveAspectRatio: 'xMidYMid slice' }, cam);
    var over = el('g', null, svg); // screen-space overlays (labels, rings) placed through the camera transform

    var camKeys = cfg.cam || [[0, 1, PX + PW / 2, PY + PH / 2]];
    var camS = 1, camF = [0, 0];
    function T(p) { return [camF[0] + (p[0] - camF[0]) * camS, camF[1] + (p[1] - camF[1]) * camS]; }

    var items = [];
    (cfg.fx || []).forEach(function (f) {
      var color = TONE[f.tone || 'red'] || f.tone;
      var it = { f: f };
      switch (f.type) {
        case 'patch': // cover part of the photo (e.g. the original handle) with a flat colour
          it.n = el('polygon', { points: pts(f.points), fill: f.fill }, cam); it.always = true; break;
        case 'sprite': // a cut-out from the photo that rotates around a pivot
          it.g = el('g', null, cam);
          el('image', { href: f.src, x: f.x, y: f.y, width: f.w, height: f.h }, it.g);
          it.always = true; break;
        case 'poly':
          it.n = el('polygon', { points: pts(f.points), fill: f.fill ? color : 'none', 'fill-opacity': f.fill ? 0.18 : null, stroke: color, 'stroke-width': 4, 'stroke-dasharray': f.dash === false ? null : '14 9', 'vector-effect': 'non-scaling-stroke' }, cam); break;
        case 'ghost': // outline that morphs between two shapes (e.g. a sash closing)
          it.n = el('polygon', { fill: color, 'fill-opacity': 0.12, stroke: color, 'stroke-width': 3, 'stroke-dasharray': '10 7', 'vector-effect': 'non-scaling-stroke' }, cam); break;
        case 'arrow':
          it.n = el('path', { d: f.d, fill: 'none', stroke: color, 'stroke-width': f.w || 6, 'stroke-linecap': 'round', 'stroke-dasharray': f.dashed === false ? null : '16 11', 'marker-end': arrowM(color), 'vector-effect': 'non-scaling-stroke' }, cam); break;
        case 'flow': // particles along a path (air, water)
          it.path = el('path', { d: f.d, fill: 'none', stroke: 'none' }, cam);
          it.dots = [];
          for (var i = 0; i < (f.n || 14); i++) it.dots.push(el(f.drop ? 'path' : 'circle', f.drop ? { d: 'M0 -7Q5 0 0 5Q-5 0 0 -7Z', fill: color } : { r: f.r || 5, fill: color, opacity: 0.85 }, cam));
          break;
        case 'crack':
          it.g = el('g', { stroke: f.color || '#ffffff', 'stroke-width': 2.2, fill: 'none', 'vector-effect': 'non-scaling-stroke' }, cam);
          var seed = 7; var rnd = function () { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
          it.lines = [];
          for (var c = 0; c < (f.n || 9); c++) {
            var a = c / (f.n || 9) * Math.PI * 2 + rnd() * 0.5, x = f.x, y = f.y, d = 'M' + x + ' ' + y, len = 0;
            for (var s = 0; s < 4; s++) { var L = (f.len || 120) / 4 * (0.6 + rnd() * 0.8); a += (rnd() - 0.5) * 0.7; x += Math.cos(a) * L; y += Math.sin(a) * L; len += L; d += 'L' + x.toFixed(1) + ' ' + y.toFixed(1); }
            it.lines.push({ n: el('path', { d: d, 'stroke-dasharray': len.toFixed(0), 'stroke-dashoffset': len.toFixed(0), 'vector-effect': 'non-scaling-stroke' }, it.g), len: len });
          }
          el('circle', { cx: f.x, cy: f.y, r: 5, fill: '#fff', stroke: 'none' }, it.g);
          break;
        case 'tint':
          it.n = el('polygon', { points: pts(f.points), fill: color, opacity: 0 }, cam); break;
        case 'ring': case 'spin': case 'label': case 'gap': case 'check':
          it.g = el('g', null, over);
          if (f.type === 'ring') { el('circle', { r: f.r || 22, fill: 'none', stroke: color, 'stroke-width': 4 }, it.g); it.p = el('circle', { r: f.r || 22, fill: 'none', stroke: color, 'stroke-width': 3 }, it.g); }
          if (f.type === 'spin') { var R = f.r || 40; it.s = el('path', { d: 'M' + R + ' 0A' + R + ' ' + R + ' 0 1 1 0 ' + (-R), fill: 'none', stroke: color, 'stroke-width': 5, 'stroke-linecap': 'round', 'marker-end': arrowM(color) }, it.g); }
          if (f.type === 'label') {
            it.leader = el('line', { stroke: color, 'stroke-width': 2.5 }, over);
            it.leader.setAttribute('opacity', 0);
            var tx = el('text', { class: 'exp-label', x: 0, y: 0 }, it.g); tx.textContent = f.text;
            it.tx = tx; it.bgR = el('rect', { rx: 4, fill: color }, it.g); it.g.insertBefore(it.bgR, tx);
            if (f.tone === 'white' || f.tone === 'amber') tx.setAttribute('fill', C.navy);
          }
          if (f.type === 'gap') {
            it.line = el('path', { stroke: color, 'stroke-width': 3, fill: 'none' }, it.g);
            it.tx = el('text', { class: 'exp-dim', fill: color }, it.g); it.tx.textContent = f.text || 'GAP';
          }
          if (f.type === 'check') { el('circle', { r: 30, fill: C.green }, it.g); el('path', { d: 'M-13 1l9 9l17 -18', stroke: '#fff', 'stroke-width': 6, fill: 'none', 'stroke-linecap': 'round' }, it.g); }
          break;
      }
      items.push(it);
    });
    over.parentNode.appendChild(over);

    // bubble (photo or diagram per state)
    var B = null;
    if (cfg.bubble) {
      var b = cfg.bubble, bx = b.x, by = b.y, br = b.r || 140;
      B = { cfg: b, g: el('g', null, svg) };
      B.leader = el('path', { stroke: '#fff', 'stroke-width': 2.5, 'stroke-dasharray': '7 6', fill: 'none' }, B.g);
      B.dot = el('circle', { r: 8, fill: 'none', stroke: '#fff', 'stroke-width': 2.5 }, B.g);
      B.body = el('g', null, B.g);
      B.ring = el('circle', { cx: bx, cy: by, r: br + 6, fill: C.navy }, B.body);
      el('circle', { cx: bx, cy: by, r: br, fill: '#F7FAFE' }, B.body);
      var bc = el('clipPath', { id: id + 'bc' }, defs); el('circle', { cx: bx, cy: by, r: br }, bc);
      B.inner = el('g', { 'clip-path': 'url(#' + id + 'bc)' }, B.body);
      el('rect', { x: bx - br, y: by - br, width: 2 * br, height: 2 * br, fill: 'url(#' + id + 'g)' }, B.inner);
      B.states = (b.states || []).map(function (st) {
        var g = el('g', { opacity: 0 }, B.inner), upd = null;
        if (st.img) el('image', { href: st.img, x: bx - br, y: by - br, width: 2 * br, height: 2 * br, preserveAspectRatio: 'xMidYMid slice' }, g);
        if (st.diagram && DIAGRAMS[st.diagram]) upd = DIAGRAMS[st.diagram](g, bx, by);
        return { st: st, g: g, upd: upd };
      });
      B.tagG = el('g', null, B.body);
      B.tagR = el('rect', { y: by + br - 8, height: 28, rx: 14, fill: C.navy }, B.tagG);
      B.tag = el('text', { x: bx, y: by + br + 11, 'text-anchor': 'middle', class: 'exp-tag' }, B.tagG);
      B.bx = bx; B.by = by; B.br = br;
    }
    if (cfg.title) {
      var tb = el('g', null, svg), w = 300;
      el('rect', { x: 24, y: 24, width: w, height: 22 + cfg.title.length * 20, fill: '#fff', 'fill-opacity': 0.9, stroke: C.line, 'stroke-width': 1.2 }, tb);
      cfg.title.forEach(function (t, i) { var x = el('text', { x: 36, y: 50 + i * 20, class: i ? 'exp-tb-l' : 'exp-tb-h' }, tb); x.textContent = t; });
    }

    function pathPoint(path, k) { var L = path.getTotalLength(); return path.getPointAtLength(L * k); }

    return function update(t, time) {
      // camera
      var s = 1, f0 = camKeys[0];
      var i = 0; while (i < camKeys.length - 1 && t >= camKeys[i + 1][0]) i++;
      var a = camKeys[i], b2 = camKeys[Math.min(i + 1, camKeys.length - 1)];
      var k = b2 === a ? 0 : ease(ramp(t, a[0], b2[0]));
      camS = lerp(a[1], b2[1], k); camF = [lerp(a[2], b2[2], k), lerp(a[3], b2[3], k)];
      cam.setAttribute('transform', 'translate(' + camF[0] + ' ' + camF[1] + ') scale(' + camS + ') translate(' + -camF[0] + ' ' + -camF[1] + ')');
      items.forEach(function (it) {
        var f = it.f, v = it.always ? 1 : win(t, f.t);
        if (it.n && !it.always && f.type !== 'tint') it.n.setAttribute('opacity', v);
        if (it.g && !it.always) it.g.setAttribute('opacity', v);
        if (f.type === 'sprite') {
          var ang = f.keys ? keyed(f.keys, t) : 0;
          if (f.wiggle && t > f.wiggle[0] && t < f.wiggle[1]) ang += Math.sin(time * 18) * (f.wiggleDeg || 8);
          it.g.setAttribute('transform', 'rotate(' + ang + ' ' + f.px + ' ' + f.py + ')');
        }
        if (f.type === 'tint') it.n.setAttribute('opacity', v * (f.opacity || 0.35));
        if (f.type === 'ghost') {
          var m = f.keys ? keyed(f.keys, t) : 0;
          it.n.setAttribute('points', pts(f.from.map(function (p, j) { return [lerp(p[0], f.to[j][0], m), lerp(p[1], f.to[j][1], m)]; })));
        }
        if (f.type === 'arrow' && f.dashed !== false) it.n.setAttribute('stroke-dashoffset', -time * 50);
        if (f.type === 'flow') {
          it.dots.forEach(function (d, j) {
            var p = pathPoint(it.path, ((time * (f.speed || 0.4)) + j / it.dots.length) % 1);
            if (f.drop) d.setAttribute('transform', 'translate(' + p.x + ' ' + p.y + ')'); else { d.setAttribute('cx', p.x); d.setAttribute('cy', p.y); }
            d.setAttribute('opacity', v * 0.9);
          });
        }
        if (f.type === 'crack') {
          var gk = ramp(t, f.t[0], f.t[0] + (f.grow || 1.2));
          it.lines.forEach(function (l) { l.n.setAttribute('stroke-dashoffset', (l.len * (1 - gk)).toFixed(0)); });
        }
        if (it.g && it.f.type !== 'sprite' && it.f.type !== 'crack') {
          var P = T([f.x || 0, f.y || 0]);
          if (f.type === 'ring') { it.g.setAttribute('transform', 'translate(' + P[0] + ' ' + P[1] + ')'); var pk = (time * 1.1) % 1; it.p.setAttribute('r', (f.r || 22) + pk * 26); it.p.setAttribute('opacity', 1 - pk); }
          if (f.type === 'spin') it.g.setAttribute('transform', 'translate(' + P[0] + ' ' + P[1] + ') rotate(' + ((f.dir === -1 ? -1 : 1) * time * 260 % 360) + ')');
          if (f.type === 'check') it.g.setAttribute('transform', 'translate(' + P[0] + ' ' + P[1] + ') scale(' + (0.6 + 0.4 * ease(ramp(t, f.t[0], f.t[0] + 0.4))) + ')');
          if (f.type === 'label') {
            var L = [P[0] + (f.dx || 40), P[1] + (f.dy || -40)];
            if (!it.wd) { var bb = it.tx.getBBox(); it.wd = bb.width; }
            var left = (f.dx || 40) < 0;
            var bx0 = left ? L[0] - it.wd - 22 : L[0];
            it.tx.setAttribute('x', bx0 + 11); it.tx.setAttribute('y', L[1] + 6);
            it.bgR.setAttribute('x', bx0); it.bgR.setAttribute('y', L[1] - 15); it.bgR.setAttribute('width', it.wd + 22); it.bgR.setAttribute('height', 30);
            it.leader.setAttribute('x1', P[0]); it.leader.setAttribute('y1', P[1]); it.leader.setAttribute('x2', left ? bx0 + it.wd + 22 : bx0); it.leader.setAttribute('y2', L[1]);
            it.leader.setAttribute('opacity', v);
          }
          if (f.type === 'gap') {
            var A = T(f.a), Bp = T(f.b), vx = Bp[0] - A[0], vy = Bp[1] - A[1], ln = Math.hypot(vx, vy) || 1, nx = -vy / ln * 14, ny = vx / ln * 14;
            it.line.setAttribute('d', 'M' + A[0] + ' ' + A[1] + 'L' + Bp[0] + ' ' + Bp[1] + 'M' + (A[0] - nx) + ' ' + (A[1] - ny) + 'L' + (A[0] + nx) + ' ' + (A[1] + ny) + 'M' + (Bp[0] - nx) + ' ' + (Bp[1] - ny) + 'L' + (Bp[0] + nx) + ' ' + (Bp[1] + ny));
            it.tx.setAttribute('x', (A[0] + Bp[0]) / 2 + (f.tdx || 12)); it.tx.setAttribute('y', (A[1] + Bp[1]) / 2 + (f.tdy || 5));
          }
        }
      });
      if (B) {
        var bc = B.cfg, bv = win(t, bc.t, 0.5), sc = 0.6 + 0.4 * ease(bv);
        B.g.setAttribute('opacity', bv);
        B.body.setAttribute('transform', 'translate(' + B.bx + ' ' + B.by + ') scale(' + sc + ') translate(' + -B.bx + ' ' + -B.by + ')');
        var AP = T(bc.anchor);
        B.dot.setAttribute('cx', AP[0]); B.dot.setAttribute('cy', AP[1]);
        var ang2 = Math.atan2(AP[1] - B.by, AP[0] - B.bx);
        B.leader.setAttribute('d', 'M' + AP[0] + ' ' + AP[1] + 'L' + (B.bx + Math.cos(ang2) * (B.br + 6)) + ' ' + (B.by + Math.sin(ang2) * (B.br + 6)));
        var cur = 0; B.states.forEach(function (s2, j) { if (t >= (s2.st.t || 0)) cur = j; });
        B.states.forEach(function (s2, j) {
          var on = j === cur;
          s2.g.setAttribute('opacity', on ? 1 : 0);
          if (on && s2.upd) s2.upd(time, !!s2.st.fixed, ramp(t, s2.st.t || 0, (s2.st.t || 0) + 1.5));
        });
        var st = B.states[cur].st, tone = TONE[st.tone || 'navy'];
        B.tag.textContent = st.tag || '';
        B.tagR.setAttribute('fill', tone); B.ring.setAttribute('fill', st.tone === 'green' ? C.green : (st.tone === 'red' ? C.red : C.navy));
        var tw = (st.tag || '').length * 8.6 + 30; B.tagR.setAttribute('x', B.bx - tw / 2); B.tagR.setAttribute('width', tw);
      }
    };
  }

  // ------------------------------------------------------------ player (same controls as the other explainers)
  function setup(root) {
    var cfgEl = root.querySelector('script.ex-config');
    if (!cfgEl) return;
    var cfg = JSON.parse(cfgEl.textContent);
    var base = root.dataset.base || '';
    function fix(u) { return u && u.charAt(0) === '/' ? base + u.slice(1) : u; }
    if (base) {
      cfg.photo.src = fix(cfg.photo.src); cfg.bg = fix(cfg.bg);
      (cfg.fx || []).forEach(function (f) { if (f.src) f.src = fix(f.src); });
      if (cfg.bubble) cfg.bubble.states.forEach(function (s) { if (s.img) s.img = fix(s.img); });
    }
    var update = build(root, cfg);
    var steps = [].slice.call(root.querySelectorAll('.ex-steps li'));
    var starts = steps.map(function (li) { return parseFloat(li.dataset.start); });
    var dur = parseFloat(root.dataset.duration);
    var cap = root.querySelector('.ex-caption'), btn = root.querySelector('.ex-play');
    var t = reduce ? starts[Math.min(3, starts.length - 1)] + 1 : 0, playing = !reduce, visible = false, last = 0, active = -1;
    function stepAt(x) { var i = 0; for (var k = 0; k < starts.length; k++) if (x >= starts[k]) i = k; return i; }
    function render(time) {
      update(t, time);
      var i = stepAt(t);
      if (i !== active) {
        active = i;
        steps.forEach(function (li, k) { li.classList.toggle('on', k === i); li.classList.toggle('done', k < i); });
        cap.textContent = steps[i].querySelector('.ex-text').textContent;
        cap.classList.remove('in'); void cap.offsetWidth; cap.classList.add('in');
      }
      root.style.setProperty('--ex-progress', (t / dur).toFixed(4));
    }
    function setPlaying(p) { playing = p; btn.setAttribute('aria-pressed', p ? 'true' : 'false'); btn.querySelector('span').textContent = p ? 'Pause' : 'Play'; }
    setPlaying(playing);
    btn.addEventListener('click', function () { if (!playing && t >= dur) t = 0; setPlaying(!playing); });
    steps.forEach(function (li, k) {
      li.tabIndex = 0;
      function go() { t = starts[k] + 0.01; render(performance.now() / 1000); }
      li.addEventListener('click', go);
      li.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
    });
    root.exSeek = function (x) { t = x; setPlaying(false); render(performance.now() / 1000); };
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }, { threshold: 0.15 }).observe(root);
    else visible = true;
    function frame(now) {
      requestAnimationFrame(frame);
      var time = now / 1000, dt = Math.min(time - last, 0.1); last = time;
      if (!visible) return;
      if (playing) { t += dt; if (t > dur + 1.5) t = 0; }
      render(time);
    }
    render(0);
    requestAnimationFrame(frame);
    root.classList.add('ready');
  }
  [].forEach.call(document.querySelectorAll('.explainer[data-render="photo"]'), function (r) {
    try { setup(r); } catch (e) { r.classList.add('ex-failed'); if (window.console) console.error(e); }
  });
})();
