// Pulls one day's open jobs from Workiz (API v1) and returns them in the app's simple shape.
// Needs WORKIZ_API_TOKEN and APP_ACCESS_KEY in Netlify environment variables. The token never reaches the browser.
// Not yet tested against a live Workiz account: field names follow Workiz's v1 job records
// and are read defensively, so check the first pull and adjust normalize() if needed.
const BASE = 'https://api.workiz.com/api/v1';

import { reply, preflight, authorized } from '../lib/http.mjs';

export default async (req) => {
  const pre = preflight(req);
  if (pre) return pre;
  if (!authorized(req)) return reply(req, { error: 'unauthorized' }, 401);
  const token = process.env.WORKIZ_API_TOKEN;
  if (!token) return reply(req, { error: 'not-connected' }, 503);
  const date = new URL(req.url).searchParams.get('date') || new Date().toISOString().slice(0, 10);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) return reply(req, { error: 'bad-date' }, 400);

  const rows = [];
  try {
    for (let offset = 0; offset < 1000; offset += 100) {
      const r = await fetch(`${BASE}/${token}/job/all/?start_date=${date}&offset=${offset}&records=100&only_open=true`);
      if (!r.ok) return reply(req, { error: `workiz-${r.status}` }, 502);
      const body = await r.json();
      const page = Array.isArray(body.data) ? body.data : Array.isArray(body) ? body : [];
      rows.push(...page);
      if (page.length < 100) break;
    }
  } catch (e) {
    return reply(req, { error: 'workiz-unreachable' }, 502);
  }

  const jobs = rows.map(normalize).filter(j => !j.date || j.date === date);
  return reply(req, { date, jobs });
};

const num = v => (v === null || v === undefined || v === '' ? null : Number(v));
const pick = (o, ...keys) => { for (const k of keys) if (o[k] !== undefined && o[k] !== null && o[k] !== '') return o[k]; return ''; };

function normalize(j) {
  const start = String(pick(j, 'JobDateTime', 'job_date_time', 'StartDate'));
  const end = String(pick(j, 'JobEndDateTime', 'job_end_date_time', 'EndDate'));
  return {
    ref: String(pick(j, 'UUID', 'uuid', 'SerialId', 'id')),
    number: String(pick(j, 'SerialId', 'serial_id')),
    client: [pick(j, 'FirstName', 'first_name'), pick(j, 'LastName', 'last_name')].filter(Boolean).join(' ') || String(pick(j, 'Company', 'ClientName')),
    phone: String(pick(j, 'Phone', 'phone')),
    address: String(pick(j, 'Address', 'address')),
    city: String(pick(j, 'City', 'city')),
    postal: String(pick(j, 'PostalCode', 'postal_code', 'Zip')),
    lat: num(pick(j, 'Latitude', 'latitude', 'lat')),
    lng: num(pick(j, 'Longitude', 'longitude', 'lng')),
    type: String(pick(j, 'JobType', 'job_type', 'Type')),
    notes: String(pick(j, 'JobNotes', 'job_notes', 'Comments')),
    status: String(pick(j, 'Status', 'status')),
    date: start.slice(0, 10),
    time: start.slice(11, 16),
    endTime: end.slice(11, 16),
  };
}
