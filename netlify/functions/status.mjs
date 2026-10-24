// Tells the app which connections are set up, without exposing the keys.
export default async () =>
  Response.json({ workiz: !!process.env.WORKIZ_API_TOKEN, google: !!process.env.GOOGLE_MAPS_API_KEY });

export const config = { path: '/api/status' };
