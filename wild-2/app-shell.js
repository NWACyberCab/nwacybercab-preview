// Theme toggle: dark/light, saved in localStorage (initial value set inline in <head>).
(function () {
  var d = document.documentElement;
  function label() { var t = d.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
    [].forEach.call(document.querySelectorAll('[data-theme-toggle]'), function (b) { b.setAttribute('aria-label', t === 'light' ? 'Switch to dark theme' : 'Switch to light theme'); b.title = b.getAttribute('aria-label'); }); }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-theme-toggle]'); if (!b) return;
    var t = d.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    d.setAttribute('data-theme', t); try { localStorage.setItem('rr-theme', t); } catch (x) {}
    label();
  });
  label();
})();
