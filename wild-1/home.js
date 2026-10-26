// ===== FSD miles counter config (fleet-based projection; edit only this object to re-anchor) =====
// Model: miles(t) = latest official miles anchor + integral from that anchor to t of fleet(t) x milesPerCarPerDay(t).
// After an anchor with ratePerSec, miles grow at that official pace instead of the fleet model.
// RE-ANCHOR CHECKLIST:
//   1. New official cumulative total from Tesla? Add it to MILES_ANCHORS. The anchor with the latest date that
//      has already passed becomes the base (chosen by date, not by array order). An older or rounder total,
//      including Q3's "nearly two million" on Sept 30, must not replace a newer official figure.
//   2. New full-fleet count (tracker or Tesla)? Append it to FLEET_ANCHORS with a `cars` field (keep dates ascending).
//      Fleet is linearly interpolated between those anchors, then extrapolated from the last one (see FLEET_EXTRAP).
//      Cybercab-only counts (Austin in-service, Texas registry) go in the same array WITHOUT `cars`, so they
//      are on record and cannot pull the fleet model backward.
//   3. Optionally retune MPD (miles per car per day) if Tesla gives utilization data. Do not retune the forward
//      rate off an older rounded total when a newer official pace exists.
// Dates are ISO with Central offset. All numbers are estimates except the MILES_ANCHORS Tesla stated.
const FSD_COUNTER = {
  // Official cumulative unsupervised miles stated by Tesla. The latest date that has passed wins.
  MILES_ANCHORS: [
    { date: '2026-09-03T19:00:00-05:00', miles: 1000000, src: 'Ashok Elluswamy, Tesla Cybercab event, Austin (time approximate)' },
    // Q3 2026 Update, SEC exhibit 99.1 (filed with the Oct 21, 2026 earnings release): "We reached nearly two
    // million cumulative unsupervised miles for our Robotaxi service as of the end of the quarter." End of
    // quarter = Sept 30, 2026. Stored as 2,000,000 because Tesla gave a rounded phrase, not an odometer reading.
    // Historical only: Oct 18's 3,112,541 is newer and more precise, so this anchor must not become the base
    // or slow the counter. The same update says cumulative unsupervised miles grew eightfold quarter over quarter.
    { date: '2026-09-30T23:59:59-05:00', miles: 2000000, src: 'Tesla Q3 2026 Update, SEC exhibit 99.1: nearly two million cumulative unsupervised miles as of Sept 30, 2026 (rounded)' },
    // Tesla Robotaxi Vehicle Safety Report (tesla.com/robotaxi/safety, launched Oct 2026): "Miles Driven Autonomously",
    // 3,112,541 mi as of 10/18/2026 23:59:59 CT (Jan 22 - Oct 18, no safety monitor in the car; TX + FL; Bay Area excluded).
    // ratePerSec = the pace Tesla's own live counter on that page adds (0.0009221 mi/ms = 0.9221 mi/s ≈ 79,669 mi/day;
    // confirmed by reading the page 60 s apart on Oct 21: +56 and +55 mi). After this anchor the counter grows at that rate.
    // Not retuned for Q3: Sept 30 -> Oct 18 added about 1.11 million miles in 18 days (~62,000/day), below this later
    // official pace, which fits a growing fleet. Using the rounded Sept 30 figure forward would move the counter backward.
    { date: '2026-10-18T23:59:59-05:00', miles: 3112541, ratePerSec: 0.9221, src: 'Tesla Robotaxi Vehicle Safety Report, tesla.com/robotaxi/safety' }
    // Next: replace with Tesla's next official figure (an update to the safety page, or a later stated total).
  ],
  // Unsupervised (no one in the car) robotaxi fleet counts. Bay Area safety-driver cars excluded.
  // Entries with `cars` are the full tracked driverless fleet and drive interpolation.
  // Entries without `cars` are Cybercab-only notes and are ignored by fsdFleet().
  FLEET_ANCHORS: [
    { date: '2026-09-03T19:00:00-05:00', cars: 256, src: 'RobotaxiTracker via The Verge, six cities' },
    { date: '2026-10-10T12:00:00-05:00', cars: 374, src: 'Tracker: Austin 275 + Dallas 67 + Houston 32 (Teslarati / EV, Oct 10-11)' },
    { date: '2026-10-10T18:00:00-05:00', cybercabs: 300, scope: 'austin-in-service', src: 'Tesla Robotaxi account: 300+ Cybercabs serving Austin (Tesla News Wire). Cybercab-only, not the full TX driverless fleet, so no `cars` field.' },
    { date: '2026-10-12T12:00:00-05:00', cars: 435, src: 'Tracker: Austin 335 (Tesla News Wire) + Dallas/Houston ~100' },
    { date: '2026-10-14T12:00:00-05:00', cars: 501, src: 'Tracker: Austin 400 + Dallas 68 + Houston 33 (teslanewswire.com/robotaxi-tracker)' },
    { date: '2026-10-19T08:00:00-05:00', cars: 508, src: 'Robotaxi Tracker via @moondough on X, Oct 19: Austin 405 + Dallas 70 + Houston 33 (TX driverless; FL 29 and Bay Area excluded as before). TxDMV registry 803 (454 MY + 349 CC) is registered, not in service' },
    { date: '2026-10-19T12:00:00-05:00', cybercabs: 349, scope: 'tx-dmv-registered', src: 'Texas DMV registry: 349 Cybercabs (Tesla News Wire). Registered vehicles, not the in-service total. Does not replace the 508-car tracker anchor.' },
    { date: '2026-10-21T16:30:00-05:00', cybercabGrowth: 'about 10x since launch ~1 month earlier', scope: 'austin-cybercab', src: 'Elon Musk, Q3 2026 earnings call (Oct 21, 4:30 p.m. CT). No exact fleet total; the Q3 deck gives none. Does not replace the 508-car tracker anchor.' }
  ],
  // Fleet counts drive the model only BEFORE the newest official anchor (and its MPD fit); after an anchor that has
  // ratePerSec, the official pace is used instead. After the last fleet anchor that has `cars`: add CARS_PER_DAY (≈ the Sept 3 -> Oct 14 average, 245 cars / 41 days, not the
  // faster last-week burst; kept at 6 on Oct 19 although Oct 14-19 showed only +7 cars, too short/noisy a window to retune; Q3 gave no fleet total, so not retuned Oct 22) for MAX_DAYS, then hold the fleet flat. FREEZE_DAYS after the last fleet anchor the
  // counter stops entirely and shows "needs a new baseline". ANCHOR_FREEZE_DAYS: when the newest official anchor has a
  // ratePerSec, the counter instead stops that many days after it (Dec 13, 2026 for the Oct 18 anchor): a flat rate
  // gets stale as the fleet grows, so it should be re-anchored to Tesla's page before then. Q3's rounded Sept 30
  // total did not move this freeze.
  FLEET_EXTRAP: { CARS_PER_DAY: 6, MAX_DAYS: 56, FREEZE_DAYS: 84, ANCHOR_FREEZE_DAYS: 56 },
  // Miles per car per day: rises linearly with fleet size (bigger fleets = better utilization), capped.
  // Retuned Oct 21 to Tesla's official numbers: the old 150 -> 200 curve gave 3,664,133 mi at Oct 18 23:59:59 CT vs
  // Tesla's 3,112,541 (+18%). Sept 3 -> Oct 18 officially added 2,112,541 mi in 45.2 days ≈ 46,700 mi/day over an
  // average ~344-car tracked fleet ≈ 136 mi/car/day. Now: 121 at 256 cars, +36 per 252 extra cars, cap 157
  // (= Tesla's 79,669 mi/day / 508 cars on Oct 18-19). This reproduces 2,114,579 mi for that window (+0.1%).
  // Left as-is on Oct 22: the Q3 "nearly 2 million" point is rounded and older than the Oct 18 anchor.
  MPD: { BASE: 121, BASE_FLEET: 256, PER_CAR: 36 / 252, CAP: 157 }
};
// ===========================================================================
function fsdFleetAnchors() { return FSD_COUNTER.FLEET_ANCHORS.filter(a => typeof a.cars === 'number'); }
function fsdMilesAnchor(ms) { // latest-dated anchor at or before ms (array order cannot let an older total win)
  const past = FSD_COUNTER.MILES_ANCHORS.filter(a => Date.parse(a.date) <= ms);
  const list = past.length ? past : FSD_COUNTER.MILES_ANCHORS;
  return list.reduce((best, a) => Date.parse(a.date) > Date.parse(best.date) ? a : best);
}
function fsdFleet(ms) {
  const A = fsdFleetAnchors(), X = FSD_COUNTER.FLEET_EXTRAP, DAY = 864e5;
  const t = (a) => Date.parse(a.date);
  if (ms <= t(A[0])) return A[0].cars;
  for (let i = 1; i < A.length; i++) if (ms <= t(A[i])) {
    const k = (ms - t(A[i - 1])) / (t(A[i]) - t(A[i - 1])); return A[i - 1].cars + k * (A[i].cars - A[i - 1].cars);
  }
  const last = A[A.length - 1];
  return last.cars + X.CARS_PER_DAY * Math.min(X.MAX_DAYS, (ms - t(last)) / DAY);
}
function fsdMpd(cars) { const m = FSD_COUNTER.MPD; return Math.min(m.CAP, Math.max(m.BASE, m.BASE + m.PER_CAR * (cars - m.BASE_FLEET))); }
function fsdOfficialRate(ms) { // official pace from the newest past anchor that has one (mi/ms), else null
  const a = fsdMilesAnchor(ms);
  return a && a.ratePerSec ? a.ratePerSec / 1000 : null;
}
function fsdRate(ms) { const o = fsdOfficialRate(ms); if (o !== null) return o; const f = fsdFleet(ms); return f * fsdMpd(f) / 864e5; } // miles per millisecond
// Precomputed cumulative miles at hourly steps (Simpson's rule), then interpolated: cheap per tick, smooth.
const FSD_TABLE = (() => {
  const c = FSD_COUNTER, H = 36e5, now = Date.now();
  const base = fsdMilesAnchor(now);
  const t0 = Date.parse(base.date), lastFleet = Date.parse(fsdFleetAnchors()[fsdFleetAnchors().length - 1].date);
  const tEnd = base.ratePerSec ? t0 + c.FLEET_EXTRAP.ANCHOR_FREEZE_DAYS * 864e5 : lastFleet + c.FLEET_EXTRAP.FREEZE_DAYS * 864e5;
  const cum = [base.miles];
  for (let t = t0; t < tEnd; t += H) cum.push(cum[cum.length - 1] + H / 6 * (fsdRate(t) + 4 * fsdRate(t + H / 2) + fsdRate(t + H)));
  return { t0, tEnd, H, cum, base };
})();
function fsdProjection(now) {
  const T = FSD_TABLE, capped = now >= T.tEnd, t = Math.min(Math.max(now, T.t0), T.tEnd);
  const i = Math.min(Math.floor((t - T.t0) / T.H), T.cum.length - 2), dt = t - (T.t0 + i * T.H);
  // within the hour: exact-enough linear step using the instantaneous rate
  return { miles: Math.min(T.cum[i] + fsdRate(T.t0 + i * T.H + dt / 2) * dt, T.cum[i + 1]), capped, fleet: fsdFleet(t), mpd: fsdMpd(fsdFleet(t)), perDay: fsdRate(t) * 864e5 };
}

// ===========================================================================
// RoboRide experimental homepage behaviour (vanilla JS, no framework).
(function () {
  var doc = document, reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  doc.documentElement.classList.add('js');
  var $$ = function (s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); };
  var nf = new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 });

  // ---- Miles counter (whole miles only) ----
  var pr0 = fsdProjection(Date.now());
  var fill = function (sel, v) { $$(sel).forEach(function (el) { el.textContent = v; }); };
  fill('[data-fsd-base]', nf.format(FSD_TABLE.base.miles));
  fill('[data-fsd-basedate]', new Date(FSD_TABLE.base.date).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric', timeZone: 'America/Chicago' }));
  fill('[data-fsd-perday]', nf.format(Math.round(pr0.perDay)));
  fill('[data-fsd-rounded]', nf.format(Math.round(pr0.miles / 1000) * 1000));
  if (pr0.capped) $$('[data-fsd-capped]').forEach(function (el) { el.hidden = false; });
  var miles = $$('[data-fsd-miles]');
  var setMiles = function (n) { var t = nf.format(Math.floor(n)); miles.forEach(function (el) { el.textContent = t; }); };
  var timer = 0;
  var tick = function () { setMiles(fsdProjection(Date.now()).miles); };
  var startLive = function () { if (timer) return; tick(); timer = setInterval(tick, reduce ? 5000 : 250); };
  if (miles.length) {
    if (reduce || !('IntersectionObserver' in window)) startLive();
    else {
      setMiles(FSD_TABLE.base.miles);
      var counted = false;
      var io = new IntersectionObserver(function (es) {
        if (counted || !es.some(function (e) { return e.isIntersecting; })) return;
        counted = true; io.disconnect();
        var from = FSD_TABLE.base.miles, t0 = performance.now(), D = 1400;
        (function step(t) {
          var k = Math.min(1, (t - t0) / D), e = 1 - Math.pow(1 - k, 3), to = fsdProjection(Date.now()).miles;
          setMiles(from + (to - from) * e);
          if (k < 1) requestAnimationFrame(step); else startLive();
        })(t0);
      }, { threshold: 0.3 });
      miles.forEach(function (m) { io.observe(m); });
    }
  }

  // ---- Waitlist (Formspree, same endpoint as the live site) ----
  $$('form[data-waitlist]').forEach(function (form) {
    var wrap = form.closest('[data-waitlist-wrap]') || form.parentNode;
    var msg = wrap.querySelector('[data-waitlist-msg]'), done = wrap.querySelector('[data-waitlist-done]');
    var btn = form.querySelector('[type=submit]'), label = btn.textContent;
    form.setAttribute('novalidate', '');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = (form.email.value || '').trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { msg.textContent = 'Please enter a valid email address.'; form.email.setAttribute('aria-invalid', 'true'); form.email.focus(); return; }
      form.email.removeAttribute('aria-invalid'); msg.textContent = '';
      var ok = function () { form.hidden = true; done.hidden = false; var echo = done.querySelector('[data-waitlist-echo]'); if (echo) echo.textContent = email; done.focus(); };
      if (form._gotcha && form._gotcha.value) { ok(); return; }
      var interest = form.interest ? form.interest.value : 'Rides';
      btn.disabled = true; btn.setAttribute('aria-busy', 'true'); btn.textContent = 'Joining…';
      fetch('https://formspree.io/f/mljgwkpr', { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({ email: email, interest: interest, _subject: 'RoboRide waitlist: ' + interest, page: location.href }) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) {
          if (!r.ok) throw new Error(d && Array.isArray(d.errors) ? d.errors.map(function (x) { return x.message; }).join(' ') : '');
          ok();
        }); })
        .catch(function (err) { msg.textContent = (err && err.message ? err.message + ' ' : '') + "We couldn't add you to the waitlist just now. Please check your connection and try again."; })
        .then(function () { btn.disabled = false; btn.removeAttribute('aria-busy'); btn.textContent = label; });
    });
    var reset = wrap.querySelector('[data-waitlist-reset]');
    if (reset) reset.addEventListener('click', function (e) { e.preventDefault(); form.reset(); form.hidden = false; done.hidden = true; form.email.focus(); });
  });

  // ---- Trip planner (illustration: straight-line miles between city centers) ----
  var CITIES = { 'Bentonville': [131, 99, 36.3729, -94.2088], 'Rogers': [156, 112, 36.332, -94.1185], 'Springdale': [153, 162, 36.1867, -94.1288],
    'Fayetteville': [147, 204, 36.0626, -94.1574], 'Farmington': [120, 211, 36.042, -94.2471], 'Siloam Springs': [40, 161, 36.1881, -94.5405], 'Eureka Springs': [260, 89, 36.4011, -93.738] };
  function mi(a, b) { var R = 3958.8, r = Math.PI / 180, dA = (b[2] - a[2]) * r, dO = (b[3] - a[3]) * r, h = Math.sin(dA / 2) * Math.sin(dA / 2) + Math.cos(a[2] * r) * Math.cos(b[2] * r) * Math.sin(dO / 2) * Math.sin(dO / 2); return 2 * R * Math.asin(Math.sqrt(h)); }
  $$('[data-trip]').forEach(function (box) {
    var from = box.querySelector('[name=from]'), to = box.querySelector('[name=to]'), out = box.querySelector('[data-trip-out]');
    var svg = box.querySelector('[data-trip-map]'), mode = 'ride', NS = 'http://www.w3.org/2000/svg';
    [from, to].forEach(function (sel, k) { Object.keys(CITIES).forEach(function (c, i) { var o = doc.createElement('option'); o.value = o.textContent = c; sel.appendChild(o); }); });
    from.value = box.getAttribute('data-from') || 'Bentonville'; to.value = box.getAttribute('data-to') || 'Fayetteville';
    var line, dots = {};
    if (svg) {
      line = doc.createElementNS(NS, 'line'); line.setAttribute('class', 'trip-line'); svg.appendChild(line);
      Object.keys(CITIES).forEach(function (c) {
        var g = doc.createElementNS(NS, 'g'), p = CITIES[c], ci = doc.createElementNS(NS, 'circle'), tx = doc.createElementNS(NS, 'text');
        ci.setAttribute('cx', p[0]); ci.setAttribute('cy', p[1]); ci.setAttribute('r', 5);
        var lft = p[0] > 220 || c === 'Farmington' || c === 'Bentonville'; tx.setAttribute('x', p[0] + (lft ? -8 : 8)); tx.setAttribute('y', p[1] + 4); tx.setAttribute('text-anchor', lft ? 'end' : 'start'); tx.textContent = c;
        g.appendChild(ci); g.appendChild(tx); g.setAttribute('class', 'trip-city'); svg.appendChild(g); dots[c] = g;
      });
    }
    function draw() {
      var a = CITIES[from.value], b = CITIES[to.value], same = from.value === to.value;
      Object.keys(dots).forEach(function (c) { dots[c].classList.toggle('on', c === from.value || c === to.value); });
      if (line) { line.setAttribute('x1', a[0]); line.setAttribute('y1', a[1]); line.setAttribute('x2', b[0]); line.setAttribute('y2', b[1]); line.style.opacity = same ? 0 : 1;
        if (!reduce && line.getTotalLength) { var L = Math.hypot(b[0] - a[0], b[1] - a[1]); line.style.transition = 'none'; line.style.strokeDasharray = L; line.style.strokeDashoffset = L; line.getBoundingClientRect(); line.style.transition = 'stroke-dashoffset .7s ease'; line.style.strokeDashoffset = 0; } }
      if (same) { out.innerHTML = '<b>Pick two different cities</b> to picture a trip.'; return; }
      var d = mi(a, b);
      out.innerHTML = '<span class="trip-mi"><b>' + d.toFixed(1) + '</b> mi</span><span class="trip-copy">' +
        (mode === 'ride' ? 'straight-line from ' + from.value + ' to ' + to.value + '. That is your time back: read, rest, or take the call while the Cybercab drives.'
                         : 'straight-line for a package from ' + from.value + ' to ' + to.value + '. No driver to schedule, just a Cybercab at the curb.') + '</span>';
    }
    from.addEventListener('change', draw); to.addEventListener('change', draw);
    var sw = box.querySelector('[data-trip-swap]'); if (sw) sw.addEventListener('click', function () { var t = from.value; from.value = to.value; to.value = t; draw(); });
    $$('[data-mode]', box).forEach(function (b) { b.addEventListener('click', function () { mode = b.getAttribute('data-mode'); $$('[data-mode]', box).forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); draw(); }); });
    draw();
  });

  // ---- Reveal on scroll ----
  var rv = $$('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    var ro = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); ro.unobserve(en.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    rv.forEach(function (el) { ro.observe(el); });
  } else rv.forEach(function (el) { el.classList.add('in'); });

  // ---- Simple mobile menu: [data-menu-btn] toggles [data-menu] ----
  var mb = doc.querySelector('[data-menu-btn]'), mn = doc.querySelector('[data-menu]');
  if (mb && mn) {
    var set = function (o) { mn.classList.toggle('open', o); mb.setAttribute('aria-expanded', o); mb.setAttribute('aria-label', o ? 'Close menu' : 'Open menu'); doc.documentElement.classList.toggle('menu-open', o); };
    mb.addEventListener('click', function () { set(!mn.classList.contains('open')); if (mn.classList.contains('open')) { var a = mn.querySelector('a'); if (a) a.focus(); } });
    mn.addEventListener('click', function (e) { if (e.target.closest('a')) set(false); });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape' && mn.classList.contains('open')) { set(false); mb.focus(); } });
  }
  window.RR = { reduce: reduce };
})();
// Scene changes: body background shifts per chapter; rail shows progress through the ride.
(function () {
  var scenes = [].slice.call(document.querySelectorAll('[data-scene-set]')), links = [].slice.call(document.querySelectorAll('[data-stop]'));
  var rail = document.querySelector('.rail');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { document.body.setAttribute('data-scene', e.target.getAttribute('data-scene-set'));
        links.forEach(function (a) { a.classList.toggle('on', a.getAttribute('data-stop') === e.target.id); }); } });
    }, { rootMargin: '-45% 0px -45% 0px' });
    scenes.forEach(function (s) { io.observe(s); });
    var hero = document.querySelector('.hero');
    new IntersectionObserver(function (es) { if (es[0].isIntersecting) { document.body.setAttribute('data-scene', 'night'); links.forEach(function (a) { a.classList.remove('on'); }); } }, { rootMargin: '-45% 0px -45% 0px' }).observe(hero);
  }
  if (rail && scenes.length) {
    var first = scenes[0], last = scenes[scenes.length - 1], raf = 0;
    var upd = function () { raf = 0; var a = first.offsetTop - innerHeight / 2, b = last.offsetTop - innerHeight / 2; var p = Math.max(0, Math.min(1, (scrollY - a) / (b - a))); rail.style.setProperty('--p', p.toFixed(3)); };
    addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(upd); }, { passive: true }); upd();
  }
})();
