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
    ("Save 50–70% compared with replacement", "Repairing the failed glass or part typically costs 50–70% less than replacing the whole window."),
    ("5-year seal warranty on new glass in vinyl windows", "New sealed glass units we install in vinyl frames carry a 5-year warranty against seal failure."),
    ("1-year workmanship warranty", "Every repair is backed by our 1-year workmanship warranty."),
    ("Price match", "Have a written quote from another licensed company for the same work? Show us and we'll match it."),
    ("No travel charge in the GTA", "No extra charge for travel anywhere in the Greater Toronto Area."),
    ("Fully insured and WSIB covered", "We are fully insured and covered by WSIB, Ontario's workplace safety insurance, so you're protected while we work in your home or business."),
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
        "slug": "fapim-windows-toronto-condos",
        "title": "FAPIM windows in Toronto condos: what they are and how to fix them",
        "description": "Many GTA condo windows use FAPIM hardware from Italy. How to recognize it, why the vents stop staying open or locking, and why genuine parts matter.",
        "date": "2026-10-24",
        "body": """
<p>If you live in a condo in Downtown Toronto or Mississauga and your window vent won't stay open, drops shut or won't lock, there's a good chance it has FAPIM hardware. Here's what that means.</p>
<h2>Who makes FAPIM?</h2>
<p>FAPIM is an Italian company from Tuscany that has made hardware for aluminum windows and doors since 1974. The name is an Italian acronym for "factory of accessories for metal windows and doors". It sells to more than 100 countries, and its Vista line is designed for the aluminum curtain walls and window walls used in high-rise buildings.</p>
<h2>How to recognize it</h2>
<p>Open the vent and look at the metal arms on the sides. FAPIM arms are stainless steel and the FAPIM name is usually stamped on the arm or the bracket. The handle is typically a die-cast aluminum lever that locks the vent at several points.</p>
<h2>Why these windows fail</h2>
<ul>
  <li><strong>Worn friction arms:</strong> the arms hold the vent open by friction. When they wear, the vent drops shut or won't stay put.</li>
  <li><strong>Wind damage:</strong> a gust catching an open vent on a high floor can bend an arm.</li>
  <li><strong>Handle wear:</strong> the gear and spring inside the handle wear, so it turns without locking.</li>
  <li><strong>Adjustment:</strong> keepers and corner locks drift, so the vent doesn't pull tight against the seals.</li>
</ul>
<h2>Why generic parts don't work well</h2>
<p>FAPIM arms come in specific lengths (from about 14 to 28 inches) and fit specific aluminum profiles. Generic North American arms often don't match the length or screw positions, so the vent sits crooked or doesn't seal. On a high floor, a poorly fitted arm is a safety risk.</p>
<h2>Getting it fixed</h2>
<p>FAPIM parts are hard to find in Canada. We import genuine FAPIM parts from Italy and install them from inside your unit. See <a href="/fapim-window-repair/">FAPIM window repair</a>, or the local pages for <a href="/fapim-window-repair-toronto/">Toronto</a> and <a href="/fapim-window-repair-mississauga/">Mississauga</a>.</p>
""",
    },
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
    {
        "slug": "sliding-patio-door-hard-to-open",
        "title": "Sliding patio door hard to open? 5 causes and how to fix them",
        "description": "Why sliding patio doors drag, grind or jump the track, what you can fix yourself, and when the rollers need replacing.",
        "date": "2026-10-24",
        "body": """
<p>A sliding patio door should glide with one hand. If you have to pull with your whole body, something is wrong, and forcing it makes it worse. Here are the usual causes, from easiest to hardest.</p>
<h2>1. A dirty track</h2>
<p>Sand, grit and leaves collect in the bottom track and jam the rollers. Vacuum the track, then wipe it with a damp cloth. Don't use oil or grease: they collect more dirt.</p>
<h2>2. Rollers set too low</h2>
<p>Most doors have adjustment screws at the bottom corners of the moving panel, often behind a small plastic cap. If the door drags on the track, the rollers may have dropped. Raising them a little can make a big difference.</p>
<h2>3. Worn or broken rollers</h2>
<p>This is the most common cause. The small wheels under the door flatten, crack or seize after years of use. You'll hear grinding or feel the door bump along. The fix is new rollers: the panel is lifted out, the old roller assemblies are replaced, and the door is set back and adjusted.</p>
<h2>4. A damaged track</h2>
<p>If the raised rail the rollers ride on is bent or worn flat, new rollers won't glide properly. A damaged rail can often be repaired or covered with a track cap rather than replacing the door.</p>
<h2>5. The frame has moved</h2>
<p>If the house has settled, the frame can go out of square, so the door rubs or won't lock. Adjusting the rollers and the lock keeper usually brings it back.</p>
<h2>When to call</h2>
<p>If cleaning the track doesn't help, or the door jumps off the track, call us before it gets worse. Patio door panels are heavy and the glass is large, so lifting them out is a two-person job. See <a href="/patio-door-repair/">patio door repair</a>.</p>
""",
    },
    {
        "slug": "drafty-windows-where-cold-air-gets-in",
        "title": "Drafty windows: where the cold air gets in and how to stop it",
        "description": "Find exactly where cold air leaks into your home around the windows, and the right fix for each spot, from weatherstripping to new glass.",
        "date": "2026-10-24",
        "body": """
<p>A drafty window doesn't always need replacing. Cold air usually comes in at one or two specific spots, and each one has its own fix. Here's how to find them.</p>
<h2>How to find a draft</h2>
<p>On a windy day, hold a lit candle or a strip of tissue paper near the window and move it slowly around the edges. Where it flickers or moves, air is getting in. A cheap infrared thermometer also works: cold spots show where air or heat is leaking.</p>
<h2>1. Between the sash and the frame</h2>
<p>The most common spot. Weatherstripping flattens, tears or falls off over time. New weatherstripping restores the seal. On casement windows, also check that the lock pulls the sash tight. See <a href="/window-lock-repair/">window lock repair</a>.</p>
<h2>2. Around the outside of the frame</h2>
<p>Cracked or missing exterior caulking lets wind and water in between the frame and the wall. The old caulking needs to be cut out and replaced, not covered over. See <a href="/window-caulking/">window caulking</a>.</p>
<h2>3. Through the glass</h2>
<p>A single pane or a double pane unit that has lost its seal and insulating gas feels cold to the touch. It isn't a draft, but it makes the room feel drafty. A new sealed unit with Low-E glass fixes it. See <a href="/foggy-window-repair/">foggy window repair</a>.</p>
<h2>4. A window that doesn't close all the way</h2>
<p>A bent hinge or a worn crank can leave a casement open a few millimetres. You may not see it, but you'll feel it. See <a href="/window-hinge-repair/">hinge repair</a>.</p>
<h2>5. Around the interior trim</h2>
<p>Gaps between the frame and the drywall can let cold air in from the wall cavity. Removing the trim and filling the gap with low-expansion foam fixes it.</p>
<p class="note">Fix drafts before winter. Exterior caulking needs dry weather above freezing to cure properly. Read our <a href="/winter-ready/">winter window checklist</a>.</p>
""",
    },
    {
        "slug": "tempered-vs-laminated-glass",
        "title": "Tempered vs. laminated glass: what your windows and doors need",
        "description": "The difference between regular, tempered and laminated glass, where each is required, and which to choose for security, safety and noise.",
        "date": "2026-10-24",
        "body": """
<p>When a window or door glass breaks, one of the first questions is what kind of glass it needs. The answer affects safety, security and sometimes what the building code requires.</p>
<h2>Regular (annealed) glass</h2>
<p>Standard window glass. It's the least expensive, but it breaks into large, sharp pieces. It's fine for most ordinary windows that aren't near floors, doors or bathtubs.</p>
<h2>Tempered glass</h2>
<p>Tempered glass is heat-treated to be about four times stronger than regular glass. When it does break, it shatters into small, blunt pieces that are much less likely to cause injury.</p>
<ul>
  <li>Usually required in doors, sidelites and patio doors</li>
  <li>Usually required in glass close to the floor, near stairs and around bathtubs and showers</li>
  <li>Can't be cut after it's made, so it's always ordered to the exact size</li>
</ul>
<h2>Laminated glass</h2>
<p>Laminated glass is two layers of glass bonded with a clear plastic interlayer. When it breaks, the pieces stick to the interlayer and the glass stays in the frame.</p>
<ul>
  <li><strong>Security:</strong> much harder to break through, so it slows down break-ins</li>
  <li><strong>Noise:</strong> reduces street and traffic noise</li>
  <li><strong>UV:</strong> blocks most UV light, which protects floors and furniture from fading</li>
  <li>Used in skylights and storefronts, and a good choice for ground-floor and basement windows</li>
</ul>
<h2>Which do you need?</h2>
<p>For a broken door or a window near the floor, usually tempered. For security after a break-in, laminated. For a street-facing bedroom, laminated helps with noise. We check what's required and recommend the right glass when we quote. See <a href="/window-glass-replacement/">window glass replacement</a>.</p>
""",
    },
]


# ---------------------------------------------------------------- pages
EXTRA_PAGES = [
    {
        "slug": "about",
        "crumb": "About us",
        "title": "About Us | Window Repair GTA",
        "description": "Window Repair GTA is a repair-first window and glass company serving Toronto and the GTA. Fully insured, WSIB covered, with a 1-year workmanship warranty.",
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
  <p class="lede">One contact for foggy glass, broken cranks, balcony doors and broken windows across your portfolio. Insured and WSIB covered, with clear invoices for every unit. WSIB clearance certificate available on request.</p>
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
        "title": "Window Repair for Real Estate Agents | Window Repair GTA",
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
        "slug": "privacy-policy",
        "crumb": "Privacy policy",
        "title": "Privacy Policy | Window Repair GTA",
        "description": "How Window Repair GTA collects, uses and protects the personal information you share when you request a quote or contact us.",
        "body": """
<section class="page-hero"><div class="wrap">
  {crumbs}
  <span class="tag">Privacy</span>
  <h1>Privacy policy</h1>
  <p class="lede">Last updated October 2026. This policy explains what personal information we collect when you contact us, why we collect it and how we protect it.</p>
</div></section>
<section class="section"><div class="wrap"><div class="prose">
  <h2>What we collect</h2>
  <p>When you fill in a form, call, text or message us, we may collect:</p>
  <ul>
    <li>Your name, phone number, email address and city or address</li>
    <li>Details about your windows or doors and the work you need</li>
    <li>Photos you send us of your windows, doors or property</li>
    <li>How you heard about us</li>
  </ul>
  <p>If website analytics are turned on, we also collect general information about how visitors use the site, such as pages viewed and the type of device, using cookies. This does not identify you by name.</p>
  <h2>Why we collect it</h2>
  <ul>
    <li>To answer your request and give you a quote</li>
    <li>To schedule, carry out and invoice the work</li>
    <li>To provide warranty service</li>
    <li>To improve our website and services</li>
  </ul>
  <p>We only use your information for these purposes. We don't sell or rent it to anyone.</p>
  <h2>Who we share it with</h2>
  <p>We share information only with service providers that help us run the business, such as our website host and form provider, email and phone services, and analytics, and only as needed for them to provide their service. We may also share information if the law requires it, or with your insurer if you ask us to help with a claim.</p>
  <h2>Photos</h2>
  <p>Photos you send are used to quote and plan your job. We will not publish photos of your property on our website or social media without your permission, and we never publish faces, house numbers or licence plates.</p>
  <h2>How long we keep it</h2>
  <p>We keep your information for as long as we need it to provide the service, honour warranties and meet legal and tax requirements, and then delete it.</p>
  <h2>Your choices and rights</h2>
  <p>You can ask to see the personal information we hold about you, ask us to correct it, or withdraw your consent and ask us to delete it, subject to legal requirements. To do this, contact us at {phone}.</p>
  <h2>Security</h2>
  <p>We take reasonable steps to protect your information from loss, misuse and unauthorized access. No method of sending information over the internet is completely secure.</p>
  <h2>Changes</h2>
  <p>We may update this policy from time to time. The date at the top shows when it was last changed.</p>
  <h2>Contact</h2>
  <p>Questions about privacy? Call or text us at {phone}.</p>
</div></div></section>""",
    },
    {
        "slug": "fapim-window-repair-toronto",
        "crumb": "FAPIM windows Toronto",
        "title": "FAPIM Window Repair Toronto | Genuine Italian Parts",
        "description": "FAPIM condo window repair in Toronto: stay arms, handles and locks replaced with genuine parts imported from Italy. Insured and WSIB covered.",
        "body": """
<section class="page-hero"><div class="wrap">
  {crumbs}
  <span class="tag">FAPIM specialists · Toronto</span>
  <h1>FAPIM window repair in Toronto</h1>
  <p class="lede">Condo vent that won't stay open, won't lock or lets in wind? We repair FAPIM windows in Toronto condos with genuine parts imported from Italy.</p>
  <div class="actions">{call}{text}</div>
</div></section>
{trust}
<section class="section"><div class="wrap"><div class="prose">
  <h2>FAPIM windows in Toronto condos</h2>
  <p>Many of Toronto's condo towers, especially downtown and in midtown, are built with aluminum window walls. The opening vents on those windows often use FAPIM hardware from Italy: stainless steel stay arms, a cremone handle and locking points around the frame. After years of use, wind and freeze and thaw cycles, the arms wear and the locks slip out of adjustment.</p>
  <h2>What we fix</h2>
  <ul class="ticks">
    <li>Stay arms that no longer hold the vent open, or that are bent</li>
    <li>Handles and cremones that turn but don't lock</li>
    <li>Keepers and corner locks out of adjustment, causing drafts</li>
    <li>Opening limiters and loose arm brackets</li>
  </ul>
  <h2>Genuine parts from Italy</h2>
  <p>FAPIM parts are hard to find in Canada, and generic hardware rarely fits these aluminum profiles. We import genuine FAPIM parts from Italy, so your window is repaired properly instead of patched. Read more about <a href="/fapim-window-repair/">FAPIM window repair</a>.</p>
  <h2>Buildings and areas we serve</h2>
  <p>Downtown Toronto, CityPlace, Liberty Village, King West, the Financial District, St. Lawrence, Yonge and Bloor, Yorkville, Midtown and Yonge and Eglinton, North York Centre and condos across the city.</p>
  <p class="note">Text us a photo of the arm (where the FAPIM name is stamped) and the handle. We'll tell you which parts you need.</p>
</div></div></section>
{cta}""",
    },
    {
        "slug": "fapim-window-repair-mississauga",
        "crumb": "FAPIM windows Mississauga",
        "title": "FAPIM Window Repair Mississauga | Genuine Italian Parts",
        "description": "FAPIM condo window repair in Mississauga: stay arms, handles and locks replaced with genuine parts imported from Italy. Insured and WSIB covered.",
        "body": """
<section class="page-hero"><div class="wrap">
  {crumbs}
  <span class="tag">FAPIM specialists · Mississauga</span>
  <h1>FAPIM window repair in Mississauga</h1>
  <p class="lede">FAPIM condo windows in Mississauga repaired with genuine Italian parts: stay arms, handles, cremones and locks.</p>
  <div class="actions">{call}{text}</div>
</div></section>
{trust}
<section class="section"><div class="wrap"><div class="prose">
  <h2>FAPIM windows in Mississauga condos</h2>
  <p>Mississauga's condo towers, especially around Square One and the City Centre, include many buildings with aluminum window walls and FAPIM hardware on the opening vents. When the stay arms wear out or the handle stops locking, the window can't be opened safely or lets in drafts and noise.</p>
  <h2>What we fix</h2>
  <ul class="ticks">
    <li>Stay arms that no longer hold the vent open, or that are bent</li>
    <li>Handles and cremones that turn but don't lock</li>
    <li>Keepers and corner locks out of adjustment, causing drafts</li>
    <li>Opening limiters and loose arm brackets</li>
  </ul>
  <h2>Genuine parts from Italy</h2>
  <p>FAPIM parts are hard to find in Canada, and generic hardware rarely fits these aluminum profiles. We import genuine FAPIM parts from Italy, so your window is repaired properly instead of patched. Read more about <a href="/fapim-window-repair/">FAPIM window repair</a>.</p>
  <h2>Buildings and areas we serve</h2>
  <p>Mississauga City Centre and Square One, Port Credit, Erin Mills, Cooksville, Hurontario corridor, Lakeview and condos across Mississauga.</p>
  <p class="note">Text us a photo of the arm (where the FAPIM name is stamped) and the handle. We'll tell you which parts you need.</p>
</div></div></section>
{cta}""",
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
