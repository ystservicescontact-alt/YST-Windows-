// Turns an address into map coordinates with the Google Geocoding API.
// Needs GOOGLE_MAPS_API_KEY and APP_ACCESS_KEY in Netlify environment variables. The Google key never reaches the browser.
import { reply, preflight, authorized } from '../lib/http.mjs';

export default async (req) => {
  const pre = preflight(req);
  if (pre) return pre;
  if (!authorized(req)) return reply(req, { error: 'unauthorized' }, 401);
  const key = process.env.GOOGLE_MAPS_API_KEY;
  if (!key) return reply(req, { error: 'not-connected' }, 503);
  const q = new URL(req.url).searchParams.get('q');
  if (!q) return reply(req, { error: 'missing-address' }, 400);
  try {
    const r = await fetch(`https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(q)}&region=ca&key=${key}`);
    const d = await r.json();
    const g = d.results && d.results[0];
    if (!g) return reply(req, { error: 'not-found', status: d.status }, 404);
    const part = t => (g.address_components.find(c => c.types.includes(t)) || {}).long_name || '';
    return reply(req,
      { lat: g.geometry.location.lat, lng: g.geometry.location.lng, city: part('locality') || part('sublocality'), formatted: g.formatted_address },
      200, { 'cache-control': 'private, max-age=86400' },
    );
  } catch (e) {
    return reply(req, { error: 'google-unreachable' }, 502);
  }
};

export const config = { path: '/api/geocode' };
