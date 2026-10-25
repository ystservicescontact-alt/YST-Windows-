// Shared by the server functions: lets the phone app connect (CORS) and checks the access key.

// The installed app loads from these addresses (Android, iOS).
const APP_ORIGINS = ['https://localhost', 'http://localhost', 'capacitor://localhost'];

function corsHeaders(req) {
  const origin = req.headers.get('origin') || '';
  if (!APP_ORIGINS.includes(origin)) return {};
  return {
    'access-control-allow-origin': origin,
    'access-control-allow-headers': 'x-icarus-key, content-type',
    'access-control-allow-methods': 'GET, OPTIONS',
    'access-control-max-age': '86400',
    vary: 'origin',
  };
}

export function reply(req, body, status = 200, extra = {}) {
  return Response.json(body, { status, headers: { ...corsHeaders(req), ...extra } });
}

// Answers the browser's pre-check for cross-site requests from the phone app.
export function preflight(req) {
  return req.method === 'OPTIONS' ? new Response(null, { status: 204, headers: corsHeaders(req) }) : null;
}

// Customer data needs the key set as APP_ACCESS_KEY. Without that variable, nothing is served.
export function authorized(req) {
  const key = process.env.APP_ACCESS_KEY;
  if (!key) return false;
  const given = req.headers.get('x-icarus-key') || '';
  if (given.length !== key.length) return false;
  let diff = 0;
  for (let i = 0; i < key.length; i++) diff |= key.charCodeAt(i) ^ given.charCodeAt(i);
  return diff === 0;
}
