#!/usr/bin/env python3
"""Generates RoboRide's static sub-pages (shared header/footer). Run: python3 tools/build_pages.py
index.html and privacy.html are hand-maintained and NOT generated here."""
import os, html, json, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.nwaroboride.org/"
FORM = "https://formspree.io/f/mljgwkpr"
# Public contact addresses (single source for generated pages; index.html mirrors these by hand).
EMAIL = {"hello": "hello@nwaroboride.org", "press": "press@nwaroboride.org", "partners": "partners@nwaroboride.org",
         "support": "support@nwaroboride.org", "privacy": "privacy@nwaroboride.org"}
# Social profiles (single source; index.html and 404.html mirror these by hand). X, Facebook and Instagram so far; add more here.
X_HANDLE = "@NWARoboRide"
X_URL = "https://x.com/NWARoboRide"
X_ICON = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>'
# Facebook Page has no vanity username yet: swap FB_URL here when it gets one.
FB_URL = "https://www.facebook.com/profile.php?id=61595134426111"
FB_ICON = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M24 12.07C24 5.41 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08v-3.49h3.04V9.41c0-3.02 1.8-4.7 4.54-4.7 1.31 0 2.68.24 2.68.24v2.97h-1.5c-1.5 0-1.96.93-1.96 1.89v2.26h3.32l-.53 3.5h-2.8V24C19.62 23.1 24 18.1 24 12.07"/></svg>'
def fb_link(cls="social-x social-fb"):
    return f'<a class="{cls}" href="{FB_URL}" target="_blank" rel="me noopener" aria-label="RoboRide LLC on Facebook">{FB_ICON}<span>Facebook</span></a>'
IG_URL = "https://www.instagram.com/nwaroboride/"
IG_HANDLE = "@nwaroboride"
IG_ICON = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><rect x="2.5" y="2.5" width="19" height="19" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r=".6" fill="currentColor"/></svg>'
def ig_link(cls="social-x social-ig"):
    return f'<a class="{cls}" href="{IG_URL}" target="_blank" rel="me noopener" aria-label="RoboRide on Instagram">{IG_ICON}<span>Instagram</span></a>'
def x_link(cls="social-x"):
    return f'<a class="{cls}" href="{X_URL}" target="_blank" rel="me noopener" aria-label="RoboRide on X, @NWARoboRide">{X_ICON}<span>{X_HANDLE}</span></a>'
def mail(key):
    return f'<a class="email" href="mailto:{EMAIL[key]}">{EMAIL[key]}</a>'
NAV = [("index.html#how", "Riders", None), ("businesses.html", "Businesses", "businesses"), ("service-area.html", "Service Area", "service-area"),
       ("safety.html", "Safety", "safety"), ("about.html", "About", "about"), ("index.html#faq", "FAQ", None), ("index.html#contact", "Contact", None)]

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
<meta property="og:image" content="{SITE}image/og/og-{slug}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html.escape(title)}: RoboRide, Northwest Arkansas">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="{X_HANDLE}">
<meta name="twitter:image" content="{SITE}image/og/og-{slug}.jpg">
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":SITE},{"@type":"ListItem","position":2,"name":title,"item":SITE+slug+".html"}]})}</script>
<link rel="icon" href="favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="image/favicon-32.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="fonts/syne-normal-latin-2.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/dmsans-normal-latin-1.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="site.css">
{extra_head}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <a class="logo" href="index.html" aria-label="RoboRide home"><img src="image/brand/roboride-logo-white.svg" width="30" height="30" alt="" style="display:inline-block;vertical-align:-6px;margin-right:.5rem">Robo<span>Ride</span></a>
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
        <a class="logo" href="index.html"><img src="image/brand/roboride-logo-white.svg" width="30" height="30" alt="" style="display:inline-block;vertical-align:-6px;margin-right:.5rem">Robo<span>Ride</span></a>
        <p class="muted small" style="max-width:280px">RoboRide LLC is preparing to offer autonomous Tesla Cybercab rides and goods delivery across Northwest Arkansas. Not affiliated with Tesla, Inc.</p>
      </div>
      <div><h2>Riders</h2><ul><li><a href="index.html#how">How it will work</a></li><li><a href="service-area.html">Service area</a></li><li><a href="index.html#faq">FAQ</a></li><li><a href="index.html#signup">Join the waitlist</a></li></ul></div>
      <div><h2>Businesses</h2><ul><li><a href="businesses.html">Delivery &amp; business</a></li><li><a href="businesses.html#interest">Register interest</a></li></ul></div>
      <div><h2>Company</h2><ul><li><a href="about.html">About &amp; mission</a></li><li><a href="about.html#roadmap">Launch roadmap</a></li><li><a href="safety.html">Safety &amp; regulation</a></li><li><a href="https://www.tesla.com/robotaxi/safety" target="_blank" rel="noopener">Tesla Robotaxi safety report</a></li><li><a href="press.html">Press kit</a></li><li><a href="privacy.html">Privacy Policy</a></li></ul></div>
      <div><h2>Contact</h2><ul><li>{mail("hello")}</li><li><a href="index.html#contact">All contact options</a></li><li>{x_link()}</li><li>{fb_link()}</li><li>{ig_link()}</li></ul></div>
    </div>
    <div class="share-row"><button type="button" class="share-btn" data-share data-title="{html.escape(title)} | RoboRide"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12v7a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-7M16 6l-4-4-4 4M12 2v13"/></svg><span>Share this page</span></button><span class="share-status" role="status" aria-live="polite"></span></div>
    <div class="base"><span>© 2026 RoboRide LLC. Tesla and Cybercab are trademarks of Tesla, Inc.; RoboRide is an independent company.</span><span>Northwest Arkansas <span aria-hidden="true">🌲</span></span></div>
  </div>
</footer>
<aside aria-label="Page tools"><a href="#main" class="to-top" aria-label="Back to top" hidden><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg></a></aside>
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
  <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr))">{use_cards}</div>
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
  <p style="margin:-1rem 0 2rem">Prefer email? Write to {mail("partners")}.</p>
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
import re as _re, pathlib as _pl
_ROOT = _pl.Path(__file__).resolve().parent.parent
ROADS = (_ROOT / "tools/map_roads.svg").read_text().rstrip("\n")
# Shared road layer: also written into index.html between ROADS markers so the two maps can't drift.
_idx = (_ROOT / "index.html").read_text()
_idx = _re.sub(r"(<!-- ROADS:BEGIN[^>]*-->\n).*?(\s*<!-- ROADS:END -->)", lambda m: m.group(1) + ROADS + m.group(2), _idx, flags=_re.S)
(_ROOT / "index.html").write_text(_idx)
# Label positions from index.html rawCities (labelX, labelY, align) so labels match the homepage map.
LBL = {}
for _m in _re.finditer(r"name: '([^']+)', x: \d+, y: \d+, labelX: (\d+), labelY: (\d+), align: '(\w+)'", _idx):
    _n, _lx, _ly, _al = _m.group(1), int(_m.group(2)), int(_m.group(3)), _m.group(4)
    LBL[_n] = (_lx, _ly, "start" if _al in ("left", "leftish") else "end")
CENSUS = "https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/cities/totals/sub-est2025_5.csv"
QF = "https://www.census.gov/quickfacts/"
LATLON = {"Bentonville": (36.3729, -94.2088), "Rogers": (36.332, -94.1185), "Springdale": (36.1867, -94.1288), "Fayetteville": (36.0626, -94.1574), "Farmington": (36.042, -94.2471), "Siloam Springs": (36.1881, -94.5405), "Eureka Springs": (36.4011, -93.738)}  # city-center coordinates
cities = [  # name, x, y, pop (Census V2025, July 1 2025), county note
  ("Bentonville", 131, 99, 63057, "Benton County seat"),
  ("Rogers", 156, 112, 76956, "Benton County"),
  ("Springdale", 153, 162, 90685, "Washington and Benton counties"),
  ("Fayetteville", 147, 204, 106623, "Washington County seat; home of the University of Arkansas"),
  ("Farmington", 120, 211, 10658, "Washington County"),
  ("Siloam Springs", 40, 161, 21298, "Benton County"),
  ("Eureka Springs", 260, 89, 2258, "a Carroll County seat"),
]
pins = "\n".join(f'''        <g class="pin" data-city="{n}" role="button" tabindex="0" aria-pressed="false" aria-label="{n}"><circle class="hit" cx="{x}" cy="{y-7}" r="15" fill="transparent"/><line x1="{x}" y1="{y}" x2="{LBL[n][0]}" y2="{LBL[n][1]}" stroke="#e8b74e" stroke-width="0.75" opacity="0.4"/><circle class="ring" cx="{x}" cy="{y}" r="5" fill="rgba(232,183,78,.08)" stroke="#e8b74e" stroke-width="1" opacity=".5"/><use href="#rr-pin" class="rr-pin rr-planned" x="{x-7:.1f}" y="{y-18.1:.1f}" width="14" height="18.1"/><text x="{LBL[n][0]}" y="{LBL[n][1]}" dominant-baseline="middle" text-anchor="{LBL[n][2]}" font-size="8.5" fill="#f2dba0" font-family="DM Sans, sans-serif" font-weight="600" pointer-events="none" style="paint-order:stroke" stroke="#15120c" stroke-width="2.5">{n}</text></g>''' for n, x, y, *_ in cities)
btns = "".join(f'<li><button type="button" data-city="{n}" aria-pressed="false">{n}</button></li>' for n, *_ in cities)
data_js = ",".join(f'"{n}":{{pop:{p},county:"{c}"}}' for n, _, _, p, c in cities)
_rd = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "map_roads.svg")).read()
_edges = []
_rdn = {}
for _nm, _al, _d in re.findall(r'<path data-road="([^"]+)"(?: data-name="([^"]+)")? d="([^"]+)"', _rd):
    if _al: _rdn[_nm] = _al
    _pts = re.findall(r'(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)', _d)
    for (_a, _b2), (_c, _e) in zip(_pts, _pts[1:]):
        _edges.append(f'[{_a},{_b2},{_c},{_e},"{_nm}"]')
roadjs = "[" + ",".join(_edges) + "]"
rnjs = json.dumps(_rdn)
simjs = "{" + ",".join(f'"{n}":{{"x":{x},"y":{y},"lat":{LATLON[n][0]},"lon":{LATLON[n][1]}}}' for n, x, y, *_ in cities) + "}"
page("service-area", "Service Area", "RoboRide's planned Northwest Arkansas service area: Bentonville, Rogers, Springdale, Fayetteville, Farmington, Siloam Springs and Eureka Springs.", f'''
<section class="page-hero"><div class="wrap">
  <div class="eyebrow"><img src="image/brand/roboride-pin.svg" width="14" height="18" alt="" style="vertical-align:-3px;margin-right:.4rem">Planned service area</div>
  <h1>Seven cities,<br><em class="hl">one region.</em></h1>
  <p class="lead">RoboRide is planning service across Northwest Arkansas, launching city by city. <strong style="color:#fff;font-weight:500">No cities are live yet.</strong> Pick a city to learn more.</p>
</div></section>
<section class="section" style="padding-top:1rem"><div class="wrap">
  <div class="explorer" id="map">
    <div class="map" role="region" aria-label="Map of planned RoboRide cities in Northwest Arkansas (simplified, not to scale for roads)">
      <svg viewBox="0 0 300 300" aria-hidden="false"><defs><symbol id="rr-pin" viewBox="70 32 260 336"><path fill="#e8b74e" d="M200 40C127 40 78 92 78 160C78 245 200 360 200 360S322 245 322 160C322 92 273 40 200 40Z"/><path fill="#0a0806" fill-rule="evenodd" transform="translate(87.86 63.42) scale(0.56)" d="M102.25 291.02C104.45 290.22 104.77 290.02 106.56 288.23C108.63 286.18 109.20 285.18 110.04 282.16C110.54 280.38 110.75 276.56 110.75 269.20C110.75 267.11 110.83 266.45 111.14 266.14C111.50 265.79 119.97 265.75 200.59 265.75C269.53 265.75 289.72 265.82 289.95 266.05C290.17 266.27 290.25 268.36 290.25 273.88C290.25 282.30 290.35 282.96 291.95 285.62C293.66 288.45 295.97 290.19 299.69 291.47C301.23 291.99 301.51 292.00 319.63 292.00L338.02 292.00L339.45 291.42C340.23 291.09 341.43 290.63 342.12 290.37C342.99 290.05 343.87 289.40 345.12 288.15C346.87 286.38 347.39 285.49 348.41 282.50C348.86 281.17 348.87 279.32 348.85 228.30L348.82 175.47L347.97 174.58C347.51 174.10 346.38 173.18 345.47 172.54C344.55 171.90 342.53 170.42 340.97 169.24C339.40 168.07 337.83 166.89 337.47 166.62C337.11 166.35 335.70 165.28 334.34 164.24C332.99 163.20 331.31 161.97 330.62 161.50C329.02 160.41 323.88 156.40 322.79 155.39C322.33 154.97 321.69 154.12 321.35 153.50C321.02 152.88 320.25 151.59 319.64 150.62C318.60 149.00 317.23 146.72 315.78 144.17C315.45 143.60 314.10 141.39 312.78 139.27C310.26 135.24 309.21 133.52 307.51 130.62C306.94 129.66 306.11 128.26 305.66 127.50C305.21 126.74 304.05 124.78 303.08 123.12C302.12 121.47 300.44 118.70 299.35 116.96C295.69 111.08 294.33 108.89 292.85 106.42C292.04 105.07 291.02 103.38 290.60 102.67C290.17 101.96 289.27 100.45 288.60 99.32C283.96 91.50 282.60 89.31 282.07 88.81L281.47 88.25L262.66 88.25C247.99 88.25 243.76 88.18 243.45 87.94C243.14 87.69 243.03 86.90 242.93 84.08L242.80 80.53L241.77 78.48C240.55 76.05 239.23 74.52 237.07 73.06C234.04 71.00 236.46 71.12 200.12 71.12C169.08 71.12 167.82 71.14 166.50 71.60C163.23 72.73 160.10 75.68 158.76 78.88C158.04 80.62 158.00 80.89 158.00 84.09C158.00 86.82 157.93 87.54 157.61 87.86C157.26 88.21 155.15 88.25 138.14 88.25C119.42 88.25 119.06 88.26 118.43 88.75C117.84 89.21 116.97 90.58 114.18 95.38C113.62 96.34 112.41 98.36 111.50 99.88C109.44 103.29 105.16 110.41 102.18 115.38C100.95 117.44 99.68 119.52 99.37 120.00C99.06 120.48 97.60 122.90 96.14 125.38C94.67 127.85 93.01 130.61 92.45 131.50C91.89 132.39 91.07 133.74 90.63 134.50C90.19 135.26 89.49 136.44 89.07 137.12C88.66 137.81 87.59 139.61 86.70 141.12C85.81 142.64 84.02 145.64 82.73 147.80C81.43 149.96 79.96 152.42 79.45 153.27C78.50 154.86 78.65 154.74 70.75 160.83C69.44 161.84 67.59 163.22 66.62 163.89C65.66 164.57 63.19 166.41 61.12 167.98C59.06 169.55 56.53 171.48 55.50 172.26C54.47 173.04 53.26 174.02 52.81 174.44L52.00 175.20L51.94 211.79C51.90 231.91 51.88 255.74 51.88 264.75L51.88 281.12L52.45 282.87C53.46 285.97 55.75 288.83 58.23 290.12C58.70 290.36 60.00 290.88 61.11 291.27L63.12 291.99L81.50 291.93L99.88 291.88L102.25 291.02ZM113.49 214.56C107.44 212.48 105.97 212.00 105.71 212.00C105.57 212.00 105.10 211.83 104.66 211.63C104.23 211.43 102.64 210.87 101.12 210.39C97.27 209.18 96.13 208.80 94.12 208.08C93.16 207.74 91.64 207.26 90.75 207.01C89.86 206.77 86.54 205.72 83.38 204.68C74.46 201.74 72.12 201.00 71.67 201.00C71.44 201.00 71.03 200.78 70.75 200.50C70.27 200.02 70.26 199.77 70.41 192.44C70.50 188.28 70.67 184.68 70.79 184.44C71.12 183.79 71.96 183.90 74.03 184.85C75.89 185.71 77.12 186.18 80.97 187.51C82.12 187.91 83.19 188.34 83.34 188.46C83.50 188.58 84.69 189.04 85.98 189.47C87.28 189.91 88.46 190.36 88.61 190.47C88.75 190.59 90.00 191.05 91.38 191.51C92.75 191.96 93.99 192.42 94.12 192.52C94.38 192.70 98.00 194.14 100.48 195.04C101.23 195.32 102.57 195.87 103.46 196.27C104.34 196.67 105.17 197.00 105.30 197.00C105.42 197.00 106.67 197.49 108.08 198.09C109.48 198.69 111.53 199.52 112.62 199.95C113.72 200.37 117.16 201.70 120.25 202.90L125.88 205.08L200.25 205.08L274.62 205.09L276.62 204.27C278.84 203.36 282.32 201.99 284.62 201.12C285.45 200.80 287.31 200.08 288.75 199.50C290.19 198.92 292.27 198.11 293.38 197.70C294.48 197.29 295.77 196.78 296.25 196.57C296.73 196.36 298.14 195.82 299.38 195.37C300.61 194.91 302.86 194.07 304.38 193.49C305.89 192.92 308.23 192.07 309.58 191.61C310.93 191.15 312.17 190.67 312.33 190.54C312.74 190.21 320.91 186.95 323.38 186.13C323.93 185.95 325.33 185.39 326.49 184.90C328.79 183.92 329.86 183.77 330.10 184.40C330.18 184.61 330.25 188.14 330.25 192.22C330.25 197.77 330.17 199.76 329.94 200.08C329.65 200.47 325.86 201.94 322.38 203.00C320.16 203.68 316.29 205.01 315.00 205.53C314.38 205.79 312.86 206.28 311.62 206.63C310.39 206.98 308.81 207.48 308.12 207.74C306.42 208.39 299.91 210.42 298.38 210.77C297.69 210.93 296.89 211.21 296.59 211.39C296.30 211.57 295.35 211.91 294.47 212.13C293.59 212.36 291.86 212.92 290.62 213.38C289.39 213.84 287.42 214.52 286.25 214.89L284.12 215.55L200.37 215.59L116.61 215.62L113.49 214.56ZM127.68 188.94C127.46 188.77 127.01 188.27 126.70 187.83C125.94 186.77 123.41 183.69 122.00 182.11C121.38 181.41 119.58 179.34 118.00 177.51C116.42 175.68 113.15 171.92 110.74 169.15C108.33 166.39 105.13 162.66 103.63 160.88C102.14 159.09 100.48 157.15 99.96 156.57C99.43 155.99 99.00 155.33 99.00 155.11C99.00 154.90 99.82 153.46 100.83 151.92C101.84 150.38 103.43 147.83 104.37 146.25C105.31 144.67 106.38 142.93 106.74 142.38C107.38 141.41 108.18 140.05 110.50 136.00C111.09 134.97 111.93 133.56 112.37 132.88C115.11 128.58 122.28 116.70 125.60 110.94C126.85 108.77 128.07 106.78 128.31 106.50C128.74 106.00 128.95 106.00 200.31 106.06L271.88 106.12L272.62 107.29C273.04 107.93 273.69 109.00 274.08 109.66C274.46 110.33 275.18 111.55 275.67 112.38C276.16 113.20 277.43 115.34 278.50 117.12C281.97 122.96 289.71 135.72 290.82 137.44C291.84 139.03 292.40 139.95 294.50 143.51C295.71 145.55 300.12 152.71 300.74 153.62C301.56 154.84 301.40 155.39 299.62 157.34C298.73 158.32 296.90 160.44 295.56 162.04C291.73 166.63 282.33 177.63 280.12 180.12C278.05 182.44 276.13 184.71 273.78 187.60L272.43 189.25L200.26 189.25C142.92 189.25 128.01 189.19 127.68 188.94ZM171.94 88.23C170.82 88.05 169.44 86.91 168.87 85.70C168.00 83.85 168.87 81.96 171.07 80.90L172.38 80.27L200.49 80.28C231.57 80.30 229.75 80.20 231.24 81.91C232.72 83.59 232.57 85.25 230.76 87.06C230.03 87.79 229.34 88.26 228.97 88.27C225.10 88.37 172.59 88.34 171.94 88.23Z"/></symbol></defs>
{ROADS}
        <path data-route d="" fill="none" stroke="#f6d58c" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="5 4"/>
{pins}
        <g data-car opacity="0" pointer-events="none"><circle r="9" fill="rgba(232,183,78,.28)"/><circle r="4.2" fill="#fff" stroke="#e8b74e" stroke-width="2"/></g>
      </svg>
    </div>
    <div>
      <div class="route-bar" id="route-bar"><div class="rb-ends"><div class="rb-end" id="rb-from"><span>From</span><b>–</b></div><div class="rb-end" id="rb-to"><span>To</span><b>–</b></div></div><p class="rb-prompt" id="route-prompt" aria-live="polite"><b>Step 1:</b> tap a city on the map or below to set <b>From</b>.</p><div class="rb-actions"><button type="button" class="btn-ghost" id="trip-swap" disabled>Swap</button><button type="button" class="btn-ghost" id="trip-clear" disabled>Clear route</button></div></div>
      <ul class="city-list" aria-label="Choose a city">{btns}</ul>
      <div class="panel" id="city-panel" aria-live="polite">
        <span class="badge warn">Planned · not yet served</span>
        <h2 id="city-name" style="margin:.8rem 0 .25rem">Northwest Arkansas</h2>
        <p class="muted" id="city-blurb" style="margin:0">Select a city on the map or from the list.</p>
        <dl id="city-facts" hidden><dt>Population</dt><dd id="city-pop"></dd><dt>County</dt><dd id="city-county"></dd><dt>RoboRide status</dt><dd>Planned; no service yet</dd></dl>
        <p class="cite" style="margin-top:1rem">Population: U.S. Census Bureau, Vintage 2025 estimates (July 1, 2025): {ext(CENSUS, "dataset")} · {ext(QF, "QuickFacts")}</p>
        <div class="trip" id="trip" aria-labelledby="trip-h">
          <h3 id="trip-h">Picture a trip</h3>
          <p class="muted trip-hint" id="trip-hint">Tap one city for <b>From</b>, then another for <b>To</b>. The route draws on the map.</p>
          <div class="trip-ends"><div><span>From</span><b id="trip-from">–</b></div><div><span>To</span><b id="trip-to">–</b></div></div>
          <div class="mode" role="group" aria-label="Trip type"><button type="button" data-mode="ride" aria-pressed="true">Ride</button><button type="button" data-mode="delivery" aria-pressed="false">Delivery</button></div>
          <div class="readout" aria-live="polite"><div><b data-sim-dist>–</b><span>Straight-line miles (approx.)</span></div><div><b data-sim-road>–</b><span>Route (simplified)</span></div></div>
          <p class="tiny" style="margin:0">An illustration, not a booking tool: RoboRide isn't operating yet. Miles are straight-line between city centers; road trips are longer. Prices and trip times haven't been set.</p>
        </div>
        <div class="actions" style="margin-top:1.25rem"><a class="btn" href="index.html#signup">Join the waitlist</a></div>
      </div>
    </div>
  </div>
  <p class="tiny" style="margin-top:1.5rem">Map positions follow real latitude/longitude; roads are simplified, traced from OpenStreetMap (© OpenStreetMap contributors, ODbL). Thin lines are state-highway back roads. Launch order and exact coverage zones haven't been decided.</p>
</div></section>
<script>
(function(){{var D={{{data_js}}},C={simjs},E={roadjs},RN={rnjs},nf=new Intl.NumberFormat('en-US'),$=function(i){{return document.getElementById(i)}};
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches,cur=null,A=null,B=null,mode='ride',anim=0;
var route=document.querySelector('[data-route]'),car=document.querySelector('[data-car]');
/* road graph built from the shared map_roads.svg */
var N={{}},key=function(x,y){{return x+','+y}};
E.forEach(function(e){{var a=key(e[0],e[1]),b=key(e[2],e[3]),w=Math.hypot(e[2]-e[0],e[3]-e[1])*(/^AR-/.test(e[4])?1.08:1);
(N[a]=N[a]||[]).push([b,w,e[4]]);(N[b]=N[b]||[]).push([a,w,e[4]]);}});
function path(s,t){{var d={{}},pv={{}},pn={{}},seen={{}};d[s]=0;for(;;){{var u=null;for(var k in d)if(!seen[k]&&(u===null||d[k]<d[u]))u=k;if(u===null)return null;if(u===t)break;seen[u]=1;
(N[u]||[]).forEach(function(n){{var v=d[u]+n[1];if(d[n[0]]===undefined||v<d[n[0]]){{d[n[0]]=v;pv[n[0]]=u;pn[n[0]]=n[2];}}}});}}
var pts=[t],names=[];for(var c=t;c!==s;c=pv[c]){{if(pn[c]&&names.indexOf(pn[c])<0)names.unshift(pn[c]);pts.unshift(pv[c]);}}return {{pts:pts,names:names}};}}
function mi(a,b){{var R=3958.8,r=Math.PI/180,dA=(b.lat-a.lat)*r,dO=(b.lon-a.lon)*r,h=Math.sin(dA/2)*Math.sin(dA/2)+Math.cos(a.lat*r)*Math.cos(b.lat*r)*Math.sin(dO/2)*Math.sin(dO/2);return 2*R*Math.asin(Math.sqrt(h))}}
function mark(){{document.querySelectorAll('.map [data-city]').forEach(function(el){{var n=el.getAttribute('data-city');el.classList.toggle('is-start',n===A);el.classList.toggle('is-end',n===B);}});}}
function nm(r){{return r&&r.names.length?r.names.map(function(n){{return RN[n]?n+' ('+RN[n]+')':n}}).join(' → '):''}}
function draw(){{cancelAnimationFrame(anim);var r=A&&B?path(key(C[A].x,C[A].y),key(C[B].x,C[B].y)):null,VIA=nm(r);$('trip-from').textContent=A||'–';$('trip-to').textContent=B||'–';$('trip-clear').disabled=!(A||B);$('trip-swap').disabled=!(A&&B);
$('rb-from').querySelector('b').textContent=A||'–';$('rb-to').querySelector('b').textContent=B||'–';$('rb-from').classList.toggle('is-set',!!A);$('rb-to').classList.toggle('is-set',!!B);$('rb-from').classList.toggle('is-next',!A);$('rb-to').classList.toggle('is-next',!!A&&!B);
$('route-prompt').innerHTML=!A?'<b>Step 1:</b> tap a city on the map or below to set <b>From</b>.':!B?'<b>Step 2:</b> tap another city to set <b>To</b>.':'Route shown: <b>'+A+'</b> to <b>'+B+'</b>'+(VIA?' via '+VIA:'')+'. Tap any city to start a new trip.';mark();
var dist=document.querySelector('[data-sim-dist]'),road=document.querySelector('[data-sim-road]');
if(!A||!B){{route.setAttribute('d','');car.setAttribute('opacity',0);dist.textContent='–';road.textContent='–';$('trip-hint').hidden=false;return}}
$('trip-hint').hidden=true;
dist.textContent='≈ '+Math.round(mi(C[A],C[B]))+' mi';road.textContent=VIA||'Secondary roads';
route.setAttribute('d',r?'M'+r.pts.map(function(p){{return p.replace(',',' ')}}).join(' L'):'');route.setAttribute('stroke',mode==='ride'?'#f6d58c':'#7fd6ff');
var L=route.getTotalLength();car.setAttribute('opacity',L?1:0);if(!L)return;
if(reduce){{var e=route.getPointAtLength(L);car.setAttribute('transform','translate('+e.x+' '+e.y+')');return}}
var t0=performance.now(),Dur=Math.max(1400,L*14);(function step(tm){{var k=Math.min(1,((tm-t0)%(Dur+700))/Dur),q=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2,pt=route.getPointAtLength(L*q);
car.setAttribute('transform','translate('+pt.x.toFixed(2)+' '+pt.y.toFixed(2)+')');anim=requestAnimationFrame(step)}})(t0);}}
function pick(n){{var d=D[n];if(!d)return;cur=n;$('city-name').textContent=n;
$('city-blurb').textContent=n+' is part of RoboRide\u2019s planned Northwest Arkansas service area.';
$('city-pop').textContent=nf.format(d.pop)+' (July 1, 2025 estimate)';$('city-county').textContent=d.county.charAt(0).toUpperCase()+d.county.slice(1);
$('city-facts').hidden=false;
document.querySelectorAll('[data-city]').forEach(function(el){{el.setAttribute('aria-pressed',el.getAttribute('data-city')===n?'true':'false');}});}}
/* a tap sets From, the next tap sets To; a tap after a full route starts a new trip */
function choose(n){{if(!D[n])return;if(!A||(A&&B)){{A=n;B=null;}}else if(n===A){{A=null;}}else B=n;pick(n);draw();}}
document.querySelectorAll('[data-city]').forEach(function(el){{el.addEventListener('click',function(e){{e.preventDefault();choose(el.getAttribute('data-city'));}});
el.addEventListener('keydown',function(e){{if(e.key==='Enter'||e.key===' '){{e.preventDefault();choose(el.getAttribute('data-city'));}}}});}});
$('trip-swap').addEventListener('click',function(){{if(!(A&&B))return;var t=A;A=B;B=t;draw();}});
document.querySelectorAll('[data-mode]').forEach(function(btn){{btn.addEventListener('click',function(){{mode=btn.getAttribute('data-mode');document.querySelectorAll('[data-mode]').forEach(function(x){{x.setAttribute('aria-pressed',x===btn?'true':'false')}});draw();}});}});
$('trip-clear').addEventListener('click',function(){{A=B=null;draw();if(cur)pick(cur);}});
var h=decodeURIComponent(location.hash.slice(1)).replace(/-/g,' ');Object.keys(D).forEach(function(k){{if(k.toLowerCase()===h.toLowerCase())pick(k);}});draw();}})();
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
RT_SAFETY = "https://www.tesla.com/robotaxi/safety"
page("safety", "Safety & Regulation", "How autonomous vehicles are regulated in the U.S. and in Arkansas, and how RoboRide thinks about safety.", f'''
<section class="page-hero"><div class="wrap">
  <div class="eyebrow">Safety &amp; regulation</div>
  <h1>Safety first,<br><em class="hl">and by the rules.</em></h1>
  <p class="lead">Driverless vehicles are regulated at both the federal and state level. Here's a plain-language overview of the rules that apply in Arkansas, with links to the sources.</p>
  <p class="note" style="margin-top:1.5rem;max-width:760px">This page is general information, not legal advice. It's a summary as of October 2026; laws and rules change, so check the linked sources for the current text.</p>
</div></section>

<section class="section" style="padding-top:2rem;padding-bottom:2rem"><div class="wrap">
  <div class="card" id="tesla-safety-report" style="max-width:760px;border-color:rgba(232,183,78,.45)">
    <div class="eyebrow">Safety data</div>
    <h2 style="font-size:1.5rem;margin:.25rem 0 .5rem">Tesla's official Robotaxi safety report</h2>
    <p>Tesla's live page with driverless miles and crash and injury data for its Robotaxi fleet. Published by Tesla, Inc.; RoboRide is independent and links to it as industry information.</p>
    <p style="margin:1rem 0 0"><a class="btn" href="{RT_SAFETY}" target="_blank" rel="noopener">View Tesla's Robotaxi safety report <span aria-hidden="true">↗</span></a></p>
  </div>
</div></section>

<section class="section alt"><div class="wrap prose">
  <div class="eyebrow">Federal oversight</div>
  <h2>NHTSA sets the <em class="hl">vehicle rules.</em></h2>
  <p>The National Highway Traffic Safety Administration (NHTSA) regulates the safety of vehicles themselves. Manufacturers certify that their vehicles meet the Federal Motor Vehicle Safety Standards (FMVSS). For vehicles that don't fit standards written around human drivers, such as cars without a steering wheel, NHTSA runs exemption programs; in 2025 it opened its automated vehicle exemption program to U.S.-built vehicles. {ext(AVEP, "NHTSA")} · {ext(NHTSA_RPT, "NHTSA report to Congress, July 2025")}</p>
  <p>Under NHTSA's <strong>Standing General Order</strong>, companies operating automated driving systems must report certain crashes. Serious ones (for example a fatality, a hospital-treated injury, a struck pedestrian or cyclist, an air-bag deployment, or a tow-away) must be reported within five days. The current version took effect June 16, 2025. {ext(SGO, "NHTSA Standing General Order")}</p>
  <p>NHTSA is reviewing how Tesla certified the Cybercab to federal standards; according to news reports, Tesla's sworn answers were due October 30, 2026, and Tesla has since received a 30-day extension. {ext(TESLARATI, "Teslarati")} · {ext("https://www.notateslaapp.com/news/4819/tesla-cybercab-to-let-riders-see-rear-and-side-camera-feeds", "Not a Tesla App")}</p>
  <p>Separately, on October 9, 2026 NHTSA opened a review of a defect petition (DP26010) alleging that Tesla robotaxis, Model Y and Cybercab, exceeded posted speed limits in active school zones. NHTSA will decide whether to open a formal investigation. {ext("https://www.theverge.com/transportation/1010364/tesla-robotaxi-school-zonespeeding-investigation", "The Verge")}</p>
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
    <div class="card reveal"><h3>The technology</h3><p>The Cybercab runs Tesla's autonomous driving software. Tesla publishes its own safety data for its driverless Robotaxi fleet; we link to it rather than repeat its claims. {ext(RT_SAFETY, "Tesla Robotaxi Vehicle Safety Report")}</p></div>
    <div class="card reveal"><h3>Transparency</h3><p>As service begins, we'll post updates on this site about how RoboRide operates</p></div>
  </div>
</div></section>
''')

# ---------------- ABOUT ----------------
page("about", "About & Mission", "RoboRide LLC is a Northwest Arkansas company preparing to operate autonomous Cybercabs for rides and goods delivery.", '''
<section class="page-hero"><div class="wrap">
  <div class="eyebrow">About RoboRide</div>
  <h1>Built in NWA,<br><em class="hl">for NWA.</em></h1>
  <p class="lead">RoboRide LLC is an independent Northwest Arkansas company preparing to operate a fleet of autonomous Tesla Cybercabs for rides and goods delivery. We aren't operating yet; this page explains what we're building and how we plan to get there. Founded June 8, 2026.</p>
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
  <div class="card" style="max-width:760px;display:flex;gap:1.5rem;flex-wrap:wrap;align-items:flex-start"><div style="flex:0 0 200px"><picture><source type="image/avif" srcset="image/founder-joseph-400.avif 400w, image/founder-joseph-800.avif 800w" sizes="200px"><source type="image/webp" srcset="image/founder-joseph-400.webp 400w, image/founder-joseph-800.webp 800w" sizes="200px"><img src="image/founder-joseph-400.jpg" srcset="image/founder-joseph-400.jpg 400w, image/founder-joseph-800.jpg 800w" sizes="200px" width="400" height="500" loading="lazy" decoding="async" alt="Joseph Bowers, founder of RoboRide LLC" style="width:200px;height:auto;aspect-ratio:4/5;border-radius:14px;display:block;object-fit:cover"></picture></div><div style="flex:1 1 280px"><h3>Joseph Bowers, Founder</h3><p>Joseph Bowers is the founder of RoboRide LLC. Born and raised in Fayetteville, he's an Arkansas native who drives a Tesla with Full Self-Driving and has seen up close what autonomous driving can do. At 23, he started RoboRide to bring safe, driverless transportation to his home region and to help make Northwest Arkansas roads safer for everyone.</p></div></div>
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
''' + f'''
<section class="section alt" id="contact"><div class="wrap">
  <div class="eyebrow">Contact</div>
  <h2>Say <em class="hl">hello.</em></h2>
  <p class="lead">General questions about RoboRide: {mail("hello")}. Media: {mail("press")}. Businesses: {mail("partners")}.</p>
</div></section>
''')

# ---------------- PRESS ----------------
page("press", "Press Kit", "Press information, boilerplate and media assets for RoboRide LLC.", f'''
<section class="page-hero"><div class="wrap">
  <div class="eyebrow">Press kit</div>
  <h1>Writing about<br><em class="hl">RoboRide?</em></h1>
  <p class="lead">Here's what you need: a short description, key facts and assets you can use. For interviews or questions, email {mail("press")}. For announcements and launch news, media can follow <a href="{X_URL}" target="_blank" rel="me noopener" aria-label="RoboRide on X, @NWARoboRide">{X_HANDLE}</a> on X, <a href="{FB_URL}" target="_blank" rel="me noopener" aria-label="RoboRide LLC on Facebook">RoboRide LLC on Facebook</a> and <a href="{IG_URL}" target="_blank" rel="me noopener" aria-label="RoboRide on Instagram">RoboRide on Instagram</a>.</p>
  <div class="actions"><a class="btn" href="mailto:{EMAIL["press"]}">Email press@</a>{x_link("btn ghost social-x")}{fb_link("btn ghost social-x social-fb")}{ig_link("btn ghost social-x social-ig")}</div>
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
    <li><strong>Founded:</strong> June 8, 2026</li>
  </ul>
</div></section>

<section class="section"><div class="wrap">
  <div class="eyebrow">Assets</div>
  <h2>Logos &amp; <em class="hl">images.</em></h2>
  <div class="grid" style="margin-top:1.5rem">
    <div class="card"><div style="background:#0a0806;border:.5px solid var(--line);border-radius:.6rem;padding:1.5rem;text-align:center;margin-bottom:1rem"><img src="image/brand/roboride-logo-white.svg" width="96" height="96" alt="RoboRide logo, white" loading="lazy"></div><h3>Logo (white)</h3><p>For dark backgrounds. <a href="image/brand/roboride-logo-white.svg" download>SVG</a> · <a href="image/brand/roboride-logo-white-1024.png" download>PNG 1024</a></p></div>
    <div class="card"><div style="background:#f4efe6;border:.5px solid var(--line);border-radius:.6rem;padding:1.5rem;text-align:center;margin-bottom:1rem"><img src="image/brand/roboride-logo-dark.svg" width="96" height="96" alt="RoboRide logo, dark" loading="lazy"></div><h3>Logo (dark)</h3><p>For light backgrounds. <a href="image/brand/roboride-logo-dark.svg" download>SVG</a> · <a href="image/brand/roboride-logo-dark-1024.png" download>PNG 1024</a></p></div>
    <div class="card"><div style="background:#0a0806;border:.5px solid var(--line);border-radius:.6rem;padding:1.5rem;text-align:center;margin-bottom:1rem"><img src="image/brand/roboride-icon.svg" width="96" height="96" alt="RoboRide app icon" loading="lazy" style="border-radius:.6rem"></div><h3>App icon</h3><p>Square, on dark. <a href="image/brand/roboride-icon.svg" download>SVG</a> · <a href="image/brand/roboride-icon-1024.png" download>PNG 1024</a></p></div>
    <div class="card"><div style="background:#0a0806;border:.5px solid var(--line);border-radius:.6rem;padding:1.5rem;text-align:center;margin-bottom:1rem"><img src="image/brand/roboride-pin.svg" width="75" height="96" alt="RoboRide service-area pin" loading="lazy"></div><h3>Service-area pin (secondary mark)</h3><p>The RoboRide cab in a gold map pin. Use it for places RoboRide serves or plans to serve, not as a replacement for the main logo. <a href="image/brand/roboride-pin.svg" download>SVG</a> · <a href="image/brand/roboride-pin-512.png" download>PNG 512</a></p></div>
    <div class="card"><div style="background:#0a0806;border:.5px solid var(--line);border-radius:.6rem;padding:1.5rem;text-align:center;margin-bottom:1rem"><span class="logo" style="font-size:clamp(1.3rem,6vw,2rem);white-space:nowrap"><img src="image/brand/roboride-logo-white.svg" width="30" height="30" alt="" style="display:inline-block;vertical-align:-6px;margin-right:.5rem">Robo<span>Ride</span></span></div><h3>Wordmark</h3><p>Set in Syne ExtraBold; "Robo" in white, "Ride" in gold #E8B74E on dark #0A0806, with the logo to the left.</p></div>
    <div class="card"><picture><source type="image/avif" srcset="image/founder-joseph-400.avif"><source type="image/webp" srcset="image/founder-joseph-400.webp"><img src="image/founder-joseph-400.jpg" alt="Joseph Bowers, founder of RoboRide LLC" width="400" height="500" loading="lazy" decoding="async" style="width:120px;height:auto;border-radius:.6rem;display:block;margin-bottom:1rem"></picture><h3>Founder headshot</h3><p>Joseph Bowers. <a href="image/founder-joseph-800.jpg" download>Download JPG (800×1000)</a></p></div>
    <div class="card"><picture><source type="image/avif" srcset="image/hero-cybercab-960.avif"><source type="image/webp" srcset="image/hero-cybercab-960.webp"><img src="image/hero-cybercab-960.jpg" alt="Front view of a Tesla Cybercab with doors raised" width="960" height="540" style="width:100%;height:auto;border-radius:.6rem;display:block;margin-bottom:1rem" loading="lazy" decoding="async"></picture><h3>Cybercab photo</h3><p>"Front of the Tesla Cybercab" by Steve Jurvetson, <a href="https://creativecommons.org/licenses/by/2.0/" target="_blank" rel="noopener">CC BY 2.0</a>; credit required. <a href="https://commons.wikimedia.org/wiki/File:Front_of_the_Tesla_Cybercab.jpg" target="_blank" rel="noopener">Original</a></p></div>
  </div>
  <p class="tiny" style="margin-top:1.25rem">Brand colors: gold #E8B74E · deep gold #C98F2B · background #0A0806 · text #E8E4DC. Tesla and Cybercab are trademarks of Tesla, Inc.</p>
</div></section>
''')
print("built: businesses, service-area, safety, about, press")

# ---------------- PRIVACY (content kept in privacy.html between markers) ----------------
_pv = open(os.path.join(ROOT, "privacy.html")).read()
if "<!-- PRIVACY:BEGIN -->" in _pv:
    _pc = _pv.split("<!-- PRIVACY:BEGIN -->")[1].split("<!-- PRIVACY:END -->")[0]
else:
    _pc = _pv.split("<main>")[1].split("</main>")[0]
    _pc = _pc.replace('<p style="color:#a89c88;margin:0">Effective date', '<p class="muted" style="margin:0">Effective date')
assert "DRAFT" not in _pc and EMAIL["privacy"] in _pc, "privacy.html content must be final and list the privacy@ address"
page("privacy", "Privacy Policy", "How RoboRide LLC handles the information you share when you join the waitlist or register business interest.", f'''
<section class="section prose-wrap"><div class="wrap prose">
<!-- PRIVACY:BEGIN -->{_pc}<!-- PRIVACY:END -->
</div></section>
''')
