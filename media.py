"""Photo and video slots.

Nothing is shown until the file exists. Drop files into src/photos/ using
these exact names (jpg, jpeg, png or webp), then run python3 build.py.

  hero.jpg                          home page background photo
  team.jpg                          you / your team / your van (home page)
  services/<service-slug>.jpg       photo on the service card and service page
  services/<service-slug>-before.jpg + -after.jpg   before/after pair on the service page
  cities/<town-page-slug>.jpg       a job photo on that town's page
  gallery/<NN>-before.jpg + <NN>-after.jpg          extra before/after pairs (home page)

Videos are YouTube links: add the video ID to VIDEOS below.
"""
from pathlib import Path

PHOTOS = Path(__file__).parent / "src" / "photos"
EXTS = (".jpg", ".jpeg", ".png", ".webp")

# YouTube video IDs, e.g. {"foggy-window-repair": "dQw4w9WgXcQ", "home": "..."}
VIDEOS = {}

# Captions for gallery pairs, keyed by number: {"01": ("Foggy picture window", "Mississauga")}
GALLERY_CAPTIONS = {}


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
            title, city = GALLERY_CAPTIONS.get(n, ("Recent job", ""))
            out.append({"before": p[0], "after": p[1], "title": title, "city": city})
    return out


def video_html(key, title):
    vid = VIDEOS.get(key)
    if not vid:
        return ""
    return (f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="{title}" '
            f'loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture" allowfullscreen></iframe></div>')
