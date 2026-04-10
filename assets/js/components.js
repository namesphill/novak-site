// Shared header/footer rendering for Novak Technologies bilingual site.
// Reads <body data-lang="es|en" data-page="home|products|product-dce|product-wsa|product-ppa|services|about|contact">
// and injects <div id="site-header"> and <div id="site-footer">.

(function () {
  const TRANSLATIONS = {
    es: {
      nav: {
        products: 'Productos',
        services: 'Servicios',
        about: 'Quiénes somos',
        contact: 'Contáctanos',
        switchLang: 'EN',
        switchLangLabel: 'Ver en inglés',
        openMenu: 'Abrir menú',
      },
      footer: {
        rights: 'Todos los derechos reservados.',
      },
    },
    en: {
      nav: {
        products: 'Products',
        services: 'Services',
        about: 'About',
        contact: 'Contact',
        switchLang: 'ES',
        switchLangLabel: 'View in Spanish',
        openMenu: 'Open menu',
      },
      footer: {
        rights: 'All rights reserved.',
      },
    },
  };

  // Canonical page paths per language. Keyed by page id.
  const PAGE_PATHS = {
    es: {
      home: '/es/index.html',
      services: '/es/servicios.html',
      about: '/es/quienes-somos.html',
      contact: '/es/contacto.html',
      products: '/es/productos/index.html',
      'product-dce': '/es/productos/serie-dce.html',
      'product-wsa': '/es/productos/serie-wsa.html',
      'product-ppa': '/es/productos/serie-ppa.html',
    },
    en: {
      home: '/en/index.html',
      services: '/en/services.html',
      about: '/en/about.html',
      contact: '/en/contact.html',
      products: '/en/products/index.html',
      'product-dce': '/en/products/dce-series.html',
      'product-wsa': '/en/products/wsa-series.html',
      'product-ppa': '/en/products/ppa-series.html',
    },
  };

  function otherLang(lang) {
    return lang === 'es' ? 'en' : 'es';
  }

  // Given the current page id and language, return the URL of the
  // equivalent page in the other language.
  function languageSwitchURL(lang, pageId) {
    const other = otherLang(lang);
    return PAGE_PATHS[other][pageId] || `/${other}/`;
  }

  function renderHeader(lang, pageId) {
    const t = TRANSLATIONS[lang].nav;
    const paths = PAGE_PATHS[lang];
    const langHref = languageSwitchURL(lang, pageId);

    const activeClass = (id) => (pageId === id ? ' class="active"' : '');
    // Products is "active" for both the overview page and each product detail page
    const productsActive =
      pageId === 'products' ||
      pageId === 'product-dce' ||
      pageId === 'product-wsa' ||
      pageId === 'product-ppa'
        ? ' class="active"'
        : '';

    const headerHTML = `
      <header>
        <nav class="container cluster nav">
          <a class="brand" href="${paths.home}" aria-label="Novak Technologies">
            <img src="/assets/images/logo_dark.png" alt="Novak Technologies" />
          </a>
          <button class="menu-btn" aria-expanded="false" aria-controls="primary-menu" aria-label="${t.openMenu}">
            <img src="/assets/images/hamburger.svg" alt="" />
          </button>
          <div id="primary-menu" class="cluster nav-links" role="navigation" aria-label="primary">
            <a href="${paths.products}"${productsActive}>${t.products}</a>
            <a href="${paths.services}"${activeClass('services')}>${t.services}</a>
            <a href="${paths.about}"${activeClass('about')}>${t.about}</a>
            <a href="${langHref}" aria-label="${t.switchLangLabel}">${t.switchLang}</a>
            <a class="cta" href="${paths.contact}">${t.contact}</a>
          </div>
        </nav>
      </header>
    `;

    const host = document.getElementById('site-header');
    if (host) host.outerHTML = headerHTML;
  }

  function renderFooter(lang) {
    const t = TRANSLATIONS[lang].footer;
    const year = new Date().getFullYear();
    const footerHTML = `
      <footer>
        <div class="container">© ${year} Novak Technologies. ${t.rights}</div>
      </footer>
    `;
    const host = document.getElementById('site-footer');
    if (host) host.outerHTML = footerHTML;
  }

  function init() {
    const body = document.body;
    const lang = body.getAttribute('data-lang') || 'es';
    const pageId = body.getAttribute('data-page') || 'home';

    renderHeader(lang, pageId);
    renderFooter(lang);

    // Initialize nav toggle and year (defined in main.js) AFTER header is injected.
    if (typeof window.initNavToggle === 'function') window.initNavToggle();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Expose for debugging
  window.NovakComponents = { renderHeader, renderFooter, PAGE_PATHS, languageSwitchURL };
})();
