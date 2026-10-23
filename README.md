# Window Repair GTA

Static website for Window Repair GTA (window, glass and patio door repair in Toronto and the GTA).

## Structure

- `content.py`: all page text (services, city pages, home, contact). Edit here.
- `build.py`: builds the site into `site/`. Business name, phone and domain are in `SITE` at the top.
- `src/assets/`: CSS, the foggy-glass demo script and the favicon.
- `netlify.toml`: Netlify runs `python3 build.py` and publishes `site/`.

Build locally:

```
python3 build.py
cd site && python3 -m http.server 8000
```

## Going live (one-time)

1. Create a free Netlify account and choose "Import from Git", then pick this repository and branch.
2. Buy the domain `windowrepairgta.ca` (or update `SITE["domain"]` in `build.py` if you use another) and connect it in Netlify under Domain management.
3. Netlify Forms: the estimate form is detected automatically. Under Forms > Notifications, add an email notification so every request reaches your inbox.
4. Google Search Console: add the domain, verify it, and submit `https://windowrepairgta.ca/sitemap.xml`.

## Measuring results

Every form submission records the page it came from (`page`) and how the customer found us (`heard`).
The site shares its phone number with YST Services, so calls can't be split by site. Ask callers how they found you,
or add a call-tracking number later.
