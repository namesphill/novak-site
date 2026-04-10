// Novak Technologies — shared page behaviors.
// Exposes initNavToggle() and initYear() on window so components.js can call
// them after the header/footer have been injected into the DOM.

(function () {
  // Year injection: finds <span id="y"></span> and writes the current year.
  // Safe to call on pages that don't have the span (no-op in that case).
  function initYear() {
    var el = document.getElementById('y');
    if (el) el.textContent = new Date().getFullYear();
  }

  // Mobile nav toggle. Must be called AFTER the <header> is present in the
  // DOM — components.js renders the header dynamically, so it invokes this
  // from its own init() once the header markup has replaced the placeholder.
  function initNavToggle() {
    var header = document.querySelector('header');
    var btn = document.querySelector('.menu-btn');
    var panel = document.getElementById('primary-menu');
    if (!header || !btn || !panel) return;

    var mql = window.matchMedia('(max-width: 900px)');

    function closeMenu() {
      header.removeAttribute('data-open');
      btn.setAttribute('aria-expanded', 'false');
    }
    function openMenu() {
      header.setAttribute('data-open', 'true');
      btn.setAttribute('aria-expanded', 'true');
    }

    btn.addEventListener('click', function () {
      var open = header.getAttribute('data-open') === 'true';
      if (open) closeMenu(); else openMenu();
    });

    panel.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { if (mql.matches) closeMenu(); });
    });

    window.addEventListener('resize', function () { if (!mql.matches) closeMenu(); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenu();
    });
  }

  // Smooth scroll for in-page anchor links (e.g. href="#contacto"). Harmless
  // on pages without anchor links. Runs on DOMContentLoaded.
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var id = a.getAttribute('href');
        if (!id || id === '#') return;
        var el = document.querySelector(id);
        if (el) {
          e.preventDefault();
          el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSmoothScroll);
  } else {
    initSmoothScroll();
  }

  // Expose for components.js (header injection timing) and debugging.
  window.initNavToggle = initNavToggle;
  window.initYear = initYear;
})();
</content>
</invoke>