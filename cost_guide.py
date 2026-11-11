"""Glass replacement cost guide (our own 2026 prices).

Fill PRICING from the owner's price list. Until every size tier has a price,
the page is built with noindex, left out of the sitemap and not linked,
so no made-up number is ever published.
"""

SLUG = "glass-replacement-cost"

# Sealed glass unit replacement, supply + install, before HST. Numbers in dollars.
# (key, name, size band, example, low, high). high None means "and up".
TIERS = [
    ("small", "Small", "Up to 10 sq ft", "Bathroom, basement or small bedroom window", None, None),
    ("medium", "Medium", "10 to 20 sq ft", "Most bedroom and kitchen windows", None, None),
    ("large", "Large", "20 to 30 sq ft", "Living room windows and patio door panels", None, None),
    ("picture", "Picture window", "Over 30 sq ft", "Large fixed windows", None, None),
]

# Glass options. Value is a percent added to the base price (e.g. 12) or None if not set yet.
ADDONS = [
    ("lowe", "Low-E coating", "Reflects heat back into the room in winter and keeps sun heat out in summer.", None),
    ("argon", "Argon gas fill", "Fills the space between the panes for better insulation.", None),
    ("tempered", "Tempered safety glass", "Breaks into small blunt pieces. Required in some spots, like doors and glass close to the floor.", None),
    ("frosted", "Frosted or obscure glass", "Lets light in and keeps bathrooms private.", None),
    ("triple", "Triple pane", "Three layers of glass for quieter, warmer rooms.", None),
]

# Free-text terms from the owner. None hides the line.
TERMS = {
    "floor": None,      # e.g. "25% more for 3rd floor and up, condo balconies or windows that need a lift"
    "qty": None,        # e.g. "5% off 5 or more units in one order"
    "grilles": None,    # e.g. "$50 per unit"
    "visit": None,      # e.g. "Free quote from photos. Measuring visit $30, credited to the job."
    "lead": None,       # e.g. "7 to 10 business days from measuring to installation"
    "included": None,   # list of strings
    "excluded": None,   # list of strings
}


def ready():
    return all(t[4] is not None for t in TIERS)


FACTORS = [
    ("Size", "The biggest factor",
     "The price follows the size of the sealed unit. Bigger glass costs more to make, and units over about 30 sq ft need two people to carry and set safely."),
    ("Glass type", "Coatings and layers",
     "Clear double pane is the base price. Low-E, argon, tempered, frosted or triple pane each add to it."),
    ("Where the window is", "Floor and access",
     "Ground and second floor windows are standard. High floors, condo balconies and windows that need a lift or scaffold take more time and cost more."),
    ("How many windows", "One visit, several units",
     "Replacing several units at once costs less per window, because we measure, order and install them together."),
    ("Shape and extras", "Custom work",
     "Grilles between the panes, arches, circles and decorative glass are priced one by one."),
    ("Frame condition", "We reuse your frame",
     "If the frame or the glass stops are damaged, we tell you before we order and price that repair separately."),
]

ASK_BEFORE = [
    ("Is this the all-in price?", "Ask whether measuring, removing the old glass and HST are in the number you were given."),
    ("Is there a floor or access charge?", "High floors, balconies and lifts often cost extra. It should be on the quote, not a surprise on the invoice."),
    ("Are there rush or after-hours fees?", "Ours is simple: calls after 10 PM have a $100 after-hours call-out fee."),
    ("Is there a minimum charge?", "Some companies charge a minimum per job, which matters if you only need one small window."),
    ("What does a follow-up visit cost after the warranty ends?", "Know how long the warranty lasts and what a service call costs once it's over."),
]

CHECKS = [
    "A written quote that names the glass: double or triple pane, Low-E, argon, tempered",
    "A written warranty that says what is covered and for how long",
    "Liability insurance and WSIB coverage for the workers on your property",
    "Time to think it over, with no pressure to sign on the spot",
    "Real photos of their own jobs and reviews you can check",
    "A proper receipt with HST",
]

TIPS = [
    "Replace only the glass and keep the frame when the frame is still solid. It costs a fraction of a new window.",
    "Do several windows in one visit to bring the price per window down.",
    "Book before the cold weather. Foggy glass requests climb every fall, and lead times grow with them.",
    'Send clear photos and rough sizes. You get a faster, more accurate quote. <a href="/measure-glass/">How to measure your glass</a>.',
    "Fix small things in the same visit: a crank, a seal or a screen costs less when we're already there.",
    "Look for a date stamped between the panes. Some sealed units still have a manufacturer's warranty.",
]

WHY = [
    "Fully insured and WSIB covered",
    "5-year seal warranty on new glass in vinyl windows",
    "1-year workmanship warranty",
    "Same-day appointments and 24/7 emergency service",
    "Genuine FAPIM parts imported from Italy for Italian condo windows",
]


def faqs():
    out = [
        ("What's the difference between glass replacement and window replacement?",
         "Glass replacement swaps only the sealed glass unit and keeps your existing frame. It costs much less and is done faster. Window replacement takes out the whole window, frame included."),
        ("How long does a sealed glass unit last?",
         "Most sealed units last between 15 and 25 years. Sun exposure, the quality of the unit and how it was installed all play a part."),
        ("How do I know if I need new glass or a new window?",
         "Fog or moisture between the panes that you can't wipe off from either side means the seal has failed: you need new glass. A rotted, warped or broken frame means it may be time for a new window."),
        ("Do your prices include HST?",
         "No. The prices on this page are before HST. They include the new sealed unit and installation."),
        ("What warranty do you give on new glass?",
         "New sealed units in vinyl windows come with a 5-year seal warranty, and all our work has a 1-year workmanship warranty."),
    ]
    if TERMS["lead"]:
        out.append(("How long does it take?", f"{TERMS['lead']}."))
    if TERMS["visit"]:
        out.append(("Do you charge for a quote?", TERMS["visit"]))
    return out
