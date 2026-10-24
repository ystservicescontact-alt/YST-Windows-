#!/usr/bin/env python3
"""Builds the Window Repair GTA static site into ./site.

Usage: python3 build.py
Business details live in SITE below; page text lives in content.py.
Photos: put image files in src/photos/ and reference them in content.py
(a service's "image", or GALLERY entries). They are copied to /photos/.
"""
import json
import shutil
from datetime import date
from html import escape
from pathlib import Path

from content import SERVICES, CITIES, HOME, PAGES, GALLERY

ROOT = Path(__file__).parent
OUT = ROOT / "site"

SITE = {
    "name": "Window Repair GTA",
    "domain": "https://windowrepairgta.ca",
    "phone": "(365) 340-4760",
    "tel": "+13653404760",
    "whatsapp": "",          # e.g. "13653404760" to show a WhatsApp button
    "ga4": "",               # Google Analytics 4 ID, e.g. "G-XXXXXXX"
    "hours": "",             # e.g. "Mon–Sat 8am–7pm"
    "area": "Toronto and the Greater Toronto Area",
}

FONTS = ("https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800"
         "&family=Archivo+Narrow:wght@700&display=swap")

# Simple stroke icons (24x24, currentColor)
_I = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{}</svg>'
ICONS = {
    "fog": _I.format('<rect x="4" y="3" width="16" height="18"/><path d="M12 3v18M4 12h16"/><path d="M7 7.5h.01M9 9h.01M15.5 6.5h.01M17 9h.01M7.5 16h.01M9.5 17.5h.01M15 15.5h.01M17 18h.01"/>'),
    "broken": _I.format('<rect x="4" y="3" width="16" height="18"/><path d="M9 3l2 5-3 3 4 3-1 7M11 8l5 2M12 14l5-1"/>'),
    "patio": _I.format('<rect x="3" y="3" width="18" height="18"/><path d="M12 3v18M8 11v2M16 11v2M3 18h18"/>'),
    "crank": _I.format('<circle cx="9" cy="15" r="3"/><path d="M9 12V5h7"/><path d="M16 5v4"/><path d="M4 21h16"/>'),
    "caulk": _I.format('<path d="M3 10h11v4H3z"/><path d="M14 11h4l3-1v4l-3-1h-4"/><path d="M6 14v4M9 14v2"/>'),
    "screen": _I.format('<rect x="4" y="3" width="16" height="18"/><path d="M4 8h16M4 13h16M4 18h16M9 3v18M15 3v18"/>'),
    "replace": _I.format('<rect x="4" y="3" width="16" height="18"/><path d="M12 8v8M8 12h8"/>'),
    "commercial": _I.format('<path d="M3 9l1.5-5h15L21 9"/><path d="M3 9h18v2a3 3 0 01-6 0 3 3 0 01-6 0 3 3 0 01-6 0z"/><path d="M5 13v8h14v-8M10 21v-5h4v5"/>'),
    "emergency": _I.format('<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>'),
    "phone": _I.format('<path d="M5 3h4l2 5-3 2a12 12 0 006 6l2-3 5 2v4a2 2 0 01-2 2A17 17 0 013 5a2 2 0 012-2"/>'),
    "camera": _I.format('<path d="M4 7h3l2-3h6l2 3h3v13H4z"/><circle cx="12" cy="13" r="4"/>'),
    "shield": _I.format('<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>'),
    "tag": _I.format('<path d="M3 12V3h9l9 9-9 9z"/><circle cx="7.5" cy="7.5" r="1.5"/>'),
    "pin": _I.format('<path d="M12 21s-7-6.5-7-12a7 7 0 0114 0c0 5.5-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>'),
    "tools": _I.format('<path d="M14 6a4 4 0 00-5 5l-6 6 3 3 6-6a4 4 0 005-5l-3 3-3-3z"/>'),
}
SERVICE_ICON = {
    "foggy-window-repair": "fog", "window-glass-replacement": "broken", "patio-door-repair": "patio",
    "window-crank-repair": "crank", "window-caulking": "caulk", "window-screen-repair": "screen",
    "window-replacement": "replace", "commercial-glass-repair": "commercial", "emergency-glass-repair": "emergency",
}
# Options in the quick-quote widget: (value, label, icon)
QUICK_OPTIONS = [
    ("Foggy glass", "Foggy between panes", "fog"),
    ("Broken glass", "Cracked or broken", "broken"),
    ("Crank / hinge / lock", "Won't open or close", "crank"),
    ("Patio door", "Patio door sticks", "patio"),
]


def url(slug):
    return "/" if not slug else f"/{slug}/"


def sms_href():
    return f"sms:{SITE['tel']}"


# ---------------------------------------------------------------- schema
def business_schema():
    return {
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "@id": SITE["domain"] + "/#business",
        "name": SITE["name"],
        "url": SITE["domain"] + "/",
        "telephone": SITE["tel"],
        "priceRange": "$$",
        "areaServed": [{"@type": "City", "name": c["name"]} for c in CITIES],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Window and glass repair services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"],
                                                    "url": SITE["domain"] + url(s["slug"])}}
                for s in SERVICES],
        },
    }


def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def breadcrumb_schema(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n,
                                 "item": SITE["domain"] + h} for i, (n, h) in enumerate(trail)]}


def service_schema(name, slug, area):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": name,
            "provider": {"@id": SITE["domain"] + "/#business"}, "areaServed": area,
            "url": SITE["domain"] + url(slug)}


# ---------------------------------------------------------------- pieces
def call_btn(where, cls="btn-yellow", label=None):
    return (f'<a class="btn {cls}" href="tel:{SITE["tel"]}" data-where="{where}">'
            f'{ICONS["phone"]}{label or "Call " + SITE["phone"]}</a>')


def text_btn(where, cls="btn-outline"):
    if SITE["whatsapp"]:
        return (f'<a class="btn {cls}" href="https://wa.me/{SITE["whatsapp"]}" data-where="{where}">'
                f'{ICONS["camera"]}WhatsApp a photo</a>')
    return f'<a class="btn {cls}" href="{sms_href()}" data-where="{where}">{ICONS["camera"]}Text us a photo</a>'


def crumbs_html(trail):
    parts = []
    for i, (n, h) in enumerate(trail):
        parts.append(f'<li aria-current="page">{escape(n)}</li>' if i == len(trail) - 1
                     else f'<li><a href="{h}">{escape(n)}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(parts)}</ol></nav>'


def faq_html(faqs, soft=True):
    if not faqs:
        return ""
    items = "".join(f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q, a in faqs)
    return f"""
<section class="section{' soft' if soft else ''}" id="faq"><div class="wrap">
  <div class="section-head"><div><h2>Common questions</h2></div></div>
  <div class="faq">{items}</div>
</div></section>"""


def cta_html():
    return f"""
<section class="cta"><div class="wrap">
  <div><h2>Send us a photo. Get a price.</h2><p>Free estimates across {SITE['area']}.</p></div>
  <div class="actions">{call_btn("cta", "btn-navy")}{text_btn("cta", "btn-outline")}</div>
</div></section>"""


def trust_html():
    items = [("tag", "Free estimates"), ("tools", "Repair first, replace only if needed"),
             ("shield", "All window brands"), ("pin", "All of the GTA")]
    return '<section class="trust" aria-label="Why choose us"><div class="wrap">' + "".join(
        f"<div>{ICONS[i]}<span>{t}</span></div>" for i, t in items) + "</div></section>"


def card_media(s):
    if s.get("image"):
        return f'<img src="/photos/{escape(s["image"])}" alt="{escape(s["name"])}" loading="lazy">'
    return ICONS[SERVICE_ICON[s["slug"]]]


def cards_html(items):
    return '<div class="cards">' + "".join(f"""
<a class="card" href="{url(s['slug'])}">
  <div class="card-media">{card_media(s)}</div>
  <div class="card-body"><h3>{escape(s['name'])}</h3><p>{escape(s['card'])}</p><span class="go">Learn more →</span></div>
</a>""" for s in items) + "</div>"


def gallery_html():
    if not GALLERY:
        return ""
    figs = "".join(f"""
<figure class="ba">
  <div class="ba-pair">
    <div><img src="/photos/{escape(g['before'])}" alt="Before: {escape(g['title'])}" loading="lazy"><span>Before</span></div>
    <div><img src="/photos/{escape(g['after'])}" alt="After: {escape(g['title'])}" loading="lazy"><span>After</span></div>
  </div>
  <figcaption>{escape(g['title'])}<small>{escape(g.get('city', ''))}</small></figcaption>
</figure>""" for g in GALLERY)
    return f"""
<section class="section" id="work"><div class="wrap">
  <div class="section-head"><div><h2>Recent work</h2><p>Real jobs from around the GTA.</p></div></div>
  <div class="gallery">{figs}</div>
</div></section>"""


def areas_html():
    links = "".join(f'<li><a href="{url(c["slug"])}">{escape(c["name"])}</a></li>' for c in CITIES)
    extra = "".join(f"<li><span>{escape(n)}</span></li>" for n in HOME["extra_areas"])
    return f'<ul class="areas">{links}{extra}</ul>'


def quick_form():
    opts = "".join(f"""
<label class="choice"><input type="radio" name="problem" value="{escape(v)}"{' checked' if i == 0 else ''}>
  <span>{ICONS[ic]}{escape(lbl)}</span></label>""" for i, (v, lbl, ic) in enumerate(QUICK_OPTIONS))
    return f"""
<form class="quick" name="quick-quote" method="POST" action="/thanks/" data-netlify="true"
      netlify-honeypot="bot-field" enctype="multipart/form-data" data-where="hero">
  <input type="hidden" name="form-name" value="quick-quote">
  <input type="hidden" name="page" value="home">
  <p class="hidden-field"><label>Leave this empty <input name="bot-field"></label></p>
  <h2>Free quote in 60 seconds</h2>
  <p class="sub">Pick the problem, add a photo, and we'll text you a price.</p>
  <fieldset class="choices"><legend>What's wrong?</legend>{opts}</fieldset>
  <div class="row">
    <label for="h-name">Name<input id="h-name" name="name" autocomplete="name" required></label>
    <label for="h-phone">Mobile<input id="h-phone" name="phone" type="tel" autocomplete="tel" required></label>
  </div>
  <label for="h-photo">Photo <span class="hint">Optional, helps us quote faster</span>
    <input id="h-photo" name="photo" type="file" accept="image/*"></label>
  <button class="btn btn-navy" type="submit">Get my free quote</button>
  <p class="or-text">or</p>
  {call_btn("hero-form", "btn-outline")}
</form>"""


def full_form(source):
    problems = "".join(f"<option>{escape(s['name'])}</option>" for s in SERVICES) + "<option>Something else</option>"
    return f"""
<form class="form-card" name="quote" method="POST" action="/thanks/" data-netlify="true"
      netlify-honeypot="bot-field" enctype="multipart/form-data" data-where="contact">
  <input type="hidden" name="form-name" value="quote">
  <input type="hidden" name="page" value="{escape(source)}">
  <p class="hidden-field"><label>Leave this empty <input name="bot-field"></label></p>
  <div class="row">
    <label for="q-name">Name<input id="q-name" name="name" autocomplete="name" required></label>
    <label for="q-phone">Phone<input id="q-phone" name="phone" type="tel" autocomplete="tel" required></label>
  </div>
  <div class="row">
    <label for="q-email">Email<input id="q-email" name="email" type="email" autocomplete="email"></label>
    <label for="q-city">City<input id="q-city" name="city" autocomplete="address-level2" placeholder="e.g. Mississauga"></label>
  </div>
  <div class="row">
    <label for="q-problem">What's wrong?<select id="q-problem" name="problem">{problems}</select></label>
    <label for="q-count">How many windows?<input id="q-count" name="count" type="number" min="1" value="1" inputmode="numeric"></label>
  </div>
  <label for="q-details">Details <span class="hint">Where in the house, size if you know it</span>
    <textarea id="q-details" name="details"></textarea></label>
  <label for="q-photo">Photo <span class="hint">Optional, one image up to 8 MB</span>
    <input id="q-photo" name="photo" type="file" accept="image/*"></label>
  <label for="q-heard">How did you find us?
    <select id="q-heard" name="heard">
      <option>Google search</option><option>Google Maps</option><option>Friend or neighbour</option>
      <option>Saw your truck</option><option>Other</option>
    </select></label>
  <button class="btn btn-navy" type="submit">Request my free estimate</button>
</form>"""


# ---------------------------------------------------------------- layout
def layout(*, slug, title, description, body, schemas=(), noindex=False):
    canonical = SITE["domain"] + url(slug)
    services = "".join(f'<li><a href="{url(s["slug"])}">{escape(s["name"])}</a></li>' for s in SERVICES)
    half = (len(CITIES) + 1) // 2
    cities_a = "".join(f'<li><a href="{url(c["slug"])}">{escape(c["name"])}</a></li>' for c in CITIES[:half])
    cities_b = "".join(f'<li><a href="{url(c["slug"])}">{escape(c["name"])}</a></li>' for c in CITIES[half:])
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    ga = ""
    if SITE["ga4"]:
        ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={SITE["ga4"]}"></script>'
              f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}"
              f"gtag('js',new Date());gtag('config','{SITE['ga4']}');</script>")
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    hours = f'<b>{escape(SITE["hours"])}</b> · ' if SITE["hours"] else ""
    return f"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{canonical}">
{robots}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{canonical}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/style.css">
{ga}
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
  <span><span class="hide-sm">Window &amp; glass repair · </span>Toronto, Mississauga, Brampton, Vaughan, Markham &amp; the GTA</span>
  <span class="hide-sm">{hours}<b>Free estimates</b></span>
</div></div>
<header class="site-header"><div class="wrap">
  <a class="logo" href="/" aria-label="{SITE['name']} home">
    <span class="logo-mark" aria-hidden="true"><span></span><span></span><span></span><span></span></span>
    <span class="logo-text"><b>{SITE['name']}</b><small>Glass · Hardware · Patio Doors</small></span>
  </a>
  <nav class="nav" aria-label="Main">
    <a href="/services/">Services</a>
    <a href="/#areas">Service Areas</a>
    <a href="/window-brands/">Brands We Fix</a>
    <a href="/contact/">Free Estimate</a>
    <a class="nav-phone" href="tel:{SITE['tel']}" data-where="header"><small>Call for a free quote</small><b>{SITE['phone']}</b></a>
  </nav>
</div></header>
<main id="main">
{body}
</main>
<footer>
  <div class="wrap footer-grid">
    <div>
      <h2>{SITE['name']}</h2>
      <p>Window, glass and patio door repair for homes and businesses across {SITE['area']}.</p>
      <p style="margin-top:14px"><a class="f-phone" href="tel:{SITE['tel']}" data-where="footer">{SITE['phone']}</a></p>
    </div>
    <div><h2>Services</h2><ul>{services}</ul></div>
    <div><h2>Service areas</h2><ul>{cities_a}</ul></div>
    <div><h2>&nbsp;</h2><ul>{cities_b}<li><a href="/window-brands/">Brands we fix</a></li><li><a href="/contact/">Free estimate</a></li></ul></div>
  </div>
  <div class="wrap footer-bottom">© {date.today().year} {SITE['name']}</div>
</footer>
<div class="call-bar">
  <a class="btn btn-yellow" href="tel:{SITE['tel']}" data-where="callbar">{ICONS['phone']}Call</a>
  <a class="btn btn-navy" href="{('https://wa.me/' + SITE['whatsapp']) if SITE['whatsapp'] else sms_href()}" data-where="callbar">{ICONS['camera']}Text a photo</a>
</div>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""


def write(slug, html):
    path = OUT / slug / "index.html" if slug else OUT / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


# ---------------------------------------------------------------- pages
def build_home():
    h = HOME
    checks = "".join(f"<li>{escape(c)}</li>" for c in h["checks"])
    body = f"""
<section class="hero"><div class="wrap">
  <div class="hero-copy">
    <span class="tag">{escape(h['tag'])}</span>
    <h1>{escape(h['h1'])}</h1>
    <p class="lede">{escape(h['lede'])}</p>
    <div class="actions">{call_btn("hero")}{text_btn("hero")}</div>
    <ul class="checks">{checks}</ul>
  </div>
  {quick_form()}
</div></section>
{trust_html()}
<section class="section" id="services"><div class="wrap">
  <div class="section-head"><div><h2>What we fix</h2><p>Most window problems come down to one worn or broken part. We find it and replace it.</p></div>
    <a class="more-link" href="/services/">All services →</a></div>
  {cards_html(SERVICES)}
</div></section>
<section class="section soft" id="repair-or-replace"><div class="wrap">
  <div class="section-head"><div><h2>Repair or replace?</h2><p>If the frame is solid, repairing the failed part is faster and costs far less.</p></div></div>
  <div class="versus">
    <div><h3>We repair</h3><ul class="yes"><li>New glass or part, same frame</li><li>Usually under an hour per window</li><li>Walls, trim and paint untouched</li><li>A fraction of the cost</li></ul></div>
    <div><h3>Full replacement</h3><ul class="no"><li>New frame, glass and install</li><li>Often a full day of work</li><li>Trim and drywall redone</li><li>Several times the price</li></ul></div>
  </div>
</div></section>
<section class="section" id="process"><div class="wrap">
  <div class="section-head"><div><h2>How it works</h2></div></div>
  <ol class="steps">
    <li><h3>Send a photo</h3><p>Text us or use the form. We can often quote from the photo alone.</p></li>
    <li><h3>We measure</h3><p>We check the frame and measure the glass to the 1/16 of an inch.</p></li>
    <li><h3>Glass is made</h3><p>Sealed units are made to your exact size. Hardware is usually on the truck.</p></li>
    <li><h3>We fix it</h3><p>We install, clean up and test that the window opens, closes and locks.</p></li>
  </ol>
</div></section>
{gallery_html()}
<section class="section soft" id="areas"><div class="wrap">
  <div class="section-head"><div><h2>Service areas</h2><p>We come to you anywhere in the GTA. Don't see your city? Call us.</p></div></div>
  <div class="area-map">
    <iframe title="Map of our service area in the Greater Toronto Area" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
      src="https://www.google.com/maps?q=Greater+Toronto+Area,+ON&amp;z=9&amp;output=embed"></iframe>
    {areas_html()}
  </div>
</div></section>
{faq_html(h['faqs'], soft=False)}
{cta_html()}"""
    write("", layout(slug="", title=h["title"], description=h["description"], body=body,
                     schemas=[business_schema(), faq_schema(h["faqs"])]))


def aside_html(current_slug):
    links = "".join(f'<li><a href="{url(s["slug"])}">{escape(s["name"])}</a></li>'
                    for s in SERVICES if s["slug"] != current_slug)
    return f"""
<aside class="aside" aria-label="Get a quote">
  <div class="aside-box">
    <h2>Free estimate</h2>
    <a class="phone-big" href="tel:{SITE['tel']}" data-where="aside">{SITE['phone']}</a>
    {text_btn("aside", "btn-yellow")}
    <a class="btn btn-navy" href="/contact/">Request online</a>
  </div>
  <div class="aside-links"><h2>Other services</h2><ul>{links}</ul></div>
</aside>"""


def build_article(page, trail, schemas, extra_html=""):
    body = f"""
<section class="page-hero"><div class="wrap">
  {crumbs_html(trail)}
  <span class="tag">{escape(page['eyebrow'])}</span>
  <h1>{escape(page['h1'])}</h1>
  <p class="lede">{escape(page['lede'])}</p>
  <div class="actions">{call_btn("page-hero")}{text_btn("page-hero")}</div>
</div></section>
{trust_html()}
<div class="wrap article">
  <div class="prose">{page['body']}{extra_html}</div>
  {aside_html(page['slug'])}
</div>
{faq_html(page.get('faqs', []))}
{cta_html()}"""
    schemas = [business_schema(), breadcrumb_schema(trail), *schemas]
    if page.get("faqs"):
        schemas.append(faq_schema(page["faqs"]))
    write(page["slug"], layout(slug=page["slug"], title=page["title"], description=page["description"],
                               body=body, schemas=schemas))


def build_service(s):
    trail = [("Home", "/"), ("Services", "/services/"), (s["name"], url(s["slug"]))]
    extra = f"<h2>Where we do this work</h2><p>Anywhere in {SITE['area']}, including:</p>{areas_html()}"
    build_article(s, trail, [service_schema(s["name"], s["slug"], SITE["area"])], extra)


def build_city(c):
    trail = [("Home", "/"), (f"Window repair {c['name']}", url(c["slug"]))]
    items = "".join(f'<li><a href="{url(s["slug"])}">{escape(s["name"])}</a></li>' for s in SERVICES)
    extra = f"<h2>Our services in {escape(c['name'])}</h2><ul>{items}</ul>"
    build_article(c, trail, [service_schema(f"Window repair in {c['name']}", c["slug"], c["name"])], extra)


def build_pages():
    for p in PAGES:
        trail = [("Home", "/"), (p["crumb"], url(p["slug"]))]
        body = p["body"].format(
            crumbs=crumbs_html(trail), phone=SITE["phone"], tel=SITE["tel"], area=SITE["area"],
            form=full_form(p["slug"]), cards=cards_html(SERVICES), call=call_btn(p["slug"]),
            text=text_btn(p["slug"]), cta=cta_html(), trust=trust_html())
        write(p["slug"], layout(slug=p["slug"], title=p["title"], description=p["description"], body=body,
                                schemas=[business_schema(), breadcrumb_schema(trail)],
                                noindex=p.get("noindex", False)))


def build_404():
    body = f"""
<section class="page-hero"><div class="wrap">
  <span class="tag">Page not found</span>
  <h1>This page doesn't exist</h1>
  <p class="lede">The link may be old. Go to the home page, or call us at {SITE['phone']}.</p>
  <div class="actions"><a class="btn btn-navy" href="/">Go to the home page</a>{call_btn("404")}</div>
</div></section>"""
    (OUT / "404.html").write_text(layout(slug="404", title=f"Page not found | {SITE['name']}",
                                         description="Page not found.", body=body, noindex=True), encoding="utf-8")


def build_sitemap():
    slugs = [""] + [s["slug"] for s in SERVICES] + [c["slug"] for c in CITIES] + \
            [p["slug"] for p in PAGES if not p.get("noindex")]
    today = date.today().isoformat()
    urls = "\n".join(f"  <url><loc>{SITE['domain']}{url(s)}</loc><lastmod>{today}</lastmod></url>" for s in slugs)
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                     '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     f"{urls}\n</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE['domain']}/sitemap.xml\n",
                                    encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "src" / "assets", OUT / "assets")
    photos = ROOT / "src" / "photos"
    if photos.exists():
        shutil.copytree(photos, OUT / "photos")
    build_home()
    for s in SERVICES:
        build_service(s)
    for c in CITIES:
        build_city(c)
    build_pages()
    build_404()
    build_sitemap()
    print(f"Built {len(list(OUT.rglob('*.html')))} pages into {OUT}")


if __name__ == "__main__":
    main()
