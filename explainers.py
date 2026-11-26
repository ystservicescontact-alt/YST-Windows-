"""Animated problem explainers shown near the top of service pages.
Each step's start time (seconds) must match the timeline in src/assets/explainers.js."""
from html import escape

EXPLAINERS = {
    "window-crank-repair": {
        "scene": "crank3d",
        "render": "3d",
        "images": {"view": "/photos/explainers/crank-view.jpg"},
        "duration": 22,
        "heading": "Why the crank spins but the window won't close",
        "steps": [
            (0, "A casement window opens and closes with a crank on the sill."),
            (3.5, "The handle keeps turning, but the window stops partway."),
            (7.5, "Cold air, rain and bugs get in through the gap."),
            (10.5, "Inside the operator, the gear teeth are stripped. The handle spins without moving the arm."),
            (14.5, "We replace the crank operator. The window, glass and frame stay."),
            (17.2, "Now every turn pulls the window shut, tight and sealed."),
        ],
    },
    "foggy-window-repair": {
        "scene": "fog",
        "duration": 15,
        "images": {"clear": "/photos/explainers/fog-condo-clear.jpg", "fog": "/photos/explainers/fog-condo-fog.jpg",
                   "bg": "/photos/explainers/fog-condo-bg.jpg"},
        "heading": "Where the fog between the panes comes from",
        "steps": [
            (0, "A double-pane window is two sheets of glass sealed at the edge, with argon gas between them."),
            (2.5, "Years of freeze-thaw, sun and wind crack the edge seal."),
            (4.5, "The argon leaks out and humid air gets in."),
            (7, "The moisture condenses between the panes. You can't wipe it off because it's inside."),
            (10.5, "We don't reseal or \"defog\" it. We replace the glass with a new unit made to size. The frame and handle stay."),
            (12.5, "New glass, clear view of the city again."),
        ],
    },
}


def explainer_html(slug):
    e = EXPLAINERS.get(slug)
    if not e:
        return ""
    steps = "".join(
        f'<li data-start="{t}"><span class="ex-num">{i + 1}</span><span class="ex-text">{escape(txt)}</span></li>'
        for i, (t, txt) in enumerate(e["steps"]))
    is3d = e.get("render") == "3d"
    imgs = "".join(f' data-{k}="{v}"' for k, v in e.get("images", {}).items())
    if is3d:
        art = (f'<div class="ex-canvas" role="img" aria-label="{escape(e["heading"])}. Animated 3D render; the steps are listed below.">'
               f'<img class="ex-poster" src="/photos/explainers/{e["scene"]}-poster.jpg" alt="" width="1200" height="750"></div>'
               '<div class="ex-labels" aria-hidden="true"></div>')
        script = '<script type="module" src="/assets/explainer3d.js"></script>'
    else:
        art = f'<svg viewBox="0 0 1200 750" role="img" aria-label="{escape(e["heading"])}. Animated drawing; the steps are listed below."></svg>'
        script = '<script src="/assets/explainers.js" defer></script>'
    return f"""
<section class="section ex-section"><div class="wrap">
  <div class="explainer" data-scene="{e['scene']}" data-duration="{e['duration']}" data-render="{'3d' if is3d else '2d'}"{imgs}>
    <div class="ex-head"><span class="tag">See the problem</span><h2>{escape(e['heading'])}</h2></div>
    <div class="ex-stage">
      {art}
      <p class="ex-caption" aria-hidden="true">{escape(e['steps'][0][1])}</p>
      <button type="button" class="ex-play" aria-pressed="true"><svg viewBox="0 0 24 24" aria-hidden="true"><path class="i-pause" d="M7 5h3v14H7zM14 5h3v14h-3z"/><path class="i-play" d="M8 5l11 7-11 7z"/></svg><span>Pause</span></button>
      <div class="ex-bar" aria-hidden="true"></div>
    </div>
    <ol class="ex-steps">{steps}</ol>
  </div>
</div></section>
{script}"""
