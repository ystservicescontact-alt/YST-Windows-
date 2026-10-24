"""Service-in-city pages, e.g. /window-repair-vaughan/window-crank-repair/.

Each page combines one service (COMBO_SERVICES) with one city (CITY_LOCAL).
Keep the city text specific to that city so pages are useful, not duplicates.
"""

# Services that get a page in every city. Keys are service slugs from content.py.
COMBO_SERVICES = {
    "foggy-window-repair": {
        "short": "Foggy Window Repair",
        "lede": "Fog or moisture between your panes means the seal has failed. We replace the sealed glass unit in your existing frame, so trim and walls stay untouched.",
        "what": "Double and triple pane windows are sealed units. When the edge seal breaks down, humid air gets in and condenses between the glass, and it can't be wiped off. We measure the unit, have new glass made to the exact size, and install it in the frame you already have.",
        "bullets": [
            "Foggy double and triple pane glass replaced",
            "Picture, casement, awning and slider windows",
            "Custom shapes, arches and transoms",
            "Low-E coating and argon fill upgrades",
            "Patio door sealed units",
        ],
        "faqs": [
            ("How much does foggy window repair cost in {city}?",
             "It depends on the size and type of glass. Text us a photo of the window and we'll give you a price. Replacing the glass is usually a fraction of the cost of a new window."),
            ("Can the fog be cleaned out instead?",
             "Drilling and cleaning can make glass look clearer for a while, but it doesn't restore the seal or the insulating gas. A new sealed unit fixes it properly."),
            ("How long does it take?",
             "We measure first, the glass is made to order in a few days, and installation is usually under an hour per window."),
            ("Is my foggy glass still under warranty?",
             "Many sealed units carry a 10 to 20 year manufacturer warranty. Send us a photo of the printing on the spacer between the panes and we'll help you check."),
        ],
    },
    "window-glass-replacement": {
        "short": "Window Glass Replacement",
        "lede": "Cracked or broken window glass replaced in your existing frame, matched to the original. Single pane, double pane and tempered glass.",
        "what": "A cracked pane doesn't mean a new window. We secure the opening if needed, measure the glass to the 1/16 of an inch, and install new glass or a new sealed unit with fresh seals, then check the window opens, closes and locks.",
        "bullets": [
            "Sealed double and triple pane units",
            "Single pane, storm and older wood windows",
            "Tempered safety glass for doors and low windows",
            "Laminated and obscure glass",
            "Board-up when the opening is exposed",
        ],
        "faqs": [
            ("How much does window glass replacement cost in {city}?",
             "Price depends on the size, thickness and type of glass. Send us a photo and the rough size and we'll quote it."),
            ("Can you replace just the glass?",
             "Yes. Replacing only the glass is our most common job. The frame stays in place."),
            ("Do I need tempered glass?",
             "Doors, sidelights and glass near floors, stairs and bathtubs usually need safety glass. We check and use the right type."),
            ("What should I do until you arrive?",
             "Keep people away from the glass and tape a small crack with clear packing tape on both sides. If the opening is exposed, call us to board it up."),
        ],
    },
    "window-crank-repair": {
        "short": "Window Crank Repair",
        "lede": "A stripped or stiff window crank makes a casement impossible to open or close. We replace crank operators, hinges, handles and locks, usually in one visit.",
        "what": "Casement and awning windows open with a crank operator, a small gearbox at the bottom of the frame. Over the years the gears strip, seize or corrode. Most homeowners think that means a new window. In most cases replacing the operator takes under an hour and costs a fraction of a new window.",
        "bullets": [
            "Crank operator replacement, all major brands",
            "Crank handle replacement",
            "Casement and awning window hinges",
            "Multi-point lock adjustment and replacement",
            "Matching or compatible parts for older windows",
        ],
        "faqs": [
            ("How much does window crank repair cost in {city}?",
             "It depends on the operator and whether hinges need replacing too. Send us a photo of the crank and hinge and we'll quote it."),
            ("My crank spins but the window doesn't move. What's wrong?",
             "The gears inside the operator are stripped. The fix is a new operator, not a new window."),
            ("Can you get parts for older windows?",
             "Yes. We find matching or compatible parts for most windows, including older and discontinued models."),
            ("How long does crank repair take?",
             "Most crank and hinge repairs are done in one short visit once we know which parts you need."),
        ],
    },
    "patio-door-repair": {
        "short": "Patio Door Repair",
        "lede": "Sliding patio door hard to open, off track or not locking? We replace rollers, repair tracks, fix locks and handles, and replace patio door glass.",
        "what": "Most sliding doors ride on two small roller assemblies under the moving panel. When the wheels wear out or crack, the door drags, grinds or jumps the track. We lift the panel out, replace the rollers, clean and repair the track, and adjust the door so it glides and locks again.",
        "bullets": [
            "Roller replacement and height adjustment",
            "Track cleaning and repair",
            "Locks, keepers and handle sets",
            "Foggy or broken patio door glass",
            "Weatherstripping and screen doors",
        ],
        "faqs": [
            ("How much does patio door repair cost in {city}?",
             "Most roller and lock repairs cost far less than a new door. Send us a photo of the door and the bottom corner of the panel and we'll quote it."),
            ("Why is my sliding door so hard to open?",
             "Usually worn rollers or a dirty, damaged track. New rollers and a cleaned track normally fix it."),
            ("Can you replace the glass in my patio door?",
             "Yes. We replace the tempered sealed unit in the existing door panel."),
            ("Do you fix balcony doors in condos?",
             "Yes. We repair sliding balcony doors in condos and apartments."),
        ],
    },
}

# Local text for each city: what the housing is like, and nearby areas.
CITY_LOCAL = {
    "Toronto": {
        "local": "Toronto has every kind of window: century homes with wood sashes in the Annex and Leslieville, postwar bungalows, 1990s replacement windows now failing, and thousands of condo units with floor-to-ceiling glass and sliding balcony doors.",
        "nearby": ["North York", "Etobicoke", "Scarborough", "East York", "York"],
    },
    "North York": {
        "local": "North York mixes 1950s and 1960s bungalows in Don Mills and Bathurst Manor, large rebuilt homes in York Mills and Bayview Village, and condo towers along Yonge Street. Many houses have 25 to 30 year old replacement windows with worn hardware and failing seals.",
        "nearby": ["Toronto", "Thornhill", "Vaughan", "Scarborough", "Etobicoke"],
    },
    "Scarborough": {
        "local": "Scarborough has many 1950s to 1970s bungalows, back-splits and townhouses, plus apartment towers. A lot of homes got replacement windows in the 1990s, and those seals, cranks and slider wheels are wearing out now.",
        "nearby": ["Toronto", "North York", "Markham", "Pickering"],
    },
    "Etobicoke": {
        "local": "Etobicoke ranges from postwar split-levels and bungalows on large lots in Islington and the Kingsway to lakeside condos in Mimico and Humber Bay Shores, where balcony doors and big sealed units take a beating from wind off the lake.",
        "nearby": ["Toronto", "Mississauga", "North York", "Vaughan"],
    },
    "Mississauga": {
        "local": "Much of Mississauga was built from the 1970s to the 2000s in Erin Mills, Meadowvale, Churchill Meadows and Streetsville. Many of those homes still have their original sealed units and casement hardware, right at the age when seals fail and operators wear out.",
        "nearby": ["Etobicoke", "Brampton", "Oakville", "Milton"],
    },
    "Brampton": {
        "local": "Brampton goes from the 1960s and 1970s homes of Bramalea to newer subdivisions in Springdale, Castlemore and Mount Pleasant with large windows and wide patio doors. Older homes need hardware and glass; newer homes have more and bigger seals that can fail.",
        "nearby": ["Mississauga", "Vaughan", "Caledon", "Etobicoke"],
    },
    "Vaughan": {
        "local": "Vaughan has many large detached homes built from the 1990s on in Woodbridge, Maple and Thornhill, and custom builds in Kleinburg, often with oversized picture windows, transoms and wide patio doors. Those big sealed units and crank operators are the first things to go.",
        "nearby": ["Woodbridge", "Maple", "Thornhill", "Richmond Hill", "Brampton"],
    },
    "Markham": {
        "local": "Markham has heritage homes around Main Street Unionville and Markham Village, 1980s and 1990s subdivisions, and newer communities like Cornell and Berczy Village. We repair windows of every age and match glass and hardware so the repair blends in.",
        "nearby": ["Unionville", "Richmond Hill", "Scarborough", "Stouffville"],
    },
    "Richmond Hill": {
        "local": "Homes in Bayview Hill, Mill Pond and Jefferson often have two-storey foyer glass, large picture windows and wide patio doors. Big sealed units are the most likely to fog and the most expensive to replace as whole windows, so replacing just the glass saves the most here.",
        "nearby": ["Thornhill", "Markham", "Vaughan", "Aurora"],
    },
    "Oakville": {
        "local": "Many Oakville homes in Glen Abbey, River Oaks and Joshua Creek were built in the 1980s to 2000s with large windows, arched transoms and wide garden doors. Those large custom sealed units are the ones that fog first.",
        "nearby": ["Burlington", "Mississauga", "Milton"],
    },
    "Newmarket": {
        "local": "Newmarket grew fast in the 1980s and 1990s in Summerhill, Glenway and Armitage. Windows from that era are now 25 to 40 years old, and foggy glass, failed seals and stripped crank operators are very common.",
        "nearby": ["Aurora", "East Gwillimbury", "Richmond Hill"],
    },
}

WHY = [
    ("Repair, not replace", "We fix the part that failed. A new sealed unit or operator costs a fraction of a new window."),
    ("Quotes from a photo", "Text us a photo and we can usually give you a price without a visit."),
    ("All window brands", "We work on most major brands and Canadian manufacturers, old and new."),
    ("Full check included", "While we're there, we check the seals, hardware and weatherstripping for other problems."),
]


def combo_slug(city_slug, service_slug):
    return f"{city_slug}/{service_slug}"
