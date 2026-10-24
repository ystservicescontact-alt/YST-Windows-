"""Extra sections added to the bottom of service pages (keyed by service slug).

price_factors: what changes the price (shown as a checklist).
html: any extra sections, written as HTML.
"""

EXTRAS = {
    "foggy-window-repair": {
        "price_factors": [
            "The size of each glass unit",
            "Glass thickness and the gap between the panes",
            "Glass type: clear, Low-E, frosted, tinted or tempered",
            "Shape: rectangle, arch or custom",
            "How many windows you're fixing",
            "Access: ground floor or upper floors",
        ],
        "html": """
<h2>Upgrade while you're at it</h2>
<p>A new sealed unit doesn't have to match the old one exactly. Since the glass is being made anyway, you can choose:</p>
<ul class="ticks">
  <li><strong>Low-E coating</strong> to reflect heat back into the room in winter and keep summer sun out</li>
  <li><strong>Argon gas fill</strong> for better insulation than plain air</li>
  <li><strong>Warm-edge spacers</strong> that reduce condensation and frost at the edge of the glass</li>
  <li><strong>Triple pane</strong> where the frame is deep enough, for quieter, warmer rooms</li>
</ul>
<h2>Why repair beats replacement</h2>
<p>Replacing a whole window means removing interior trim, patching drywall and repainting. When only the sealed unit has failed, none of that is needed. The frame, sash and hardware are usually still in good shape. If the frame is too damaged to save, we'll tell you so.</p>
""",
    },
    "window-glass-replacement": {
        "price_factors": [
            "The size of the glass",
            "Single pane or sealed double or triple pane unit",
            "Glass type: tempered, laminated, Low-E or obscure",
            "Whether the opening needs to be boarded up first",
            "Access: ground floor, upper floor or condo",
        ],
        "html": """
<h2>Types of glass, explained</h2>
<ul class="ticks">
  <li><strong>Annealed glass:</strong> standard window glass. Breaks into sharp pieces.</li>
  <li><strong>Tempered glass:</strong> about four times stronger and breaks into small, dull pieces. Required in doors and many low windows.</li>
  <li><strong>Laminated glass:</strong> two layers bonded with a plastic interlayer. Holds together when broken, reduces noise and slows break-ins.</li>
  <li><strong>Obscure glass:</strong> textured or frosted for privacy in bathrooms and entries.</li>
</ul>
""",
    },
    "patio-door-repair": {
        "price_factors": [
            "Which parts need replacing: rollers, lock, handle or track",
            "Door size and weight",
            "Whether the glass needs replacing",
            "Brand and availability of parts",
        ],
        "html": """
<h2>Keep your patio door gliding</h2>
<ol class="tips">
  <li><strong>Vacuum the track</strong> every few months. Grit is what wears rollers out.</li>
  <li><strong>Don't oil the track.</strong> Oil collects dirt. Use a silicone spray on the rollers if needed.</li>
  <li><strong>Don't force a sticking door.</strong> Forcing it cracks rollers and bends the frame. Call us instead.</li>
  <li><strong>Check the weatherstripping</strong> each fall. Worn strips let in cold air and water.</li>
</ol>
""",
    },
    "window-crank-repair": {
        "price_factors": [
            "Which parts need replacing: operator, handle, hinges or locks",
            "How many windows need work",
            "Brand and age of the hardware",
            "Whether parts are standard or need to be special-ordered",
        ],
        "html": """
<h2>Hardware we replace</h2>
<div class="why">
  <div><h3>Crank operators</h3><p>The gearbox that opens and closes casement and awning windows.</p></div>
  <div><h3>Folding handles</h3><p>The handle you turn to operate the window.</p></div>
  <div><h3>Hinges</h3><p>The metal arms at the top and bottom that let the sash swing open.</p></div>
  <div><h3>Multi-point locks</h3><p>Locks that pull the sash tight at several points along the frame.</p></div>
  <div><h3>Keepers and strike plates</h3><p>The parts on the frame that the locks hook into.</p></div>
  <div><h3>Tilt latches and balances</h3><p>The parts that let hung windows tilt in and stay open.</p></div>
</div>
<h2>Hardware brands we work with</h2>
<p>Most Canadian casement and awning windows use hardware from a handful of makers. We find matching or compatible parts for:</p>
<ul class="ticks">
  <li><strong>AmesburyTruth</strong> (formerly Truth Hardware), the most common in Canadian casements</li>
  <li><strong>Roto</strong>, common on European-style and tilt-and-turn windows</li>
  <li><strong>Maxim</strong>, found on many older vinyl windows</li>
  <li><strong>Encore</strong>, common in builder-grade homes</li>
  <li><strong>Entrygard</strong> and other operator systems</li>
</ul>
<p class="note">Not sure what you have? Text us a close-up photo of your crank and the hinge arm and we'll identify it.</p>
<h2>Why cranks fail</h2>
<ul>
  <li>Freeze and thaw cycles cause rust and corrosion in the gears</li>
  <li>Lack of lubrication lets dirt seize the mechanism</li>
  <li>Forcing a window that's frozen shut strips the gears</li>
  <li>Normal wear after 15 to 20 years of daily use</li>
</ul>
<h2>Make your hardware last longer</h2>
<ol class="tips">
  <li><strong>Lubricate once a year</strong> with a silicone spray on hinges and moving parts.</li>
  <li><strong>Keep tracks clean.</strong> Vacuum dirt out of the hinge tracks each spring.</li>
  <li><strong>Check weatherstripping.</strong> Worn strips make the window harder to close and strain the lock.</li>
  <li><strong>Never force it.</strong> If a window won't close in winter, let it thaw or call us.</li>
</ol>
""",
    },
    "window-caulking": {
        "price_factors": [
            "Number of windows and doors",
            "Length of each joint and how deep the gaps are",
            "Removing old caulking completely",
            "Height and access, including ladders",
        ],
        "html": "",
    },
    "window-screen-repair": {
        "price_factors": [
            "Rescreen only, or a new frame",
            "Mesh type: standard, pet-resistant or solar",
            "Size and number of screens",
        ],
        "html": "",
    },
    "window-replacement": {
        "price_factors": [
            "Window size, style and opening type",
            "Frame material and colour",
            "Glass package: double or triple pane, Low-E, argon",
            "Interior and exterior finishing",
        ],
        "html": "",
    },
    "commercial-glass-repair": {
        "price_factors": [
            "Glass size and thickness",
            "Tempered or laminated glass",
            "Emergency board-up needed first",
            "After-hours work to avoid closing your business",
        ],
        "html": "",
    },
    "emergency-glass-repair": {
        "price_factors": [
            "Board-up materials and size of the opening",
            "Glass size and type for the permanent fix",
            "Time of day",
        ],
        "html": "",
    },
}
