#!/usr/bin/env python3
"""Builds the Window Repair GTA static site into ./site.

Usage: python3 build.py
Business details live in SITE below; page text lives in content.py.
Photos: put image files in src/photos/ and reference them in content.py
(see media.py for the exact file names). They are copied to /photos/.
"""
import json
import shutil
from datetime import date
from html import escape
from pathlib import Path

from content import SERVICES, CITIES, HOME, PAGES
from local import COMBO_SERVICES, CITY_LOCAL, WHY, combo_slug
from areas import REGIONS, town_slug
from extras import EXTRAS
from media import photo, pair, gallery_pairs, video_html
from services_more import CATEGORIES
from pages_more import (VISIT_FEE, CUSTOMERS, YEARS, CLIENT_LOGOS, ABOUT_STORY, WORK, PROMISES, CHECK_12,
                        WHO, SIGNS, BLOG, EXTRA_PAGES)

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
    "tilt": _I.format('<rect x="4" y="3" width="16" height="18"/><path d="M8 7l4-3 4 3M12 4v8"/>'),
    "handle": _I.format('<circle cx="7" cy="12" r="3"/><path d="M10 12h10M17 12v4"/>'),
    "hinge": _I.format('<path d="M5 4v16M5 6l14 5M5 18l14-5"/>'),
    "lock": _I.format('<rect x="5" y="11" width="14" height="10"/><path d="M8 11V7a4 4 0 018 0v4M12 15v2"/>'),
    "latch": _I.format('<rect x="4" y="9" width="10" height="6"/><path d="M14 12h6M18 10v4"/>'),
    "door": _I.format('<path d="M6 21V3h12v18M3 21h18M15 12h.01"/>'),
    "doorglass": _I.format('<path d="M6 21V3h12v18M3 21h18"/><rect x="9" y="6" width="6" height="8"/>'),
    "curved": _I.format('<path d="M4 20V12a8 8 0 0116 0v8z"/><path d="M12 4v16M4 14h16"/>'),
    "wood": _I.format('<rect x="4" y="3" width="16" height="18"/><path d="M8 7c2 1 2 3 0 4M14 13c2 1 2 3 0 4"/>'),
    "drop": _I.format('<path d="M12 3s6 7 6 11a6 6 0 01-12 0c0-4 6-11 6-11z"/>'),
    "skylight": _I.format('<path d="M3 14l9-9 9 9"/><rect x="8" y="10" width="8" height="6"/>'),
    "tools": _I.format('<path d="M14 6a4 4 0 00-5 5l-6 6 3 3 6-6a4 4 0 005-5l-3 3-3-3z"/>'),
}
SERVICE_ICON = {
    "foggy-window-repair": "fog", "window-glass-replacement": "broken", "patio-door-repair": "patio",
    "window-crank-repair": "crank", "window-caulking": "caulk", "window-screen-repair": "screen",
    "window-replacement": "replace", "commercial-glass-repair": "commercial", "emergency-glass-repair": "emergency",
    "tilt-and-turn-window-repair": "tilt", "window-handle-repair": "handle", "window-hinge-repair": "hinge",
    "window-lock-repair": "lock", "window-latch-repair": "latch", "door-repair": "door", "front-door-glass": "doorglass",
    "curved-glass-replacement": "curved", "wood-window-repair": "wood", "window-leak-drainage-repair": "drop",
    "skylight-repair": "skylight",
}
FEATURED = SERVICES[:9]
BY_SLUG = {s["slug"]: s for s in SERVICES}
WA_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 00-8.6 15.1L2 22l5-1.3A10 10 0 1012 2zm0 18.2a8.2 8.2 0 01-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1112 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 01-3.3-2.9c-.3-.4.2-.4.7-1.3a.5.5 0 000-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 00-.7.3 3 3 0 00-.9 2.2 5.2 5.2 0 001.1 2.7 11.8 11.8 0 004.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 001.8-1.2 2.2 2.2 0 00.1-1.2c0-.1-.2-.2-.5-.3z"/></svg>')

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
    items = [("shield", "Fully insured"), ("tools", "1-year workmanship warranty"),
             ("emergency", "Same-day appointments"), ("tag", "Free estimates")]
    return '<section class="trust" aria-label="Why choose us"><div class="wrap">' + "".join(
        f"<div>{ICONS[i]}<span>{t}</span></div>" for i, t in items) + "</div></section>"


def card_media(s):
    img = photo(f"services/{s['slug']}")
    if img:
        return f'<img src="{img}" alt="{escape(s["name"])}" loading="lazy">'
    return ICONS[SERVICE_ICON[s["slug"]]]


def ba_figure(before, after, title, city=""):
    return f"""
<figure class="ba">
  <div class="ba-pair">
    <div><img src="{before}" alt="Before: {escape(title)}" loading="lazy"><span>Before</span></div>
    <div><img src="{after}" alt="After: {escape(title)}" loading="lazy"><span>After</span></div>
  </div>
  <figcaption>{escape(title)}<small>{escape(city)}</small></figcaption>
</figure>"""


def media_block(service_slug, title):
    """Service photo, before/after pair and video, if any exist."""
    out = ""
    img = photo(f"services/{service_slug}")
    if img:
        out += f'<img class="prose-img" src="{img}" alt="{escape(title)}" loading="lazy">'
    p = pair(f"services/{service_slug}")
    if p:
        out += f'<div class="gallery">{ba_figure(p[0], p[1], title)}</div>'
    return out + video_html(service_slug, title)


def cards_html(items):
    return '<div class="cards">' + "".join(f"""
<a class="card" href="{url(s['slug'])}">
  <div class="card-media">{card_media(s)}</div>
  <div class="card-body"><h3>{escape(s['name'])}</h3><p>{escape(s['card'])}</p><span class="go">Learn more →</span></div>
</a>""" for s in items) + "</div>"


def gallery_html():
    items = gallery_pairs()
    for sv in SERVICES:
        p = pair(f"services/{sv['slug']}")
        if p:
            items.append({"before": p[0], "after": p[1], "title": sv["name"], "city": ""})
    if not items:
        return ""
    figs = "".join(ba_figure(g["before"], g["after"], g["title"], g["city"]) for g in items[:9])
    return f"""
<section class="section" id="work"><div class="wrap">
  <div class="section-head"><div><h2>Recent work</h2><p>Real jobs from around the GTA.</p></div></div>
  <div class="gallery">{figs}</div>
</div></section>"""


def team_html():
    img = photo("team")
    vid = video_html("home", "Window Repair GTA at work")
    if not img and not vid:
        return ""
    media = f'<img src="{img}" alt="Our team" loading="lazy">' if img else vid
    second = vid if img else ""
    return f"""
<section class="section soft" id="team"><div class="wrap team">
  <div class="team-media">{media}</div>
  <div class="prose"><h2>Local, hands-on window repair</h2>
    <p>We fix windows and patio doors every day across the GTA. When you call, you talk to the people who do the work.</p>
    {second}<div class="actions">{call_btn("team")}{text_btn("team")}</div></div>
</div></section>"""


def areas_html():
    links = "".join(f'<li><a href="{url(c["slug"])}">{escape(c["name"])}</a></li>' for c in CITIES)
    extra = "".join(f'<li><a href="{town_href(n)}">{escape(n)}</a></li>' for n in HOME["extra_areas"])
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
<label for="h-urgency">When do you need us?
    <select id="h-urgency" name="urgency"><option>As soon as possible</option><option>Emergency (broken / not secure)</option><option>Planning ahead</option></select></label>
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
<label for="q-urgency">When do you need us?
    <select id="q-urgency" name="urgency"><option>As soon as possible</option><option>Emergency (broken / not secure)</option><option>Planning ahead</option></select></label>
  <fieldset class="photos"><legend>Photos <span class="hint">Optional, up to 3, 8 MB each</span></legend>
    <input id="q-photo" name="photo" type="file" accept="image/*" aria-label="Photo 1">
    <input id="q-photo2" name="photo2" type="file" accept="image/*" aria-label="Photo 2">
    <input id="q-photo3" name="photo3" type="file" accept="image/*" aria-label="Photo 3">
  </fieldset>
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
    services = "".join(f'<li><a href="{url(s["slug"])}">{escape(s["name"])}</a></li>' for s in FEATURED) + \
        '<li><a href="/services/"><strong>All services</strong></a></li>'
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
  <span class="hide-sm">{hours}<b>Fully insured · 1-year warranty · Same-day appointments · 24/7 emergency</b></span>
</div></div>
<header class="site-header"><div class="wrap">
  <a class="logo" href="/" aria-label="{SITE['name']} home">
    <span class="logo-mark" aria-hidden="true"><span></span><span></span><span></span><span></span></span>
    <span class="logo-text"><b>{SITE['name']}</b><small>Glass · Hardware · Patio Doors</small></span>
  </a>
  <nav class="nav" aria-label="Main">
    <a href="/services/">Services</a>
    <a href="/service-areas/">Service Areas</a>
    <a href="/about/">About</a>
    <a href="/blog/">Blog</a>
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
    <div><h2>&nbsp;</h2><ul>{cities_b}<li><a href="/service-areas/">All service areas</a></li><li><a href="/window-brands/">Brands we fix</a></li><li><a href="/about/">About us</a></li><li><a href="/blog/">Blog</a></li><li><a href="/quote/">Get a quote</a></li><li><a href="/measure-glass/">Measure your glass</a></li><li><a href="/property-managers/">Property managers</a></li><li><a href="/real-estate-agents/">Real estate agents</a></li>{('<li><a href="/our-work/">Our work</a></li>') if WORK else ''}<li><a href="/insurance-claims/">Insurance claims</a></li><li><a href="/winter-ready/">Winter-ready checklist</a></li><li><a href="/contact/">Free estimate</a></li></ul></div>
  </div>
  <div class="wrap footer-bottom">© {date.today().year} {SITE['name']}</div>
</footer>
<div class="call-bar">
  <a class="btn btn-yellow" href="tel:{SITE['tel']}" data-where="callbar">{ICONS['phone']}Call</a>
  <a class="btn btn-navy" href="{('https://wa.me/' + SITE['whatsapp']) if SITE['whatsapp'] else sms_href()}" data-where="callbar">{ICONS['camera']}Text a photo</a>
</div>
{('<a class="wa-float" href="https://wa.me/' + SITE['whatsapp'] + '" data-where="wa-float" aria-label="Send us a photo on WhatsApp">' + WA_ICON + '<span>WhatsApp</span></a>') if SITE['whatsapp'] else ''}
<script src="/assets/site.js" defer></script>
</body>
</html>
"""


def write(slug, html):
    path = OUT / slug / "index.html" if slug else OUT / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


# ---------------------------------------------------------------- extra sections
def who_html():
    cards = "".join(f'<a class="who-card" href="{href}"><h3>{escape(t)}</h3><p>{escape(d)}</p><span class="go">{escape(cta)} →</span></a>'
                    for t, d, href, cta in WHO)
    return f"""
<section class="section" id="who"><div class="wrap">
  <div class="section-head"><div><h2>Who we work with</h2></div></div>
  <div class="who">{cards}</div>
</div></section>"""


def signs_html():
    items = "".join(f"<div><h3>{escape(t)}</h3><p>{escape(d)}</p></div>" for t, d in SIGNS)
    return f"""
<section class="section" id="signs"><div class="wrap">
  <div class="section-head"><div><h2>Signs your window needs a repair, not a replacement</h2></div></div>
  <div class="signs">{items}</div>
</div></section>"""


def promises_list():
    items = list(PROMISES)
    if VISIT_FEE:
        items.append((f"{VISIT_FEE} on-site assessment",
                      f"An on-site assessment is {VISIT_FEE}, credited toward your repair when you go ahead. Photo quotes are free."))
    return '<div class="promises">' + "".join(f"<div><h3>{escape(t)}</h3><p>{escape(d)}</p></div>" for t, d in items) + "</div>"


def promises_section():
    return f"""
<section class="section soft" id="promises"><div class="wrap">
  <div class="section-head"><div><h2>Our promises</h2></div><a class="more-link" href="/about/">About us →</a></div>
  {promises_list()}
</div></section>"""


def check12_html():
    return '<ol class="check12">' + "".join(f"<li>{escape(c)}</li>" for c in CHECK_12) + "</ol>"


def logos_html():
    if not CLIENT_LOGOS:
        return ""
    names = "".join(f"<li>{escape(n)}</li>" for n in CLIENT_LOGOS)
    return f"""
<section class="section" id="clients"><div class="wrap">
  <div class="section-head"><div><h2>Businesses we've worked for</h2></div></div>
  <ul class="logos">{names}</ul>
  <p class="hint">Names belong to their owners. No affiliation or endorsement is implied.</p>
</div></section>"""


def grouped_cards_html():
    return "".join(f"""
<div class="cat"><h2 class="cat-title">{escape(name)}</h2>{cards_html([BY_SLUG[g] for g in group])}</div>"""
                   for name, group in CATEGORIES)


def quote_forms_html():
    def form(name, title, sub, fields):
        return f"""
<details class="qf"{' open' if name == 'glass-quote' else ''}><summary><span>{escape(title)}</span><small>{escape(sub)}</small></summary>
<form class="form-card" name="{name}" method="POST" action="/thanks/" data-netlify="true" netlify-honeypot="bot-field"
      enctype="multipart/form-data" data-where="{name}">
  <input type="hidden" name="form-name" value="{name}">
  <p class="hidden-field"><label>Leave this empty <input name="bot-field"></label></p>
  <div class="row">
    <label for="{name}-name">Name<input id="{name}-name" name="name" autocomplete="name" required></label>
    <label for="{name}-phone">Phone<input id="{name}-phone" name="phone" type="tel" autocomplete="tel" required></label>
  </div>
  <label for="{name}-city">City<input id="{name}-city" name="city" autocomplete="address-level2"></label>
  {fields.format(n=name)}
  <fieldset class="photos"><legend>Photos <span class="hint">Optional, up to 3</span></legend>
    <input name="photo" type="file" accept="image/*" aria-label="Photo 1">
    <input name="photo2" type="file" accept="image/*" aria-label="Photo 2">
    <input name="photo3" type="file" accept="image/*" aria-label="Photo 3">
  </fieldset>
  <button class="btn btn-navy" type="submit">Send for a quote</button>
</form></details>"""
    glass = """<div class="row">
    <label for="{n}-w">Visible width (inches)<input id="{n}-w" name="width" inputmode="decimal"></label>
    <label for="{n}-h">Visible height (inches)<input id="{n}-h" name="height" inputmode="decimal"></label></div>
  <div class="row">
    <label for="{n}-panes">Panes<select id="{n}-panes" name="panes"><option>Double</option><option>Triple</option><option>Single</option><option>Not sure</option></select></label>
    <label for="{n}-issue">Problem<select id="{n}-issue" name="issue"><option>Foggy</option><option>Cracked / broken</option><option>Upgrade</option></select></label></div>
  <div class="row">
    <label for="{n}-type">Glass<select id="{n}-type" name="glass"><option>Clear</option><option>Frosted / textured</option><option>Tinted</option><option>Not sure</option></select></label>
    <label for="{n}-count">How many?<input id="{n}-count" name="count" type="number" min="1" value="1"></label></div>
  <p class="hint">Not sure how to measure? <a href="/measure-glass/">See our guide</a>, or just send photos.</p>"""
    hardware = """<div class="row">
    <label for="{n}-part">Part<select id="{n}-part" name="part"><option>Crank / operator</option><option>Handle</option><option>Hinges</option><option>Lock / latch</option><option>Tilt &amp; turn</option><option>Patio door rollers / lock</option><option>Not sure</option></select></label>
    <label for="{n}-count">How many windows?<input id="{n}-count" name="count" type="number" min="1" value="1"></label></div>
  <label for="{n}-brand">Window brand <span class="hint">If you know it</span><input id="{n}-brand" name="brand"></label>
  <p class="hint">A close-up photo of the crank and hinge arm helps us bring the right part.</p>"""
    seal = """<div class="row">
    <label for="{n}-issue">Problem<select id="{n}-issue" name="issue"><option>Drafts</option><option>Water leak</option><option>Old caulking</option><option>Wood rot</option></select></label>
    <label for="{n}-count">How many windows/doors?<input id="{n}-count" name="count" type="number" min="1" value="1"></label></div>
  <label for="{n}-floors">Highest floor<select id="{n}-floors" name="floors"><option>Ground floor</option><option>2nd floor</option><option>3rd floor or higher</option></select></label>"""
    return (form("glass-quote", "Glass quote", "Foggy, cracked or broken glass", glass) +
            form("hardware-quote", "Hardware quote", "Cranks, hinges, handles, locks, patio doors", hardware) +
            form("sealing-quote", "Caulking & leaks quote", "Drafts, leaks, caulking, wood", seal) +
            '<p class="hint" style="margin-top:12px">Something else? Use the <a href="/contact/">general form</a>.</p>')


def blog_list_html():
    return '<div class="blog-list">' + "".join(
        f'<a class="blog-card" href="/blog/{b["slug"]}/"><h2>{escape(b["title"])}</h2><p>{escape(b["description"])}</p><span class="go">Read →</span></a>'
        for b in BLOG) + "</div>"


def build_blog_posts():
    for b in BLOG:
        slug = f"blog/{b['slug']}"
        trail = [("Home", "/"), ("Blog", "/blog/"), (b["title"], url(slug))]
        others = "".join(f'<li><a href="/blog/{o["slug"]}/">{escape(o["title"])}</a></li>' for o in BLOG if o is not b)
        body = f"""
<section class="page-hero"><div class="wrap">
  {crumbs_html(trail)}
  <span class="tag">Guide</span>
  <h1>{escape(b['title'])}</h1>
  <p class="lede">{escape(b['description'])}</p>
</div></section>
<div class="wrap article">
  <article class="prose">{b['body']}<h2>More guides</h2><ul>{others}</ul></article>
  {aside_html("")}
</div>
{cta_html()}"""
        schema = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": b["title"],
                  "description": b["description"], "datePublished": b["date"],
                  "author": {"@type": "Organization", "name": SITE["name"]},
                  "publisher": {"@id": SITE["domain"] + "/#business"}, "mainEntityOfPage": SITE["domain"] + url(slug)}
        write(slug, layout(slug=slug, title=f"{b['title']} | {SITE['name']}", description=b["description"], body=body,
                           schemas=[business_schema(), breadcrumb_schema(trail), schema]))


def build_work():
    if not WORK:
        return
    for w in WORK:
        slug = f"our-work/{w['slug']}"
        trail = [("Home", "/"), ("Our work", "/our-work/"), (w["title"], url(slug))]
        sv = BY_SLUG.get(w.get("service"))
        pair_html = ""
        if w.get("before") and w.get("after"):
            pair_html = '<div class="gallery">' + ba_figure("/photos/" + w["before"], "/photos/" + w["after"], w["title"], w["city"]) + "</div>"
        review = (f'<blockquote class="review"><p>{escape(w["review"])}</p><cite>{escape(w.get("reviewer", ""))}</cite></blockquote>'
                  if w.get("review") else "")
        service_link = f'<p>Service: <a href="{url(sv["slug"])}">{escape(sv["name"])}</a></p>' if sv else ""
        body = f"""
<section class="page-hero"><div class="wrap">
  {crumbs_html(trail)}
  <span class="tag">{escape(w['city'])}</span>
  <h1>{escape(w['title'])} in {escape(w['city'])}</h1>
  <p class="lede">{escape(w['summary'])}</p>
  <div class="actions">{call_btn("work")}{text_btn("work")}</div>
</div></section>
<div class="wrap article"><div class="prose">{pair_html}{review}{service_link}</div>{aside_html(w.get("service", ""))}</div>
{cta_html()}"""
        write(slug, layout(slug=slug, title=f"{w['title']} in {w['city']} | {SITE['name']}", description=w["summary"],
                           body=body, schemas=[business_schema(), breadcrumb_schema(trail)]))
    items = "".join(f'<li><a href="/our-work/{w["slug"]}/">{escape(w["title"])} · {escape(w["city"])}</a></li>' for w in WORK)
    trail = [("Home", "/"), ("Our work", "/our-work/")]
    body = f"""
<section class="page-hero"><div class="wrap">{crumbs_html(trail)}<span class="tag">Our work</span>
  <h1>Jobs we've completed</h1><p class="lede">Real repairs from homes and businesses around the GTA.</p></div></section>
<section class="section"><div class="wrap"><ul class="areas">{items}</ul></div></section>{cta_html()}"""
    write("our-work", layout(slug="our-work", title=f"Our Work | {SITE['name']}",
                             description="Window and glass repairs we've completed across the GTA.",
                             body=body, schemas=[business_schema(), breadcrumb_schema(trail)]))


# ---------------------------------------------------------------- pages
def build_home():
    h = HOME
    extra_checks = ([f"{YEARS} years in business"] if YEARS else []) + ([f"{CUSTOMERS} customers"] if CUSTOMERS else [])
    checks = "".join(f"<li>{escape(c)}</li>" for c in h["checks"] + extra_checks)
    body = f"""
<section{(' class="hero has-photo" style="--hero-img:url(' + photo("hero") + ')"') if photo("hero") else ' class="hero"'}><div class="wrap">
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
  {cards_html(FEATURED)}
</div></section>
{who_html()}
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
{signs_html()}
{promises_section()}
{gallery_html()}
{logos_html()}
{team_html()}
<section class="section soft" id="areas"><div class="wrap">
  <div class="section-head"><div><h2>Service areas</h2><p>We come to you anywhere in the GTA. Don't see your city? Call us.</p></div></div>
  <div class="area-map">
    <iframe title="Map of our service area in the Greater Toronto Area" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
      src="https://www.google.com/maps?q=Greater+Toronto+Area,+ON&amp;z=9&amp;output=embed"></iframe>
    <div style="display:flex;flex-direction:column;gap:16px">{areas_html()}
      <a class="btn btn-navy" href="/service-areas/">See all {sum(len(r["towns"]) for r in REGIONS)}+ areas we serve</a></div>
  </div>
</div></section>
{faq_html(h['faqs'], soft=False)}
{cta_html()}"""
    write("", layout(slug="", title=h["title"], description=h["description"], body=body,
                     schemas=[business_schema(), faq_schema(h["faqs"])]))


def aside_html(current_slug):
    group = next((g for _, g in CATEGORIES if current_slug in g), [])
    order = [BY_SLUG[g] for g in group if g != current_slug] + \
            [s for s in FEATURED if s["slug"] not in group and s["slug"] != current_slug]
    links = "".join(f'<li><a href="{url(s["slug"])}">{escape(s["name"])}</a></li>' for s in order[:9]) + \
        '<li><a href="/services/"><strong>All services</strong></a></li>'
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


def extras_html(slug, city=None, price_only=False):
    e = EXTRAS.get(slug)
    if not e:
        return ""
    where = f" in {escape(city)}" if city else ""
    factors = "".join(f"<li>{escape(f)}</li>" for f in e["price_factors"])
    return (f"<h2>What affects the price{where}</h2><p>Every window is different. The price depends on:</p>"
            f'<ul class="ticks">{factors}</ul><p>Text us a photo of your window and we\'ll give you a free quote, '
            f"usually the same day.</p>" + ("" if price_only else e["html"]))


def build_service(s):
    trail = [("Home", "/"), ("Services", "/services/"), (s["name"], url(s["slug"]))]
    more = extras_html(s["slug"])
    if s["slug"] in COMBO_SERVICES:
        short = COMBO_SERVICES[s["slug"]]["short"]
        links = "".join(f'<li><a href="{url(combo_slug(c["slug"], s["slug"]))}">{escape(short)} {escape(c["name"])}</a></li>'
                        for c in CITIES)
        extra = f"<h2>Where we do this work</h2><p>Anywhere in {SITE['area']}, including:</p><ul class=\"areas\">{links}</ul>"
    else:
        extra = f"<h2>Where we do this work</h2><p>Anywhere in {SITE['area']}, including:</p>{areas_html()}"
    build_article(s, trail, [service_schema(s["name"], s["slug"], SITE["area"])],
                  media_block(s["slug"], s["name"]) + more + extra)


def build_city(c):
    trail = [("Home", "/"), (f"Window repair {c['name']}", url(c["slug"]))]
    items = "".join(
        f'<li><a href="{url(combo_slug(c["slug"], s["slug"]) if s["slug"] in COMBO_SERVICES else s["slug"])}">'
        f'{escape(s["name"])}{" in " + escape(c["name"]) if s["slug"] in COMBO_SERVICES else ""}</a></li>' for s in SERVICES)
    extra = f"<h2>Our services in {escape(c['name'])}</h2><ul>{items}</ul>"
    build_article(c, trail, [service_schema(f"Window repair in {c['name']}", c["slug"], c["name"])], extra)


def build_combo(c, s):
    cs = COMBO_SERVICES[s["slug"]]
    loc = CITY_LOCAL[c["name"]]
    city = c["name"]
    slug = combo_slug(c["slug"], s["slug"])
    title_name = f"{cs['short']} in {city}"
    trail = [("Home", "/"), (f"Window repair {city}", url(c["slug"])), (cs["short"], url(slug))]
    bullets = "".join(f"<li>{escape(b)}</li>" for b in cs["bullets"])
    why = "".join(f'<div><h3>{escape(t)}</h3><p>{escape(d)}</p></div>' for t, d in WHY)
    others = "".join(
        f'<li><a href="{url(combo_slug(c["slug"], k))}">{escape(v["short"])} in {escape(city)}</a></li>'
        for k, v in COMBO_SERVICES.items() if k != s["slug"])
    same_service = "".join(
        f'<li><a href="{url(combo_slug(o["slug"], s["slug"]))}">{escape(o["name"])}</a></li>'
        for o in CITIES if o["slug"] != c["slug"])
    faqs = [(q.format(city=city), a.format(city=city)) for q, a in cs["faqs"]]
    nearby = ", ".join(loc["nearby"])
    body = f"""
<section class="page-hero"><div class="wrap">
  {crumbs_html(trail)}
  <span class="tag">{escape(city)}, ON</span>
  <h1>{escape(title_name)}</h1>
  <p class="lede">{escape(cs['lede'])}</p>
  <div class="actions">{call_btn("combo-hero")}{text_btn("combo-hero")}</div>
</div></section>
{trust_html()}
<div class="wrap article">
  <div class="prose">
    {media_block(s["slug"], title_name)}
    <h2>{escape(cs['short'])} in {escape(city)}: what we do</h2>
    <p>{escape(cs['what'])}</p>
    <ul class="ticks">{bullets}</ul>
    {extras_html(s["slug"], city, price_only=True)}
    <h2>Why {escape(city)} homeowners call us</h2>
    <div class="why">{why}</div>
    <div class="local-box">
      <h2>Serving {escape(city)} and nearby</h2>
      <p>{escape(loc['local'])}</p>
      <p>We also serve {escape(nearby)}. See our <a href="{url(c['slug'])}">{escape(city)} service area page</a>
        or learn more about <a href="{url(s['slug'])}">{escape(s['name'].lower())}</a>.</p>
    </div>
    <h2>Other repairs in {escape(city)}</h2>
    <ul>{others}</ul>
  </div>
  {aside_html(s['slug'])}
</div>
{faq_html(faqs)}
<section class="section"><div class="wrap">
  <div class="section-head"><div><h2>{escape(cs['short'])} in other cities</h2></div></div>
  <ul class="areas">{same_service}</ul>
</div></section>
{cta_html()}"""
    desc = (f"{cs['short']} in {city}, ON. {cs['lede'].split('.')[0]}. Free estimates, quotes from a photo. "
            f"Call {SITE['phone']}.")
    schemas = [business_schema(), breadcrumb_schema(trail), service_schema(title_name, slug, city), faq_schema(faqs)]
    write(slug, layout(slug=slug, title=f"{title_name} | {SITE['name']}", description=desc, body=body,
                       schemas=schemas))


# ---------------------------------------------------------------- towns & regions
RICH = {c["name"]: c["slug"] for c in CITIES}


def town_href(name):
    return url(RICH.get(name) or town_slug(name))


def region_slug(r):
    return f"areas/{r['slug']}"


def town_links(names):
    return "".join(f'<li><a href="{town_href(n)}">{escape(n)}</a></li>' for n in names)


def build_town(r, name, part):
    slug = town_slug(name)
    where = f"{name}, {part}" if part else name
    region_names = [n for n, _ in r["towns"] if n != name]
    i = [n for n, _ in r["towns"]].index(name)
    nearby = (region_names[i:] + region_names[:i])[:8]
    trail = [("Home", "/"), ("Service areas", "/service-areas/"), (r["name"], url(region_slug(r))),
             (name, url(slug))]
    services = "".join(f'<li><a href="{url(sv["slug"])}">{escape(sv["name"])}</a>: {escape(sv["card"])}</li>'
                       for sv in SERVICES)
    faqs = [
        (f"Do you do window repair in {name}?",
         f"Yes. {name} is part of our {r['name']} service area. Call or text us and we'll book a time that works."),
        ("Can you give me a price from a photo?",
         "Usually, yes. Text us a photo of the whole window and a close-up of the problem. For sealed glass we confirm the exact size when we measure."),
        ("Do I need a new window or just a repair?",
         "If the frame is solid, a new sealed unit or a new crank, hinge or roller is usually all you need, at a fraction of the cost of a new window."),
        ("Which window brands do you repair?",
         "Most of them, including the windows builders install in new subdivisions. See our brands page or send us a photo of the label."),
    ]
    part_line = f" {escape(name)} is {escape(part)}." if part else ""
    body = f"""
<section class="page-hero"><div class="wrap">
  {crumbs_html(trail)}
  <span class="tag">{escape(r['name'])}</span>
  <h1>Window repair in {escape(name)}</h1>
  <p class="lede">Foggy glass, broken windows, stripped cranks and sticking patio doors repaired in {escape(where)}. Free estimates and quotes from a photo.</p>
  <div class="actions">{call_btn("town-hero")}{text_btn("town-hero")}</div>
</div></section>
{trust_html()}
<div class="wrap article">
  <div class="prose">
    {(f'<img class="prose-img" src="{photo("cities/" + slug)}" alt="Window repair job in {escape(name)}" loading="lazy">') if photo("cities/" + slug) else ""}
    <h2>Window and glass repair in {escape(name)}</h2>
    <p>We repair windows and patio doors in homes, condos and businesses across {escape(r['name'])}.{part_line} Most problems come down to one failed part, so we replace the glass or hardware and keep your frame, trim and walls as they are.</p>
    <div class="local-box">
      <h2>About windows in {escape(r['name'])}</h2>
      <p>{escape(r['intro'])}</p>
    </div>
    <h2>What we fix in {escape(name)}</h2>
    <ul>{services}</ul>
    <h2>How it works</h2>
    <ol>
      <li><strong>Send a photo.</strong> Text us or use the online form.</li>
      <li><strong>Get a price.</strong> We quote from the photo or come to measure.</li>
      <li><strong>We fix it.</strong> New glass or parts, installed and tested.</li>
    </ol>
    <h2>Nearby areas we serve</h2>
    <ul class="areas">{town_links(nearby)}<li><a href="{url(region_slug(r))}">All of {escape(r['name'])}</a></li></ul>
  </div>
  {aside_html("")}
</div>
{faq_html(faqs)}
{cta_html()}"""
    desc = (f"Window and glass repair in {name}: foggy sealed units, broken glass, cranks, hinges and patio doors. "
            f"Free estimates. Call {SITE['phone']}.")
    schemas = [business_schema(), breadcrumb_schema(trail),
               service_schema(f"Window repair in {name}", slug, name), faq_schema(faqs)]
    write(slug, layout(slug=slug, title=f"Window Repair {name} | Glass, Cranks & Patio Doors", description=desc,
                       body=body, schemas=schemas))


def build_region(r):
    slug = region_slug(r)
    trail = [("Home", "/"), ("Service areas", "/service-areas/"), (r["name"], url(slug))]
    body = f"""
<section class="page-hero"><div class="wrap">
  {crumbs_html(trail)}
  <span class="tag">Service area</span>
  <h1>Window repair in {escape(r['name'])}</h1>
  <p class="lede">{escape(r['intro'])}</p>
  <div class="actions">{call_btn("region-hero")}{text_btn("region-hero")}</div>
</div></section>
{trust_html()}
<section class="section"><div class="wrap">
  <div class="section-head"><div><h2>Towns and cities in {escape(r['name'])}</h2>
    <p>Pick your community for local details, or just call us.</p></div></div>
  <ul class="areas">{town_links([n for n, _ in r['towns']])}</ul>
</div></section>
<section class="section soft"><div class="wrap">
  <div class="section-head"><div><h2>What we fix</h2></div></div>
  {cards_html(SERVICES)}
</div></section>
{cta_html()}"""
    write(slug, layout(slug=slug, title=f"Window Repair {r['name']} | {SITE['name']}",
                       description=f"Window, glass and patio door repair across {r['name']}. Free estimates, quotes from a photo.",
                       body=body, schemas=[business_schema(), breadcrumb_schema(trail)]))


def build_areas_index():
    trail = [("Home", "/"), ("Service areas", "/service-areas/")]
    blocks = "".join(f"""
<section class="section{' soft' if i % 2 else ''}"><div class="wrap">
  <div class="section-head"><div><h2>{escape(r['name'])}</h2></div>
    <a class="more-link" href="{url(region_slug(r))}">About {escape(r['name'])} →</a></div>
  <ul class="areas">{town_links([n for n, _ in r['towns']])}</ul>
</div></section>""" for i, r in enumerate(REGIONS))
    total = sum(len(r["towns"]) for r in REGIONS)
    body = f"""
<section class="page-hero"><div class="wrap">
  {crumbs_html(trail)}
  <span class="tag">{total}+ communities</span>
  <h1>Our service areas</h1>
  <p class="lede">We repair windows, glass and patio doors across Toronto, the GTA, Hamilton, Niagara, Waterloo, Barrie and the communities in between.</p>
  <div class="actions">{call_btn("areas-hero")}{text_btn("areas-hero")}</div>
</div></section>
{blocks}
{cta_html()}"""
    write("service-areas", layout(slug="service-areas", title=f"Service Areas | {SITE['name']}",
                                  description="Every city and town where we repair windows, glass and patio doors: Toronto, York, Peel, Halton, Durham, Hamilton, Niagara, Waterloo, Barrie and more.",
                                  body=body, schemas=[business_schema(), breadcrumb_schema(trail)]))


def build_pages():
    for p in PAGES + EXTRA_PAGES:
        trail = [("Home", "/"), (p["crumb"], url(p["slug"]))]
        story = f"<h2>Our story</h2><p>{escape(ABOUT_STORY)}</p>" if ABOUT_STORY else ""
        body = p["body"].format(
            crumbs=crumbs_html(trail), phone=SITE["phone"], tel=SITE["tel"], area=SITE["area"],
            form=full_form(p["slug"]), cards=grouped_cards_html(), call=call_btn(p["slug"]),
            text=text_btn(p["slug"]), cta=cta_html(), trust=trust_html(), story=story,
            promises=promises_list(), check12=check12_html(), quote_forms=quote_forms_html(),
            blog_list=blog_list_html())
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
            [p["slug"] for p in PAGES + EXTRA_PAGES if not p.get("noindex")] + \
            [f"blog/{b['slug']}" for b in BLOG] + \
            ([f"our-work/{w['slug']}" for w in WORK] + ["our-work"] if WORK else []) + \
            [combo_slug(c["slug"], k) for c in CITIES for k in COMBO_SERVICES] + ["service-areas"] + \
            [region_slug(r) for r in REGIONS] + \
            [town_slug(n) for r in REGIONS for n, _ in r["towns"] if n not in RICH]
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
        for sv in SERVICES:
            if sv["slug"] in COMBO_SERVICES:
                build_combo(c, sv)
    build_pages()
    build_blog_posts()
    build_work()
    build_areas_index()
    for r in REGIONS:
        build_region(r)
        for n, part in r["towns"]:
            if n not in RICH:
                build_town(r, n, part)
    build_404()
    build_sitemap()
    print(f"Built {len(list(OUT.rglob('*.html')))} pages into {OUT}")


if __name__ == "__main__":
    main()
