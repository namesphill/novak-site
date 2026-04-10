# Novak Technologies — Bilingual Site Restructuring Plan

## Context

Novak Technologies is a Mexico/Texas-based B2B manufacturer of industrial power supplies and rectifiers (Serie DCe, WSa, PPa), used in galvanoplating, semiconductors, MEMS, and related processes. The site's purpose is **informational and publication-oriented** — lead generation, product showcasing, and credibility — not e-commerce.

**The current state:** a single `index.html` (plain HTML/CSS/vanilla JS, no framework, no build tool) where everything lives on one page via anchor-based navigation. The header nav links are anchor scrolls, the EN/ES toggle is a dummy link, and only Serie DCe has a (placeholder Lorem ipsum) detail section. WSa and PPa detail sections don't exist. No data sheets are hosted.

**The client's feedback** (Ana Laura Diaz, 2026-04-09) triggered this work:
- The header feels empty — links should go to real pages, not just scroll
- Everything is on the landing page instead of being separate pages
- Serie DCe copy needs to be replaced (client provided new copy)
- Data sheet for DCe needs to be uploaded
- Pages for Serie WSa and Serie PPa don't exist — they should match DCe's hierarchy, each with its own data sheet

**Additional scope from Felipe:**
- Once the Spanish site is structured correctly, mirror the entire site in English
- Root `/` should redirect to `/en/` (English as default home)
- Routes: `/es/*` for Spanish, `/en/*` for English
- **All code, filenames, variables, classes stay in English** — only copy is localized
- Legacy previous-site ZIP (exported from cPanel) will be committed to the repo as a reference for product copy, images, and data sheet content — it's not yet in the repo

**Intended outcome:** a clean, maintainable, plain-HTML multi-page site with 7 pages per language (14 total), a shared layout, real navigation, client-approved product content, placeholder data sheet buttons, and a root redirect to `/en/`.

---

## Confirmed Decisions (from client + debate agent)

| # | Question | Decision |
|---|---|---|
| 1 | Data sheet PDFs | **DCe: use the real PDF.** `legacy-site/es/DCeSeries.pdf` and `legacy-site/en/DCeSeries.pdf` are valid 4-page data sheets (REF2009A 26NOV14). Copy them into `/assets/docs/` and wire up the button. **WSa/PPa: placeholder buttons** with `title="Próximamente"` / `title="Coming soon"` — no legacy data sheets exist for those series. |
| 2 | Product images for WSa/PPa | **Reuse `dce.png`** across all three product pages until client provides distinct images. |
| 3 | Contact form placement | **Dedicated contact page only.** Home page shows a prominent CTA section (headline + benefit + button) linking to `/es/contacto.html` or `/en/contact.html`. Single source of truth for the form; lighter home page; aligns with the client's "separate pages" directive. Also include `tel:` and `mailto:` fallbacks on the home CTA. |
| 4 | Products nav | **Products overview page** (`/es/productos/index.html`, `/en/products/index.html`) linked from the header. The overview shows all 3 series as cards; each card links to its detail page. |
| 5 | Hosting platform | **Stay on existing cPanel.** The previous site is already there, email hosting (@novaktech.net) almost certainly uses the same MX records, and migrating DNS risks breaking business email. cPanel `.htaccess` handles 301 redirects cleanly, supports PHP for the contact form backend later, and SSL is free via AutoSSL on most providers. Cloudflare Pages is the escape hatch if the team later outgrows cPanel. |
| 6 | WSa/PPa copy | **Adapt the DCe copy** — swap "DCe" for "WSa" / "PPa" in the opening line; otherwise identical per client's "adaptenlo pls" instruction. |

---

## Legacy Site Mining (from `legacy-site/`)

The cPanel ZIP of Novak's previous website has been extracted and committed under `legacy-site/`. The old site is FrontPage-era HTML (circa mid-2000s, last updated 2014 based on the PDF timestamp), but it contains several assets and content blocks worth reusing:

### Assets to reuse
- **`legacy-site/es/DCeSeries.pdf`** (4 pages, ~334 KB) — real DCe data sheet in Spanish. Copy to `assets/docs/ficha-tecnica-dce.pdf`.
- **`legacy-site/en/DCeSeries.pdf`** (4 pages, ~335 KB) — English version. Copy to `assets/docs/dce-datasheet.pdf`.
- **`legacy-site/es/images/logos.jpg`** — collage of customer logos (433×274px) — usable as-is for a "Nuestros clientes" strip on the home or about page.
- **`legacy-site/es/images/foto.about.jpg`, `foto.home.jpg`, `foto.products.jpg`, `foto.services.jpg`** — legacy stock photos. Lower priority: the current site already has better photos (`bg.jpg`, `equipo.png`, `dce.png`). Use only if needed as fallbacks.

### Content blocks to mine
- **General features bullet list** (from `legacy-site/es/products.htm` lines 112–130 and `legacy-site/en/products.htm` lines 108–120). Reusable verbatim on each product detail page under a "Características generales" / "General Characteristics" heading:
  - Ambientes rudos — cámara electrónica sellada
  - Alta eficiencia, compactas y ligeras
  - Conmutación suave con control de fase
  - Controles precisos de potencia
  - Interfaz de usuario amigable (menús + pantalla alfanumérica)
  - Interfaces para automatización (digital/analógico, PLC o computadora)
  - Operación controlada por microprocesadores
  - Control total de voltios y amperes
  - Regulación contra variaciones de línea (VAC) y carga
  - Totalizador Amp-Horas, temporizadores programables, alarmas
  - Barras de cobre para conexiones
  - Garantía de 2 años

- **About copy** (from `legacy-site/en/about.htm`) — richer and slightly different from what's on the current site. Mentions "OEM power conversion design and manufacturing industry" and "Electrochemical, Electromachining, MEMS (Nanotechnology), Semiconductor and Specialty Pulse Power areas" + "design and manufacturing private label services". Worth merging with the current about text. ⚠ Has typos ("microprocesor", "enviroment", "commited") that should be fixed in the new site.

- **Services copy** mentions past clients like Motorola, Philips, Flextronics, Visteon — usable as social proof in the services page intro.

- **Customer list** (from `legacy-site/es/productusers.htm`, ~33 names) — includes recognizable names: Aerojet, Avery Dennison, AVX Corporation, General Dynamics, Motorola, Philips, Rohm Haas Electronic Materials, Semitool, Novellus Systems, Vishay Thin Films, Visteon, Custom Microwave, CIDETEQ, CIMAV, and more. **Use this for a new "Nuestros clientes" / "Our customers" section on the home page or about page** — strong social proof for a B2B industrial site.

### ⚠ Critical naming inconsistency flagged for client

The **legacy site and the current site have WSa and PPa swapped**:

| | Current live site | Legacy site (EN) |
|---|---|---|
| **WSa** | DC pulsante (pulsing) | DC Pulse, Pulse Reverse, wave sequencing |
| **PPa** | Impulsos inversos + secuenciación de ondas | DC Pulsing |

In other words, what the legacy site called "PPa = pulsing" is what the current site calls "WSa = pulsing", and vice versa. Either:
1. The current site got the two descriptions swapped by mistake when it was built
2. Novak deliberately renamed / rebranded the two product lines (swapped letter codes)

**Action:** flag to the client (Ana Laura) to confirm which is correct before we ship any real product copy. **For this implementation pass**, we will **preserve the current live site's naming** (WSa = pulsing, PPa = pulse reverse + wave sequencing), since that's what the client has been reviewing and gave feedback on. This note goes into the implementation commit message so it's not lost.

### ⚠ DCe amperage range discrepancy

The client-provided copy says "**fuentes DCe desde 10A hasta 2,000A**", but the DCe data sheet model table only goes up to **DCe1000-12-4 (1000A)**. Either the data sheet is outdated or the 2,000A figure is aspirational/misspoken. Preserving the client's copy as-is for now and flagging to confirm — the PDF is from 2014 and could well be outdated.

---

## Architecture: Plain Multi-Page HTML

**Decision:** stay with plain HTML — no framework, no SSG, no build step.

**Rationale:**
- The team is comfortable with plain HTML
- The site is small (~14 files total)
- Zero build step = simple cPanel deployment (drag into File Manager or SFTP)
- Duplication of header/footer is avoided via a small JS component-injection layer

**Shared resources (new):**
- `/assets/css/styles.css` — extracted from the current inline `<style>` block
- `/assets/js/main.js` — nav toggle, smooth scroll, year injection (extracted from current inline scripts)
- `/assets/js/components.js` — `renderHeader(lang, activePage)` and `renderFooter(lang)` functions that inject the same header/footer HTML into every page. Takes `lang` and `activePage` parameters so the nav renders language-appropriate labels, active-state styling, and the correct language-switcher target URL.

---

## Directory Structure

```
novak-site/
├── index.html                          # Root redirect → /en/ (meta-refresh fallback; .htaccess does 301 on the server)
│
├── .htaccess                           # (created at deploy time on server, not now) — 301 redirect rule for /
│
├── assets/
│   ├── css/
│   │   └── styles.css                  # Shared stylesheet
│   ├── js/
│   │   ├── main.js                     # Nav toggle, smooth scroll, year
│   │   └── components.js               # Header/footer injection
│   ├── images/                         # Renamed subfolder (currently flat in /assets/)
│   │   ├── logo.png
│   │   ├── logo_dark.png
│   │   ├── bg.jpg
│   │   ├── dce.png
│   │   ├── equipo.png
│   │   ├── hamburger.svg
│   │   ├── arrow-down-90.png
│   │   └── fav.png, fav_dark.png
│   └── docs/                           # Empty for now; placeholder buttons don't link here yet
│
├── es/                                 # === SPANISH SITE ===
│   ├── index.html                      # Home (landing)
│   ├── servicios.html                  # Services
│   ├── quienes-somos.html              # About
│   ├── contacto.html                   # Contact (form)
│   └── productos/
│       ├── index.html                  # Products overview (all 3 series as cards)
│       ├── serie-dce.html              # Serie DCe detail
│       ├── serie-wsa.html              # Serie WSa detail
│       └── serie-ppa.html              # Serie PPa detail
│
├── en/                                 # === ENGLISH SITE ===
│   ├── index.html                      # Home
│   ├── services.html                   # Services
│   ├── about.html                      # About
│   ├── contact.html                    # Contact
│   └── products/
│       ├── index.html                  # Products overview
│       ├── dce-series.html             # DCe Series detail
│       ├── wsa-series.html             # WSa Series detail
│       └── ppa-series.html             # PPa Series detail
│
└── legacy-site/                        # (to be committed separately by user) — old site as reference
```

---

## Phased Implementation

### Phase 0 — Legacy content available ✅

The cPanel ZIP has been extracted and committed under `legacy-site/`. Key reusable assets are inventoried in the **Legacy Site Mining** section above. Phase 1 can start.

### Phase 1 — Scaffold shared resources

- Extract inline CSS from `index.html` → `assets/css/styles.css`
- Extract inline JS → `assets/js/main.js`
- Create `assets/js/components.js` with `renderHeader(lang, activePage)` and `renderFooter(lang)` — a dictionary of nav labels per language, active-link highlighting, language-switcher link computed from the current page's data attribute
- Create `assets/images/` subfolder; move existing image files into it; update all paths
- Create `assets/docs/` and copy the legacy DCe data sheets into it:
  - `legacy-site/es/DCeSeries.pdf` → `assets/docs/ficha-tecnica-dce.pdf`
  - `legacy-site/en/DCeSeries.pdf` → `assets/docs/dce-datasheet.pdf`
- Build a single page template boilerplate that every page will start from: doctype, meta, CSS link, `<div id="header"></div>`, `<main>` with page content, `<div id="footer"></div>`, JS scripts at the bottom with `renderHeader('es', 'productos')` etc.

### Phase 2 — Spanish site (`/es/`)

Build the 7 Spanish pages using the template. Content per page:

**`/es/index.html` (home)**
- Hero (unchanged)
- Company strap (unchanged)
- Services overview — condensed 3-card block + "Ver todos los servicios" link to `/es/servicios.html`
- Products overview — 3-card block; "Ver más" links now go to `/es/productos/serie-dce.html`, etc.
- **Contact CTA section** (new) — headline + short benefit line + button → `/es/contacto.html` + `tel:` and `mailto:` fallbacks
- About teaser + link to `/es/quienes-somos.html`
- Remove the inline `#detalle-dce` section entirely

**`/es/servicios.html`** — full 3-card services content (current `#servicios` section content)

**`/es/quienes-somos.html`** — full about content (current `#quienes` section content)

**`/es/contacto.html`** — full contact info (Chihuahua + El Paso addresses, phones, emails) + the form (currently a demo with `alert()`; leave as demo for now — functional backend is out of scope for this pass)

**`/es/productos/index.html`** — products overview: short intro paragraph + 3 cards for DCe/WSa/PPa + "Ver más" links

**`/es/productos/serie-dce.html`** — the Serie DCe page. Client-provided copy (with minor polish — "Ethernet" capitalized, comma clarity):

> Nuestra serie DCe está compuesta de fuentes de poder industriales compactas y de alto desempeño, diseñadas para optimizar espacio y reducir costos de operación.
>
> Su gabinete sellado y resistente a la corrosión garantiza una operación confiable incluso en entornos industriales exigentes. Ofrece salida de voltaje y corriente ajustables, y una alta eficiencia. Incorpora rampas de arranque programables y un proceso manual configurable de hasta cuatro pasos para un control preciso del proceso.
>
> Nuestra especialidad está en fuentes DCe desde 10A hasta 2,000A, con opción de tener interfaz digital RS485 con aislamiento óptico, controlador de amperes-hora, control remoto y Ethernet de acuerdo a las necesidades del cliente.

Page includes: breadcrumb back to products overview, sidebar cross-links to WSa and PPa, `dce.png` image, the client copy above, a "Características generales" section with the bullet list mined from `legacy-site/es/products.htm`, and two CTA buttons — "Descarga la ficha técnica" → `/assets/docs/ficha-tecnica-dce.pdf` (real PDF, not a placeholder) and "Obtén una cotización" → `/es/contacto.html`.

**`/es/productos/serie-wsa.html`** — same structure as DCe. Opening line adapted: "Nuestra serie WSa está compuesta de..." — rest of the copy identical. Same `dce.png` image. Same placeholder buttons.

**`/es/productos/serie-ppa.html`** — same structure, "Nuestra serie PPa está compuesta de..." — rest identical. Same image. Same placeholder buttons.

### Phase 3 — English site (`/en/`)

Mirror every Spanish page with translated copy. `<html lang="en">`, translated titles, meta descriptions, nav labels, body content, form labels (Nombre→Name, Apellido→Last Name, Empresa→Company, Correo electrónico→Email, Mensaje→Message), button text, etc.

Each page includes:
- `<link rel="alternate" hreflang="es" href="/es/...">` pointing to its Spanish counterpart
- `<link rel="alternate" hreflang="en" href="/en/...">` self-reference
- `<link rel="alternate" hreflang="x-default" href="/en/...">`

The Spanish pages get the mirror-image `hreflang` tags.

The Serie DCe/WSa/PPa English copy is a direct translation of the adapted Spanish copy.

### Phase 4 — Wiring, redirect, polish

- Root `index.html` — simple HTML page with `<meta http-equiv="refresh" content="0; url=/en/">` + a `<script>window.location.replace('/en/')</script>` + a `<noscript>` link. Server-side 301 via `.htaccess` is documented for the client to apply on cPanel (one-liner: `RewriteEngine On` + `RewriteRule ^$ /en/ [R=301,L]`) but the `.htaccess` file itself is not committed now — it lives on the server.
- Language switcher — in `components.js`, compute the switcher href from `activePage` + a lookup table mapping each Spanish page to its English equivalent (and vice versa)
- Active nav state — add a CSS class to the current page's nav link in `renderHeader()`
- SEO basics — unique `<title>` and `<meta name="description">` per page
- Favicon — wire `/assets/images/fav.png` into every page's `<head>`
- Smoke-test every link on every page (no 404s, language switcher works both directions, header renders on every page)

---

## Sub-Agent Parallelization (for implementation)

| Agent | Scope | Depends on |
|---|---|---|
| **A: Scaffold** | Phase 1 — extract CSS/JS, build `components.js`, reorganize assets, create page template | none (runs first) |
| **B: Spanish site** | Phase 2 — build all 7 Spanish pages | A |
| **C: English site** | Phase 3 — build all 7 English pages (translate from Spanish) | A (can run parallel to B once template is ready) |
| **D: Wiring & polish** | Phase 4 — root redirect, hreflang, language switcher logic, active states, favicon, smoke test | B + C |

B and C run **in parallel** after A completes.

---

## Critical Files

**To be created:**
- `assets/css/styles.css`
- `assets/js/main.js`
- `assets/js/components.js`
- `index.html` (replaced — becomes root redirect)
- `es/index.html`
- `es/servicios.html`
- `es/quienes-somos.html`
- `es/contacto.html`
- `es/productos/index.html`
- `es/productos/serie-dce.html`
- `es/productos/serie-wsa.html`
- `es/productos/serie-ppa.html`
- `en/index.html`
- `en/services.html`
- `en/about.html`
- `en/contact.html`
- `en/products/index.html`
- `en/products/dce-series.html`
- `en/products/wsa-series.html`
- `en/products/ppa-series.html`

**To be reorganized:**
- `assets/*.png|jpg|svg` → `assets/images/`

**To be replaced:**
- `index.html` (current monolithic file → thin root redirect)

---

## Verification

After implementation, verify end-to-end:

1. **Smoke test locally** — serve the site root via `python3 -m http.server 8000` (or any static server); visit `http://localhost:8000/` and confirm it redirects to `/en/`.
2. **Link crawl** — walk every nav link on every page (both languages) and confirm no 404s. Confirm "Productos" → overview → individual series detail pages.
3. **Language switcher** — from every page, click EN/ES and confirm it lands on the correct counterpart (e.g., `/es/productos/serie-dce.html` ↔ `/en/products/dce-series.html`).
4. **Header consistency** — confirm the header renders identically on every page (it's injected via `components.js`), with the correct active-page highlight.
5. **Mobile menu** — resize to ≤900px on every page type and confirm hamburger opens/closes, escape key works, clicking a link closes the menu.
6. **Content audit** — on each product page, confirm the client-approved copy appears verbatim (DCe exact, WSa/PPa with adapted opening line).
7. **Placeholder buttons** — confirm data sheet buttons have `title="Próximamente"` / `title="Coming soon"` and don't 404.
8. **SEO tags** — view-source each page and confirm unique `<title>`, `<meta description>`, and correct `<link rel="alternate" hreflang>` pairs.
9. **Validate HTML** — optional: run the W3C validator on a couple of representative pages.

---

## Open Items to Resolve Before or During Implementation

1. **Legacy ZIP needs to be committed** by the user so content/images/data sheet source can be mined. This blocks eventually replacing the placeholders with real data sheet PDFs and possibly richer product copy, but **does NOT block the structural work in Phases 1–4** — we can proceed with placeholders now and backfill later.
2. **Contact form backend** is out of scope for this pass — the form stays as a demo (`alert()` on submit). A later task can add a PHP mailer endpoint on cPanel.
3. **Real data sheet PDFs** — placeholders only now; real files land in `/assets/docs/` in a follow-up.
4. **Distinct product images** for WSa/PPa — reuse `dce.png` now; swap later when client provides them.
