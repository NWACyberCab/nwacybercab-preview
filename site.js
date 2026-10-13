/* Shared behaviour for RoboRide sub-pages. */
(function () {
  document.documentElement.classList.add('js');
  // Mobile menu
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('site-nav');
  function setOpen(open) {
    if (!btn || !nav) return;
    nav.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.style.overflow = open ? 'hidden' : '';
    if (open) { var a = nav.querySelector('a'); if (a) a.focus(); } else btn.focus();
  }
  if (btn && nav) {
    btn.addEventListener('click', function () { setOpen(!nav.classList.contains('open')); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a') && nav.classList.contains('open')) setOpen(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.classList.contains('open')) setOpen(false); });
  }
  // Reveal on scroll
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else els.forEach(function (el) { el.classList.add('in'); });
  // Formspree forms: <form data-formspree action="https://formspree.io/f/...">
  document.querySelectorAll('form[data-formspree]').forEach(function (form) {
    var status = form.querySelector('.form-status'), submit = form.querySelector('[type=submit]');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.querySelector('[name=_gotcha]').value) { status.textContent = 'Thanks!'; return; }
      if (!form.reportValidity()) return;
      var data = {}; new FormData(form).forEach(function (v, k) { if (k !== '_gotcha') data[k] = v; });
      data.page = location.href;
      if (data.use_case) data._subject = 'RoboRide business interest: ' + data.use_case;
      submit.disabled = true; var label = submit.textContent; submit.textContent = 'Sending…';
      status.className = 'form-status'; status.textContent = '';
      fetch(form.action, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) {
          if (!r.ok) throw new Error(d && d.errors ? d.errors.map(function (x) { return x.message; }).join(' ') : '');
          form.reset(); status.className = 'form-status ok'; status.textContent = "Thanks! We've received your details and will be in touch.";
        }); })
        .catch(function (err) { status.className = 'form-status err'; status.textContent = (err.message ? err.message + ' ' : '') + "We couldn't send that just now. Please check your connection and try again."; })
        .finally(function () { submit.disabled = false; submit.textContent = label; });
    });
  });
})();
