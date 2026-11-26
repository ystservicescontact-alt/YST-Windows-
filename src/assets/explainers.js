/* Animated problem explainers on service pages.
   Each .explainer has data-scene and a list of steps (data-start seconds) that double as captions.
   Drawn in SVG; no libraries. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function el(tag, attrs, parent) {
    var n = document.createElementNS(NS, tag);
    if (attrs) for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }
  function clamp(x, a, b) { return Math.max(a, Math.min(b, x)); }
  function ramp(t, a, b) { return clamp((t - a) / (b - a), 0, 1); }
  function ease(x) { return x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2; }
  function lerp(a, b, k) { return a + (b - a) * k; }
  function pts(list) { return list.map(function (p) { return p[0].toFixed(1) + ',' + p[1].toFixed(1); }).join(' '); }

  var C = {
    navy: '#0F1B33', ink: '#22304A', red: '#E5262E', green: '#1E9E5A', blue: '#3D9BE0',
    wall: '#EFE9E1', wall2: '#E4DCD1', trim: '#FBFBF9', trimShade: '#D9D5CE', line: '#22304A',
  };

  // Shared defs for each SVG
  function defs(svg, id) {
    var d = el('defs', null, svg);
    var g = el('linearGradient', { id: id + '-wall', x1: 0, y1: 0, x2: 0, y2: 1 }, d);
    el('stop', { offset: 0, 'stop-color': '#F3EEE7' }, g); el('stop', { offset: 1, 'stop-color': '#E2D9CD' }, g);
    var m = el('linearGradient', { id: id + '-metal', x1: 0, y1: 0, x2: 0, y2: 1 }, d);
    el('stop', { offset: 0, 'stop-color': '#F2F3F5' }, m); el('stop', { offset: 0.5, 'stop-color': '#B9C0CA' }, m); el('stop', { offset: 1, 'stop-color': '#8C95A3' }, m);
    var gl = el('linearGradient', { id: id + '-glass', x1: 0, y1: 0, x2: 1, y2: 1 }, d);
    el('stop', { offset: 0, 'stop-color': '#ffffff', 'stop-opacity': 0.0 }, gl);
    el('stop', { offset: 0.42, 'stop-color': '#ffffff', 'stop-opacity': 0.0 }, gl);
    el('stop', { offset: 0.47, 'stop-color': '#ffffff', 'stop-opacity': 0.28 }, gl);
    el('stop', { offset: 0.55, 'stop-color': '#ffffff', 'stop-opacity': 0.0 }, gl);
    el('stop', { offset: 0.62, 'stop-color': '#ffffff', 'stop-opacity': 0.14 }, gl);
    el('stop', { offset: 0.66, 'stop-color': '#ffffff', 'stop-opacity': 0.0 }, gl);
    var grid = el('pattern', { id: id + '-grid', width: 16, height: 16, patternUnits: 'userSpaceOnUse' }, d);
    el('path', { d: 'M16 0H0V16', fill: 'none', stroke: '#9DB7D8', 'stroke-width': 0.6, opacity: 0.55 }, grid);
    var f = el('filter', { id: id + '-shadow', x: '-10%', y: '-10%', width: '120%', height: '130%' }, d);
    el('feDropShadow', { dx: 0, dy: 6, stdDeviation: 8, 'flood-color': '#0F1B33', 'flood-opacity': 0.18 }, f);
    var b = el('filter', { id: id + '-blur', x: '-5%', y: '-5%', width: '110%', height: '110%' }, d);
    el('feGaussianBlur', { stdDeviation: 7 }, b);
    var arrow = el('marker', { id: id + '-arrow', viewBox: '0 0 10 10', refX: 6, refY: 5, markerWidth: 5, markerHeight: 5, orient: 'auto-start-reverse' }, d);
    el('path', { d: 'M0 0L10 5L0 10z', fill: C.blue }, arrow);
    var arrowR = el('marker', { id: id + '-arrowR', viewBox: '0 0 10 10', refX: 6, refY: 5, markerWidth: 5, markerHeight: 5, orient: 'auto-start-reverse' }, d);
    el('path', { d: 'M0 0L10 5L0 10z', fill: C.red }, arrowR);
    return d;
  }

  // Blueprint-style title block in the corner
  function titleBlock(svg, x, y, lines) {
    var g = el('g', { class: 'ex-tb' }, svg);
    el('rect', { x: x, y: y, width: 300, height: 22 + lines.length * 20, fill: '#ffffff', 'fill-opacity': 0.85, stroke: C.line, 'stroke-width': 1.2 }, g);
    lines.forEach(function (t, i) {
      var tx = el('text', { x: x + 12, y: y + 26 + i * 20, class: i === 0 ? 'ex-tb-h' : 'ex-tb-l' }, g);
      tx.textContent = t;
    });
    return g;
  }

  // Zoom bubble with blueprint grid and leader line
  function bubble(svg, id, cx, cy, r, tx, ty, title) {
    var g = el('g', { class: 'ex-bubble' }, svg);
    var leader = el('path', { d: 'M' + tx + ' ' + ty + 'L' + (cx - r * 0.72) + ' ' + (cy + r * 0.69), stroke: C.navy, 'stroke-width': 2, 'stroke-dasharray': '6 5', fill: 'none' }, g);
    el('circle', { cx: tx, cy: ty, r: 7, fill: 'none', stroke: C.navy, 'stroke-width': 2 }, g);
    var body = el('g', null, g);
    el('circle', { cx: cx, cy: cy, r: r + 6, fill: C.navy }, body);
    el('circle', { cx: cx, cy: cy, r: r, fill: '#F7FAFE' }, body);
    var clip = el('clipPath', { id: id + '-bclip' }, svg);
    el('circle', { cx: cx, cy: cy, r: r }, clip);
    var inner = el('g', { 'clip-path': 'url(#' + id + '-bclip)' }, body);
    el('rect', { x: cx - r, y: cy - r, width: 2 * r, height: 2 * r, fill: 'url(#' + id + '-grid)' }, inner);
    var tag = el('g', null, body);
    el('rect', { x: cx - 70, y: cy + r - 8, width: 140, height: 26, rx: 13, fill: C.navy }, tag);
    var tt = el('text', { x: cx, y: cy + r + 10, class: 'ex-bubble-tag', 'text-anchor': 'middle' }, tag);
    tt.textContent = title;
    return { g: g, body: body, inner: inner, tagText: tt, leader: leader, cx: cx, cy: cy };
  }
  function showBubble(b, k) {
    var s = 0.6 + 0.4 * ease(k);
    b.g.setAttribute('opacity', k);
    b.body.setAttribute('transform', 'translate(' + b.cx + ' ' + b.cy + ') scale(' + s + ') translate(' + -b.cx + ' ' + -b.cy + ')');
  }

  // Canadian maple leaf (same outline as the logo), centred on 0,0, about 100 units tall
  var LEAF = 'M50 5 L58 22 L68 17 L64 40 L78 28 L82 36 L95 33 L89 47 L96 51 L72 70 L76 78 L54 75 L54 95 L46 95 L46 75 L24 78 L28 70 L4 51 L11 47 L5 33 L18 36 L22 28 L36 40 L32 17 L42 22 Z';

  // ------------------------------------------------------------ Street view (house)
  function streetView(g, x, y, w, h) {
    var sky = el('linearGradient', { id: 'sv-sky', x1: 0, y1: 0, x2: 0, y2: 1 }, g);
    el('stop', { offset: 0, 'stop-color': '#8EC3EC' }, sky); el('stop', { offset: 1, 'stop-color': '#DDEEF8' }, sky);
    el('rect', { x: x, y: y, width: w, height: h, fill: 'url(#sv-sky)' }, g);
    // clouds
    [[x + 90, y + 60, 1], [x + 330, y + 40, 0.8]].forEach(function (c) {
      var cl = el('g', { fill: '#ffffff', opacity: 0.85 }, g);
      el('ellipse', { cx: c[0], cy: c[1], rx: 46 * c[2], ry: 14 * c[2] }, cl);
      el('ellipse', { cx: c[0] + 24 * c[2], cy: c[1] - 9 * c[2], rx: 28 * c[2], ry: 13 * c[2] }, cl);
    });
    var base = y + h * 0.66;
    // houses across the street: brick, gables, white trim
    var houses = [[x - 20, 170, 120, '#9A4B3C'], [x + 160, 150, 135, '#B0644A'], [x + 320, 175, 125, '#8E4436']];
    houses.forEach(function (hs, i) {
      var hx = hs[0], hw = hs[1], hh = hs[2], top = base - hh;
      el('rect', { x: hx, y: top, width: hw, height: hh, fill: hs[3], stroke: C.line, 'stroke-width': 1.2 }, g);
      // brick hint
      for (var r = top + 10; r < base; r += 10) el('line', { x1: hx, y1: r, x2: hx + hw, y2: r, stroke: '#000', 'stroke-opacity': 0.08 }, g);
      el('polygon', { points: pts([[hx - 10, top], [hx + hw / 2, top - 62], [hx + hw + 10, top]]), fill: '#3B3F46', stroke: C.line, 'stroke-width': 1.2 }, g);
      // windows + door
      [[0.18, 0.22], [0.62, 0.22]].forEach(function (p) {
        el('rect', { x: hx + hw * p[0], y: top + hh * p[1], width: hw * 0.22, height: hh * 0.24, fill: '#CFE3F1', stroke: '#ffffff', 'stroke-width': 4 }, g);
      });
      el('rect', { x: hx + hw * 0.42, y: base - hh * 0.36, width: hw * 0.17, height: hh * 0.36, fill: i === 1 ? '#1F4E79' : '#2E3A2F', stroke: '#ffffff', 'stroke-width': 3 }, g);
      el('rect', { x: hx + hw * 0.1, y: base - hh * 0.3, width: hw * 0.24, height: hh * 0.2, fill: '#CFE3F1', stroke: '#ffffff', 'stroke-width': 4 }, g);
    });
    // flag on the middle house
    var fx = x + 300, fy = base - 210;
    el('line', { x1: fx, y1: fy, x2: fx, y2: fy + 120, stroke: '#6B7280', 'stroke-width': 3 }, g);
    var flag = el('g', { transform: 'translate(' + fx + ' ' + fy + ')' }, g);
    el('rect', { x: 0, y: 0, width: 66, height: 33, fill: '#ffffff', stroke: C.line, 'stroke-width': 0.8 }, flag);
    el('rect', { x: 0, y: 0, width: 16.5, height: 33, fill: C.red }, flag);
    el('rect', { x: 49.5, y: 0, width: 16.5, height: 33, fill: C.red }, flag);
    el('path', { d: LEAF, fill: C.red, transform: 'translate(24 6) scale(0.2)' }, flag);
    // lawn, sidewalk, road
    el('rect', { x: x, y: base, width: w, height: 22, fill: '#7FA650' }, g);
    el('rect', { x: x, y: base + 22, width: w, height: 18, fill: '#C9C6BF' }, g);
    el('rect', { x: x, y: base + 40, width: w, height: h, fill: '#5A5E66' }, g);
    el('rect', { x: x, y: base + 40, width: w, height: 5, fill: '#8B8F96' }, g);
    // maple tree in autumn
    var tx = x + 120, ty = base + 20;
    el('rect', { x: tx - 7, y: ty - 120, width: 14, height: 122, fill: '#5B3A26' }, g);
    var crown = el('g', { stroke: C.line, 'stroke-width': 1 }, g);
    [[0, -150, 62, '#D9481F'], [-48, -125, 44, '#C23A1B'], [48, -128, 46, '#E36A1E'], [-20, -190, 42, '#E8862A'], [28, -180, 40, '#CF4A1C'], [0, -112, 40, '#B8331A']].forEach(function (c) {
      el('circle', { cx: tx + c[0], cy: ty + c[1], r: c[2], fill: c[3] }, crown);
    });
    // a few falling leaves (animated by the scene)
    var leaves = [];
    for (var i = 0; i < 5; i++) {
      var lf = el('path', { d: LEAF, fill: i % 2 ? '#E36A1E' : '#C23A1B', transform: 'scale(0.1)' }, g);
      leaves.push({ n: lf, x0: tx - 60 + i * 30, y0: ty - 150 + (i % 3) * 20, ph: i * 1.7 });
    }
    return {
      tick: function (time) {
        leaves.forEach(function (l) {
          var k = ((time * 0.12 + l.ph / 7) % 1);
          var lx = l.x0 + Math.sin(time * 1.4 + l.ph) * 14 + k * 40, ly = l.y0 + k * 190;
          l.n.setAttribute('transform', 'translate(' + lx + ' ' + ly + ') rotate(' + (time * 90 + l.ph * 40) + ' 5 5) scale(0.1)');
          l.n.setAttribute('opacity', k > 0.9 ? (1 - k) * 10 : 1);
        });
      },
    };
  }

  // ============================================================ Scene: window crank
  function sceneCrank(svg, id) {
    defs(svg, id);
    el('rect', { x: 0, y: 0, width: 1200, height: 750, fill: 'url(#' + id + '-wall)' }, svg);
    // window casing (trim), frame, view
    var ox = 360, oy = 120, ow = 480, oh = 450; // glass opening of the frame
    el('rect', { x: ox - 62, y: oy - 58, width: ow + 124, height: oh + 100, fill: C.trim, stroke: C.line, 'stroke-width': 1.5, filter: 'url(#' + id + '-shadow)' }, svg);
    el('rect', { x: ox - 30, y: oy - 28, width: ow + 60, height: oh + 46, fill: '#EDEBE6', stroke: C.line, 'stroke-width': 1.2 }, svg);
    var viewClip = el('clipPath', { id: id + '-view' }, svg);
    el('rect', { x: ox, y: oy, width: ow, height: oh }, viewClip);
    var view = el('g', { 'clip-path': 'url(#' + id + '-view)' }, svg);
    var street = streetView(view, ox, oy, ow, oh);
    // sash (casement hinged on the left, opens outward)
    var sashG = el('g', null, svg);
    var sashFrame = el('path', { fill: '#F7F7F4', stroke: C.line, 'stroke-width': 1.5, 'fill-rule': 'evenodd' }, sashG);
    var sashGlass = el('polygon', { fill: '#BFE0F2', 'fill-opacity': 0.18, stroke: C.line, 'stroke-width': 1 }, sashG);
    var sashShine = el('polygon', { fill: 'url(#' + id + '-glass)' }, sashG);
    var gap = el('polygon', { fill: '#0F1B33', 'fill-opacity': 0.0 }, svg);
    // stool (inside sill)
    el('rect', { x: ox - 90, y: oy + oh + 18, width: ow + 180, height: 24, fill: C.trim, stroke: C.line, 'stroke-width': 1.5 }, svg);
    el('rect', { x: ox - 80, y: oy + oh + 42, width: ow + 160, height: 14, fill: C.trimShade, stroke: C.line, 'stroke-width': 1 }, svg);
    // operator arm, housing and handle
    var arm = el('path', { stroke: '#7C8594', 'stroke-width': 9, 'stroke-linecap': 'round', fill: 'none' }, svg);
    var armJ = el('circle', { r: 6, fill: '#5F6876', stroke: C.line, 'stroke-width': 1 }, svg);
    var opX = 700, opY = oy + oh + 6;
    var housing = el('rect', { x: opX - 48, y: opY - 6, width: 96, height: 24, rx: 6, fill: 'url(#' + id + '-metal)', stroke: C.line, 'stroke-width': 1.5 }, svg);
    var hub = { x: opX, y: oy + oh + 52 };
    var handle = el('g', null, svg);
    el('rect', { x: -6, y: -6, width: 58, height: 12, rx: 6, fill: '#2B3442', stroke: C.line, 'stroke-width': 1 }, handle);
    el('circle', { cx: 50, cy: 0, r: 10, fill: '#3A4556', stroke: C.line, 'stroke-width': 1 }, handle);
    el('circle', { cx: 0, cy: 0, r: 13, fill: '#C7CDD6', stroke: C.line, 'stroke-width': 1.5 }, svg).setAttribute('transform', 'translate(' + hub.x + ' ' + hub.y + ')');
    var spin = el('path', { d: 'M' + (hub.x - 70) + ' ' + (hub.y - 8) + 'A70 70 0 0 1 ' + (hub.x - 40) + ' ' + (hub.y - 60), fill: 'none', stroke: C.red, 'stroke-width': 4, 'marker-end': 'url(#' + id + '-arrowR)', opacity: 0 }, svg);
    var okRing = el('rect', { x: opX - 60, y: opY - 16, width: 120, height: 92, rx: 14, fill: 'none', stroke: C.green, 'stroke-width': 4, 'stroke-dasharray': '10 7', opacity: 0 }, svg);
    // cold air through the gap
    var air = el('g', { opacity: 0 }, svg);
    var airPaths = [];
    for (var a = 0; a < 3; a++) {
      airPaths.push(el('path', { fill: 'none', stroke: C.blue, 'stroke-width': 4, 'stroke-linecap': 'round', 'stroke-dasharray': '18 12', 'marker-end': 'url(#' + id + '-arrow)' }, air));
    }
    // gap dimension label
    var gapDim = el('g', { opacity: 0 }, svg);
    var gapLine = el('path', { stroke: C.red, 'stroke-width': 2, fill: 'none' }, gapDim);
    var gapText = el('text', { class: 'ex-dim', fill: C.red }, gapDim); gapText.textContent = 'GAP';

    titleBlock(svg, 30, 30, ['CASEMENT WINDOW', 'Crank operator · inside view']);

    // zoom bubble: worm + gear
    var B = bubble(svg, id, 1030, 300, 140, opX + 48, opY + 6, 'CRANK OPERATOR');
    var gx = 1030, gy = 340, gr = 62;
    var gearOld = el('g', null, B.inner), gearNew = el('g', { opacity: 0 }, B.inner);
    function gear(parent, color, missing) {
      var gg = el('g', null, parent);
      for (var i = 0; i < 18; i++) {
        var ang = i * 20;
        if (missing && (i <= 2 || i >= 16)) {
          el('rect', { x: gx - 4, y: gy - gr - 2, width: 8, height: 4, fill: C.red, transform: 'rotate(' + ang + ' ' + gx + ' ' + gy + ')' }, gg);
          continue;
        }
        el('rect', { x: gx - 7, y: gy - gr - 12, width: 14, height: 16, rx: 2, fill: color, stroke: C.line, 'stroke-width': 1, transform: 'rotate(' + ang + ' ' + gx + ' ' + gy + ')' }, gg);
      }
      el('circle', { cx: gx, cy: gy, r: gr, fill: color, stroke: C.line, 'stroke-width': 1.5 }, gg);
      el('circle', { cx: gx, cy: gy, r: 16, fill: '#ffffff', stroke: C.line, 'stroke-width': 1.5 }, gg);
      el('line', { x1: gx, y1: gy + 16, x2: gx, y2: gy + gr - 6, stroke: C.line, 'stroke-width': 3 }, gg);
      return gg;
    }
    var gOld = gear(gearOld, '#C9B28A', true);
    var gNew = gear(gearNew, '#A9D8BC', false);
    // worm screw across the top of the gear
    var wy = gy - gr - 34, wClip = el('clipPath', { id: id + '-worm' }, svg);
    el('rect', { x: gx - 110, y: wy - 18, width: 220, height: 36, rx: 16 }, wClip);
    el('rect', { x: gx - 110, y: wy - 18, width: 220, height: 36, rx: 16, fill: 'url(#' + id + '-metal)', stroke: C.line, 'stroke-width': 1.5 }, B.inner);
    var threads = el('g', { 'clip-path': 'url(#' + id + '-worm)' }, B.inner);
    for (var k = -12; k < 14; k++) el('line', { x1: gx + k * 18, y1: wy - 20, x2: gx + k * 18 - 12, y2: wy + 20, stroke: C.line, 'stroke-width': 2.5 }, threads);
    var stripTag = el('g', null, B.inner);
    el('rect', { x: gx - 64, y: gy - 6, width: 128, height: 24, rx: 4, fill: C.red }, stripTag);
    var st = el('text', { x: gx, y: gy + 11, 'text-anchor': 'middle', class: 'ex-chip' }, stripTag); st.textContent = 'STRIPPED TEETH';
    var newTag = el('g', { opacity: 0 }, B.inner);
    el('rect', { x: gx - 54, y: gy - 6, width: 108, height: 24, rx: 4, fill: C.green }, newTag);
    var nt = el('text', { x: gx, y: gy + 11, 'text-anchor': 'middle', class: 'ex-chip' }, newTag); nt.textContent = 'NEW GEARS';
    var wormArrow = el('path', { d: 'M' + (gx - 60) + ' ' + (wy - 30) + 'H' + (gx + 60), stroke: C.red, 'stroke-width': 3, fill: 'none', 'marker-end': 'url(#' + id + '-arrowR)' }, B.inner);

    // geometry of the opening sash as a quad (hinge on the left)
    var X0 = ox + 4, X1 = ox + ow - 4, Y0 = oy + 4, Y1 = oy + oh - 4, SW = X1 - X0;
    function quad(theta) {
      var c = Math.cos(theta), s = Math.sin(theta);
      var xr = X0 + SW * c, d = 46 * s;
      return [[X0, Y0], [xr, Y0 + d], [xr, Y1 - d], [X0, Y1]];
    }
    function inset(q, u0, v0) {
      function at(u, v) {
        var top = [lerp(q[0][0], q[1][0], u), lerp(q[0][1], q[1][1], u)];
        var bot = [lerp(q[3][0], q[2][0], u), lerp(q[3][1], q[2][1], u)];
        return [lerp(top[0], bot[0], v), lerp(top[1], bot[1], v)];
      }
      return [at(u0, v0), at(1 - u0, v0), at(1 - u0, 1 - v0), at(u0, 1 - v0)];
    }
    function pathOf(q) { return 'M' + q.map(function (p) { return p[0].toFixed(1) + ' ' + p[1].toFixed(1); }).join('L') + 'Z'; }

    var DEG = Math.PI / 180;
    // timeline (seconds): matches the caption steps in the page
    function sashAngle(t) {
      if (t < 3.5) return lerp(34, 16, ease(ramp(t, 0, 3.5))) * DEG;
      if (t < 17) return (16 + (t > 3.5 && t < 7.5 ? Math.sin(t * 30) * 0.4 : 0)) * DEG;
      return lerp(16, 0, ease(ramp(t, 17, 20.5))) * DEG;
    }
    function turned(t) { // seconds the handle has been turning
      return Math.min(t, 14.5) + Math.max(0, Math.min(t, 20.5) - 17);
    }

    return function update(t, time) {
      street.tick(time);
      var th = sashAngle(t), q = quad(th), qi = inset(q, 0.06, 0.06);
      sashFrame.setAttribute('d', pathOf(q) + pathOf(qi));
      sashGlass.setAttribute('points', pts(qi)); sashShine.setAttribute('points', pts(qi));
      // gap between sash edge and frame (when the window isn't closed)
      gap.setAttribute('points', pts([q[1], [X1 + 4, Y0 - 4], [X1 + 4, Y1 + 4], q[2]]));
      gap.setAttribute('fill-opacity', th > 0.5 * DEG ? 0.1 : 0);
      // operator arm from the housing to the sash's bottom rail
      var u = 0.78, ax = lerp(q[3][0], q[2][0], u), ay = lerp(q[3][1], q[2][1], u);
      var px = opX - 20, py = opY + 2;
      var ex = lerp(px + 110, ax, clamp(th / (34 * DEG) * 1.6, 0, 1)), ey = lerp(py - 2, ay - 4, clamp(th / (34 * DEG) * 1.6, 0, 1));
      arm.setAttribute('d', 'M' + px + ' ' + py + 'L' + ex.toFixed(1) + ' ' + ey.toFixed(1));
      armJ.setAttribute('cx', ex); armJ.setAttribute('cy', ey);
      // handle
      var hAng = -turned(t) * 300;
      handle.setAttribute('transform', 'translate(' + hub.x + ' ' + hub.y + ') rotate(' + hAng + ')');
      var spinning = (t > 3.5 && t < 14.5);
      spin.setAttribute('opacity', spinning ? 0.9 : 0);
      // air through the gap
      var airK = ramp(t, 7.5, 8.2) * (1 - ramp(t, 17, 18));
      air.setAttribute('opacity', airK);
      for (var i = 0; i < airPaths.length; i++) {
        var sy = lerp(q[1][1], q[2][1], 0.25 + i * 0.25), sx = (q[1][0] + X1) / 2;
        airPaths[i].setAttribute('d', 'M' + sx + ' ' + sy + 'C' + (sx + 60) + ' ' + (sy + 10) + ' ' + (sx + 40) + ' ' + (sy + 70) + ' ' + (sx + 120) + ' ' + (sy + 80));
        airPaths[i].setAttribute('stroke-dashoffset', -time * 60 - i * 10);
      }
      gapDim.setAttribute('opacity', ramp(t, 4.5, 5.2) * (1 - ramp(t, 17, 17.6)));
      var gm = (q[1][1] + q[2][1]) / 2;
      gapLine.setAttribute('d', 'M' + q[1][0] + ' ' + (gm - 40) + 'V' + (gm + 40) + 'M' + X1 + ' ' + (gm - 40) + 'V' + (gm + 40) + 'M' + q[1][0] + ' ' + gm + 'H' + X1 + 'M' + X1 + ' ' + gm + 'H' + (X1 + 30));
      gapText.setAttribute('x', X1 + 36); gapText.setAttribute('y', gm + 5);
      // bubble
      showBubble(B, ramp(t, 10.5, 11.3));
      var fixK = ramp(t, 14.5, 15.5);
      gearOld.setAttribute('opacity', 1 - fixK); gearNew.setAttribute('opacity', fixK);
      stripTag.setAttribute('opacity', 1 - fixK); newTag.setAttribute('opacity', fixK);
      B.tagText.textContent = fixK > 0.5 ? 'NEW OPERATOR' : 'CRANK OPERATOR';
      var tw = turned(t) * 40;
      threads.setAttribute('transform', 'translate(' + (tw % 18) + ' 0)');
      wormArrow.setAttribute('opacity', spinning || t > 17 ? 1 : 0);
      var gearRot = Math.max(0, Math.min(t, 20.5) - 17) * 26;
      gNew.setAttribute('transform', 'rotate(' + gearRot + ' ' + gx + ' ' + gy + ')');
      okRing.setAttribute('opacity', ramp(t, 14.5, 15.2) * (1 - ramp(t, 21, 22)));
    };
  }

  // ============================================================ Scene: foggy glass (condo, real photo)
  // Two plates of the same photo: clear, and fogged (made from the photo itself). The fogged plate is
  // revealed by a soft circle growing from the corner where the seal failed.
  function sceneFog(svg, id, root) {
    defs(svg, id);
    var clearUrl = root.dataset.clear, fogUrl = root.dataset.fog;
    el('image', { href: clearUrl, x: 0, y: 0, width: 1200, height: 750, preserveAspectRatio: 'xMidYMid slice' }, svg);
    var mask = el('mask', { id: id + '-fogmask', maskUnits: 'userSpaceOnUse', x: 0, y: 0, width: 1200, height: 750 }, svg);
    var rg = el('radialGradient', { id: id + '-fogrg' }, svg);
    el('stop', { offset: 0.6, 'stop-color': '#fff' }, rg); el('stop', { offset: 1, 'stop-color': '#fff', 'stop-opacity': 0 }, rg);
    var cxF = 168, cyF = 575; // failed corner: bottom-left of the glass, along the frame
    var fogCircle = el('circle', { cx: cxF, cy: cyF, r: 0, fill: 'url(#' + id + '-fogrg)' }, mask);
    var fog = el('image', { href: fogUrl, x: 0, y: 0, width: 1200, height: 750, preserveAspectRatio: 'xMidYMid slice', mask: 'url(#' + id + '-fogmask)' }, svg);
    var glassPoly = '95,413 657,0 1200,0 1200,750 583,750 230,734';
    var newRing = el('polygon', { points: glassPoly, fill: 'none', stroke: C.green, 'stroke-width': 7, 'stroke-dasharray': '18 12', opacity: 0 }, svg);
    var crackMark = el('g', { opacity: 0 }, svg);
    el('circle', { cx: cxF, cy: cyF, r: 20, fill: 'none', stroke: C.red, 'stroke-width': 4 }, crackMark);
    var pulse = el('circle', { cx: cxF, cy: cyF, r: 20, fill: 'none', stroke: C.red, 'stroke-width': 3 }, crackMark);
    titleBlock(svg, 30, 30, ['CONDO WINDOW · TORONTO', 'Sealed glass unit · edge seal']);

    // bubble: cross-section of the glass edge
    var B = bubble(svg, id, 1040, 300, 140, cxF, cyF, 'EDGE OF THE GLASS');
    var bx = 1040, by = 300, inn = B.inner;
    var top = by - 150, bot = by + 60;
    var p1x = bx - 62, p2x = bx + 38, pw = 24;
    el('rect', { x: p1x, y: top, width: pw, height: bot - top, fill: '#CDE8F6', stroke: C.line, 'stroke-width': 1.5 }, inn);
    el('rect', { x: p2x, y: top, width: pw, height: bot - top, fill: '#CDE8F6', stroke: C.line, 'stroke-width': 1.5 }, inn);
    var gapX0 = p1x + pw, gapX1 = p2x, spTop = bot - 46;
    el('rect', { x: gapX0 + 4, y: spTop, width: gapX1 - gapX0 - 8, height: 34, fill: '#B8BFC9', stroke: C.line, 'stroke-width': 1.5 }, inn);
    for (var d1 = 0; d1 < 8; d1++) el('circle', { cx: gapX0 + 14 + (d1 % 4) * 18, cy: spTop + 10 + Math.floor(d1 / 4) * 14, r: 4, fill: '#F2E7C9', stroke: C.line, 'stroke-width': 0.6 }, inn);
    var seal = el('rect', { x: gapX0 - pw, y: bot - 12, width: (p2x + pw) - (gapX0 - pw), height: 30, fill: '#1F242D', stroke: C.line, 'stroke-width': 1.5 }, inn);
    var crack = el('path', { d: 'M' + (bx - 6) + ' ' + (bot - 12) + 'l6 10l-8 6l7 8l-4 6', stroke: C.red, 'stroke-width': 4, fill: 'none', opacity: 0 }, inn);
    function lab(x, y, text, anchor) { var t = el('text', { x: x, y: y, class: 'ex-blabel', 'text-anchor': anchor || 'start' }, inn); t.textContent = text; return t; }
    lab(p1x - 6, by - 10, 'Glass', 'end'); lab(p2x + pw + 6, by - 10, 'Glass');
    lab(p2x + pw + 6, spTop + 22, 'Spacer'); lab(p2x + pw + 6, bot + 8, 'Seal');
    var gasLabel = lab(bx - 13, top + 30, 'Argon', 'middle');
    var seed = 11; function rnd() { seed = (seed * 16807) % 2147483647; return seed / 2147483647; }
    var argon = [], moist = [];
    for (var a = 0; a < 16; a++) argon.push({ n: el('circle', { r: 4.5, fill: '#8B6CD9', stroke: '#5B3FA8', 'stroke-width': 1 }, inn), x: gapX0 + 8 + rnd() * (gapX1 - gapX0 - 16), y: top + 40 + rnd() * (spTop - top - 50), ph: rnd() * 6, leave: 7.3 + rnd() * 3 });
    for (var m = 0; m < 14; m++) moist.push({ n: el('circle', { r: 4.5, fill: C.blue, stroke: '#1F6FAE', 'stroke-width': 1 }, inn), x: gapX0 + 8 + rnd() * (gapX1 - gapX0 - 16), y: top + 30 + rnd() * (spTop - top - 40), ph: rnd() * 6, enter: 8 + rnd() * 3 });
    var condense = el('g', { opacity: 0 }, inn);
    for (var c2 = 0; c2 < 10; c2++) { el('circle', { cx: gapX0 + 3, cy: top + 30 + c2 * 14, r: 3, fill: '#ffffff', stroke: C.blue, 'stroke-width': 1 }, condense); el('circle', { cx: gapX1 - 3, cy: top + 36 + c2 * 14, r: 3, fill: '#ffffff', stroke: C.blue, 'stroke-width': 1 }, condense); }
    var crackX = bx - 6, crackY = bot + 4;

    return function update(t, time) {
      var grow = ease(ramp(t, 11, 15.5)), clear = ease(ramp(t, 16.2, 18.2));
      fogCircle.setAttribute('r', (grow * 1400).toFixed(1));
      fog.setAttribute('opacity', 1 - clear);
      crackMark.setAttribute('opacity', ramp(t, 4, 4.5) * (1 - ramp(t, 16, 16.6)));
      var pk = (time * 1.2) % 1; pulse.setAttribute('r', 20 + pk * 26); pulse.setAttribute('opacity', 1 - pk);
      newRing.setAttribute('opacity', ramp(t, 16, 16.6) * (1 - ramp(t, 22, 23)));
      showBubble(B, ramp(t, 0.3, 1.1) * (1 - ramp(t, 11.5, 12.2) * (1 - ramp(t, 15.8, 16.4))));
      var fixed = t >= 16.2;
      crack.setAttribute('opacity', ramp(t, 4, 5) * (fixed ? 0 : 1));
      seal.setAttribute('fill', fixed ? '#16301F' : '#1F242D');
      seal.setAttribute('stroke', fixed ? C.green : C.line);
      B.tagText.textContent = fixed ? 'NEW SEALED UNIT' : 'EDGE OF THE GLASS';
      condense.setAttribute('opacity', fixed ? 0 : ramp(t, 11, 13));
      gasLabel.textContent = fixed ? 'New argon' : (t > 9 ? 'Humid air' : 'Argon');
      argon.forEach(function (p) {
        var x = p.x + Math.sin(time * 1.3 + p.ph) * 5, y = p.y + Math.cos(time * 1.1 + p.ph) * 5, op = 1;
        if (!fixed && t > p.leave) {
          var k = ramp(t, p.leave, p.leave + 2.2);
          x = lerp(x, crackX, k); y = lerp(y, crackY + k * 50, k); op = 1 - ramp(t, p.leave + 1.6, p.leave + 2.2);
        }
        if (fixed) op = ramp(t, 17, 18);
        p.n.setAttribute('cx', x.toFixed(1)); p.n.setAttribute('cy', y.toFixed(1)); p.n.setAttribute('opacity', op);
      });
      moist.forEach(function (p) {
        var x = p.x + Math.sin(time * 1.5 + p.ph) * 6, y = p.y + Math.cos(time * 1.2 + p.ph) * 6, op = 0;
        if (!fixed && t > p.enter) {
          var k = 1 - ramp(t, p.enter, p.enter + 2.2);
          x = lerp(x, crackX, k); y = lerp(y, crackY + 60 * k, k); op = ramp(t, p.enter, p.enter + 0.4);
        }
        p.n.setAttribute('cx', x.toFixed(1)); p.n.setAttribute('cy', y.toFixed(1)); p.n.setAttribute('opacity', op);
      });
    };
  }

  var SCENES = { crank: sceneCrank, fog: sceneFog };

  // ------------------------------------------------------------ player
  function setup(root) {
    var make = SCENES[root.dataset.scene];
    var svg = root.querySelector('svg');
    if (!make || !svg) return;
    var update = make(svg, 'ex-' + root.dataset.scene, root);
    var steps = [].slice.call(root.querySelectorAll('.ex-steps li'));
    var starts = steps.map(function (li) { return parseFloat(li.dataset.start); });
    var dur = parseFloat(root.dataset.duration);
    var cap = root.querySelector('.ex-caption');
    var btn = root.querySelector('.ex-play');
    var t = reduce ? starts[Math.min(3, starts.length - 1)] + 2 : 0, playing = !reduce, visible = false, last = 0, active = -1;
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
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }, { threshold: 0.25 }).observe(root);
    } else visible = true;
    function frame(now) {
      requestAnimationFrame(frame);
      var time = now / 1000, dt = Math.min(time - last, 0.1); last = time;
      if (!visible) return;
      if (playing) { t += dt; if (t > dur + 2) t = 0; }
      render(time);
    }
    render(0);
    requestAnimationFrame(frame);
    root.classList.add('ready');
  }

  [].forEach.call(document.querySelectorAll('.explainer'), function (r) {
    try { setup(r); } catch (e) { r.classList.add('ex-failed'); }
  });
})();
