# Icarus Dispatch

Sorts the day's jobs by technician skills and area, and builds each tech's route.
It runs as a website, and as a phone app for Android and iPhone (built with Capacitor from the same code).

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
- `netlify/functions/`: small server pieces that keep keys out of the browser. Workiz and address lookups need the
  access key (`APP_ACCESS_KEY`), so customer data isn't open to anyone who finds the address.
  - `workiz-jobs.mjs` → `/api/workiz-jobs?date=YYYY-MM-DD`
  - `geocode.mjs` → `/api/geocode?q=address` (Google Geocoding)
  - `status.mjs` → `/api/status`

## Phone app (Android and iPhone)

The phone apps are the same `app/` folder inside a native shell (Capacitor). App id: `ca.icarus.dispatch`.

- `android/`, `ios/`: the native projects. After changing anything in `app/`, run `npx cap sync`.
- `assets/`: app icon and launch screen sources. Regenerate with
  `npx @capacitor/assets generate --android --ios --iconBackgroundColor '#14201D' --splashBackgroundColor '#14201D'`.
- In the phone app, Google Maps links open the Maps app and phone numbers start a call.
- The phone app reaches Workiz through the website: enter the website address and access key under Settings
  (or set `ICARUS_SERVER` in `app/config.js` before building).

**Android**
- Test build: `npm run android:apk` → `android/app/build/outputs/apk/debug/app-debug.apk`. Install it on a phone
  (allow "install unknown apps"). GitHub builds the same file on every push (Actions → Android app → Artifacts).
- Google Play: create a Play Console account (one-time US$25), make an upload key, then `npm run android:release`
  and upload the `.aab` from `android/app/build/outputs/bundle/release/`.

**iPhone**
- Needs a Mac with Xcode and an Apple Developer account (US$99/year).
- `npm install && npm run ios:open`, pick your team under Signing, then run it on a connected iPhone,
  or Product → Archive to send it to TestFlight / the App Store.
- Without a Mac, a cloud build service (for example Codemagic or a GitHub macOS runner) can build and sign it
  with the Apple account's certificates.

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
   - `APP_ACCESS_KEY`: a long password you choose. Enter the same key in the app under Settings.
3. Redeploy. Settings in the app shows whether each connection is on.

## Not done yet / next steps

- The Workiz pull has not been tested against a live account. Check the first pull and adjust `normalize()` in
  `workiz-jobs.mjs` if fields differ.
- Drive times are estimates (distance × 1.3 at an average speed). Real traffic times can come from the
  Google Routes API later.
- Sending assignments back into Workiz (assign tech, set time).
- Shared data across devices (a small database) and logins for techs.
- Google Maps route links show up to about 9 stops per route.
