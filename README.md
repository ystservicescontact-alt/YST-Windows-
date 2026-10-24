# Icarus Dispatch

Sorts the day's jobs by technician skills and area, and builds each tech's route.
It runs as a website and installs on a phone like an app (Add to Home Screen).

## What it does

- **Team:** each tech has skills (Windows, Sliding doors, Garage doors, Entry doors, Other × Repair / Install),
  a start address, working hours and a job limit. Estimates go to anyone who works on that product.
- **Jobs:** pulled from Workiz, imported from a Workiz CSV export, or added by hand. The job type text
  ("Garage door spring repair") is read to guess product and repair/install; the guess can be changed per job.
- **Schedule:** every job goes only to a tech who can do it. Jobs are grouped by area, ordered to cut driving,
  and checked against time windows and working hours. Jobs that can't fit are listed with the reason, with an
  "Assign to…" option.
- **On the road:** "Open route in Google Maps" for each tech's whole day, "Navigate" for each stop,
  and "Copy for tech" to paste the day into WhatsApp or a text.

Data is saved in the browser on each device for now.

## Files

- `app/`: the app itself (plain HTML/CSS/JS, no build step).
  - `scheduler.js`: the planning logic (no page code).
  - `data.js`: product types, default job lengths, GTA towns, the sample day.
  - `app.js`: screens and actions. `styles.css`: look.
  - `manifest.webmanifest`, `sw.js`, `icons/`: installable app and offline opening.
- `netlify/functions/`: small server pieces that keep keys out of the browser.
  - `workiz-jobs.mjs` → `/api/workiz-jobs?date=YYYY-MM-DD`
  - `geocode.mjs` → `/api/geocode?q=address` (Google Geocoding)
  - `status.mjs` → `/api/status`

## Run locally

```
cd app && python3 -m http.server 8000
```

The `/api/...` parts need Netlify (`npx netlify dev`). Without them the app still works, placing addresses by town.

## Go live on Netlify

1. New site → Import from Git → pick this repository. No build command; publish directory is `app` (set in `netlify.toml`).
2. Site configuration → Environment variables:
   - `WORKIZ_API_TOKEN`: from Workiz → Settings → Integrations → Developer (turn on the Developer API add-on first).
   - `GOOGLE_MAPS_API_KEY`: a Google Cloud key with the Geocoding API turned on.
3. Redeploy. Settings in the app shows whether each connection is on.

## Not done yet / next steps

- The Workiz pull has not been tested against a live account. Check the first pull and adjust `normalize()` in
  `workiz-jobs.mjs` if fields differ.
- Drive times are estimates (distance × 1.3 at an average speed). Real traffic times can come from the
  Google Routes API later.
- Sending assignments back into Workiz (assign tech, set time).
- Shared data across devices (a small database) and logins for techs.
- App store versions: wrap `app/` with Capacitor when needed.
- Google Maps route links show up to about 9 stops per route.
