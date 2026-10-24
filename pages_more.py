"""Extra pages, promises, blog posts and placeholders for business facts.

Facts that need a real number stay empty ("" or None) and their sections stay
hidden until filled in.
"""

# ---------------------------------------------------------------- business facts (fill in to show)
VISIT_FEE = ""        # e.g. "$29"  -> "On-site assessment $29, credited to your repair"
CUSTOMERS = ""        # e.g. "500+" -> shown in the trust area
YEARS = ""            # e.g. "15"   -> "15 years fixing GTA windows"
CLIENT_LOGOS = []     # commercial clients you've worked for, e.g. ["Tim Hortons", "BMO"]
ABOUT_STORY = ""      # a short paragraph about you and how the business started

# Completed jobs. Each gets its own page under /our-work/<slug>/ once added.
# {"slug": "foggy-picture-window-mississauga", "title": "Foggy picture window", "city": "Mississauga",
#  "service": "foggy-window-repair", "summary": "...", "before": "work/x-before.jpg", "after": "work/x-after.jpg",
#  "review": "...", "reviewer": "First name"}
WORK = []

# ---------------------------------------------------------------- promises (approved by the owner)
PROMISES = [
    ("The price we quote is the price you pay", "Once your quote is confirmed, the price doesn't change on site. No surprises."),
    ("Save 50–70% compared with replacement", "Repairing the failed glass or part typically costs 50–70% less than replacing the whole window."),
    ("10-year seal warranty on new glass", "New sealed glass units we install in vinyl frames carry a 10-year warranty against seal failure."),
    ("1-year workmanship warranty", "Every repair is backed by our 1-year workmanship warranty."),
    ("Price match", "Have a written quote from another licensed company for the same work? Show us and we'll match it."),
    ("No travel or after-hours surcharge", "No extra charge for travel anywhere in our service area, and no after-hours surcharge for emergencies."),
    ("Insured and WSIB covered", "We are fully insured and WSIB covered, so you're protected while we work in your home or business."),
    ("12-point window check", "Every visit includes a 12-point check of your window, so you know about any other problem before it gets worse."),
]

CHECK_12 = [
    "Glass seal: fog, haze or mineral streaks between the panes",
    "Glass: cracks, chips and stress cracks",
    "Frame: rot, cracks, warping or loose corners",
    "Sash alignment: does it sit square and close evenly",
    "Hinges: bends, rust and sagging",
    "Crank operator: gears, handle and smooth operation",
    "Locks and keepers: do they pull the sash tight",
    "Weatherstripping: gaps, tears and flattening",
    "Exterior caulking: cracks, gaps and missing sealant",
    "Drainage: weep holes clear and the sill draining away",
    "Screen: tears, fit and frame condition",
    "Final test: opens, closes and locks properly",
]

WHO = [
    ("Homeowners", "Fast, honest repairs for houses, townhouses and condos, with a clear recommendation before any work starts.", "/contact/", "Get a quote"),
    ("Property managers & landlords", "Repeat repairs across units and buildings, one point of contact, clear invoices.", "/property-managers/", "For property managers"),
    ("Real estate agents", "Pre-listing and pre-closing repairs so windows don't become an inspection issue.", "/real-estate-agents/", "For agents"),
    ("Businesses", "Storefront glass, commercial doors and emergency board-up for shops and offices.", "/commercial-glass-repair/", "Commercial services"),
]

SIGNS = [
    ("Drafts", "Cold air around the sash usually means worn weatherstripping, loose hardware or a failed seal. A repair restores the seal."),
    ("Fog between the panes", "The glass seal has failed. Only the glass unit needs replacing, not the window."),
    ("Hard to open, close or lock", "A stripped crank, bent hinge or misaligned lock. A new part fixes it in one visit."),
    ("Visible damage", "Cracks, chips or a broken latch. The glass or part can be replaced in the existing frame."),
    ("Water on the sill", "Blocked drainage, failed caulking or worn seals. We find the source and fix it."),
    ("When to replace", "Rot through the frame or a badly bent frame means a repair won't last. We'll tell you plainly."),
]

# ---------------------------------------------------------------- blog
BLOG = [
    {
        "slug": "condensation-between-window-panes",
        "title": "Why is there condensation between my window panes?",
        "description": "Fog or moisture between double pane glass means the seal has failed. What causes it, whether it can be fixed, and what it costs compared with a new window.",
        "date": "2026-10-24",
        "body": """
<p>If there's fog, droplets or a milky haze <strong>between</strong> the two panes of your window, and you can't wipe it off from either side, the window's seal has failed. It's one of the most common window problems in the GTA, and the fix is simpler than most people expect.</p>
<h2>How a double pane window works</h2>
<p>A double pane window is a sealed unit: two sheets of glass held apart by a spacer bar around the edge. The space between them is sealed and often filled with argon gas. The spacer contains a drying agent that absorbs any moisture trapped during manufacturing.</p>
<h2>Why the seal fails</h2>
<ul>
  <li><strong>Age:</strong> seals usually last 15 to 25 years.</li>
  <li><strong>Temperature swings:</strong> Toronto's freeze and thaw cycles make the glass expand and contract, working the seal loose.</li>
  <li><strong>Sun:</strong> south and west facing windows age faster.</li>
  <li><strong>Water sitting on the seal:</strong> blocked drainage at the bottom of the frame keeps the edge of the glass wet.</li>
</ul>
<p>Once the seal fails, humid air gets in, the drying agent fills up, and moisture condenses on the inside of the glass.</p>
<h2>Is it a problem?</h2>
<p>Beyond the view, a failed unit has lost its insulating gas, so the window lets more heat out in winter. Over time the moisture leaves permanent mineral stains on the glass.</p>
<h2>Can it be fixed?</h2>
<p>Yes. The frame is almost always fine. The fix is to replace just the sealed glass unit: we measure it, have a new unit made to size, and install it in your existing frame. Your trim and walls aren't touched. See <a href="/foggy-window-repair/">foggy window repair</a>.</p>
<h2>What about defogging?</h2>
<p>Some services drill small holes, clean the glass and seal the holes. It can look clearer for a while, but the seal is still broken and the insulating gas is gone. Replacing the unit is the lasting fix.</p>
<h2>Condensation on the inside of the glass is different</h2>
<p>If the water is on the room side and you can wipe it off, the seal is fine. That's indoor humidity, and you can reduce it with fans and a lower humidifier setting. Read our <a href="/winter-ready/">winter window checklist</a>.</p>
""",
    },
    {
        "slug": "window-crank-repair-or-replace",
        "title": "Window crank not working? Repair it before you replace the window",
        "description": "A casement window crank that spins, sticks or won't close is almost always a worn operator or hinge. How to tell what's wrong and why a repair beats a new window.",
        "date": "2026-10-24",
        "body": """
<p>Casement and awning windows open with a crank. When the crank spins without moving the window, takes a lot of force, or the window won't close tight, most people assume they need a new window. Almost always, they don't.</p>
<h2>What's actually broken</h2>
<ul>
  <li><strong>Handle spins, window doesn't move:</strong> stripped gears inside the crank operator.</li>
  <li><strong>Handle is loose on its shaft:</strong> a worn handle. The cheapest fix of all.</li>
  <li><strong>Window rubs or sags:</strong> bent or worn hinges.</li>
  <li><strong>Window closes but won't lock tight:</strong> the lock is out of line with its keepers, usually because the sash has sagged.</li>
</ul>
<h2>Why cranks fail</h2>
<p>Cold weather is hard on window hardware. Forcing a window that's frozen shut strips the gears, and rust and dirt seize the mechanism. After 15 to 20 years of daily use, operators simply wear out.</p>
<h2>The fix</h2>
<p>Replacing a crank operator usually takes under an hour and typically costs $150–$400, depending on the type of operator. Condo windows usually cost more because the work is more complex. We identify the hardware, often made by AmesburyTruth, Roto, Maxim or Encore, fit a matching or compatible part, and check the hinges and lock while we're there. See <a href="/window-crank-repair/">window crank repair</a> and <a href="/window-hinge-repair/">hinge repair</a>.</p>
<h2>Keep it working</h2>
<ol>
  <li>Spray hinges and moving parts with silicone once a year.</li>
  <li>Vacuum dirt out of the hinge tracks in spring.</li>
  <li>Never force a frozen window. Let it thaw.</li>
</ol>
""",
    },
    {
        "slug": "repair-or-replace-windows",
        "title": "Should I repair or replace my windows?",
        "description": "A simple guide for GTA homeowners: when a window repair makes sense, when replacement does, and how to tell the difference.",
        "date": "2026-10-24",
        "body": """
<p>Window companies that only sell new windows will usually recommend replacement. But most window problems come down to one failed part, and fixing that part costs a fraction of a new window.</p>
<h2>Repair makes sense when</h2>
<ul>
  <li>The glass is foggy or cracked, but the frame is solid</li>
  <li>A crank, hinge, handle, lock or latch is broken</li>
  <li>Drafts come from worn weatherstripping or old caulking</li>
  <li>A patio door drags on worn rollers</li>
</ul>
<h2>Replacement makes sense when</h2>
<ul>
  <li>The frame is rotted, soft or cracked through</li>
  <li>The window is badly out of square and can't be adjusted</li>
  <li>Several parts have failed at once and repairs add up close to a new window</li>
  <li>You want a different style or size of window</li>
</ul>
<h2>What repair saves you</h2>
<p>Besides cost, a repair avoids removing interior trim, patching drywall and repainting. It's usually done in under an hour per window. And you can upgrade the glass while you're at it with Low-E and argon.</p>
<h2>Get an honest answer</h2>
<p>Send us a photo of the window and the problem. We'll tell you whether it can be repaired, and if it can't, we'll say so. See <a href="/window-replacement/">window replacement</a> or <a href="/contact/">request a quote</a>.</p>
""",
    },
]

# ---------------------------------------------------------------- pages
EXTRA_PAGES = [
    {
        "slug": "about",
        "crumb": "About us",
        "title": "About Us | Window Repair GTA",
        "description": "Window Repair GTA is a repair-first window and glass company serving Toronto and the GTA. Insured, WSIB covered, with a 1-year workmanship warranty.",
        "body": """
<section class="page-hero"><div class="wrap">
  {crumbs}
  <span class="tag">About us</span>
  <h1>We fix windows. We don't push new ones.</h1>
  <p class="lede">Window Repair GTA repairs windows, glass and patio doors for homes and businesses across Toronto and the GTA. Our job is to fix what failed, and to tell you honestly when a window is past saving.</p>
  <div class="actions">{call}{text}</div>
</div></section>
{trust}
<section class="section"><div class="wrap"><div class="prose">
  {story}
  <h2>What we believe</h2>
  <p>Most windows don't need to be replaced. A foggy glass unit, a stripped crank or a worn roller can be fixed in under an hour, for a fraction of the price of a new window, without tearing out trim or drywall. That's the work we do every day.</p>
  <h2>Our promises</h2>
  {promises}
  <h2>Our 12-point window check</h2>
  <p>Every visit includes a check of the whole window, not just the part you called about:</p>
  {check12}
</div></div></section>
{cta}""",
    },
    {
        "slug": "property-managers",
        "crumb": "Property managers",
        "title": "Window Repair for Property Managers & Landlords | Window Repair GTA",
        "description": "Window, glass and patio door repairs for property managers and landlords across the GTA: repeat work, multiple units, clear invoices, insured and WSIB covered.",
        "body": """
<section class="page-hero"><div class="wrap">
  {crumbs}
  <span class="tag">Property managers & landlords</span>
  <h1>Window repairs across your units and buildings</h1>
  <p class="lede">One contact for foggy glass, broken cranks, balcony doors and broken windows across your portfolio. Insured, WSIB covered, with clear invoices for every unit.</p>
  <div class="actions">{call}<a class="btn btn-outline" href="/quote/">Request a quote</a></div>
</div></section>
{trust}
<section class="section"><div class="wrap"><div class="prose">
  <h2>What we handle</h2>
  <ul class="ticks">
    <li>Foggy and broken sealed units in apartments, condos and townhouses</li>
    <li>Balcony and patio door rollers, tracks and locks</li>
    <li>Casement cranks, hinges, locks and window safety stops</li>
    <li>Caulking and leak repairs between tenants</li>
    <li>Emergency board-up after break-ins and accidents</li>
    <li>Storefront and commercial door repairs in mixed-use buildings</li>
  </ul>
  <h2>How we work with managers</h2>
  <ol class="tips">
    <li><strong>Building survey.</strong> We can walk a building and list every failed unit and part, with one quote.</li>
    <li><strong>Batch the work.</strong> Glass is ordered together and installed in as few visits as possible.</li>
    <li><strong>Work around tenants.</strong> We coordinate access, elevators and building rules with you.</li>
    <li><strong>Clear paperwork.</strong> Invoices broken down by unit, with photos when you need them.</li>
  </ol>
  <h2>Why repair, not replace</h2>
  <p>Replacing windows across a building is a capital project. Replacing the glass units and hardware that have failed keeps units rentable and tenants comfortable at a fraction of the cost.</p>
</div></div></section>
{cta}""",
    },
    {
        "slug": "real-estate-agents",
        "crumb": "Real estate agents",
        "title": "Window Repair for Real Estate Agents | Pre-Listing & Inspection Fixes | Window Repair GTA",
        "description": "Foggy glass, broken cranks and sticking doors fixed fast before listing or closing. Window repairs for real estate agents and sellers across the GTA.",
        "body": """
<section class="page-hero"><div class="wrap">
  {crumbs}
  <span class="tag">Real estate agents</span>
  <h1>Window fixes before listing and closing</h1>
  <p class="lede">Foggy glass and broken cranks show up in listing photos and inspection reports. We fix them quickly so they don't become a negotiating point.</p>
  <div class="actions">{call}{text}</div>
</div></section>
{trust}
<section class="section"><div class="wrap"><div class="prose">
  <h2>Common pre-sale window fixes</h2>
  <ul class="ticks">
    <li>Foggy sealed units that buyers notice in showings</li>
    <li>Windows that won't open or lock, flagged by home inspectors</li>
    <li>Patio doors that drag or won't lock</li>
    <li>Torn screens and cracked glass</li>
    <li>Caulking and leak repairs</li>
  </ul>
  <h2>Built around your timeline</h2>
  <p>Send us the inspection report or photos and we'll quote every item. Hardware is often fixed in one visit. Sealed units are made to order, so call us early when glass is involved.</p>
  <h2>Documentation for buyers</h2>
  <p>We provide an itemized invoice describing the work, which you can share with buyers or their agent.</p>
</div></div></section>
{cta}""",
    },
    {
        "slug": "measure-glass",
        "crumb": "Measure your glass",
        "title": "How to Measure Window Glass for a Quote | Window Repair GTA",
        "description": "A simple, safe guide to measuring your window glass so we can prepare your quote. We always confirm final sizes on site.",
        "body": """
<section class="page-hero"><div class="wrap">
  {crumbs}
  <span class="tag">Optional</span>
  <h1>How to measure your glass</h1>
  <p class="lede">Rough measurements help us prepare your quote faster. You don't have to measure: a photo is enough. We always confirm the exact size before ordering.</p>
  <div class="actions">{text}<a class="btn btn-outline" href="/quote/">Send measurements</a></div>
</div></section>
<section class="section"><div class="wrap"><div class="prose">
  <p class="note"><strong>Safety first:</strong> never measure cracked or broken glass, and don't press on damaged panes. Measure only glass that's intact and that you can reach safely from the floor.</p>
  <h2>What you need</h2>
  <ul><li>A tape measure in inches</li><li>Your phone camera</li></ul>
  <h2>Step by step</h2>
  <ol class="tips">
    <li><strong>Measure the visible glass width</strong>, from the edge of the frame or rubber seal on the left to the right. Write it to the nearest 1/8 inch.</li>
    <li><strong>Measure the visible glass height</strong> the same way, top to bottom.</li>
    <li><strong>Count the panes.</strong> Look at the edge of the glass: two or three layers?</li>
    <li><strong>Photograph the spacer.</strong> The metal or plastic strip between the panes often has a printed code with the maker and date. Take a close-up.</li>
    <li><strong>Note the glass type.</strong> Clear, frosted or textured? Is there a grille between the panes? Is it a door or near the floor (that usually means tempered glass)?</li>
    <li><strong>Take two photos:</strong> one of the whole window from inside, one close-up of the problem.</li>
  </ol>
  <h2>Why we still measure on site</h2>
  <p>The glass sits inside the frame, so the real size is a bit bigger than what you can see. We take exact measurements before ordering so the new unit fits perfectly.</p>
</div></div></section>
{cta}""",
    },
    {
        "slug": "quote",
        "crumb": "Get a quote",
        "title": "Get a Quote: Glass, Hardware or Leaks | Window Repair GTA",
        "description": "Get a quote for window glass replacement, crank and hardware repair, or caulking and leaks. Pick the form for your job, add a photo, and we'll reply with a price.",
        "body": """
<section class="page-hero"><div class="wrap">
  {crumbs}
  <span class="tag">Free quote</span>
  <h1>Pick your job, get a price</h1>
  <p class="lede">Choose the form that fits your problem. Each one asks only what we need to quote it. Not sure? Use the general form or just text us a photo.</p>
  <div class="actions">{call}{text}</div>
</div></section>
<section class="section"><div class="wrap quote-forms">{quote_forms}</div></section>""",
    },
    {
        "slug": "blog",
        "crumb": "Blog",
        "title": "Window Repair Tips & Guides | Window Repair GTA Blog",
        "description": "Practical guides on foggy windows, window cranks, repair versus replacement and keeping your windows working through a GTA winter.",
        "body": """
<section class="page-hero"><div class="wrap">
  {crumbs}
  <span class="tag">Blog</span>
  <h1>Window tips and guides</h1>
  <p class="lede">Straight answers about foggy glass, broken cranks, drafts and when a window really needs replacing.</p>
</div></section>
<section class="section"><div class="wrap">{blog_list}</div></section>
{cta}""",
    },
]
