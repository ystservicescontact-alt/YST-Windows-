// Tells the app which connections are set up, without exposing the keys.
import { reply, preflight, authorized } from '../lib/http.mjs';

export default async (req) => preflight(req) || reply(req, {
  workiz: !!process.env.WORKIZ_API_TOKEN,
  google: !!process.env.GOOGLE_MAPS_API_KEY,
  keySet: !!process.env.APP_ACCESS_KEY,
  keyOk: authorized(req),
});

export const config = { path: '/api/status' };
