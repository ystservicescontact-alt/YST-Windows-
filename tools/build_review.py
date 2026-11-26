"""Builds a Hebrew review page of every explainer (for checking the animations; the site stays English).

python3 tools/build_review.py <out dir>
"""
import copy, re, shutil, sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
from explainers import EXPLAINERS, explainer_html  # noqa: E402
from explainers_he import HE, CATEGORIES_HE  # noqa: E402
from content import SERVICES  # noqa: E402
from services_more import CATEGORIES  # noqa: E402

NAMES = {}
for s in SERVICES:
    NAMES[s["slug"]] = s["name"]


def hebrew(slug):
    e = copy.deepcopy(EXPLAINERS[slug]); he = HE[slug]
    e["heading"] = he["heading"]
    assert len(he["steps"]) == len(e["steps"]), slug
    e["steps"] = [(t, txt) for (t, _), txt in zip(e["steps"], he["steps"])]
    cfg = e.get("config")
    if cfg:
        real = "Real job" in " ".join(cfg.get("title", []))
        t = he.get("title")
        cfg["title"] = t if isinstance(t, list) else [t or cfg["title"][0], "עבודה אמיתית · טורונטו" if real else "Window Repair GTA"]
        labels = [f for f in cfg["fx"] if f["type"] == "label"]
        if isinstance(he.get("labels"), dict):
            for f in labels: f["text"] = he["labels"].get(f["text"], f["text"])
        elif he.get("labels"):
            for f, txt in zip(labels, he["labels"]): f["text"] = txt
        for f in cfg["fx"]:
            if f["type"] == "gap":
                f["text"] = (he.get("gap") or he.get("labels") if isinstance(he.get("labels"), dict) else he.get("gap") or {}).get(f["text"], f["text"])
        states = cfg["bubble"]["states"]
        if isinstance(he.get("tags"), dict):
            for st in states: st["tag"] = he["tags"].get(st["tag"], st["tag"])
        elif he.get("tags"):
            for st, txt in zip(states, he["tags"]): st["tag"] = txt
    html = explainer_html(slug) if False else None
    EXPLAINERS["__he"] = e
    html = explainer_html("__he")
    del EXPLAINERS["__he"]
    html = html.replace('<span class="tag">See the problem</span>', '<span class="tag">הבעיה</span>')
    html = re.sub(r'<script src="[^"]+"[^>]*></script>|<script type="module"[^>]*></script>', "", html)
    html = html.replace('"/photos/', '"photos/').replace('"/assets/', '"assets/')
    return html


def main(out):
    out = Path(out); shutil.rmtree(out, ignore_errors=True); out.mkdir(parents=True)
    for d in ["assets/3d", "photos/explainers", "photos/services"]:
        (out / d).mkdir(parents=True, exist_ok=True)
    for f in ["style.css", "explainers.js", "explainer-photo.js", "explainer3d.js"]:
        shutil.copy(ROOT / "src/assets" / f, out / "assets" / f)
    for f in (ROOT / "src/assets/3d").iterdir():
        shutil.copy(f, out / "assets/3d" / f.name)
    used = set()
    sections, toc = [], []
    for cat, slugs in CATEGORIES_HE:
        cards = []
        for slug in slugs:
            if slug not in EXPLAINERS or slug not in HE: continue
            frag = hebrew(slug)
            used.update(re.findall(r'photos/(?:explainers|services)/[\w.-]+', frag))
            name = NAMES.get(slug, slug)
            cards.append(f'<article class="rv-card" id="{slug}"><p class="rv-page">בעמוד באתר: <b dir="ltr">{escape(name)}</b> · <span dir="ltr">/{slug}/</span></p>{frag}</article>')
            toc.append(f'<a href="#{slug}">{escape(HE[slug]["heading"])}</a>')
        sections.append(f'<section class="rv-cat"><h2 class="rv-cat-h">{cat}</h2>{"".join(cards)}</section>')
    for u in used:
        shutil.copy(ROOT / "src" / u, out / u)
    page = f"""<meta charset="utf-8">
<title>סקירת אנימציות האתר</title>
<meta name="description" content="כל אנימציות ההסבר של Window Repair GTA בעברית, לבדיקה">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;800&display=swap">
<link rel="stylesheet" href="assets/style.css">
<style>
:root {{ --rv-bg: #F2F5F9; --rv-card: #ffffff; --rv-ink: #0F1B33; --rv-muted: #4A5A70; --rv-red: #C41E25; color-scheme: light; }}
body {{ background: var(--rv-bg); color: var(--rv-ink); font-family: Heebo, Arial, sans-serif; }}
.rv {{ direction: rtl; max-width: 1100px; margin: 0 auto; padding-block: 28px 80px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); display: flex; flex-direction: column; gap: 28px; }}
.rv h1 {{ font: 800 clamp(28px, 4vw, 40px)/1.1 Heebo, Arial, sans-serif; margin: 0; }}
.rv-intro {{ font-size: 17px; line-height: 1.6; color: var(--rv-muted); max-width: 62ch; margin: 0; }}
.rv-toc {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.rv-toc a {{ font-size: 14px; padding: 6px 10px; background: var(--rv-card); border: 1px solid #E3E8EF; color: var(--rv-ink); text-decoration: none; }}
.rv-cat {{ display: flex; flex-direction: column; gap: 22px; }}
.rv-cat-h {{ font: 800 26px Heebo, Arial, sans-serif; margin: 12px 0 0; padding-bottom: 6px; border-bottom: 3px solid var(--rv-red); }}
.rv-card {{ background: var(--rv-card); border: 1px solid #E3E8EF; padding: 6px 18px 18px; }}
.rv-page {{ font-size: 14px; color: var(--rv-muted); margin: 10px 0 0; }}
.rv .ex-section {{ padding-block: 10px 0; }}
.rv .ex-section .wrap {{ padding: 0; }}
.rv .ex-head h2 {{ font-family: Heebo, Arial, sans-serif; text-transform: none; font-size: 24px; }}
.rv .ex-caption, .rv .ex-steps li {{ font-family: Heebo, Arial, sans-serif; direction: rtl; }}
.rv .ex-stage {{ direction: ltr; }}
.rv .ex-steps li {{ border-left: 0; border-right: 4px solid #E3E8EF; }}
.rv .ex-steps li.on {{ border-right-color: #E5262E; }}
.rv .exp-label, .rv .exp-tag, .rv .exp-dim, .rv .exp-tb-h, .rv .exp-tb-l {{ font-family: Heebo, Arial, sans-serif; }}
</style>
<main class="rv">
  <h1>סקירת אנימציות ההסבר</h1>
  <p class="rv-intro">כל האנימציות שבנויות לאתר, כאן עם כתוביות בעברית כדי שיהיה קל לעבור עליהן. באתר עצמו הן באנגלית. כל אנימציה מתחילה לבד כשגוללים אליה, ואפשר ללחוץ על שלב כדי לקפוץ אליו.</p>
  <nav class="rv-toc" aria-label="תוכן">{"".join(toc)}</nav>
  {"".join(sections)}
</main>
<script src="assets/explainers.js" defer></script>
<script src="assets/explainer-photo.js" defer></script>
<script type="module" src="assets/explainer3d.js"></script>
"""
    (out / "index.html").write_text(page, encoding="utf-8")
    print(len(toc), "scenes;", len(used), "photos")


if __name__ == "__main__":
    main(sys.argv[1])
