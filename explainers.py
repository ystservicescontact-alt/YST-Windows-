"""Animated problem explainers shown near the top of service pages.
Each step's start time (seconds) must match the timeline in src/assets/explainers.js."""
import json
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
    if e.get("render") == "photo":
        return photo_explainer_html(e)
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


def _steps_html(e):
    return "".join(
        f'<li data-start="{t}"><span class="ex-num">{i + 1}</span><span class="ex-text">{escape(txt)}</span></li>'
        for i, (t, txt) in enumerate(e["steps"]))


def photo_explainer_html(e):
    cfg = json.dumps(e["config"], separators=(",", ":")).replace("</", "<\\/")
    return f"""
<section class="section ex-section"><div class="wrap">
  <div class="explainer" data-scene="{e['scene']}" data-duration="{e['duration']}" data-render="photo">
    <div class="ex-head"><span class="tag">See the problem</span><h2>{escape(e['heading'])}</h2></div>
    <div class="ex-stage">
      <svg class="exp-svg" viewBox="0 0 1200 750" role="img" aria-label="{escape(e['heading'])}. Animated photo; the steps are listed below."></svg>
      <script type="application/json" class="ex-config">{cfg}</script>
      <p class="ex-caption" aria-hidden="true">{escape(e['steps'][0][1])}</p>
      <button type="button" class="ex-play" aria-pressed="true"><svg viewBox="0 0 24 24" aria-hidden="true"><path class="i-pause" d="M7 5h3v14H7zM14 5h3v14h-3z"/><path class="i-play" d="M8 5l11 7-11 7z"/></svg><span>Pause</span></button>
      <div class="ex-bar" aria-hidden="true"></div>
    </div>
    <ol class="ex-steps">{_steps_html(e)}</ol>
  </div>
</div></section>
<script src="/assets/explainer-photo.js" defer></script>"""


def _p(x, y, sx=0.46875, ox=0, oy=300, px=40):
    """Source-photo pixel -> stage coordinates for a portrait photo placed at x=40."""
    return [round(px + (x - ox) * sx, 1), round((y - oy) * sx, 1)]


PH = "/photos/explainers/"

EXPLAINERS["fapim-window-repair"] = {
    "scene": "fapim", "render": "photo", "duration": 17,
    "heading": "Why a FAPIM condo window won't close",
    "steps": [
        (0, "Many Toronto condos have FAPIM windows: one handle opens the window and pulls it shut."),
        (1.2, "Turn the handle to close it, and the arm should pull the window in."),
        (3.2, "With worn hardware, the handle jams and the window stops halfway."),
        (6.5, "It stays open at the bottom: cold air, rain and noise get in, and it won't lock."),
        (8.5, "Inside, the FAPIM gearbox and stay arm wear out. Pivots get loose, bent or seized."),
        (12, "We replace the worn FAPIM parts with matching ones. The window and glass stay."),
        (14, "The handle turns smoothly, and the window closes and locks."),
    ],
    "config": {
        "photo": {"src": PH + "fapim.jpg", "x": 40, "w": 709},
        "bg": PH + "fapim-bg.jpg",
        "title": ["FAPIM CONDO WINDOW", "Real job · Toronto"],
        "cam": [[0, 1, 394, 375], [1.0, 1, 394, 375], [2.0, 1.7, 560, 470], [6.2, 1.7, 560, 470],
                [7.2, 1.6, 300, 575], [11.5, 1.6, 300, 575], [12.4, 1, 394, 375], [13.1, 1.4, 560, 470],
                [15.2, 1.4, 560, 470], [16.2, 1, 394, 375]],
        "fx": [
            {"type": "sprite", "src": PH + "fapim-sprite.png", "x": 522.8, "y": 379.7, "w": 98.4, "h": 178.1,
             "px": 546.3, "py": 503.9,
             "keys": [[0, 0], [1.3, 0], [2.6, -70], [3.3, -70], [3.8, -38], [4.4, -70], [5.0, -38], [5.6, -70],
                      [6.6, 0], [12.6, 0], [14, -90], [16.8, -90]]},
            {"type": "ring", "x": 583.8, "y": 468.8, "r": 26, "tone": "white", "t": [0.3, 3.0]},
            {"type": "label", "x": 600, "y": 420, "text": "FAPIM handle", "tone": "navy", "dx": 50, "dy": -60, "t": [0.3, 3.0]},
            {"type": "arrow", "d": "M300 500 L300 592", "tone": "green", "t": [1.4, 3.2]},
            {"type": "spin", "x": 546, "y": 504, "r": 70, "dir": -1, "tone": "red", "t": [3.2, 6.3]},
            {"type": "label", "x": 600, "y": 440, "text": "Jammed", "tone": "red", "dx": 50, "dy": -50, "t": [3.4, 6.3]},
            {"type": "gap", "a": _p(400, 1440), "b": _p(400, 1590), "text": "WON'T CLOSE", "tone": "red", "tdx": 16, "t": [6.5, 12]},
            {"type": "flow", "d": "M120 470 C190 520 240 560 300 585 S400 650 470 740", "tone": "blue", "n": 16, "r": 5, "speed": 0.35, "t": [6.8, 11.8]},
            {"type": "ring", "x": 342.3, "y": 590.6, "r": 24, "tone": "red", "t": [8.0, 12]},
            {"type": "ring", "x": 342.3, "y": 590.6, "r": 24, "tone": "green", "t": [12, 15.5]},
            {"type": "ring", "x": 583.8, "y": 468.8, "r": 26, "tone": "green", "t": [12.2, 15.5]},
            {"type": "arrow", "d": "M300 500 L300 592", "tone": "green", "t": [14, 16.5]},
            {"type": "check", "x": 600, "y": 330, "t": [14.6, 17.5]},
        ],
        "bubble": {"x": 985, "y": 330, "r": 165, "anchor": [342.3, 590.6], "t": [8.3, 16.5],
                   "states": [{"t": 0, "img": PH + "fapim-bubble-worn.jpg", "tag": "WORN STAY ARM", "tone": "red"},
                              {"t": 12, "img": PH + "fapim-bubble-new.jpg", "tag": "NEW FAPIM PARTS", "tone": "green"}]},
    },
}
