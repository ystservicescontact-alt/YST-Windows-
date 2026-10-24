// Turns an address into map coordinates with the Google Geocoding API.
// Needs GOOGLE_MAPS_API_KEY in Netlify environment variables. The key never reaches the browser.
export default async (req) => {
  const key = process.env.GOOGLE_MAPS_API_KEY;
  if (!key) return Response.json({ error: 'not-connected' }, { status: 503 });
  const q = new URL(req.url).searchParams.get('q');
  if (!q) return Response.json({ error: 'missing-address' }, { status: 400 });
  try {
    const r = await fetch(`https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(q)}&region=ca&key=${key}`);
    const d = await r.json();
    const g = d.results && d.results[0];
    if (!g) return Response.json({ error: 'not-found', status: d.status }, { status: 404 });
    const part = t => (g.address_components.find(c => c.types.includes(t)) || {}).long_name || '';
    return Response.json(
      { lat: g.geometry.location.lat, lng: g.geometry.location.lng, city: part('locality') || part('sublocality'), formatted: g.formatted_address },
      { headers: { 'cache-control': 'public, max-age=86400' } },
    );
  } catch (e) {
    return Response.json({ error: 'google-unreachable' }, { status: 502 });
  }
};

export const config = { path: '/api/geocode' };
