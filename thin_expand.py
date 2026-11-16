"""Extra sections and FAQs for service pages that were too short (Nov 2026).

Each entry is appended to the page body and FAQ list in content.py.
No prices or claims beyond what the owner has confirmed.
"""

EXPAND = {
    "window-screen-repair": {
        "body": """
<h2>Signs your screen needs work</h2>
<ul>
  <li>Torn, stretched or loose mesh</li>
  <li>A bent frame that no longer sits tight in the window</li>
  <li>The rubber spline that holds the mesh has popped out</li>
  <li>A sliding screen door that falls off its track, drags or won't latch</li>
  <li>A missing screen after windows were replaced or a move</li>
</ul>
<h2>Repair or a new screen?</h2>
<p>If the frame is straight, we re-screen it with new mesh and spline. If the frame is bent or a corner is broken, we build a new frame to size. Sliding screen doors usually need new rollers and a latch, not a whole new door.</p>
<h2>Mesh choices</h2>
<p>Standard fibreglass mesh suits most windows. If you have pets that push on screens, ask about a heavier mesh. Tell us what you need it for and we'll suggest the right one.</p>
<p>Need a size? See <a href="/measure-glass/">how to measure</a>, or send us a photo with a tape measure across the screen.</p>
""",
        "faqs": [
            ("My sliding screen door keeps falling off the track. Can it be fixed?",
             "Usually yes. Worn or misadjusted rollers are the common cause. We replace the rollers and adjust the door so it stays on the track."),
            ("Do you re-screen the frame or make a new one?",
             "If the frame is straight, we re-screen it. If it's bent or broken, we make a new frame to size."),
        ],
    },
    "window-handle-repair": {
        "body": """
<h2>Which handle do you have?</h2>
<ul>
  <li><strong>Folding crank handles</strong> on casement and awning windows. They fold flat against the operator cover.</li>
  <li><strong>T-handles and knob handles</strong> on older crank operators.</li>
  <li><strong>Lever handles</strong> on tilt and turn windows, which also control the locking points.</li>
  <li><strong>FAPIM lever handles</strong> on many Toronto and Mississauga condo vents. See <a href="/fapim-window-repair/">FAPIM window repair</a>.</li>
</ul>
<h2>Why handles break</h2>
<p>Most crank handles fit onto a splined shaft, a short metal post with fine teeth. When the teeth inside the handle wear down, the handle spins without turning the window. Handles also crack at the base, or the small set screw that holds them works loose. Lever handles wear inside, so they turn without locking.</p>
<h2>Why "just buying a handle" often fails</h2>
<p>Handles differ in spline size, length, offset and colour. A handle that looks right may not grip the shaft or may hit the window sill. Send us a photo of the handle and the operator, and we'll bring a match.</p>
""",
        "faqs": [
            ("Can I buy a handle myself?",
             "You can, but many don't fit because of spline size and shape. A photo of yours lets us bring the right one."),
            ("My handle turns but the window doesn't move. What's broken?",
             "Either the handle's teeth are worn or the gears inside the operator are stripped. We check both and replace only what's needed."),
        ],
    },
    "window-hinge-repair": {
        "body": """
<h2>Types of window hinges</h2>
<ul>
  <li><strong>Casement hinges</strong> (four-bar hinges) on the top and bottom of side-opening windows. They let the sash swing out and slide along a track.</li>
  <li><strong>Awning hinges</strong> on the sides of windows that open from the bottom.</li>
  <li><strong>Friction stays</strong> on many condo and European windows, including FAPIM, that hold the vent open by friction.</li>
</ul>
<p>Hinges come in different lengths and track styles, so we match the size, the hole pattern and the material. Stainless steel hinges last longest, especially on windows that face the weather.</p>
<h2>Hinge or operator?</h2>
<p>If the window drags on the frame, won't close square or the corner drops, it's usually the hinges. If the crank turns but the window doesn't move, it's usually the operator. See <a href="/window-crank-repair/">window crank repair</a>. Often both are worn, and we fix them in one visit.</p>
""",
        "faqs": [
            ("Why does the bottom corner of my casement window drag?",
             "Worn or bent hinges let the sash drop, so the corner rubs the frame. New hinges lift it back into place."),
            ("How do you know which hinge size I need?",
             "We measure the hinge track and check the brand and hole pattern. A photo of the open window with the hinge visible helps us quote."),
        ],
    },
    "window-lock-repair": {
        "body": """
<h2>Types of window locks</h2>
<ul>
  <li><strong>Cam locks</strong> on casement windows: a lever on the side of the frame that hooks the sash.</li>
  <li><strong>Multi-point locks</strong>: one lever moves a bar that locks the sash at two or more points, with keepers on the frame.</li>
  <li><strong>Sash locks</strong> where the two sashes of a hung window meet, and latches on sliding windows.</li>
  <li><strong>Tilt and turn locking gear</strong>, controlled by the handle. See <a href="/tilt-and-turn-window-repair/">tilt and turn window repair</a>.</li>
</ul>
<h2>Lock won't latch? It may only need adjusting</h2>
<p>Often the lock is fine and the keepers on the frame have moved, or the sash has dropped so the lock can't reach. We adjust the keepers and hinges first, and replace the lock only if it's worn or broken.</p>
<h2>Security tips</h2>
<ul>
  <li>Lock ground floor and basement windows, even when you're home.</li>
  <li>A window that closes but won't lock is an easy way in. Get it fixed before you go away.</li>
  <li>Consider laminated glass for windows that are easy to reach. See <a href="/blog/tempered-vs-laminated-glass/">tempered vs laminated glass</a>.</li>
</ul>
""",
        "faqs": [
            ("My window only locks at one point. Is that a problem?",
             "Yes. It leaves the window loose, letting in drafts and making it easier to force. Usually a keeper or the lock bar needs adjusting or replacing."),
            ("Do you replace locks on sliding windows too?",
             "Yes. We replace latches and locks on sliding, hung, casement and awning windows."),
        ],
    },
    "window-latch-repair": {
        "body": """
<h2>Signs a latch needs replacing</h2>
<ul>
  <li>The latch spins or flops and doesn't catch</li>
  <li>A hung window won't tilt in for cleaning, or won't tilt back</li>
  <li>A plastic tilt latch is cracked or the spring is gone</li>
  <li>A sliding window won't stay closed</li>
</ul>
<h2>Matching the part</h2>
<p>Latches differ by window brand, size, hand (left or right) and colour. We look at the window brand and the latch shape, then bring the right part so it fits the existing holes and looks like it came with the window.</p>
<h2>Fix it before it gets worse</h2>
<p>A broken tilt latch can let a sash fall inward when it's opened, and a sliding window that won't latch is a security problem. Latches are small parts, so it's a quick repair. Combine it with other small fixes in one visit.</p>
""",
        "faqs": [
            ("Can you replace a tilt latch without replacing the sash?",
             "Yes. Tilt latches are separate parts that we replace in the existing sash."),
            ("My sliding window won't stay closed. Is it the latch?",
             "Often. It can also be a worn roller or track. We check the window and replace what's needed."),
        ],
    },
    "door-repair": {
        "body": """
<h2>Common door problems we fix</h2>
<ul>
  <li><strong>A door that sticks or rubs</strong> at the top or side, usually from loose or worn hinges</li>
  <li><strong>A latch that won't catch</strong> the strike plate, so the door won't stay closed or lock</li>
  <li><strong>Drafts</strong> under or around the door from worn weatherstripping or a door sweep</li>
  <li><strong>Glass</strong> that's cracked or foggy. See <a href="/front-door-glass/">front door glass</a>.</li>
  <li><strong>Commercial doors</strong> that slam, drift open or don't latch, often a door closer that needs adjusting</li>
</ul>
<h2>How we fix it</h2>
<p>Most door problems are fixed with adjustment and a few parts: tightening or replacing hinges, moving the strike plate, replacing weatherstripping and sweeps, and adjusting closers. We tell you before we replace anything bigger.</p>
<h2>Doors after a break-in</h2>
<p>If a door was forced, we secure it the same day and repair the frame, strike and hardware. Calls after 10 PM have a $100 after-hours call-out fee. See <a href="/emergency-glass-repair/">emergency repairs</a>.</p>
""",
        "faqs": [
            ("My door rubs at the top corner. Can it be fixed without planing it?",
             "Usually yes. A loose or worn top hinge lets the door drop. Tightening or replacing the hinge often fixes it."),
            ("There's a draft under my front door. What fixes it?",
             "A new door sweep or threshold seal, and new weatherstripping around the frame if it's worn."),
        ],
    },
    "front-door-glass": {
        "body": """
<h2>Glass options</h2>
<ul>
  <li><strong>Clear glass</strong> for the most light</li>
  <li><strong>Frosted or textured glass</strong> for privacy</li>
  <li><strong>Decorative inserts</strong> with wrought iron, bevels or patterns</li>
</ul>
<p>Glass in doors must be safety glass. Inserts we install use tempered glass, which breaks into small blunt pieces instead of sharp shards.</p>
<h2>Sidelites and transoms</h2>
<p>The narrow glass panels beside a door (sidelites) and the glass above it (transoms) can be replaced the same way. Many owners update all of them together so they match. For arched transoms, see <a href="/curved-glass-replacement/">curved and shaped glass</a>.</p>
<h2>Fixing foggy or cracked door glass</h2>
<p>Door glass is a sealed unit, so fog between the panes or a crack means the insert is replaced. The door, frame and hardware stay.</p>
""",
        "faqs": [
            ("Will a new insert fit my door?",
             "We measure the opening and the frame around the glass, then match an insert to your door."),
            ("Can you replace the glass beside my door too?",
             "Yes. We replace sidelites and transoms, and can match them to a new door insert."),
        ],
    },
    "curved-glass-replacement": {
        "body": """
<h2>How we measure shaped glass</h2>
<p>Arched and shaped glass can't be measured with a tape alone. We take exact measurements and, when needed, make a template of the opening so the new glass fits the curve. That's why shaped glass is made to order and takes longer than a standard rectangle.</p>
<h2>Glass options</h2>
<ul>
  <li>Double pane sealed units, with Low-E coating and argon fill</li>
  <li>Tempered glass where safety glass is required, like transoms over doors</li>
  <li>Clear, frosted or decorative glass</li>
</ul>
<h2>Common problems</h2>
<p>Arched windows above doors and large windows fog up just like regular windows, and they crack from impact or frame movement. In most cases we replace only the glass and keep the frame.</p>
""",
        "faqs": [
            ("Why does shaped glass take longer?",
             "Each piece is made to the exact shape of your opening, often from a template, so it takes longer to make than a standard size."),
            ("Can you fix a foggy half-round window above my door?",
             "Yes. We replace the sealed unit in the existing frame."),
        ],
    },
    "wood-window-repair": {
        "body": """
<h2>Signs of wood rot</h2>
<ul>
  <li>Soft or spongy wood on the sill or the bottom of the sash</li>
  <li>Peeling or blistering paint that keeps coming back</li>
  <li>Gaps between the glass and the wood, or missing glazing putty</li>
  <li>Dark stains or mould at the corners</li>
</ul>
<h2>Century homes and heritage windows</h2>
<p>Many Toronto homes have original wood windows that are worth keeping. We repair rotted sills and sash parts, replace glass and glazing, and get stuck sashes moving again. If your home is in a heritage district, check with the City before you replace windows, because changes may need approval.</p>
<h2>Keep wood windows healthy</h2>
<ul>
  <li>Keep the paint and caulking intact so water can't get into the wood.</li>
  <li>Clear snow and water from sills.</li>
  <li>Fix small soft spots early, before they spread.</li>
</ul>
""",
        "faqs": [
            ("Can you replace the glass in a wood window?",
             "Yes. We replace single pane glass and sealed units in wood sashes and reglaze them."),
            ("Do you repair windows in heritage homes?",
             "Yes. We repair the existing wood windows rather than replace them where we can. Check with the City if your home is in a heritage district."),
        ],
    },
    "window-leak-drainage-repair": {
        "body": """
<h2>Is it a leak or condensation?</h2>
<p>Water on the inside of the glass in winter is usually condensation from humid indoor air, not a leak. Water that shows up after rain, runs down the wall or stains the drywall under the window is a leak. See <a href="/blog/condensation-between-window-panes/">condensation between the panes</a> for the difference.</p>
<h2>Blocked weep holes</h2>
<p>Most windows have small drain holes, called weep holes, in the bottom of the frame. When dirt, bugs or old caulking block them, rain fills the track and spills inside. Clearing them is often the whole fix.</p>
<h2>Basement windows and window wells</h2>
<p>A window well that doesn't drain fills with water and pushes it through the window. We check the well, the drain and the caulking. See <a href="/basement-window-repair/">basement window repair</a>.</p>
<h2>When it's not the window</h2>
<p>Sometimes water comes from the roof, the siding or the flashing above the window. If it's not the window, we'll tell you so you call the right trade.</p>
""",
        "faqs": [
            ("Why is there water on the inside of my window in winter?",
             "Usually it's condensation from humid indoor air. Lower humidity and better air flow help. If water appears after rain, it's a leak."),
            ("Can you fix a leak without replacing the window?",
             "Usually yes: clearing weep holes, resealing caulking or replacing seals fixes most window leaks."),
        ],
    },
    "skylight-repair": {
        "body": """
<h2>Leak or condensation?</h2>
<p>A skylight that drips in winter isn't always leaking. Warm, humid air rising to the cold glass condenses and drips down. If the water shows up only in cold weather and the glass is wet on the inside, it's likely condensation. If it shows up after rain or snow melt, it's a leak.</p>
<h2>Winter ice dams</h2>
<p>Ice that builds up on the roof around a skylight can push melting water under the flashing and seals. If your skylight leaks only when there's ice on the roof, the flashing or the roof around it needs attention, and we'll tell you if that's a job for a roofer.</p>
<h2>Foggy skylight glass</h2>
<p>Fog between the panes means the seal has failed, just like a regular window. We replace the glass unit and keep the frame when it's in good shape.</p>
""",
        "faqs": [
            ("Why does my skylight drip only in winter?",
             "Usually condensation: warm indoor air hitting cold glass. Ice dams on the roof can also cause winter leaks."),
            ("Can you replace only the skylight glass?",
             "Often yes. If the frame and flashing are sound, we replace just the glass unit."),
        ],
    },
}
