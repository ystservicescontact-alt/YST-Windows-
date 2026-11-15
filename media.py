"""Photo and video slots.

Nothing is shown until the file exists. Drop files into src/photos/ using
these exact names (jpg, jpeg, png or webp), then run python3 build.py.

  hero.jpg                          home page background photo
  team.jpg                          you / your team / your van (home page)
  services/<service-slug>.jpg       photo on the service card and service page
  services/<service-slug>-before.jpg + -after.jpg   before/after pair on the service page
  cities/<town-page-slug>.jpg       a job photo on that town's page
  gallery/<NN>-before.jpg + <NN>-after.jpg          extra before/after pairs (home page)
  jobs/<job-key>/<NN>-before.jpg + <NN>-after.jpg   before/after jobs on a service page (see JOB_PAGES)

Videos are YouTube links: add the video ID to VIDEOS below.
"""
from pathlib import Path

PHOTOS = Path(__file__).parent / "src" / "photos"
EXTS = (".jpg", ".jpeg", ".png", ".webp")

# YouTube video IDs, e.g. {"foggy-window-repair": "dQw4w9WgXcQ", "home": "..."}
VIDEOS = {}

# Captions for gallery pairs, keyed by number: {"01": ("Foggy picture window", "Mississauga")}
# Before/after jobs in src/photos/gallery/NN-before.jpg + NN-after.jpg.
# number: (title, city, service page slugs it also shows on). Every pair shows on the home page.
GALLERY_CAPTIONS = {
    "01": ("Foggy glass replacement", "Downtown Toronto", ["foggy-window-repair", "window-glass-replacement"]),
}


def photo(name):
    """Return the /photos/... URL for a slot if a file exists, else None."""
    for ext in EXTS:
        f = PHOTOS / f"{name}{ext}"
        if f.exists():
            return f"/photos/{name}{ext}"
    return None


def pair(name):
    b, a = photo(f"{name}-before"), photo(f"{name}-after")
    return (b, a) if b and a else None


def gallery_pairs():
    """Numbered pairs from src/photos/gallery/, sorted by number."""
    d = PHOTOS / "gallery"
    if not d.exists():
        return []
    nums = sorted({f.name.split("-")[0] for f in d.iterdir() if "-before" in f.name})
    out = []
    for n in nums:
        p = pair(f"gallery/{n}")
        if p:
            title, city, services = (list(GALLERY_CAPTIONS.get(n, ("Recent job", ""))) + [[]])[:3]
            out.append({"before": p[0], "after": p[1], "title": title, "city": city, "services": services})
    return out[::-1]  # newest first


# Our own video files in src/videos/: page slug -> (file, poster photo, title)
LOCAL_VIDEOS = {
    "storm-doors": ("/videos/storm-door-install-north-york.mp4", "/photos/storm-door-install-north-york-poster.jpg",
                    "Storm door installation in North York"),
}


def video_html(key, title):
    local = LOCAL_VIDEOS.get(key)
    if local:
        src, poster, vtitle = local
        return (f'<figure class="video-local"><video controls playsinline preload="none" poster="{poster}" '
                f'aria-label="{vtitle}"><source src="{src}" type="video/mp4"></video>'
                f'<figcaption>{vtitle}</figcaption></figure>')
    vid = VIDEOS.get(key)
    if not vid:
        return ""
    return (f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="{title}" '
            f'loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture" allowfullscreen></iframe></div>')


# Job folders under src/photos/jobs/ and the service page each one shows on.
JOB_PAGES = {
    "window-hinge-repair": ("window-hinge-repair", "Hinge replacement"),
    "commercial-door-glass": ("commercial-glass-repair", "Commercial door glass"),
    "window-glass-replacement": ("window-glass-replacement", "Glass replacement"),
    "condo-glass": ("window-glass-replacement", "Condo glass replacement"),
}

# Captions for job pairs: {("condo-glass", "01"): ("3 panes replaced", "Toronto")}
JOB_CAPTIONS = {}


def job_pairs(service_slug):
    """Before/after pairs from every job folder that maps to this service page."""
    out = []
    for key, (page, default_title) in JOB_PAGES.items():
        if page != service_slug:
            continue
        d = PHOTOS / "jobs" / key
        if not d.exists():
            continue
        nums = sorted({f.name.split("-")[0] for f in d.iterdir() if "-before" in f.name})
        for n in nums:
            p = pair(f"jobs/{key}/{n}")
            if p:
                title, city = JOB_CAPTIONS.get((key, n), (default_title, ""))
                out.append({"before": p[0], "after": p[1], "title": title, "city": city})
    return out
