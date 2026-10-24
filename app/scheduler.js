// Planning logic. No page code here, so it can be tested on its own or moved to a server later.
//
// How a day is planned:
// 1. A job can only go to a tech who has the skill (category + repair/install).
//    Estimates go to anyone who works on that category.
// 2. Jobs are placed one by one, hardest first (fewest techs who can do it, tightest time window),
//    each at the spot in a tech's day that adds the least driving and keeps everyone's day reasonable.
// 3. Routes are then tidied: stops are reordered and jobs are moved between techs while that cuts driving.
// Drive times are estimated from straight-line distance (x1.3 for roads) and an average speed.

const Planner = (() => {
  const ROAD_FACTOR = 1.3;

  const toMin = s => {
    const m = /^(\d{1,2}):(\d{2})/.exec(s || '');
    return m ? Number(m[1]) * 60 + Number(m[2]) : null;
  };

  function km(a, b) {
    if (!a || !b || a.lat == null || b.lat == null) return 0;
    const r = Math.PI / 180;
    const dLat = (b.lat - a.lat) * r, dLng = (b.lng - a.lng) * r;
    const x = Math.sin(dLat / 2) ** 2 + Math.cos(a.lat * r) * Math.cos(b.lat * r) * Math.sin(dLng / 2) ** 2;
    return 2 * 6371 * Math.asin(Math.sqrt(x));
  }

  function leg(a, b, s) {
    const road = km(a, b) * ROAD_FACTOR;
    if (road < 0.3) return { km: road, min: 0 };
    return { km: road, min: Math.max(5, (road / (s.speedKmh || 40)) * 60) };
  }

  function canDo(tech, job) {
    const sk = tech.skills || [];
    if (job.work === 'estimate') return sk.some(x => x.startsWith(job.category + ':'));
    return sk.includes(job.category + ':' + job.work);
  }

  // Walk through a tech's day in order and work out times.
  function simulate(tech, jobs, s) {
    const start = toMin(tech.start) ?? 480, end = toMin(tech.end) ?? 1020;
    let t = start, pos = tech.home, drive = 0, dist = 0, work = 0, late = 0, waited = 0;
    const stops = [];
    for (const job of jobs) {
      const l = leg(pos, job, s);
      t += l.min; drive += l.min; dist += l.km;
      const ws = toMin(job.windowStart), we = toMin(job.windowEnd);
      let wait = 0;
      if (ws != null && t < ws) { wait = ws - t; t = ws; waited += wait; }
      const lateBy = we != null && t > we + 0.5 ? t - we : 0;
      late += lateBy;
      const dur = Number(job.duration) || 60;
      stops.push({ job, arrive: t, depart: t + dur, drive: l.min, km: l.km, wait, lateBy });
      t += dur; work += dur; pos = job;
    }
    const back = jobs.length && s.returnHome ? leg(pos, tech.home, s) : { km: 0, min: 0 };
    const finish = t + back.min;
    const over = Math.max(0, finish - end);
    const tooMany = jobs.length > (Number(tech.maxJobs) || 99);
    return {
      stops, start, end, finish, back, waited,
      drive: drive + back.min, km: dist + back.km, work, late, over, tooMany,
      ok: late === 0 && over <= 0 && !tooMany,
    };
  }

  // Lower is better. Driving counts fully, idle waiting a little; long days cost extra so work spreads out;
  // a broken day (late, overtime, too many jobs) costs a lot.
  function cost(sim, s) {
    const busy = sim.work + sim.drive;
    const bal = Number(s.balance ?? 0.3);
    let c = sim.drive + 0.3 * sim.waited + (bal * busy * busy) / 480;
    if (!sim.ok) c += 10000 + sim.late * 50 + sim.over * 50 + (sim.tooMany ? 5000 : 0);
    return c;
  }

  function windowLen(j) {
    const a = toMin(j.windowStart), b = toMin(j.windowEnd);
    if (a == null && b == null) return 9999;
    return (b ?? 1440) - (a ?? 0);
  }

  function plan(allJobs, allTechs, s) {
    const techs = allTechs.filter(t => t.active !== false && t.home && t.home.lat != null);
    const byId = new Map(techs.map(t => [t.id, t]));
    const routes = new Map(techs.map(t => [t.id, []]));
    const unassigned = [];

    const sim = (id, list) => simulate(byId.get(id), list, s);
    const routeCost = (id, list) => cost(sim(id, list), s);

    function bestInsert(id, list, job, requireOk) {
      let best = null;
      for (let i = 0; i <= list.length; i++) {
        const cand = [...list.slice(0, i), job, ...list.slice(i)];
        const sm = sim(id, cand);
        if (requireOk && !sm.ok) continue;
        const c = cost(sm, s);
        if (!best || c < best.c) best = { c, list: cand };
      }
      return best;
    }

    const mapped = [];
    for (const j of allJobs) {
      if (j.lat == null) unassigned.push({ job: j, code: 'noAddress', techs: [] });
      else mapped.push(j);
    }

    const isLocked = j => j.lockTech && byId.has(j.lockTech);
    const elig = new Map(mapped.map(j => [j.id, techs.filter(t => canDo(t, j))]));

    // Jobs assigned by hand go first, to the tech chosen, even if the day ends up too long.
    mapped.filter(isLocked).sort((a, b) => windowLen(a) - windowLen(b)).forEach(j => {
      routes.set(j.lockTech, bestInsert(j.lockTech, routes.get(j.lockTech), j, false).list);
    });

    function place(j) {
      let best = null;
      for (const t of elig.get(j.id)) {
        const list = routes.get(t.id);
        const b = bestInsert(t.id, list, j, true);
        if (!b) continue;
        const d = b.c - routeCost(t.id, list);
        if (!best || d < best.d) best = { id: t.id, d, list: b.list };
      }
      if (best) routes.set(best.id, best.list);
      return !!best;
    }

    function improve() {
      for (let pass = 0; pass < 6; pass++) {
        let changed = false;
        // Reorder each tech's stops.
        for (const t of techs) {
          let list = routes.get(t.id), c = routeCost(t.id, list), better = true, guard = 0;
          while (better && guard++ < 200) {
            better = false;
            for (let i = 0; i < list.length && !better; i++) {
              for (let k = i + 1; k < list.length && !better; k++) {
                const cand = [...list.slice(0, i), ...list.slice(i, k + 1).reverse(), ...list.slice(k + 1)];
                const cc = routeCost(t.id, cand);
                if (cc < c - 0.01) { list = cand; c = cc; better = true; }
              }
            }
            for (let i = 0; i < list.length && !better; i++) {
              const rest = list.filter((_, x) => x !== i);
              for (let p = 0; p <= rest.length && !better; p++) {
                if (p === i) continue;
                const cand = [...rest.slice(0, p), list[i], ...rest.slice(p)];
                const cc = routeCost(t.id, cand);
                if (cc < c - 0.01) { list = cand; c = cc; better = true; }
              }
            }
            if (better) changed = true;
          }
          routes.set(t.id, list);
        }
        // Move jobs between techs when that saves overall.
        for (const a of techs) {
          for (const j of [...routes.get(a.id)]) {
            if (isLocked(j)) continue;
            const cur = routes.get(a.id);
            const without = cur.filter(x => x !== j);
            const gain = routeCost(a.id, cur) - routeCost(a.id, without);
            for (const b of elig.get(j.id)) {
              if (b.id === a.id) continue;
              const lb = routes.get(b.id);
              const ins = bestInsert(b.id, lb, j, true);
              if (!ins) continue;
              if (ins.c - routeCost(b.id, lb) < gain - 0.5) {
                routes.set(a.id, without); routes.set(b.id, ins.list); changed = true; break;
              }
            }
          }
        }
        if (!changed) break;
      }
    }

    const free = mapped.filter(j => !isLocked(j)).sort((a, b) =>
      elig.get(a.id).length - elig.get(b.id).length ||
      windowLen(a) - windowLen(b) ||
      (Number(b.duration) || 0) - (Number(a.duration) || 0));

    const pending = [];
    for (const j of free) {
      if (!elig.get(j.id).length) unassigned.push({ job: j, code: 'noSkill', techs: [] });
      else if (!place(j)) pending.push(j);
    }
    improve();
    let retried = false;
    for (const j of pending) {
      if (place(j)) retried = true;
      else unassigned.push({ job: j, code: 'noRoom', techs: elig.get(j.id).map(t => t.name) });
    }
    if (retried) improve();

    const out = techs.map(t => {
      const list = routes.get(t.id);
      const sm = simulate(t, list, s);
      const counts = {};
      list.forEach(j => { const a = nearestCity(j.lat, j.lng); counts[a] = (counts[a] || 0) + 1; });
      const areas = Object.entries(counts).sort((x, y) => y[1] - x[1]).map(e => e[0]);
      return { tech: t, ...sm, areas };
    });

    const skipped = allTechs.filter(t => t.active !== false && !(t.home && t.home.lat != null));
    return {
      routes: out,
      unassigned,
      skipped,
      totals: {
        jobs: allJobs.length,
        scheduled: out.reduce((n, r) => n + r.stops.length, 0),
        drive: out.reduce((n, r) => n + r.drive, 0),
        km: out.reduce((n, r) => n + r.km, 0),
      },
    };
  }

  return { plan, simulate, canDo, toMin, km };
})();
