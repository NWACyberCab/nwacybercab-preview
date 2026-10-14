/* Shared behaviour for RoboRide sub-pages. */
(function () {
  document.documentElement.classList.add('js');
  // Mobile menu: drawer under the header + backdrop; closes on link tap, backdrop tap, Esc
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('site-nav'), header = document.querySelector('.site-header'), backdrop = null;
  var HAMB = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#e8e4dc" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg>';
  var CLOSE = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#e8e4dc" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';
  function setHH() { if (header) document.documentElement.style.setProperty('--hh', header.offsetHeight + 'px'); }
  function setOpen(open, keepFocus) {
    if (!btn || !nav) return;
    setHH();
    nav.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    btn.innerHTML = open ? CLOSE : HAMB;
    document.documentElement.classList.toggle('menu-open', open);
    if (open) {
      if (!backdrop) { backdrop = document.createElement('div'); backdrop.className = 'nav-backdrop'; backdrop.addEventListener('click', function () { setOpen(false); }); }
      document.body.appendChild(backdrop);
      var a = nav.querySelector('a'); if (a) a.focus();
    } else {
      if (backdrop && backdrop.parentNode) backdrop.parentNode.removeChild(backdrop);
      if (!keepFocus) btn.focus();
    }
  }
  if (btn && nav) {
    btn.addEventListener('click', function () { setOpen(!nav.classList.contains('open')); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a') && nav.classList.contains('open')) setOpen(false, true); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.classList.contains('open')) setOpen(false); });
    window.addEventListener('resize', function () { setHH(); if (window.innerWidth > 1100 && nav.classList.contains('open')) setOpen(false, true); });
  }
  // Reveal on scroll
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else els.forEach(function (el) { el.classList.add('in'); });
  // Formspree forms: <form data-formspree action="https://formspree.io/f/...">
  function msgFor(el) {
    if (el.validity.valueMissing) return (el.dataset.label || 'This field') + ' is required.';
    if (el.validity.typeMismatch && el.type === 'email') return 'Please enter a valid email address, like name@company.com.';
    if (el.validity.tooLong) return 'Please keep this under ' + el.maxLength + ' characters.';
    return el.validationMessage || '';
  }
  function check(el, show) {
    if (!el.willValidate || el.name === '_gotcha') return true;
    var ok = el.checkValidity(), id = el.id + '-err', box = document.getElementById(id);
    if (!box) { box = document.createElement('span'); box.id = id; box.className = 'field-error'; box.setAttribute('aria-live', 'polite'); el.insertAdjacentElement('afterend', box); var d = el.getAttribute('aria-describedby'); el.setAttribute('aria-describedby', d ? d + ' ' + id : id); }
    if (show) { el.setAttribute('aria-invalid', ok ? 'false' : 'true'); box.textContent = ok ? '' : msgFor(el); el.classList.toggle('valid', ok && el.value !== '' && el.tagName === 'INPUT'); }
    return ok;
  }
  function validateAll(form) {
    var first = null;
    form.querySelectorAll('input,select,textarea').forEach(function (el) { if (!check(el, true) && !first) first = el; });
    if (first) first.focus();
    return !first;
  }
  document.querySelectorAll('form[data-formspree]').forEach(function (form) {
    form.setAttribute('novalidate', '');
    form.querySelectorAll('input,select,textarea').forEach(function (el) {
      var l = form.querySelector('label[for="' + el.id + '"]'); if (l) el.dataset.label = l.childNodes[0].textContent.trim();
      el.addEventListener('blur', function () { if (el.value !== '' || el.getAttribute('aria-invalid')) check(el, true); });
      el.addEventListener('input', function () { if (el.getAttribute('aria-invalid') === 'true') check(el, true); });
    });
    var status = form.querySelector('.form-status'), submit = form.querySelector('[type=submit]');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.querySelector('[name=_gotcha]').value) { status.textContent = 'Thanks!'; return; }
      if (!validateAll(form)) return;
      var data = {}; new FormData(form).forEach(function (v, k) { if (k !== '_gotcha') data[k] = v; });
      data.page = location.href;
      if (data.use_case) data._subject = 'RoboRide business interest: ' + data.use_case;
      submit.disabled = true; var label = submit.textContent; submit.textContent = 'Sending…';
      status.className = 'form-status'; status.textContent = '';
      fetch(form.action, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) {
          if (!r.ok) throw new Error(d && d.errors ? d.errors.map(function (x) { return x.message; }).join(' ') : '');
          form.reset(); form.querySelectorAll('.valid').forEach(function (x) { x.classList.remove('valid'); }); form.querySelectorAll('[aria-invalid]').forEach(function (x) { x.removeAttribute('aria-invalid'); });
          status.className = 'form-status ok'; status.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg><span><strong>Thanks!</strong> We’ve received your details and will be in touch.</span>'; status.setAttribute('tabindex', '-1'); status.focus();
        }); })
        .catch(function (err) { status.className = 'form-status err'; status.textContent = (err.message ? err.message + ' ' : '') + "We couldn't send that just now. Please check your connection and try again."; })
        .finally(function () { submit.disabled = false; submit.textContent = label; });
    });
  });
  // Share: native share sheet where available, otherwise copy the link
  document.querySelectorAll('[data-share]').forEach(function (b) {
    var st = b.parentNode.querySelector('.share-status');
    b.addEventListener('click', function () {
      var url = location.href.split('#')[0], title = b.getAttribute('data-title') || document.title;
      if (navigator.share) { navigator.share({ title: title, url: url }).catch(function () {}); return; }
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(function () { if (st) st.textContent = 'Link copied.'; }, function () { if (st) st.textContent = url; });
      else if (st) st.textContent = url;
    });
  });
  // Back to top (mobile)
  var tt = document.querySelector('.to-top');
  if (tt) {
    tt.hidden = false;
    var onS = function () { tt.classList.toggle('show', window.scrollY > window.innerHeight * 1.2); };
    window.addEventListener('scroll', onS, { passive: true }); onS();
    tt.addEventListener('click', function (e) { e.preventDefault(); window.scrollTo({ top: 0, behavior: (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) ? 'auto' : 'smooth' }); var m = document.getElementById('main'); if (m) { m.setAttribute('tabindex', '-1'); m.focus({ preventScroll: true }); } });
  }
})();
