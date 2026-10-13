#!/usr/bin/env python3
"""Generates RoboRide's static sub-pages (shared header/footer). Run: python3 tools/build_pages.py
index.html and privacy.html are hand-maintained and NOT generated here."""
import os, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.nwaroboride.org/"
FORM = "https://formspree.io/f/mljgwkpr"
FONTS = "https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=optional"
NAV = [("index.html#how", "Riders", None), ("businesses.html", "Businesses", "businesses"), ("service-area.html", "Service Area", "service-area"),
       ("safety.html", "Safety", "safety"), ("about.html", "About", "about"), ("index.html#faq", "FAQ", None)]

def ext(url, text):
    return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'

def page(slug, title, desc, body, extra_head=""):
    nav = "\n".join(f'      <li><a href="{h}"{" aria-current=\"page\"" if k == slug else ""}>{t}</a></li>' for h, t, k in NAV)
    out = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | RoboRide LLC</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#0a0806">
<link rel="canonical" href="{SITE}{slug}.html">
<meta property="og:type" content="website">
<meta property="og:site_name" content="RoboRide">
<meta property="og:title" content="{title} | RoboRide">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE}{slug}.html">
<meta property="og:image" content="{SITE}image/og-cybercab.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/jpeg" href="image/favicon.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="{FONTS}">
<link href="{FONTS}" rel="stylesheet">
<noscript><link href="{FONTS}" rel="stylesheet"></noscript>
<link rel="stylesheet" href="site.css">
{extra_head}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <a class="logo" href="index.html" aria-label="RoboRide home">Robo<span>Ride</span></a>
  <nav id="site-nav" class="nav" aria-label="Primary">
    <ul>
{nav}
      <li><a class="btn" href="index.html#signup">Join Waitlist</a></li>
    </ul>
  </nav>
  <button class="menu-btn" type="button" aria-label="Open menu" aria-controls="site-nav" aria-expanded="false">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#e8e4dc" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
  </button>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="logo" href="index.html">Robo<span>Ride</span></a>
        <p class="muted small" style="max-width:280px">RoboRide LLC is preparing to offer autonomous Tesla Cybercab rides and goods delivery across Northwest Arkansas. Not affiliated with Tesla, Inc.</p>
      </div>
      <div><h2>Riders</h2><ul><li><a href="index.html#how">How it will work</a></li><li><a href="service-area.html">Service area</a></li><li><a href="index.html#faq">FAQ</a></li><li><a href="index.html#signup">Join the waitlist</a></li></ul></div>
      <div><h2>Businesses</h2><ul><li><a href="businesses.html">Delivery &amp; business</a></li><li><a href="businesses.html#interest">Register interest</a></li></ul></div>
      <div><h2>Company</h2><ul><li><a href="about.html">About &amp; mission</a></li><li><a href="about.html#roadmap">Launch roadmap</a></li><li><a href="safety.html">Safety &amp; regulation</a></li><li><a href="press.html">Press kit</a></li><li><a href="privacy.html">Privacy Policy</a></li></ul></div>
    </div>
    <div class="base"><span>© 2026 RoboRide LLC. Tesla and Cybercab are trademarks of Tesla, Inc.; RoboRide is an independent company.</span><span>Northwest Arkansas <span aria-hidden="true">🌲</span></span></div>
  </div>
</footer>
<script src="site.js" defer></script>
</body>
</html>
'''
    open(os.path.join(ROOT, slug + ".html"), "w").write(out)

HP = '<input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">'
CITIES = ["Bentonville", "Rogers", "Springdale", "Fayetteville", "Farmington", "Siloam Springs", "Eureka Springs", "Elsewhere in NWA"]

# ---------------- BUSINESSES ----------------
uses = [("Retail &amp; local shops", "Same-region delivery of customer orders from storefronts in Bentonville, Rogers, Springdale and Fayetteville."),
        ("Restaurants &amp; catering", "Takeout and catering runs between kitchens and customers, without scheduling a driver."),
        ("Business-to-business", "Documents, parts and supplies between offices, warehouses, shops and job sites."),
        ("Employee rides", "Getting staff between offices, campuses, hotels and XNA."),
        ("Venues &amp; events", "Pickup zones and group rides for concerts, festivals and game days.")]
use_cards = "".join(f'<div class="card reveal"><h3>{t}</h3><p>{d}</p></div>' for t, d in uses)
opts = "".join(f"<option>{c}</option>" for c in CITIES)
uopts = "".join(f"<option>{html.unescape(t)}</option>" for t, _ in uses) + "<option>Something else</option>"
page("businesses", "Delivery & Business", "Autonomous goods delivery and employee rides for Northwest Arkansas businesses. Register your interest with RoboRide.", f'''
<section class="page-hero"><div class="wrap">
  <div class="eyebrow">For businesses</div>
  <h1>Autonomous delivery<br><em class="hl">for NWA businesses.</em></h1>
  <p class="lead">RoboRide plans to use the same autonomous Cybercab fleet that carries riders to move goods across Northwest Arkansas: point to point, on demand, with no courier to schedule. We're not operating yet. Tell us what you'd want to move and we'll keep you posted as plans firm up.</p>
  <div class="actions"><a class="btn" href="#interest">Register interest</a><a class="btn ghost" href="service-area.html">See the planned service area</a></div>
</div></section>

<section class="section alt"><div class="wrap">
  <div class="eyebrow">Use cases we're designing for</div>
  <h2>What could a driverless <em class="hl">Cybercab carry?</em></h2>
  <p class="lead" style="margin-bottom:2rem">These are planned use cases, not services available today. Capacity, item limits and pricing haven't been set.</p>
  <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">{use_cards}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="eyebrow">How business delivery would work</div>
  <h2>Three steps, <em class="hl">once we launch.</em></h2>
  <ol class="steps" style="max-width:760px">
    <li class="reveal"><h3>Request a pickup</h3><p>Tell us the pickup and drop-off points and what's being sent.</p></li>
    <li class="reveal"><h3>A Cybercab arrives</h3><p>Load the goods at the curb; the vehicle drives itself to the destination.</p></li>
    <li class="reveal"><h3>The recipient unloads</h3><p>The recipient meets the vehicle and takes the delivery. Exact hand-off and verification steps will be shared before launch.</p></li>
  </ol>
  <p class="tiny" style="margin-top:1rem">Booking tools, tracking, item limits and billing are still being designed. We'll share details before any service starts.</p>
</div></section>

<section class="section alt" id="interest"><div class="wrap">
  <div class="eyebrow">Register interest</div>
  <h2>Tell us about <em class="hl">your business.</em></h2>
  <p class="lead" style="margin-bottom:2rem">There's no commitment. We'll use this only to contact you about RoboRide business services. See our <a href="privacy.html">Privacy Policy</a>.</p>
  <form class="form" data-formspree action="{FORM}" method="POST" novalidate>
    {HP}
    <input type="hidden" name="type" value="business">
    <input type="hidden" name="interest" value="Business partnership">
    <div class="row">
      <div><label for="b-name">Business name</label><input id="b-name" name="business" autocomplete="organization" required></div>
      <div><label for="b-email">Work email</label><input id="b-email" name="email" type="email" autocomplete="email" required></div>
    </div>
    <div class="row">
      <div><label for="b-city">City</label><select id="b-city" name="city">{opts}</select></div>
      <div><label for="b-use">Main use case</label><select id="b-use" name="use_case">{uopts}</select></div>
    </div>
    <div><label for="b-msg">Anything else? <span class="muted">(optional)</span></label><textarea id="b-msg" name="message" maxlength="2000"></textarea></div>
    <div><button class="btn" type="submit">Send</button></div>
    <p class="form-status" role="status" aria-live="polite"></p>
  </form>
</div></section>
''')

# ---------------- SERVICE AREA ----------------
CENSUS = "https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/cities/totals/sub-est2025_5.csv"
QF = "https://www.census.gov/quickfacts/"
cities = [  # name, x, y, pop (Census V2025, July 1 2025), county note
  ("Bentonville", 131, 99, 63057, "Benton County seat"),
  ("Rogers", 156, 112, 76956, "Benton County"),
  ("Springdale", 153, 162, 90685, "Washington and Benton counties"),
  ("Fayetteville", 147, 204, 106623, "Washington County seat; home of the University of Arkansas"),
  ("Farmington", 120, 211, 10658, "Washington County"),
  ("Siloam Springs", 40, 161, 21298, "Benton County"),
  ("Eureka Springs", 260, 89, 2258, "a Carroll County seat"),
]
pins = "\n".join(f'''        <g class="pin" data-city="{n}" role="button" tabindex="0" aria-pressed="false" aria-label="{n}"><circle class="ring" cx="{x}" cy="{y}" r="11" fill="rgba(232,183,78,.08)" stroke="#e8b74e" stroke-width="1" opacity=".5"/><circle cx="{x}" cy="{y}" r="5" fill="#e8b74e"/><circle cx="{x}" cy="{y}" r="2" fill="#15120c"/><text x="{x + (8 if n not in ('Bentonville','Farmington','Eureka Springs') else -8)}" y="{y - 10 if n in ('Siloam Springs','Eureka Springs') else y + 4}" text-anchor="{'start' if n not in ('Bentonville','Farmington','Eureka Springs') else 'end'}" font-size="8.5" fill="#f2dba0" font-family="DM Sans, sans-serif" font-weight="600" pointer-events="none">{n}</text></g>''' for n, x, y, *_ in cities)
btns = "".join(f'<li><button type="button" data-city="{n}" aria-pressed="false">{n}</button></li>' for n, *_ in cities)
data_js = ",".join(f'"{n}":{{pop:{p},county:"{c}"}}' for n, _, _, p, c in cities)
page("service-area", "Service Area", "RoboRide's planned Northwest Arkansas service area: Bentonville, Rogers, Springdale, Fayetteville, Farmington, Siloam Springs and Eureka Springs.", f'''
<section class="page-hero"><div class="wrap">
  <div class="eyebrow">Planned service area</div>
  <h1>Seven cities,<br><em class="hl">one region.</em></h1>
  <p class="lead">RoboRide is planning service across Northwest Arkansas, launching city by city. <strong style="color:#fff;font-weight:500">No cities are live yet.</strong> Pick a city to learn more.</p>
</div></section>
<section class="section" style="padding-top:1rem"><div class="wrap">
  <div class="explorer">
    <div class="map" role="region" aria-label="Map of planned RoboRide cities in Northwest Arkansas (simplified, not to scale for roads)">
      <svg viewBox="0 0 300 300" aria-hidden="false">
        <g fill="none" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M126 40 L131 99 L148 125 L153 162 L147 204 L144 270" stroke="rgba(232,183,78,.45)" stroke-width="3"/>
          <path d="M18 160 L40 161 L95 166 L153 162 L215 158 L285 150" stroke="rgba(232,183,78,.28)" stroke-width="2"/>
          <path d="M156 112 L200 108 L230 96 L260 89 L285 84" stroke="rgba(232,183,78,.28)" stroke-width="2"/>
          <path d="M131 99 L156 112" stroke="rgba(232,183,78,.22)" stroke-width="1.5"/>
          <path d="M95 225 L120 211 L147 204" stroke="rgba(232,183,78,.22)" stroke-width="1.5"/>
          <text x="131" y="50" font-size="7" fill="rgba(232,183,78,.6)" font-family="DM Sans, sans-serif">I-49</text>
          <text x="60" y="176" font-size="7" fill="rgba(232,183,78,.5)" font-family="DM Sans, sans-serif">US-412</text>
          <text x="205" y="118" font-size="7" fill="rgba(232,183,78,.5)" font-family="DM Sans, sans-serif">US-62</text>
        </g>
{pins}
      </svg>
    </div>
    <div>
      <ul class="city-list" aria-label="Choose a city">{btns}</ul>
      <div class="panel" id="city-panel" aria-live="polite">
        <span class="badge warn">Planned · not yet served</span>
        <h2 id="city-name" style="margin:.8rem 0 .25rem">Northwest Arkansas</h2>
        <p class="muted" id="city-blurb" style="margin:0">Select a city on the map or from the list.</p>
        <dl id="city-facts" hidden><dt>Population</dt><dd id="city-pop"></dd><dt>County</dt><dd id="city-county"></dd><dt>RoboRide status</dt><dd>Planned; no service yet</dd></dl>
        <p class="cite" style="margin-top:1rem">Population: U.S. Census Bureau, Vintage 2025 estimates (July 1, 2025): {ext(CENSUS, "dataset")} · {ext(QF, "QuickFacts")}</p>
        <div class="actions" style="margin-top:1.25rem"><a class="btn" href="index.html#signup">Join the waitlist</a></div>
      </div>
    </div>
  </div>
  <p class="tiny" style="margin-top:1.5rem">Map positions follow real latitude/longitude; roads are simplified. Launch order and exact coverage zones haven't been decided.</p>
</div></section>
<script>
(function(){{var D={{{data_js}}},nf=new Intl.NumberFormat('en-US');
function pick(n){{var d=D[n];if(!d)return;document.getElementById('city-name').textContent=n;
document.getElementById('city-blurb').textContent=n+' is part of RoboRide\\'s planned Northwest Arkansas service area.';
document.getElementById('city-pop').textContent=nf.format(d.pop)+' (July 1, 2025 estimate)';document.getElementById('city-county').textContent=d.county.charAt(0).toUpperCase()+d.county.slice(1);
document.getElementById('city-facts').hidden=false;
document.querySelectorAll('[data-city]').forEach(function(el){{el.setAttribute('aria-pressed',el.getAttribute('data-city')===n?'true':'false');}});}}
document.querySelectorAll('[data-city]').forEach(function(el){{el.addEventListener('click',function(){{pick(el.getAttribute('data-city'));}});
el.addEventListener('keydown',function(e){{if(e.key==='Enter'||e.key===' '){{e.preventDefault();pick(el.getAttribute('data-city'));}}}});}});
var h=decodeURIComponent(location.hash.slice(1)).replace(/-/g,' ');Object.keys(D).forEach(function(k){{if(k.toLowerCase()===h.toLowerCase())pick(k);}});}})();
</script>
''')

# ---------------- SAFETY ----------------
A619 = "https://www.arkleg.state.ar.us/Home/FTPDocument?path=%2FACTS%2F2021R%2FPublic%2FACT619.pdf"
A468 = "https://arkleg.state.ar.us/Home/FTPDocument?path=%2FACTS%2F2019R%2FPublic%2FACT468.pdf"
CAR = "https://webftp.blr.arkansas.gov/Home/FTPDocument?path=CAR%2FParts%2F27CARpt115.pdf"
CAR105 = "https://codeofarrules.arkansas.gov/Rules/Rule?chapterID=224&levelType=section&partID=1010&sectionID=28660&subChapterID=274&subPartID=4553&titleID=27"
JUSTIA = "https://law.justia.com/codes/arkansas/title-27/subtitle-4/chapter-51/subchapter-20/section-27-51-2001/"
DFA = "https://www.arkleg.state.ar.us/Home/FTPDocument?path=%2FAssembly%2F2021%2F2021R%2FFiscal+Impacts%2FHB1562-DFA1.pdf"
ARDOT = "https://www.ardot.gov/autonomous"
SGO = "https://www.nhtsa.gov/laws-regulations/standing-general-order-crash-reporting"
AVEP = "https://www.nhtsa.gov/sites/nhtsa.gov/files/2025-04/automated-vehicle-exemption-program-domestic-exemptions-2025.pdf"
NHTSA_RPT = "https://www.nhtsa.gov/sites/nhtsa.gov/files/2025-07/report-congress-research-rulemaking-automated-driving-systems-july-2025-tag.pdf"
TESLARATI = "https://www.teslarati.com/tesla-cybercab-dallas/"
FSD = "https://www.tesla.com/fsd/safety"
page("safety", "Safety & Regulation", "How autonomous vehicles are regulated in the U.S. and in Arkansas, and how RoboRide thinks about safety.", f'''
<section class="page-hero"><div class="wrap">
  <div class="eyebrow">Safety &amp; regulation</div>
  <h1>Safety first,<br><em class="hl">and by the rules.</em></h1>
  <p class="lead">Driverless vehicles are regulated at both the federal and state level. Here's a plain-language overview of the rules that apply in Arkansas, with links to the sources.</p>
  <p class="note" style="margin-top:1.5rem;max-width:760px">This page is general information, not legal advice. It's a summary as of October 2026; laws and rules change, so check the linked sources for the current text.</p>
</div></section>

<section class="section alt"><div class="wrap prose">
  <div class="eyebrow">Federal oversight</div>
  <h2>NHTSA sets the <em class="hl">vehicle rules.</em></h2>
  <p>The National Highway Traffic Safety Administration (NHTSA) regulates the safety of vehicles themselves. Manufacturers certify that their vehicles meet the Federal Motor Vehicle Safety Standards (FMVSS). For vehicles that don't fit standards written around human drivers, such as cars without a steering wheel, NHTSA runs exemption programs; in 2025 it opened its automated vehicle exemption program to U.S.-built vehicles. {ext(AVEP, "NHTSA")} · {ext(NHTSA_RPT, "NHTSA report to Congress, July 2025")}</p>
  <p>Under NHTSA's <strong>Standing General Order</strong>, companies operating automated driving systems must report certain crashes. Serious ones (for example a fatality, a hospital-treated injury, a struck pedestrian or cyclist, an air-bag deployment, or a tow-away) must be reported within five days. The current version took effect June 16, 2025. {ext(SGO, "NHTSA Standing General Order")}</p>
  <p>NHTSA is reviewing how Tesla certified the Cybercab to federal standards; according to news reports, Tesla's sworn answers are due October 30, 2026. {ext(TESLARATI, "Teslarati")}</p>
</div></section>

<section class="section"><div class="wrap prose">
  <div class="eyebrow">Arkansas law</div>
  <h2>Arkansas allows <em class="hl">driverless networks</em>, with approval.</h2>
  <ul>
    <li><strong>2019: pilot program.</strong> Act 468 of 2019 first allowed autonomous vehicles on Arkansas roads under a pilot program approved by the State Highway Commission. {ext(A468, "Act 468 (2019)")}</li>
    <li><strong>2021: current framework.</strong> Act 619 of 2021 replaced the pilot. Under Ark. Code §§ 27-51-2001 to -2006, autonomous and fully autonomous vehicles may operate under an <em>autonomous vehicle program</em> approved by the State Highway Commission. {ext(A619, "Act 619 (2021)")} · {ext(JUSTIA, "Ark. Code § 27-51-2001")}</li>
    <li><strong>Rides and goods.</strong> The law defines an "on-demand driverless capable vehicle network" (an app-dispatched service carrying persons <em>or goods</em>) and says a person may operate one in the state (§ 27-51-2003). {ext(A619, "Act 619")}</li>
    <li><strong>Operators are licensed.</strong> A human operator, or a <em>remote</em> operator of a fully autonomous vehicle, must hold a valid driver's license for that vehicle class (§ 27-51-2004). {ext(A619, "Act 619")}</li>
    <li><strong>One statewide rulebook.</strong> The State Highway Commission implements the law, and local governments can't add their own operating requirements or AV-specific taxes. {ext(DFA, "Arkansas DFA fiscal impact summary")}</li>
    <li><strong>A supervised start.</strong> Under the Commission's rules (27 CAR Part 115), a human operator must be physically present in the vehicle for the first six months of an approved program. After that, the operator may apply to remove that requirement by submitting trip, mileage, disengagement and crash information. {ext(CAR105, "27 CAR § 115-105")} · {ext(CAR, "27 CAR Part 115")}</li>
    <li><strong>Applying.</strong> Programs are submitted to the State Highway Commission through ARDOT. {ext(ARDOT, "ARDOT autonomous vehicles")}</li>
  </ul>
</div></section>

<section class="section alt"><div class="wrap">
  <div class="eyebrow">Our approach</div>
  <h2>What this means <em class="hl">for RoboRide.</em></h2>
  <div class="grid two" style="margin-top:1.5rem">
    <div class="card reveal"><h3>No shortcuts on approval</h3><p>Driverless service in Arkansas requires an approved autonomous vehicle program, and we won't carry riders or goods without one. Where we are in that process will be shown on our <a href="about.html#roadmap">roadmap</a>.</p></div>
    <div class="card reveal"><h3>Supervised before driverless</h3><p>State rules require a human operator on board for the first six months of an approved program. We see that period as a feature, not a hurdle.</p></div>
    <div class="card reveal"><h3>The technology</h3><p>The Cybercab runs Tesla's autonomous driving software. Tesla publishes its own safety data for FSD (Supervised); we link to it rather than repeat its claims. {ext(FSD, "Tesla FSD safety data")}</p></div>
    <div class="card reveal"><h3>Transparency</h3><p>We'll publish what we can about our operations as they begin. <span class="todo">[TODO: Joseph to decide what operating/safety info RoboRide will publish.]</span></p></div>
  </div>
</div></section>
''')

# ---------------- ABOUT ----------------
page("about", "About & Mission", "RoboRide LLC is a Northwest Arkansas company preparing to operate autonomous Cybercabs for rides and goods delivery.", '''
<section class="page-hero"><div class="wrap">
  <div class="eyebrow">About RoboRide</div>
  <h1>Built in NWA,<br><em class="hl">for NWA.</em></h1>
  <p class="lead">RoboRide LLC is an independent Northwest Arkansas company preparing to operate a fleet of autonomous Tesla Cybercabs for rides and goods delivery. We aren't operating yet; this page explains what we're building and how we plan to get there.</p>
</div></section>

<section class="section alt"><div class="wrap">
  <div class="grid two">
    <div class="card reveal"><div class="eyebrow">Mission</div><h2 style="font-size:1.6rem">Safe, simple, driverless transportation for Northwest Arkansas.</h2><p>Make getting around NWA, and getting things across it, easier, by running a local autonomous fleet that people and businesses can count on.</p></div>
    <div class="card reveal"><div class="eyebrow">Vision</div><h2 style="font-size:1.6rem">A region where a ride or a delivery is always a tap away.</h2><p>From the University of Arkansas to XNA to Bentonville Square, with less traffic stress, no tailpipe emissions, and a local team behind the service.</p></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="eyebrow">What we believe</div>
  <h2>Our <em class="hl">principles.</em></h2>
  <div class="grid" style="margin-top:1.5rem">
    <div class="card reveal"><h3>Safety before speed</h3><p>We'll launch only with the approvals state law requires, and expand only when operations are ready.</p></div>
    <div class="card reveal"><h3>Honest by default</h3><p>No made-up numbers. If something isn't decided, such as pricing or launch timing, we'll say so.</p></div>
    <div class="card reveal"><h3>Local first</h3><p>NWA is home. We want our service to fit how this region actually moves.</p></div>
    <div class="card reveal"><h3>Privacy matters</h3><p>We'll never sell your data. See our <a href="privacy.html">Privacy Policy</a>.</p></div>
  </div>
</div></section>

<section class="section alt"><div class="wrap">
  <div class="eyebrow">Founder</div>
  <h2>Who's behind <em class="hl">RoboRide.</em></h2>
  <div class="card" style="max-width:760px;display:flex;gap:1.5rem;flex-wrap:wrap;align-items:flex-start"><div style="flex:0 0 200px"><picture><source type="image/webp" srcset="image/founder-joseph-400.webp 400w, image/founder-joseph-800.webp 800w" sizes="200px"><img src="image/founder-joseph-400.jpg" srcset="image/founder-joseph-400.jpg 400w, image/founder-joseph-800.jpg 800w" sizes="200px" width="400" height="500" loading="lazy" decoding="async" alt="Joseph Bowers, founder of RoboRide LLC" style="width:200px;height:auto;aspect-ratio:4/5;border-radius:14px;display:block;object-fit:cover"></picture></div><div style="flex:1 1 280px"><h3>Joseph Bowers, Founder</h3><p>Joseph Bowers is the founder of RoboRide LLC. Born and raised in Fayetteville, he's an Arkansas native who drives a Tesla with Full Self-Driving and has seen up close what autonomous driving can do. At 23, he started RoboRide to bring safe, driverless transportation to his home region and to help make Northwest Arkansas roads safer for everyone.</p></div></div>
</div></section>

<section class="section" id="roadmap"><div class="wrap">
  <div class="eyebrow">Launch roadmap</div>
  <h2>How we get <em class="hl">to launch.</em></h2>
  <p class="lead" style="margin-bottom:2rem">These milestones depend on vehicle availability, state approval and readiness, so they aren't dated. Each one happens only when the one before it is complete.</p>
  <ol class="steps" style="max-width:820px">
    <li class="now reveal"><h3>Build interest <span class="badge" style="margin-left:.5rem;color:#4ade80;border-color:rgba(74,222,128,.4);background:rgba(74,222,128,.08)">Now</span></h3><p>Gather riders and businesses on the waitlist so we know where demand is strongest.</p></li>
    <li class="reveal"><h3>Secure vehicles</h3><p>Acquire Cybercabs if and when they become available to independent operators like RoboRide.</p></li>
    <li class="reveal"><h3>State approval</h3><p>Apply to the Arkansas State Highway Commission for an approved autonomous vehicle program. <a href="safety.html">How this works</a></p></li>
    <li class="reveal"><h3>Supervised start</h3><p>Operate with a human operator on board for the first six months, as state rules require.</p></li>
    <li class="reveal"><h3>Driverless service in a first city</h3><p>Apply to remove the on-board operator requirement, then open driverless rides and deliveries in one NWA city.</p></li>
    <li class="reveal"><h3>Grow city by city</h3><p>Expand across the planned <a href="service-area.html">service area</a> as operations prove out.</p></li>
  </ol>
</div></section>
''')

# ---------------- PRESS ----------------
page("press", "Press Kit", "Press information, boilerplate and media assets for RoboRide LLC.", '''
<section class="page-hero"><div class="wrap">
  <div class="eyebrow">Press kit</div>
  <h1>Writing about<br><em class="hl">RoboRide?</em></h1>
  <p class="lead">Here's what you need: a short description, key facts and assets you can use. For interviews or questions, use the waitlist form and choose "Press".</p>
  <div class="actions"><a class="btn" href="index.html#signup">Contact us (choose "Press")</a></div>
</div></section>

<section class="section alt"><div class="wrap prose">
  <div class="eyebrow">Boilerplate</div>
  <h2>About RoboRide LLC</h2>
  <p class="card" style="color:#e8e4dc">RoboRide LLC is a Northwest Arkansas company preparing to operate autonomous Tesla Cybercabs for passenger rides and goods delivery across Bentonville, Rogers, Springdale, Fayetteville and the surrounding region. RoboRide is not yet operating and is not affiliated with Tesla, Inc. Learn more at www.nwaroboride.org.</p>
  <h3>Fast facts</h3>
  <ul>
    <li><strong>Company:</strong> RoboRide LLC</li>
    <li><strong>Based in:</strong> Northwest Arkansas</li>
    <li><strong>Founder:</strong> Joseph Bowers</li>
    <li><strong>Services (planned):</strong> autonomous rides; goods and package delivery</li>
    <li><strong>Planned service area:</strong> Bentonville, Rogers, Springdale, Fayetteville, Farmington, Siloam Springs, Eureka Springs</li>
    <li><strong>Status:</strong> pre-launch; waitlist open</li>
    <li><strong>Founded:</strong> <span class="todo">[TODO: year/date]</span></li>
  </ul>
</div></section>

<section class="section"><div class="wrap">
  <div class="eyebrow">Assets</div>
  <h2>Logos &amp; <em class="hl">images.</em></h2>
  <div class="grid" style="margin-top:1.5rem">
    <div class="card"><div style="background:#0a0806;border:.5px solid var(--line);border-radius:.6rem;padding:2rem;text-align:center;margin-bottom:1rem"><span class="logo" style="font-size:2rem">Robo<span>Ride</span></span></div><h3>Wordmark</h3><p>Set in Syne ExtraBold; "Robo" in white, "Ride" in gold #E8B74E on dark #0A0806. <span class="todo">[TODO: provide an official logo file (SVG/PNG).]</span></p></div>
    <div class="card"><picture><source type="image/webp" srcset="image/founder-joseph-400.webp"><img src="image/founder-joseph-400.jpg" alt="Joseph Bowers, founder of RoboRide LLC" width="400" height="500" loading="lazy" decoding="async" style="width:120px;height:auto;border-radius:.6rem;display:block;margin-bottom:1rem"></picture><h3>Founder headshot</h3><p>Joseph Bowers. <a href="image/founder-joseph-800.jpg" download>Download JPG (800×1000)</a></p></div>
    <div class="card"><img src="image/favicon.jpg" alt="RoboRide icon" width="96" height="96" style="border-radius:.6rem;display:block;margin-bottom:1rem" loading="lazy"><h3>App icon</h3><p><a href="image/favicon.jpg" download>Download JPG</a></p></div>
    <div class="card"><img src="image/hero-cybercab-960.jpg" alt="Front view of a Tesla Cybercab with doors raised" width="960" height="540" style="width:100%;height:auto;border-radius:.6rem;display:block;margin-bottom:1rem" loading="lazy"><h3>Cybercab photo</h3><p>"Front of the Tesla Cybercab" by Steve Jurvetson, <a href="https://creativecommons.org/licenses/by/2.0/" target="_blank" rel="noopener">CC BY 2.0</a>; credit required. <a href="https://commons.wikimedia.org/wiki/File:Front_of_the_Tesla_Cybercab.jpg" target="_blank" rel="noopener">Original</a></p></div>
  </div>
  <p class="tiny" style="margin-top:1.25rem">Brand colors: gold #E8B74E · deep gold #C98F2B · background #0A0806 · text #E8E4DC. Tesla and Cybercab are trademarks of Tesla, Inc.</p>
</div></section>
''')
print("built: businesses, service-area, safety, about, press")
