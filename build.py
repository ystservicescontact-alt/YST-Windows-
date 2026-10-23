#!/usr/bin/env python3
"""Builds the Window Repair GTA static site into ./site.

Usage: python3 build.py
Edit business details in SITE and page content in content.py, then rebuild.
"""
import json
import shutil
from datetime import date
from html import escape
from pathlib import Path

from content import SERVICES, CITIES, HOME, PAGES

ROOT = Path(__file__).parent
OUT = ROOT / "site"

SITE = {
    "name": "Window Repair GTA",
    "domain": "https://windowrepairgta.ca",
    "phone": "(365) 340-4760",
    "tel": "+13653404760",
    "area": "Toronto and the Greater Toronto Area",
}

FONTS = ("https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800"
         "&family=Public+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap")


def url(slug):
    return "/" if not slug else f"/{slug}/"


def business_schema():
    return {
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "@id": SITE["domain"] + "/#business",
        "name": SITE["name"],
        "url": SITE["domain"] + "/",
        "telephone": SITE["tel"],
        "priceRange": "$$",
        "areaServed": [{"@type": "City", "name": c["name"]} for c in CITIES] + [
            {"@type": "City", "name": "Toronto"}],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Window and glass repair services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"],
                                                    "url": SITE["domain"] + url(s["slug"])}}
                for s in SERVICES
            ],
        },
    }


def faq_schema(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
    }


def breadcrumb_schema(trail):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": name,
                             "item": SITE["domain"] + href} for i, (name, href) in enumerate(trail)],
    }


def service_schema(page):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": page["name"],
        "serviceType": page["name"],
        "provider": {"@id": SITE["domain"] + "/#business"},
        "areaServed": page.get("area_served", SITE["area"]),
        "url": SITE["domain"] + url(page["slug"]),
    }


def faq_html(faqs):
    if not faqs:
        return ""
    items = "\n".join(
        f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q, a in faqs)
    return f"""
<section class="section tight" id="faq">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Questions</p><h2>Common questions</h2></div>
    <div class="faq">{items}</div>
  </div>
</section>"""


def crumbs_html(trail):
    parts = []
    for i, (name, href) in enumerate(trail):
        if i == len(trail) - 1:
            parts.append(f'<li aria-current="page">{escape(name)}</li>')
        else:
            parts.append(f'<li><a href="{href}">{escape(name)}</a></li>')
    return f'<nav class="crumbs wrap" aria-label="Breadcrumb"><ol>{"".join(parts)}</ol></nav>'


def cta_html():
    return f"""
<section class="cta">
  <div class="wrap">
    <div><h2>Get a free estimate</h2><p>Send a photo of the window. We usually reply the same day.</p></div>
    <div class="actions">
      <a class="btn btn-primary" href="tel:{SITE['tel']}">Call {SITE['phone']}</a>
      <a class="btn btn-ghost" href="/contact/">Request an estimate</a>
    </div>
  </div>
</section>"""


def aside_html(current_slug):
    links = "".join(
        f'<li><a href="{url(s["slug"])}">{escape(s["name"])}</a></li>'
        for s in SERVICES if s["slug"] != current_slug)
    return f"""
<aside class="aside" aria-label="Contact">
  <h2>Free estimate</h2>
  <a class="big" href="tel:{SITE['tel']}">{SITE['phone']}</a>
  <a class="btn btn-primary" href="/contact/">Send photos for a quote</a>
  <p class="eyebrow">Other services</p>
  <ul>{links}</ul>
</aside>"""


def quote_form(source):
    problems = "".join(f"<option>{escape(s['name'])}</option>" for s in SERVICES) + "<option>Something else</option>"
    return f"""
<form class="quote-form" name="quote" method="POST" action="/thanks/" data-netlify="true"
      netlify-honeypot="bot-field" enctype="multipart/form-data">
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
  <label for="q-details">Details <span class="hint">Location in the house, size if you know it</span>
    <textarea id="q-details" name="details"></textarea></label>
  <label for="q-photo">Photo <span class="hint">Optional, one image up to 8 MB</span>
    <input id="q-photo" name="photo" type="file" accept="image/*"></label>
  <label for="q-heard">How did you find us?
    <select id="q-heard" name="heard">
      <option>Google search</option><option>Google Maps</option><option>Friend or neighbour</option>
      <option>Saw your truck</option><option>Other</option>
    </select></label>
  <button class="btn btn-primary" type="submit">Request my estimate</button>
</form>"""


def layout(*, slug, title, description, body, schemas=(), scripts=(), noindex=False):
    canonical = SITE["domain"] + url(slug)
    nav_services = "/services/" if any(p["slug"] == "services" for p in PAGES) else "/#services"
    service_links = "".join(f'<li><a href="{url(s["slug"])}">{escape(s["name"])}</a></li>' for s in SERVICES)
    city_links = "".join(f'<li><a href="{url(c["slug"])}">Window repair {escape(c["name"])}</a></li>' for c in CITIES)
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    js = "\n".join(f'<script src="{s}" defer></script>' for s in scripts)
    robots = '<meta name="robots" content="noindex">' if noindex else ""
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
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/" aria-label="{SITE['name']} home">
      <span class="logo-mark" aria-hidden="true"><span></span><span></span><span></span><span></span></span>
      {SITE['name']}
    </a>
    <nav class="nav" aria-label="Main">
      <a href="{nav_services}">Services</a>
      <a href="/#areas">Areas</a>
      <a class="phone" href="tel:{SITE['tel']}">{SITE['phone']}</a>
      <a class="btn btn-primary" href="/contact/">Free estimate</a>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer>
  <div class="wrap footer-grid">
    <div>
      <h2>{SITE['name']}</h2>
      <p>Window, glass and patio door repair for homes and businesses across {SITE['area']}.</p>
      <p style="margin-top:.8rem"><a href="tel:{SITE['tel']}"><strong>{SITE['phone']}</strong></a></p>
    </div>
    <div><h2>Services</h2><ul>{service_links}</ul></div>
    <div><h2>Areas</h2><ul>{city_links}</ul></div>
  </div>
  <div class="wrap footer-bottom">© {date.today().year} {SITE['name']}</div>
</footer>
<div class="call-bar">
  <a class="btn btn-primary" href="tel:{SITE['tel']}">Call now</a>
  <a class="btn btn-ghost" href="/contact/">Free estimate</a>
</div>
{js}
</body>
</html>
"""


def write(slug, html):
    path = OUT / (slug or "") / "index.html" if slug else OUT / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def services_grid(items):
    cards = "".join(f"""
<a class="service" href="{url(s['slug'])}">
  <h3>{escape(s['name'])}</h3>
  <p>{escape(s['card'])}</p>
  <p class="spec">{escape(s['spec'])}</p>
  <span class="more">Learn more</span>
</a>""" for s in items)
    return f'<div class="services">{cards}</div>'


def areas_list():
    items = "".join(f'<li><a href="{url(c["slug"])}">{escape(c["name"])}</a></li>' for c in CITIES)
    extra = "".join(f"<li><span>{n}</span></li>" for n in HOME["extra_areas"])
    return f'<ul class="areas">{items}{extra}</ul>'


def build_home():
    body = HOME["hero"].format(phone=SITE["phone"], tel=SITE["tel"])
    body += f"""
<section class="section" id="services">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Services</p><h2>What we repair</h2>
      <p>Most window problems come down to one worn or broken part. We find it and replace it.</p></div>
    {services_grid(SERVICES)}
  </div>
</section>"""
    body += HOME["compare"] + HOME["process"]
    body += f"""
<section class="section tight" id="areas">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Service area</p><h2>We come to you across the GTA</h2>
      <p>Don't see your city? Call us. We likely cover it.</p></div>
    {areas_list()}
  </div>
</section>"""
    body += faq_html(HOME["faqs"])
    body += f"""
<section class="section tight quote" id="quote">
  <div class="wrap">
    <div>
      <div class="section-head" style="margin-bottom:0"><p class="eyebrow">Free estimate</p>
        <h2>Tell us about your window</h2><p>We'll reply with a price or a time to come and measure.</p></div>
      <div class="contact-list">
        <div><span class="eyebrow">Phone</span><a class="value" href="tel:{SITE['tel']}">{SITE['phone']}</a></div>
        <div><span class="eyebrow">Service area</span><span>{SITE['area']}</span></div>
      </div>
      <p class="note" style="margin-top:1.8rem">Tip: a photo of the whole window plus a close-up of the
        printing on the metal spacer between the panes helps us quote faster.</p>
    </div>
    {quote_form("home")}
  </div>
</section>"""
    schemas = [business_schema(), faq_schema(HOME["faqs"])]
    write("", layout(slug="", title=HOME["title"], description=HOME["description"], body=body,
                     schemas=schemas, scripts=["/assets/fog.js"]))


def build_article(page, trail, extra_schemas=(), extra_html=""):
    body = crumbs_html(trail)
    body += f"""
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">{escape(page['eyebrow'])}</p>
    <h1>{escape(page['h1'])}</h1>
    <p class="lede">{escape(page['lede'])}</p>
    <div class="actions">
      <a class="btn btn-primary" href="tel:{SITE['tel']}">Call {SITE['phone']}</a>
      <a class="btn btn-ghost" href="/contact/">Send photos for a quote</a>
    </div>
  </div>
</section>
<div class="wrap article">
  <div class="prose">{page['body']}{extra_html}</div>
  {aside_html(page['slug'])}
</div>"""
    body += faq_html(page.get("faqs", []))
    body += cta_html()
    schemas = [business_schema(), breadcrumb_schema(trail), *extra_schemas]
    if page.get("faqs"):
        schemas.append(faq_schema(page["faqs"]))
    write(page["slug"], layout(slug=page["slug"], title=page["title"], description=page["description"],
                               body=body, schemas=schemas))


def build_service(s):
    trail = [("Home", "/"), (s["name"], url(s["slug"]))]
    cities = "".join(f'<li><a href="{url(c["slug"])}">{escape(c["name"])}</a></li>' for c in CITIES)
    extra = f'<h2>Where we do this work</h2><p>We cover {SITE["area"]}, including:</p><ul class="areas">{cities}</ul>'
    build_article(s, trail, [service_schema(s)], extra)


def build_city(c):
    trail = [("Home", "/"), (f"Window repair {c['name']}", url(c["slug"]))]
    services = "".join(
        f'<li><a href="{url(s["slug"])}">{escape(s["name"])}</a> in {escape(c["name"])}</li>' for s in SERVICES)
    extra = f"<h2>Services in {escape(c['name'])}</h2><ul>{services}</ul>"
    page = dict(c, name=f"Window repair in {c['name']}", area_served=c["name"])
    build_article(page, trail, [service_schema(page)], extra)


def build_pages():
    for p in PAGES:
        trail = [("Home", "/"), (p["crumb"], url(p["slug"]))]
        body = crumbs_html(trail) + p["body"].format(
            phone=SITE["phone"], tel=SITE["tel"], area=SITE["area"],
            form=quote_form(p["slug"]), services=services_grid(SERVICES))
        write(p["slug"], layout(slug=p["slug"], title=p["title"], description=p["description"], body=body,
                                schemas=[business_schema(), breadcrumb_schema(trail)],
                                noindex=p.get("noindex", False)))


def build_404():
    body = f"""
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Page not found</p>
  <h1>This page doesn't exist</h1>
  <p class="lede">The link may be old. Try the home page, or call us at {SITE['phone']}.</p>
  <div class="actions"><a class="btn btn-primary" href="/">Go to the home page</a></div>
</div></section>"""
    (OUT / "404.html").write_text(
        layout(slug="404", title=f"Page not found | {SITE['name']}", description="Page not found.",
               body=body, noindex=True), encoding="utf-8")


def build_sitemap():
    slugs = [""] + [s["slug"] for s in SERVICES] + [c["slug"] for c in CITIES] + \
            [p["slug"] for p in PAGES if not p.get("noindex")]
    today = date.today().isoformat()
    urls = "\n".join(f"  <url><loc>{SITE['domain']}{url(s)}</loc><lastmod>{today}</lastmod></url>" for s in slugs)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE['domain']}/sitemap.xml\n",
                                    encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "src" / "assets", OUT / "assets")
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
