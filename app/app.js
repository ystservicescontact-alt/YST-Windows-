// Screens and actions. Data lives in this browser (localStorage) for now.
(() => {
  'use strict';

  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const uid = () => Math.random().toString(36).slice(2, 10);
  const enc = encodeURIComponent;
  const isoDate = d => { const x = new Date(d); x.setMinutes(x.getMinutes() - x.getTimezoneOffset()); return x.toISOString().slice(0, 10); };
  const CAT = Object.fromEntries(CATEGORIES.map(c => [c.id, c.label]));
  const WRK = Object.fromEntries(WORK.map(c => [c.id, c.label]));
  const STORE_KEY = 'yst-dispatch-v1';
  const TABS = ['plan', 'jobs', 'team', 'settings'];

  const DEFAULT_SETTINGS = {
    speedKmh: 40, balance: 0.3, returnHome: true, arrivalWindow: 120, serverUrl: '', accessKey: '',
    durations: JSON.parse(JSON.stringify(DEFAULT_DURATIONS)),
  };

  // True inside the installed phone app (Capacitor), false in a browser.
  const NATIVE = !!(window.Capacitor && window.Capacitor.isNativePlatform && window.Capacitor.isNativePlatform());

  // The phone app has no server of its own, so its /api calls go to the website address from Settings.
  function api(path, opts = {}) {
    const base = NATIVE ? String(S.settings.serverUrl || ICARUS_SERVER || '').trim().replace(/\/+$/, '') : '';
    if (NATIVE && !base) return Promise.reject(new Error('no-server'));
    const headers = { ...(opts.headers || {}) };
    if (S.settings.accessKey) headers['x-icarus-key'] = S.settings.accessKey;
    return fetch(base + path, { ...opts, headers });
  }

  function openExternal(url) {
    const L = window.Capacitor && window.Capacitor.Plugins && window.Capacitor.Plugins.AppLauncher;
    if (L && L.openUrl) L.openUrl({ url }).catch(() => window.open(url, '_blank'));
    else window.open(url, '_blank');
  }

  const S = { tab: 'plan', date: isoDate(new Date()), techs: [], jobs: [], settings: null, plan: null, server: null };

  // ---------- time and text helpers ----------
  const toMin = Planner.toMin;
  function clock(m) {
    if (m == null) return '';
    m = Math.round(m);
    const h = Math.floor(m / 60) % 24, mm = m % 60;
    return `${((h + 11) % 12) + 1}:${String(mm).padStart(2, '0')} ${h < 12 ? 'AM' : 'PM'}`;
  }
  const clockS = s => clock(toMin(s));
  function dur(m) {
    m = Math.round(m);
    if (m < 60) return `${m} min`;
    return `${Math.floor(m / 60)}h${m % 60 ? ' ' + String(m % 60).padStart(2, '0') + 'm' : ''}`;
  }
  const dayLabel = iso => new Date(iso + 'T12:00:00').toLocaleDateString('en-CA', { weekday: 'short', month: 'short', day: 'numeric' });
  const techById = id => S.techs.find(t => t.id === id);
  const dayJobs = () => S.jobs.filter(j => j.date === S.date);
  const place = x => (x.address ? [x.address, x.city].filter(Boolean).join(', ') : `${x.lat},${x.lng}`);
  const navUrl = x => `https://www.google.com/maps/dir/?api=1&destination=${enc(place(x))}&travelmode=driving`;
  const initial = n => (String(n || '?').trim()[0] || '?').toUpperCase();
  const window2 = j => (j.windowStart || j.windowEnd) ? `${clockS(j.windowStart) || 'any'} – ${clockS(j.windowEnd) || 'any'}` : '';
  const jobTitle = j => j.type || `${CAT[j.category]} ${WRK[j.work].toLowerCase()}`;

  // ---------- storage ----------
  function load() {
    try { const raw = localStorage.getItem(STORE_KEY); if (raw) return JSON.parse(raw); } catch (e) { /* no storage */ }
    return null;
  }
  function save() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify({ techs: S.techs, jobs: S.jobs, settings: S.settings })); } catch (e) { /* no storage */ }
  }

  // ---------- map lookup ----------
  function hash(s) { let h = 2166136261; for (const c of s) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); } return h >>> 0; }
  async function geocode(address, city, postal) {
    const q = [address, city, postal, 'Ontario, Canada'].filter(Boolean).join(', ');
    if (S.server && S.server.google && S.server.keyOk !== false) {
      try {
        const r = await api('/api/geocode?q=' + enc(q));
        if (r.ok) { const d = await r.json(); if (d.lat != null) return { lat: d.lat, lng: d.lng, precise: true, city: d.city || city }; }
      } catch (e) { /* fall back */ }
    }
    const c = findCity(city) || findCity(address);
    if (!c) return null;
    const h = hash(q);
    // Spread addresses around the town centre so they don't sit on one point.
    return { lat: c[1] + ((h % 1000) / 1000 - 0.5) * 0.035, lng: c[2] + (((h >>> 10) % 1000) / 1000 - 0.5) * 0.05, precise: false, city: city || c[0] };
  }

  async function checkServer() {
    try {
      const r = await api('/api/status', { cache: 'no-store' });
      S.server = r.ok ? await r.json() : { workiz: false, google: false, offline: true };
    } catch (e) { S.server = { workiz: false, google: false, offline: true }; }
    if (S.tab === 'settings') render();
  }

  // ---------- planning ----------
  function replan() { S.plan = Planner.plan(dayJobs(), S.techs, S.settings); }

  function reasonText(u) {
    const j = u.job;
    if (u.code === 'noAddress') return 'This address could not be found on the map. Edit the job and check the street and town.';
    if (u.code === 'noSkill') return `No one on the team does ${CAT[j.category].toLowerCase()} ${j.work === 'estimate' ? 'work' : WRK[j.work].toLowerCase() + 's'}. Add the skill to a team member, or assign it by hand.`;
    const who = u.techs.join(', ');
    const w = window2(j);
    return `${who} ${u.techs.length > 1 ? 'are' : 'is'} full${w ? ` or can't arrive between ${w}` : ''}. Assign it by hand, or move it to another day.`;
  }

  // ---------- rendering ----------
  function render() {
    save();
    replan();
    const v = $('#view');
    v.innerHTML = ({ plan: viewPlan, jobs: viewJobs, team: viewTeam, settings: viewSettings })[S.tab]();
    $$('.tab').forEach(b => b.setAttribute('aria-current', b.dataset.tab === S.tab ? 'page' : 'false'));
    $('#date').value = S.date;
  }

  function empty(title, text, actions) {
    return `<div class="empty"><h2>${esc(title)}</h2><p>${esc(text)}</p><div class="btn-row">${actions || ''}</div></div>`;
  }

  function catPill(j) { return `<span class="pill">${esc(CAT[j.category])}</span><span class="pill">${esc(WRK[j.work])}</span>`; }

  function viewPlan() {
    const p = S.plan, jobs = dayJobs();
    const head = `<div class="page-head"><div><div class="eyebrow">${esc(dayLabel(S.date))}</div><h1>Schedule</h1></div>
      <div class="btn-row"><button class="btn small" data-act="tab" data-tab="jobs">${jobs.length} jobs</button></div></div>`;
    if (!S.techs.length) return head + empty('Add your team first', 'The schedule is built from who can do what. Add your technicians, their skills and where they start the day.', '<button class="btn primary" data-act="new-tech">Add a team member</button>');
    if (!jobs.length) return head + empty('No jobs on this day', 'Pull the day\'s jobs from Workiz, import a CSV export, or add a job by hand.', '<button class="btn primary" data-act="tab" data-tab="jobs">Add jobs</button><button class="btn" data-act="sample">Load a sample day</button>');

    const t = p.totals, loose = p.unassigned.length;
    const summary = `<div class="summary">
      <div><div class="n">${t.jobs}</div><div class="l">Jobs</div></div>
      <div><div class="n">${t.scheduled}</div><div class="l">Scheduled</div></div>
      <div><div class="n ${loose ? 'bad' : ''}">${loose}</div><div class="l">Need a decision</div></div>
      <div><div class="n">${dur(t.drive)}</div><div class="l">Driving, ${Math.round(t.km)} km</div></div></div>`;

    const used = p.routes.filter(r => r.stops.length);
    const idle = p.routes.filter(r => !r.stops.length);
    const sample = jobs.some(j => j.source === 'sample') ? '<p class="note"><b>Sample day.</b> These jobs and techs are examples. Replace them with your team and your Workiz jobs.</p>' : '';

    return head + sample + summary + mapSVG(p) + looseCard(p) + used.map(routeCard).join('') +
      (idle.length ? `<p class="idle">No jobs today for ${idle.map(r => esc(r.tech.name)).join(', ')}.</p>` : '') +
      (p.skipped.length ? `<p class="idle flag">Left out because their start address isn't set: ${p.skipped.map(t => esc(t.name)).join(', ')}.</p>` : '');
  }

  function looseCard(p) {
    if (!p.unassigned.length) return '';
    const opts = S.techs.filter(t => t.active !== false).map(t => `<option value="${esc(t.id)}">${esc(t.name)}</option>`).join('');
    return `<section class="card attention"><h2>Needs a decision (${p.unassigned.length})</h2><ul class="loose-list">${
      p.unassigned.map(u => `<li>
        <div><div><b>${esc(jobTitle(u.job))}</b></div><div class="muted">${esc(u.job.client)} · ${esc(u.job.city || u.job.address)}</div></div>
        <label><span class="sr">Assign to</span><select data-act="assign" data-id="${esc(u.job.id)}"><option value="">Assign to…</option>${opts}</select></label>
        <div class="why">${esc(reasonText(u))} <button class="link-btn" data-act="edit-job" data-id="${esc(u.job.id)}">Edit job</button></div></li>`).join('')
    }</ul></section>`;
  }

  function routeUrl(r) {
    const pts = r.stops.map(s => place(s.job));
    const origin = place(r.tech.home);
    const dest = S.settings.returnHome ? origin : pts[pts.length - 1];
    const way = S.settings.returnHome ? pts : pts.slice(0, -1);
    return `https://www.google.com/maps/dir/?api=1&origin=${enc(origin)}&destination=${enc(dest)}${way.length ? '&waypoints=' + enc(way.join('|')) : ''}&travelmode=driving`;
  }

  function routeCard(r) {
    const tc = r.tech, c = tc.color;
    const warns = [];
    if (r.over > 0) warns.push(`Runs ${dur(r.over)} past ${clockS(tc.end)}`);
    if (r.late > 0) warns.push('Misses a time window');
    if (r.tooMany) warns.push(`More than ${tc.maxJobs} jobs`);
    const rows = [];
    rows.push(`<li class="stop endpoint"><div class="time">${clock(r.start)}</div><div class="rail"><span class="dot"></span></div>
      <div class="body"><div class="title">Start</div><div class="addr muted">${esc(place(tc.home))}</div></div></li>`);
    r.stops.forEach((s, i) => {
      const j = s.job;
      const meta = [`${dur(j.duration)} on site`];
      const w = window2(j); if (w) meta.push(`window ${w}`);
      if (s.wait > 4) meta.push(`waits ${dur(s.wait)}`);
      rows.push(`<li class="stop"><div class="time">${clock(s.arrive)}</div><div class="rail"><span class="dot">${i + 1}</span></div>
        <div class="body">
          <div class="drive">${s.drive ? `${dur(s.drive)} drive · ${Math.round(s.km)} km` : 'Next door'}</div>
          <div class="title">${esc(jobTitle(j))} ${j.lockTech ? '<span class="pill">Assigned by hand</span>' : ''}</div>
          <div class="addr">${esc(j.client)} · ${esc(place(j))}${j.precise === false ? ' <span class="flag">(approx.)</span>' : ''}</div>
          <div class="meta">${esc(meta.join(' · '))}${s.lateBy ? ` · <span class="late">${dur(s.lateBy)} late</span>` : ''}</div>
          <div class="acts"><a class="btn small" href="${esc(navUrl(j))}" target="_blank" rel="noopener">Navigate</a>
          ${j.phone ? `<a class="btn small mono" href="tel:${esc(String(j.phone).replace(/[^0-9+]/g, ''))}" title="Call">${esc(j.phone)}</a>` : ''}
          <button class="btn small" data-act="edit-job" data-id="${esc(j.id)}">Edit</button></div>
        </div></li>`);
    });
    if (S.settings.returnHome) {
      rows.push(`<li class="stop endpoint"><div class="time">${clock(r.finish)}</div><div class="rail"><span class="dot"></span></div>
        <div class="body"><div class="drive">${dur(r.back.min)} drive · ${Math.round(r.back.km)} km</div><div class="title">Back home</div></div></li>`);
    }
    return `<section class="route" style="--c:${esc(c)}">
      <div class="route-head"><span class="route-badge">${esc(initial(tc.name))}</span>
        <div><h3>${esc(tc.name)}</h3><div class="areas">${esc(r.areas.slice(0, 3).join(', '))} · ${r.stops.length} job${r.stops.length > 1 ? 's' : ''}</div></div>
        <div class="when"><b>${clock(r.start)} – ${clock(r.finish)}</b><span class="muted">${dur(r.drive)} driving</span></div></div>
      ${warns.length ? `<div class="route-warn">${warns.map(w => `<span class="pill warn">${esc(w)}</span>`).join('')}</div>` : ''}
      <ol class="stops">${rows.join('')}</ol>
      <div class="route-foot"><a class="btn primary small" href="${esc(routeUrl(r))}" target="_blank" rel="noopener">Open route in Google Maps</a>
        <button class="btn small" data-act="copy-route" data-id="${esc(tc.id)}">Copy for ${esc(tc.name)}</button></div>
    </section>`;
  }

  function mapSVG(p) {
    const pts = [];
    p.routes.forEach(r => { if (r.stops.length) { pts.push(r.tech.home); r.stops.forEach(s => pts.push(s.job)); } });
    p.unassigned.forEach(u => { if (u.job.lat != null) pts.push(u.job); });
    if (!pts.length) return '';
    let minLat = Math.min(...pts.map(x => x.lat)), maxLat = Math.max(...pts.map(x => x.lat));
    let minLng = Math.min(...pts.map(x => x.lng)), maxLng = Math.max(...pts.map(x => x.lng));
    const cLat = (minLat + maxLat) / 2, cLng = (minLng + maxLng) / 2, k = Math.cos(cLat * Math.PI / 180);
    const W = 1000, H = 620, pad = 60;
    const wDeg = Math.max((maxLng - minLng) * k, 0.05), hDeg = Math.max(maxLat - minLat, 0.04);
    const sc = Math.min((W - pad * 2) / wDeg, (H - pad * 2) / hDeg);
    const X = lng => W / 2 + (lng - cLng) * k * sc, Y = lat => H / 2 - (lat - cLat) * sc;
    const out = [];
    // grid, one line per ~5 km
    const step = 0.05;
    const latLo = cLat - H / 2 / sc, latHi = cLat + H / 2 / sc, lngLo = cLng - W / 2 / k / sc, lngHi = cLng + W / 2 / k / sc;
    for (let a = Math.ceil(latLo / step) * step; a < latHi; a += step) out.push(`<line class="grid" x1="0" x2="${W}" y1="${Y(a).toFixed(1)}" y2="${Y(a).toFixed(1)}"/>`);
    for (let a = Math.ceil(lngLo / step) * step; a < lngHi; a += step) out.push(`<line class="grid" y1="0" y2="${H}" x1="${X(a).toFixed(1)}" x2="${X(a).toFixed(1)}"/>`);
    CITIES.filter(c => c[3] && c[1] > latLo && c[1] < latHi && c[2] > lngLo && c[2] < lngHi).forEach(c => {
      const x = X(c[2]), y = Y(c[1]);
      if (x > 40 && x < W - 40 && y > 20 && y < H - 10) out.push(`<text class="city" x="${x.toFixed(1)}" y="${(y + 44).toFixed(1)}" text-anchor="middle">${esc(c[0])}</text>`);
    });
    p.routes.forEach(r => {
      if (!r.stops.length) return;
      const seq = [r.tech.home, ...r.stops.map(s => s.job)];
      const d = seq.map(x => `${X(x.lng).toFixed(1)},${Y(x.lat).toFixed(1)}`).join(' ');
      out.push(`<polyline points="${d}" fill="none" stroke="${esc(r.tech.color)}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" opacity="0.9"/>`);
      if (S.settings.returnHome) {
        const last = seq[seq.length - 1];
        out.push(`<line x1="${X(last.lng).toFixed(1)}" y1="${Y(last.lat).toFixed(1)}" x2="${X(r.tech.home.lng).toFixed(1)}" y2="${Y(r.tech.home.lat).toFixed(1)}" stroke="${esc(r.tech.color)}" stroke-width="4" stroke-dasharray="10 9" opacity="0.6"/>`);
      }
    });
    p.routes.forEach(r => {
      if (!r.stops.length) return;
      const hx = X(r.tech.home.lng), hy = Y(r.tech.home.lat);
      out.push(`<g><title>${esc(r.tech.name)} starts here</title><rect class="ring" x="${(hx - 19).toFixed(1)}" y="${(hy - 19).toFixed(1)}" width="38" height="38" rx="5" fill="${esc(r.tech.color)}" transform="rotate(45 ${hx.toFixed(1)} ${hy.toFixed(1)})"/><text class="home-label" x="${hx.toFixed(1)}" y="${(hy + 7.5).toFixed(1)}" text-anchor="middle">${esc(initial(r.tech.name))}</text></g>`);
      r.stops.forEach((s, i) => {
        const x = X(s.job.lng), y = Y(s.job.lat);
        out.push(`<g><title>${esc(r.tech.name)} · ${i + 1}. ${esc(jobTitle(s.job))} · ${clock(s.arrive)}</title><circle class="ring" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="21" fill="${esc(r.tech.color)}"/><text class="num" x="${x.toFixed(1)}" y="${(y + 7.5).toFixed(1)}" text-anchor="middle">${i + 1}</text></g>`);
      });
    });
    p.unassigned.forEach(u => {
      if (u.job.lat == null) return;
      const x = X(u.job.lng), y = Y(u.job.lat);
      out.push(`<g><title>Not scheduled: ${esc(jobTitle(u.job))}</title><circle class="loose" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="21"/><text class="loose-t" x="${x.toFixed(1)}" y="${(y + 8).toFixed(1)}" text-anchor="middle">!</text></g>`);
    });
    const legend = p.routes.filter(r => r.stops.length).map(r => `<span style="--c:${esc(r.tech.color)}"><i></i>${esc(r.tech.name)}</span>`).join('') +
      '<span><i class="home-i"></i>Start point</span>' + (p.unassigned.length ? '<span style="--c:var(--warn)"><i></i>Not scheduled</span>' : '');
    return `<figure class="map" style="margin:0"><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Map of today's routes">${out.join('')}</svg><figcaption class="legend">${legend}</figcaption></figure>`;
  }

  function viewJobs() {
    const jobs = dayJobs().slice().sort((a, b) => (a.city || '').localeCompare(b.city || ''));
    const assigned = new Map();
    S.plan.routes.forEach(r => r.stops.forEach(s => assigned.set(s.job.id, r.tech)));
    const head = `<div class="page-head"><div><div class="eyebrow">${esc(dayLabel(S.date))}</div><h1>Jobs</h1><p>${jobs.length} on this day</p></div></div>
      <div class="toolbar">
        <button class="btn primary" data-act="workiz">Pull from Workiz</button>
        <button class="btn" data-act="csv">Import CSV</button>
        <button class="btn" data-act="new-job">Add a job</button>
      </div>`;
    if (!jobs.length) return head + empty('No jobs yet', 'Workiz: Jobs list → Export to CSV, then Import CSV here. Or add jobs by hand.', '<button class="btn" data-act="sample">Load a sample day</button>');
    const rows = jobs.map(j => {
      const t = assigned.get(j.id);
      return `<button class="row" data-act="edit-job" data-id="${esc(j.id)}" style="${t ? `--c:${esc(t.color)}` : ''}">
        <span class="stripe"></span>
        <span class="main"><span class="t">${esc(jobTitle(j))}</span>
          <span class="s">${esc(j.client)} · ${esc(place(j))}</span>
          <span class="skills">${catPill(j)}${j.guessed ? '<span class="pill warn">Check type</span>' : ''}${j.lat == null ? '<span class="pill warn">No map location</span>' : ''}</span></span>
        <span class="side">${t ? esc(t.name) : '<span class="flag">Not scheduled</span>'}<br>${dur(j.duration)}${window2(j) ? '<br>' + esc(window2(j)) : ''}</span>
      </button>`;
    }).join('');
    return head + `<div class="list">${rows}</div>
      <div class="btn-row"><button class="btn small danger" data-act="clear-day" data-confirm="Tap again to remove ${jobs.length} jobs">Remove all jobs on this day</button></div>`;
  }

  function skillPills(t) {
    const by = {};
    (t.skills || []).forEach(s => { const [c, w] = s.split(':'); (by[c] = by[c] || []).push(WRK[w]); });
    const list = CATEGORIES.filter(c => by[c.id]).map(c => `<span class="pill">${esc(c.label)}: ${esc(by[c.id].join(' + ').toLowerCase())}</span>`);
    return list.length ? list.join('') : '<span class="pill warn">No skills set</span>';
  }

  function viewTeam() {
    const head = `<div class="page-head"><div><h1>Team</h1><p>Who does what, and where they start the day.</p></div>
      <button class="btn primary" data-act="new-tech">Add a team member</button></div>`;
    if (!S.techs.length) return head + empty('No team members yet', 'Add each technician with the work they do. The schedule only sends a job to someone who can do it.', '');
    return head + `<div class="list">${S.techs.map(t => `<button class="row" data-act="edit-tech" data-id="${esc(t.id)}" style="--c:${esc(t.color)}">
      <span class="stripe"></span>
      <span class="main"><span class="t">${esc(t.name)} ${t.active === false ? '<span class="pill">Off</span>' : ''}</span>
        <span class="s">Starts ${esc(clockS(t.start))} from ${esc(t.home && (t.home.city || t.home.address) || 'no address')} · max ${esc(t.maxJobs)} jobs</span>
        <span class="skills">${skillPills(t)}</span></span>
      <span class="side">${esc(clockS(t.start))}<br>${esc(clockS(t.end))}</span></button>`).join('')}</div>`;
  }

  function viewSettings() {
    const st = S.settings, sv = S.server;
    const status = (on, yes, no) => `<div class="status ${sv ? (on ? 'on' : 'off') : ''}"><i></i>${sv ? (on ? yes : no) : 'Checking…'}</div>`;
    const durRows = CATEGORIES.map(c => `<tr><th>${esc(c.label)}</th>${WORK.map(w => `<td><input type="number" min="10" step="5" id="d-${w.id}-${c.id}" data-act="dur" data-w="${w.id}" data-c="${c.id}" value="${esc(st.durations[w.id][c.id])}" aria-label="${esc(c.label)} ${esc(w.label)} minutes"></td>`).join('')}</tr>`).join('');
    return `<div class="page-head"><div><h1>Settings</h1></div></div>
    <section class="card set-group"><h2>Connections</h2>
      ${status(sv && sv.workiz, 'Workiz connected', sv && sv.offline ? (NATIVE ? 'Workiz: add the website address below' : 'Workiz: available once the app is online on Netlify') : 'Workiz not connected')}
      ${status(sv && sv.google, 'Google Maps address lookup on', 'Google Maps lookup off: addresses are placed by town')}
      ${sv && sv.keySet && !sv.keyOk ? '<div class="status off"><i></i>Access key missing or wrong</div>' : ''}
      ${NATIVE || st.serverUrl ? `<label class="field"><span>Website address</span><input id="s-server" type="url" inputmode="url" autocomplete="off" placeholder="https://your-site.netlify.app" value="${esc(st.serverUrl)}" data-act="set-text" data-k="serverUrl"><span class="hint">The phone app gets Workiz jobs through your Icarus website.</span></label>` : ''}
      <label class="field"><span>Access key</span><input id="s-key" type="password" autocomplete="off" value="${esc(st.accessKey)}" data-act="set-text" data-k="accessKey"><span class="hint">The same key as APP_ACCESS_KEY on Netlify. It keeps customer data private.</span></label>
      <div class="btn-row"><button class="btn small" data-act="help-connect">How to connect</button></div>
    </section>
    <section class="card set-group"><h2>Planning</h2>
      <label class="field"><span>Average driving speed (km/h)</span><input type="number" id="s-speed" min="15" max="90" value="${esc(st.speedKmh)}" data-act="set" data-k="speedKmh"><span class="hint">Includes traffic. 35–45 suits most GTA days.</span></label>
      <div class="field"><span>Priority</span><div class="range-row"><span>Least driving</span><input type="range" id="s-balance" min="0" max="1" step="0.05" value="${esc(st.balance)}" data-act="set" data-k="balance" aria-label="Priority between least driving and even workload"><span>Even workload</span></div></div>
      <label class="field"><span>Booked time from Workiz becomes an arrival window of (minutes)</span><input type="number" id="s-window" min="0" step="15" value="${esc(st.arrivalWindow)}" data-act="set" data-k="arrivalWindow"></label>
      <label class="check"><input type="checkbox" id="s-home" ${st.returnHome ? 'checked' : ''} data-act="set" data-k="returnHome"> Count the drive back home in the day</label>
    </section>
    <section class="card set-group"><h2>Time on site (minutes)</h2>
      <div class="table-wrap"><table class="dur-table"><thead><tr><th></th>${WORK.map(w => `<th>${esc(w.label)}</th>`).join('')}</tr></thead><tbody>${durRows}</tbody></table></div>
      <p class="note">Used for new jobs. Each job's time can still be changed on the job.</p>
    </section>
    <section class="card set-group"><h2>Data</h2>
      <p class="note">Your team and jobs are saved on this device.</p>
      <div class="btn-row"><button class="btn small" data-act="sample">Load the sample day</button>
      <button class="btn small danger" data-act="wipe" data-confirm="Tap again to erase everything">Erase all data</button></div>
    </section>`;
  }

  // ---------- sheets (forms) ----------
  const sheet = () => $('#sheet');
  function openSheet(html) {
    const d = sheet();
    d.innerHTML = html;
    if (!d.open) { try { d.showModal(); } catch (e) { d.setAttribute('open', ''); } }
    const first = d.querySelector('input:not([type=hidden]):not([type=checkbox]):not([type=radio]), textarea');
    if (first && !first.readOnly) setTimeout(() => first.focus({ preventScroll: true }), 30);
  }
  function closeSheet() { const d = sheet(); if (d.open) d.close(); d.innerHTML = ''; }
  const sheetHead = t => `<div class="sheet-head"><h2 id="sheet-title">${esc(t)}</h2><button type="button" class="sheet-close" data-act="close" aria-label="Close">&times;</button></div>`;
  const opt = (v, label, sel) => `<option value="${esc(v)}" ${v === sel ? 'selected' : ''}>${esc(label)}</option>`;

  function jobForm(j) {
    const isNew = !j;
    j = j || { id: '', client: '', phone: '', address: '', city: '', category: 'window', work: 'repair', duration: S.settings.durations.repair.window, windowStart: '', windowEnd: '', notes: '', lockTech: '', type: '' };
    openSheet(`<form id="job-form" data-id="${esc(j.id)}" data-auto="${isNew ? 1 : 0}">${sheetHead(isNew ? 'Add a job' : 'Edit job')}
      <div class="grid2"><label class="field"><span>Customer</span><input id="f-client" value="${esc(j.client)}" autocomplete="off"></label>
      <label class="field"><span>Phone</span><input id="f-phone" type="tel" value="${esc(j.phone)}"></label></div>
      <label class="field"><span>Job description</span><input id="f-type" value="${esc(j.type)}" placeholder="e.g. Garage door spring repair"></label>
      <div class="grid2"><label class="field"><span>Street address</span><input id="f-address" value="${esc(j.address)}" required></label>
      <label class="field"><span>Town</span><input id="f-city" value="${esc(j.city)}" list="towns" required></label></div>
      <datalist id="towns">${CITIES.map(c => `<option value="${esc(c[0])}">`).join('')}</datalist>
      <div class="grid3"><label class="field"><span>Product</span><select id="f-cat">${CATEGORIES.map(c => opt(c.id, c.label, j.category)).join('')}</select></label>
      <label class="field"><span>Work</span><select id="f-work">${WORK.map(c => opt(c.id, c.label, j.work)).join('')}</select></label>
      <label class="field"><span>Minutes on site</span><input id="f-dur" type="number" min="10" step="5" value="${esc(j.duration)}"></label></div>
      <div class="grid2"><label class="field"><span>Arrive after</span><input id="f-ws" type="time" value="${esc(j.windowStart)}"></label>
      <label class="field"><span>Arrive before</span><input id="f-we" type="time" value="${esc(j.windowEnd)}"></label></div>
      <label class="field"><span>Technician</span><select id="f-lock">${opt('', 'Pick automatically', j.lockTech)}${S.techs.map(t => opt(t.id, t.name, j.lockTech)).join('')}</select></label>
      <label class="field"><span>Notes</span><textarea id="f-notes">${esc(j.notes)}</textarea></label>
      <div class="sheet-actions">${isNew ? '' : `<button type="button" class="btn danger" data-act="del-job" data-id="${esc(j.id)}" data-confirm="Tap again to delete">Delete</button>`}
        <div class="right"><button type="button" class="btn" data-act="close">Cancel</button><button class="btn primary" type="submit">${isNew ? 'Add job' : 'Save'}</button></div></div>
    </form>`);
  }

  async function submitJob(form) {
    const id = form.dataset.id;
    const old = S.jobs.find(x => x.id === id);
    const v = k => $('#' + k, form).value.trim();
    const j = Object.assign(old ? { ...old } : { id: uid(), source: 'manual', ref: '', date: S.date, lat: null, lng: null }, {
      client: v('f-client'), phone: v('f-phone'), type: v('f-type'), address: v('f-address'), city: v('f-city'),
      category: v('f-cat'), work: v('f-work'), duration: Number(v('f-dur')) || 60,
      windowStart: v('f-ws'), windowEnd: v('f-we'), lockTech: v('f-lock'), notes: v('f-notes'), guessed: false,
    });
    if (!old || old.address !== j.address || old.city !== j.city || j.lat == null) {
      const g = await geocode(j.address, j.city, j.postal);
      j.lat = g ? g.lat : null; j.lng = g ? g.lng : null; j.precise = g ? g.precise : false;
    }
    if (old) Object.assign(old, j); else S.jobs.push(j);
    closeSheet(); render();
    toast(j.lat == null ? 'Saved, but the address wasn\'t found on the map' : old ? 'Job saved' : 'Job added');
  }

  function techForm(t) {
    const isNew = !t;
    t = t || { id: '', name: '', color: PALETTE[S.techs.length % PALETTE.length], start: '08:00', end: '17:00', maxJobs: 6, active: true, home: { address: '', city: '' }, skills: [] };
    const sk = new Set(t.skills);
    const grid = `<table class="skill-grid"><thead><tr><th>Product</th><th>Repair</th><th>Install</th></tr></thead><tbody>${
      CATEGORIES.map(c => `<tr><td>${esc(c.label)}</td>${['repair', 'install'].map(w => `<td><input type="checkbox" name="sk" value="${c.id}:${w}" ${sk.has(c.id + ':' + w) ? 'checked' : ''} aria-label="${esc(c.label)} ${w}"></td>`).join('')}</tr>`).join('')
    }</tbody></table>`;
    openSheet(`<form id="tech-form" data-id="${esc(t.id)}">${sheetHead(isNew ? 'Add a team member' : 'Edit ' + t.name)}
      <label class="field"><span>Name</span><input id="t-name" value="${esc(t.name)}" required autocomplete="off"></label>
      <fieldset class="field"><legend>Colour on the map</legend><div class="swatches">${PALETTE.map((p, i) => `<label><input type="radio" name="color" id="t-c${i}" value="${p}" ${p === t.color ? 'checked' : ''} aria-label="Colour ${i + 1}"><span style="--c:${p}"></span></label>`).join('')}</div></fieldset>
      <fieldset class="field"><legend>Skills</legend>${grid}<span class="hint">Estimates go to anyone who works on that product.</span></fieldset>
      <div class="grid2"><label class="field"><span>Starts from (street)</span><input id="t-address" value="${esc(t.home.address)}"></label>
      <label class="field"><span>Town</span><input id="t-city" value="${esc(t.home.city)}" list="towns2" required></label></div>
      <datalist id="towns2">${CITIES.map(c => `<option value="${esc(c[0])}">`).join('')}</datalist>
      <div class="grid3"><label class="field"><span>Starts</span><input id="t-start" type="time" value="${esc(t.start)}"></label>
      <label class="field"><span>Ends</span><input id="t-end" type="time" value="${esc(t.end)}"></label>
      <label class="field"><span>Max jobs</span><input id="t-max" type="number" min="1" max="20" value="${esc(t.maxJobs)}"></label></div>
      <label class="check"><input type="checkbox" id="t-active" ${t.active !== false ? 'checked' : ''}> Working on the schedule</label>
      <div class="sheet-actions">${isNew ? '' : `<button type="button" class="btn danger" data-act="del-tech" data-id="${esc(t.id)}" data-confirm="Tap again to remove">Remove</button>`}
        <div class="right"><button type="button" class="btn" data-act="close">Cancel</button><button class="btn primary" type="submit">${isNew ? 'Add' : 'Save'}</button></div></div>
    </form>`);
  }

  async function submitTech(form) {
    const id = form.dataset.id;
    const old = techById(id);
    const v = k => $('#' + k, form).value.trim();
    const home = { address: v('t-address'), city: v('t-city') };
    const t = {
      id: old ? old.id : uid(), name: v('t-name') || 'Tech',
      color: (form.querySelector('input[name=color]:checked') || {}).value || PALETTE[0],
      start: v('t-start') || '08:00', end: v('t-end') || '17:00', maxJobs: Number(v('t-max')) || 6,
      active: $('#t-active', form).checked,
      skills: $$('input[name=sk]:checked', form).map(x => x.value),
      home: old ? { ...old.home, ...home } : home,
    };
    if (!old || old.home.address !== home.address || old.home.city !== home.city || t.home.lat == null) {
      const g = await geocode(home.address, home.city);
      t.home.lat = g ? g.lat : null; t.home.lng = g ? g.lng : null;
    }
    if (old) Object.assign(old, t); else S.techs.push(t);
    closeSheet(); render();
    toast(t.home.lat == null ? 'Saved, but the start address wasn\'t found' : 'Saved');
  }

  function routeText(r) {
    const lines = [`${r.tech.name}: ${dayLabel(S.date)}`, `Start ${clock(r.start)} from ${place(r.tech.home)}`, ''];
    r.stops.forEach((s, i) => {
      const j = s.job;
      lines.push(`${i + 1}. ${clock(s.arrive)}  ${jobTitle(j)} (${dur(j.duration)})`);
      lines.push(`   ${j.client}${j.phone ? ' · ' + j.phone : ''}`);
      lines.push(`   ${place(j)}`);
      if (j.notes) lines.push(`   Note: ${j.notes}`);
      lines.push(`   ${navUrl(j)}`);
      lines.push('');
    });
    lines.push(`Full route: ${routeUrl(r)}`);
    return lines.join('\n');
  }

  function copyRoute(id) {
    const r = S.plan.routes.find(x => x.tech.id === id);
    if (!r) return;
    const text = routeText(r);
    const show = () => {
      openSheet(`<div class="sheet-body">${sheetHead('Schedule for ' + r.tech.name)}<p class="note">Select the text and copy it into WhatsApp or a text message.</p><textarea class="copybox" id="copy-text" readonly>${esc(text)}</textarea></div>`);
      const ta = $('#copy-text'); ta.focus(); ta.select();
    };
    try {
      navigator.clipboard.writeText(text).then(() => toast(`Copied ${r.tech.name}'s day. Paste it in a message.`), show);
    } catch (e) { show(); }
  }

  function connectHelp(reason) {
    const offline = S.server && S.server.offline;
    openSheet(`<div class="sheet-body">${sheetHead('Connect Workiz')}
      ${reason ? `<p class="note"><b>${reason === 'unauthorized' ? 'The access key is missing or wrong.' : offline ? 'Workiz can\'t be reached from here.' : 'Workiz isn\'t connected yet.'}</b> ${reason === 'unauthorized' ? 'Enter the access key in Settings.' : offline ? (NATIVE ? 'Add your Icarus website address in Settings.' : 'Workiz is pulled once the app runs on its own site (Netlify). Until then, use Import CSV.') : ''}</p>` : ''}
      <h3>Pull jobs straight from Workiz</h3>
      <ol class="steps">
        <li>In Workiz, open <b>Feature Center / Marketplace</b> and turn on the <b>Developer API</b> add-on. Workiz may limit it to certain plans.</li>
        <li>Go to <b>Settings → Integrations → Developer</b> and copy the API token.</li>
        <li>In Netlify, open the site → <b>Site configuration → Environment variables</b>, add <code>WORKIZ_API_TOKEN</code> with the token, and <code>APP_ACCESS_KEY</code> with a long password of your choice. Redeploy.</li>
        <li>In this app, open <b>Settings</b> and enter the same access key${NATIVE ? ' and your website address' : ''}.</li>
      </ol>
      <h3>Exact addresses on the map</h3>
      <ol class="steps"><li>Create a Google Maps key with the <b>Geocoding API</b> turned on (Google Cloud Console).</li>
        <li>Add it in Netlify as <code>GOOGLE_MAPS_API_KEY</code>. Without it, jobs are placed by town, which is enough to group areas.</li></ol>
      <h3>No API? Use a CSV export</h3>
      <p class="note">In Workiz, filter the Jobs list to the day, choose <b>Export</b>, then use <b>Import CSV</b> here. Columns such as Address, City, Job Type, Client, Phone and Job Date are picked up automatically.</p>
      <div class="sheet-actions"><div class="right"><button class="btn primary" data-act="close">Done</button></div></div></div>`);
  }

  // ---------- import ----------
  function parseCSV(text) {
    const rows = []; let row = [], f = '', q = false;
    for (let i = 0; i < text.length; i++) {
      const c = text[i];
      if (q) { if (c === '"') { if (text[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += c; }
      else if (c === '"') q = true;
      else if (c === ',') { row.push(f); f = ''; }
      else if (c === '\n' || c === '\r') { if (c === '\r' && text[i + 1] === '\n') i++; row.push(f); rows.push(row); row = []; f = ''; }
      else f += c;
    }
    if (f || row.length) { row.push(f); rows.push(row); }
    return rows.filter(r => r.some(x => x.trim()));
  }

  const COLS = {
    ref: [/^(job ?#|job ?id|job ?number|serial ?id|uuid|id)$/],
    address: [/^address$/, /street|address 1|address$/, /location/],
    city: [/^city$/, /city|town/],
    postal: [/postal|zip/],
    type: [/job ?type/, /^type$/, /service/, /title/],
    client: [/^client$/, /client ?name|customer|^name$|full ?name/],
    first: [/first/], last: [/last ?name/],
    phone: [/phone|mobile|cell/],
    date: [/job ?date|scheduled|start ?date|^date$|date ?time/],
    end: [/end ?(time|date)/],
    lat: [/^lat/], lng: [/^(lng|lon)/],
    notes: [/note|description/],
  };

  function readDateTime(s) {
    s = String(s || '').trim();
    let date = '', time = '';
    let m = /(\d{4})-(\d{1,2})-(\d{1,2})/.exec(s);
    if (m) date = `${m[1]}-${m[2].padStart(2, '0')}-${m[3].padStart(2, '0')}`;
    else if ((m = /(\d{1,2})\/(\d{1,2})\/(\d{4})/.exec(s))) date = `${m[3]}-${m[1].padStart(2, '0')}-${m[2].padStart(2, '0')}`;
    const t = /(\d{1,2}):(\d{2})\s*(am|pm)?/i.exec(s.replace(/^\S*\d{4}\S*/, ''));
    if (t) { let h = Number(t[1]); const ap = (t[3] || '').toLowerCase(); if (ap === 'pm' && h < 12) h += 12; if (ap === 'am' && h === 12) h = 0; time = `${String(h).padStart(2, '0')}:${t[2]}`; }
    return { date, time };
  }

  function rowsToRecords(rows) {
    const head = rows[0].map(h => h.trim().toLowerCase());
    const idx = {};
    for (const [k, pats] of Object.entries(COLS)) {
      for (const p of pats) { const i = head.findIndex((h, n) => p.test(h) && !Object.values(idx).includes(n)); if (i >= 0) { idx[k] = i; break; } }
    }
    return rows.slice(1).map(r => {
      const g = k => (idx[k] != null ? String(r[idx[k]] || '').trim() : '');
      const dt = readDateTime(g('date'));
      return {
        ref: g('ref'), client: g('client') || [g('first'), g('last')].filter(Boolean).join(' '), phone: g('phone'),
        address: g('address'), city: g('city'), postal: g('postal'), type: g('type'), notes: g('notes'),
        lat: g('lat') ? Number(g('lat')) : null, lng: g('lng') ? Number(g('lng')) : null,
        date: dt.date, time: dt.time, endTime: readDateTime(g('end')).time,
      };
    }).filter(x => x.address || x.city);
  }

  // Shared by CSV and Workiz: turns plain records into jobs, skipping ones already in the list.
  async function addRecords(recs, source) {
    let added = 0, approx = 0;
    for (const r of recs) {
      const date = r.date || S.date;
      if (r.ref && S.jobs.some(j => j.source === source && j.ref === r.ref && j.date === date)) continue;
      const c = classifyJob(r.type || r.notes);
      const ws = r.time || '';
      let we = '';
      if (ws && S.settings.arrivalWindow > 0) { const m = toMin(ws) + Number(S.settings.arrivalWindow); we = `${String(Math.floor(m / 60) % 24).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`; }
      const j = {
        id: uid(), source, ref: r.ref || '', date, client: r.client || '', phone: r.phone || '', type: r.type || '',
        category: c.category, work: c.work, guessed: c.guessed, duration: S.settings.durations[c.work][c.category],
        address: r.address || '', city: r.city || '', postal: r.postal || '', notes: r.notes || '',
        windowStart: ws, windowEnd: we, lockTech: '', lat: null, lng: null, precise: true,
      };
      if (Number.isFinite(r.lat) && Number.isFinite(r.lng) && r.lat !== 0) { j.lat = r.lat; j.lng = r.lng; }
      else {
        const g = await geocode(j.address, j.city, j.postal);
        if (g) { j.lat = g.lat; j.lng = g.lng; j.precise = g.precise; if (!g.precise) approx++; if (!j.city) j.city = g.city || ''; }
      }
      S.jobs.push(j); added++;
    }
    return { added, approx };
  }

  async function importCSV(file) {
    const text = await file.text();
    const rows = parseCSV(text);
    if (rows.length < 2) { toast('That file has no rows to import'); return; }
    const recs = rowsToRecords(rows);
    if (!recs.length) { toast('No address column found. The file needs Address and City columns.'); return; }
    removeSample();
    toast('Importing…');
    const { added, approx } = await addRecords(recs, 'csv');
    const other = recs.filter(r => r.date && r.date !== S.date).length;
    render();
    toast(`Imported ${added} job${added === 1 ? '' : 's'}${approx ? `, ${approx} placed by town` : ''}${other ? ` (${other} on other days)` : ''}`);
  }

  async function pullWorkiz() {
    toast('Checking Workiz…');
    try {
      const r = await api('/api/workiz-jobs?date=' + enc(S.date), { cache: 'no-store' });
      const d = await r.json().catch(() => null);
      if (!r.ok || !d || d.error) throw new Error((d && d.error) || 'not-connected');
      removeSample();
      const { added, approx } = await addRecords(d.jobs || [], 'workiz');
      render();
      toast(added ? `Pulled ${added} new job${added === 1 ? '' : 's'} from Workiz${approx ? `, ${approx} placed by town` : ''}` : 'No new jobs in Workiz for this day');
    } catch (e) {
      hideToast();
      connectHelp(e.message || 'not-connected');
    }
  }

  function removeSample() {
    if (S.jobs.some(j => j.source === 'sample')) S.jobs = S.jobs.filter(j => j.source !== 'sample');
  }

  // ---------- toast ----------
  let toastTimer;
  function toast(msg) {
    const t = $('#toast'); t.textContent = msg; t.hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(hideToast, 3200);
  }
  function hideToast() { $('#toast').hidden = true; }

  // ---------- events ----------
  function armed(btn) {
    if (!btn.dataset.confirm) return true;
    if (btn.dataset.armed === '1') return true;
    btn.dataset.armed = '1'; btn.dataset.label = btn.textContent; btn.textContent = btn.dataset.confirm;
    setTimeout(() => { if (btn.isConnected) { btn.dataset.armed = ''; btn.textContent = btn.dataset.label; } }, 3500);
    return false;
  }

  function setTab(tab) {
    S.tab = TABS.includes(tab) ? tab : 'plan';
    try { history.replaceState(null, '', '#' + S.tab); } catch (e) { /* ignore */ }
    render();
    window.scrollTo(0, 0);
  }

  document.addEventListener('click', e => {
    const link = e.target.closest('a[target="_blank"]');
    if (link && NATIVE) { e.preventDefault(); openExternal(link.href); return; }
    const b = e.target.closest('[data-act]');
    if (!b || b.tagName === 'SELECT' || (b.tagName === 'INPUT' && b.type !== 'button')) return;
    const act = b.dataset.act, id = b.dataset.id;
    switch (act) {
      case 'tab': setTab(b.dataset.tab); break;
      case 'day': { const d = new Date(S.date + 'T12:00:00'); d.setDate(d.getDate() + Number(b.dataset.step)); S.date = isoDate(d); render(); break; }
      case 'new-job': jobForm(null); break;
      case 'edit-job': jobForm(S.jobs.find(j => j.id === id)); break;
      case 'del-job': if (armed(b)) { S.jobs = S.jobs.filter(j => j.id !== id); closeSheet(); render(); toast('Job deleted'); } break;
      case 'new-tech': techForm(null); break;
      case 'edit-tech': techForm(techById(id)); break;
      case 'del-tech': if (armed(b)) { S.techs = S.techs.filter(t => t.id !== id); S.jobs.forEach(j => { if (j.lockTech === id) j.lockTech = ''; }); closeSheet(); render(); toast('Removed'); } break;
      case 'close': closeSheet(); break;
      case 'copy-route': copyRoute(id); break;
      case 'workiz': pullWorkiz(); break;
      case 'csv': $('#csv-file').click(); break;
      case 'help-connect': connectHelp(''); break;
      case 'sample': { const d = sampleData(S.date); S.techs = d.techs; removeSample(); S.jobs = S.jobs.filter(j => j.date !== S.date).concat(d.jobs); setTab('plan'); toast('Sample day loaded'); break; }
      case 'clear-day': if (armed(b)) { S.jobs = S.jobs.filter(j => j.date !== S.date); render(); toast('Jobs removed'); } break;
      case 'wipe': if (armed(b)) { S.techs = []; S.jobs = []; S.settings = JSON.parse(JSON.stringify(DEFAULT_SETTINGS)); render(); toast('All data erased'); } break;
    }
  });

  document.addEventListener('change', e => {
    const el = e.target;
    if (el.id === 'date') { if (el.value) { S.date = el.value; render(); } return; }
    if (el.id === 'csv-file') { const f = el.files[0]; el.value = ''; if (f) importCSV(f); return; }
    if (el.id === 'f-cat' || el.id === 'f-work') {
      const form = el.form;
      const c = $('#f-cat', form).value, w = $('#f-work', form).value;
      if (form.dataset.auto === '1') $('#f-dur', form).value = S.settings.durations[w][c];
      return;
    }
    if (el.id === 'f-dur') { el.form.dataset.auto = '0'; return; }
    const act = el.dataset.act;
    if (act === 'assign') {
      const j = S.jobs.find(x => x.id === el.dataset.id);
      if (j && el.value) { j.lockTech = el.value; render(); toast(`Assigned to ${techById(el.value).name}`); }
    } else if (act === 'set') {
      const k = el.dataset.k;
      S.settings[k] = el.type === 'checkbox' ? el.checked : Number(el.value);
      save();
    } else if (act === 'set-text') {
      S.settings[el.dataset.k] = el.value.trim();
      save(); checkServer();
    } else if (act === 'dur') {
      const n = Number(el.value);
      if (n > 0) { S.settings.durations[el.dataset.w][el.dataset.c] = n; save(); }
    }
  });

  document.addEventListener('submit', e => {
    e.preventDefault();
    const f = e.target;
    const btn = f.querySelector('[type=submit]'); if (btn) btn.disabled = true;
    const done = () => { if (btn) btn.disabled = false; };
    if (f.id === 'job-form') submitJob(f).catch(done);
    else if (f.id === 'tech-form') submitTech(f).catch(done);
  });

  sheet().addEventListener('click', e => { if (e.target === sheet()) closeSheet(); });
  sheet().addEventListener('close', () => { sheet().innerHTML = ''; });

  // ---------- start ----------
  function start() {
    const saved = load();
    S.settings = JSON.parse(JSON.stringify(DEFAULT_SETTINGS));
    if (saved) {
      S.techs = saved.techs || []; S.jobs = saved.jobs || [];
      const st = saved.settings || {};
      Object.assign(S.settings, st, { durations: { ...S.settings.durations, ...(st.durations || {}) } });
      // Keep the sample day on today's date.
      if (S.jobs.length && S.jobs.every(j => j.source === 'sample')) S.jobs.forEach(j => { j.date = S.date; });
    } else {
      const d = sampleData(S.date); S.techs = d.techs; S.jobs = d.jobs;
    }
    const h = (location.hash || '').slice(1);
    if (TABS.includes(h)) S.tab = h;
    render();
    checkServer();
    if (!NATIVE && 'serviceWorker' in navigator && location.protocol === 'https:' && !/claude|claudeusercontent/.test(location.host)) {
      navigator.serviceWorker.register('sw.js').catch(() => {});
    }
  }
  start();
})();
