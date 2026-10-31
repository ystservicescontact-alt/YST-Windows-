"""Window style cards for the window replacement page.

Each style is a small SVG drawing. Moving parts carry a class (ws-swing, ws-up,
ws-left ...) that CSS animates when the card is hovered, focused or tapped,
so visitors can see how each window opens.
"""
from html import escape

NAVY = "#0F1B33"
GLASS = "#CFE3F2"


def glass(x, y, w, h):
    # Pane with a soft diagonal reflection.
    gx = x + w * 0.18
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{GLASS}"/>'
            f'<path d="M{gx} {y + h} L{gx + w * 0.35} {y} L{gx + w * 0.47} {y} L{gx + w * 0.12} {y + h}Z" fill="#fff" opacity=".45"/>')


def sash(x, y, w, h, cls="", handle=None):
    """A framed pane. cls makes it move; handle adds a small handle on one side."""
    inner = glass(x + 7, y + 7, w - 14, h - 14)
    hd = ""
    if handle == "right":
        hd = f'<rect x="{x + w - 6}" y="{y + h / 2 - 9}" width="4" height="18" rx="2" fill="{NAVY}"/>'
    elif handle == "left":
        hd = f'<rect x="{x + 2}" y="{y + h / 2 - 9}" width="4" height="18" rx="2" fill="{NAVY}"/>'
    elif handle == "bottom":
        hd = f'<rect x="{x + w / 2 - 9}" y="{y + h - 6}" width="18" height="4" rx="2" fill="{NAVY}"/>'
    elif handle == "top":
        hd = f'<rect x="{x + w / 2 - 9}" y="{y + 2}" width="18" height="4" rx="2" fill="{NAVY}"/>'
    rect = f'<rect x="{x + 2}" y="{y + 2}" width="{w - 4}" height="{h - 4}" fill="#fff" stroke="{NAVY}" stroke-width="3"/>'
    c = f' class="{cls}"' if cls else ""
    return f'<g{c}>{rect}{inner}{hd}</g>'


def frame(x, y, w, h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="{NAVY}" stroke-width="5"/>'


def svg(body, label):
    return (f'<svg viewBox="0 0 200 200" role="img" aria-label="{escape(label)}">'
            f'<rect width="200" height="200" fill="#EEF2F7"/>{body}'
            f'<rect x="14" y="184" width="172" height="6" fill="{NAVY}" opacity=".15"/></svg>')


def casement():
    return frame(50, 20, 100, 160) + glass(56, 26, 88, 148) + sash(54, 24, 92, 152, "ws-swing-l", "right")


def awning():
    return frame(25, 45, 150, 110) + glass(31, 51, 138, 98) + sash(29, 49, 142, 102, "ws-tilt-top", "bottom")


def picture():
    return frame(20, 30, 160, 140) + sash(24, 34, 152, 132, "ws-shine")


def casement_picture():
    return (frame(10, 30, 180, 140) + glass(14, 34, 172, 132)
            + sash(14, 34, 40, 132, "ws-swing-l", "right")
            + sash(54, 34, 92, 132)
            + sash(146, 34, 40, 132, "ws-swing-r", "left"))


def single_hung():
    return (frame(50, 15, 100, 170) + glass(54, 19, 92, 162)
            + sash(54, 19, 92, 81)
            + sash(54, 100, 92, 81, "ws-up", "top"))


def double_hung():
    return (frame(50, 15, 100, 170) + glass(54, 19, 92, 162)
            + sash(54, 19, 92, 81, "ws-down")
            + sash(54, 100, 92, 81, "ws-up", "top"))


def single_slider():
    return (frame(15, 45, 170, 110) + glass(19, 49, 162, 102)
            + sash(19, 49, 81, 102)
            + sash(100, 49, 81, 102, "ws-left", "right"))


def double_slider():
    return (frame(15, 45, 170, 110) + glass(19, 49, 162, 102)
            + sash(19, 49, 81, 102, "ws-right", "left")
            + sash(100, 49, 81, 102, "ws-left", "right"))


def end_vent():
    return (frame(8, 50, 184, 100) + glass(12, 54, 176, 92)
            + sash(52, 54, 96, 92)
            + sash(12, 54, 40, 92, "ws-right-s", "left")
            + sash(148, 54, 40, 92, "ws-left-s", "right"))


def bay():
    # Three units, the side ones drawn narrower to read as angled.
    left = (f'<polygon points="12,52 52,38 52,162 12,148" fill="#fff" stroke="{NAVY}" stroke-width="4"/>'
            f'<polygon points="18,57 46,47 46,153 18,143" fill="{GLASS}"/>')
    right = (f'<polygon points="148,38 188,52 188,148 148,162" fill="#fff" stroke="{NAVY}" stroke-width="4"/>'
             f'<polygon points="154,47 182,57 182,143 154,153" fill="{GLASS}"/>')
    centre = frame(52, 38, 96, 124) + sash(56, 42, 88, 116, "ws-shine")
    return left + right + centre


STYLES = [
    ("casement", "Casement", casement,
     "Hinged on the side and opened with a crank. It seals tightly when closed and opens all the way for airflow. The most common window in GTA homes."),
    ("awning", "Awning", awning,
     "Hinged at the top and opens out from the bottom, so it can stay open in light rain. A good fit for basements, bathrooms and under a picture window."),
    ("picture", "Picture", picture,
     "One large pane that doesn't open. The most glass and the tightest seal for the money, for the best view in the room."),
    ("casement-picture", "Picture with casements", casement_picture,
     "A wide fixed centre pane with an opening casement on one or both sides. You keep the big view and still get fresh air."),
    ("single-hung", "Single hung", single_hung,
     "The top sash stays fixed and the bottom sash slides up. A classic look that suits older Toronto homes."),
    ("double-hung", "Double hung", double_hung,
     "Both sashes slide, and most tilt in so you can clean the outside glass from indoors. Good for traditional and heritage-style houses."),
    ("single-slider", "Single slider", single_slider,
     "One sash slides sideways on a track. Simple, budget-friendly and easy to open in wide, short openings."),
    ("double-slider", "Double slider", double_slider,
     "Both sashes slide, so you can open whichever side you need. Common in kitchens and bedrooms."),
    ("end-vent-slider", "End vent slider", end_vent,
     "A fixed centre pane with a small sliding vent at each end. A wide, clear view with airflow on both sides."),
    ("bay-bow", "Bay & bow", bay,
     "Three or more windows angled out from the wall. More light, more room, and space for a seat or shelf inside."),
]


def window_styles_html():
    cards = "".join(
        f'<figure class="wstyle" tabindex="0" data-style="{key}">'
        f'<div class="wstyle-art">{svg(draw(), name + " window")}</div>'
        f'<figcaption><h3>{escape(name)}</h3><p>{escape(desc)}</p></figcaption></figure>'
        for key, name, draw, desc in STYLES)
    return (f'<p class="wstyle-hint">Tap or hover over a window to see how it opens.</p>'
            f'<div class="wstyles">{cards}</div>')
