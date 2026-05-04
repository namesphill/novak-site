#!/usr/bin/env python3
"""Novak Technologies bilingual site smoke test.

Walks every HTML file under /es/, /en/, and the root index.html and audits:
  - html lang
  - body data-lang / data-page
  - unique title
  - meta description
  - three hreflang alternates (es, en, x-default) with absolute paths
  - #site-header / #site-footer placeholders
  - script order (main.js before components.js)
  - absolute-path <a href>, <img src>, <link href>, <script src> all resolve
    to files that exist on disk relative to the repo root.

Exit code 0 if every page passes, 1 otherwise.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from html.parser import HTMLParser

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

VALID_PAGES = {
    "home",
    "products",
    "product-dce",
    "product-wsa",
    "product-ppa",
    "services",
    "about",
    "contact",
}

VALID_LANGS = {"es", "en"}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_lang: str | None = None
        self.body_lang: str | None = None
        self.body_page: str | None = None
        self.title: str | None = None
        self._in_title = False
        self.meta_description: str | None = None
        self.hreflangs: list[tuple[str, str]] = []  # (hreflang, href)
        self.has_site_header = False
        self.has_site_footer = False
        self.a_hrefs: list[str] = []
        self.img_srcs: list[str] = []
        self.link_hrefs: list[str] = []
        self.script_srcs: list[str] = []
        # Preserve order of main.js vs components.js script tags
        self.script_src_order: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or "") for k, v in attrs}
        if tag == "html":
            self.html_lang = a.get("lang")
        elif tag == "body":
            self.body_lang = a.get("data-lang")
            self.body_page = a.get("data-page")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = a.get("name", "").lower()
            if name == "description":
                self.meta_description = a.get("content", "")
        elif tag == "link":
            rel = a.get("rel", "").lower()
            href = a.get("href", "")
            if rel == "alternate" and a.get("hreflang"):
                self.hreflangs.append((a.get("hreflang", ""), href))
            if href:
                self.link_hrefs.append(href)
        elif tag == "div":
            id_ = a.get("id", "")
            if id_ == "site-header":
                self.has_site_header = True
            elif id_ == "site-footer":
                self.has_site_footer = True
        elif tag == "a":
            href = a.get("href", "")
            if href:
                self.a_hrefs.append(href)
        elif tag == "img":
            src = a.get("src", "")
            if src:
                self.img_srcs.append(src)
        elif tag == "script":
            src = a.get("src", "")
            if src:
                self.script_srcs.append(src)
                self.script_src_order.append(src)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title = (self.title or "") + data


def collect_html_files() -> list[str]:
    files: list[str] = []
    for top in ("es", "en"):
        root = os.path.join(REPO_ROOT, top)
        for dirpath, _dirnames, filenames in os.walk(root):
            for name in filenames:
                if name.endswith(".html"):
                    files.append(os.path.join(dirpath, name))
    files.append(os.path.join(REPO_ROOT, "index.html"))
    files.sort()
    return files


def resolve_abs_path(abs_url: str) -> str:
    """Map a '/foo/bar' URL into a filesystem path under REPO_ROOT."""
    # strip fragment/query
    path = abs_url.split("#", 1)[0].split("?", 1)[0]
    if not path.startswith("/"):
        return ""
    fs = os.path.join(REPO_ROOT, path.lstrip("/"))
    return fs


def is_external_or_anchor(href: str) -> bool:
    if not href:
        return True
    if href.startswith("#"):
        return True
    low = href.lower()
    return low.startswith(("mailto:", "tel:", "http://", "https://", "javascript:", "data:"))


def check_file(path: str, titles_seen: dict[str, list[str]]) -> list[str]:
    errors: list[str] = []
    rel = os.path.relpath(path, REPO_ROOT)
    is_root_index = (rel == "index.html")

    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    p = PageParser()
    p.feed(src)

    # 1. html lang
    if p.html_lang not in VALID_LANGS:
        errors.append(f"invalid or missing <html lang>: {p.html_lang!r}")

    if is_root_index:
        # Root has no body data-lang/page, no placeholders, no scripts, no hreflang script rules.
        # But it MUST have the meta refresh. We still check title + description + hreflangs.
        if not p.title:
            errors.append("missing <title>")
        if not p.meta_description:
            errors.append("missing <meta name=description>")
        # hreflang check is still meaningful for root index
        _check_hreflangs(p.hreflangs, errors)
        # Check that link/script/img absolute paths that exist resolve
        _check_asset_refs(p, errors, check_anchors=False)
        # Track title uniqueness
        if p.title:
            titles_seen.setdefault(p.title.strip(), []).append(rel)
        return errors

    # 2. body data-lang / data-page
    if p.body_lang not in VALID_LANGS:
        errors.append(f"invalid or missing <body data-lang>: {p.body_lang!r}")
    if p.body_page not in VALID_PAGES:
        errors.append(
            f"invalid or missing <body data-page>: {p.body_page!r} "
            f"(valid: {sorted(VALID_PAGES)})"
        )
    # Consistency: <html lang> should match <body data-lang>
    if p.html_lang and p.body_lang and p.html_lang != p.body_lang:
        errors.append(
            f"<html lang={p.html_lang!r}> does not match <body data-lang={p.body_lang!r}>"
        )

    # 3. title
    if not p.title or not p.title.strip():
        errors.append("missing <title>")
    else:
        titles_seen.setdefault(p.title.strip(), []).append(rel)

    # 4. meta description
    if not p.meta_description:
        errors.append("missing <meta name=description>")

    # 5. hreflang alternates
    _check_hreflangs(p.hreflangs, errors)

    # 6. site-header / site-footer placeholders
    if not p.has_site_header:
        errors.append("missing <div id=site-header>")
    if not p.has_site_footer:
        errors.append("missing <div id=site-footer>")

    # 7. Script order: main.js before components.js
    script_basenames = [os.path.basename(s) for s in p.script_src_order]
    if "main.js" not in script_basenames:
        errors.append("missing <script src=.../main.js>")
    if "components.js" not in script_basenames:
        errors.append("missing <script src=.../components.js>")
    if "main.js" in script_basenames and "components.js" in script_basenames:
        if script_basenames.index("main.js") > script_basenames.index("components.js"):
            errors.append("main.js must appear BEFORE components.js in script order")

    # 8. asset resolution
    _check_asset_refs(p, errors, check_anchors=True)

    return errors


def _check_hreflangs(hreflangs: list[tuple[str, str]], errors: list[str]) -> None:
    langs = {h for h, _ in hreflangs}
    for required in ("es", "en", "x-default"):
        if required not in langs:
            errors.append(f"missing hreflang={required!r}")
    for h, href in hreflangs:
        if not href.startswith("/"):
            errors.append(
                f"hreflang={h!r} must use an absolute path starting with '/': {href!r}"
            )


def _check_asset_refs(p: PageParser, errors: list[str], check_anchors: bool) -> None:
    # <a href>
    if check_anchors:
        for href in p.a_hrefs:
            if is_external_or_anchor(href):
                continue
            if href.startswith("/"):
                fs = resolve_abs_path(href)
                if not os.path.isfile(fs):
                    errors.append(f"broken <a href>: {href} (expected {fs})")
    # <img src>
    for src in p.img_srcs:
        if is_external_or_anchor(src):
            continue
        if src.startswith("/"):
            fs = resolve_abs_path(src)
            if not os.path.isfile(fs):
                errors.append(f"broken <img src>: {src} (expected {fs})")
    # <link href>
    for href in p.link_hrefs:
        if is_external_or_anchor(href):
            continue
        if href.startswith("/"):
            fs = resolve_abs_path(href)
            if not os.path.isfile(fs):
                errors.append(f"broken <link href>: {href} (expected {fs})")
    # <script src>
    for src in p.script_srcs:
        if is_external_or_anchor(src):
            continue
        if src.startswith("/"):
            fs = resolve_abs_path(src)
            if not os.path.isfile(fs):
                errors.append(f"broken <script src>: {src} (expected {fs})")


# Telltale strings that should never appear in a hand-written source file.
# These are tool-call artifacts that have leaked into file contents in the
# past (specifically Agent A wrote the literal closing tags of its own
# Write tool-call into styles.css, main.js, and components.js). Scanning for
# these catches the regression even though the resulting JS happens to be
# parseable-looking at a glance.
ARTIFACT_MARKERS = (
    "</invoke>",
    "</content>",
    "<function_calls>",
    "</function_calls>",
)

# Text files we scan for tool artifacts. Binary assets (images, PDFs) are
# skipped; so is legacy-site/ (archived third-party content).
ARTIFACT_SCAN_EXTENSIONS = {".html", ".htm", ".css", ".js", ".json", ".md"}

# Skip these directories entirely when scanning for artifacts.
ARTIFACT_SCAN_SKIP_DIRS = {".git", "legacy-site", "node_modules"}


def scan_for_tool_artifacts() -> list[str]:
    """Return a list of 'path: marker' errors for any source file containing
    a tool-call artifact marker."""
    errors: list[str] = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        # prune skipped directories in-place so os.walk doesn't descend into them
        dirnames[:] = [d for d in dirnames if d not in ARTIFACT_SCAN_SKIP_DIRS]
        for name in filenames:
            ext = os.path.splitext(name)[1].lower()
            if ext not in ARTIFACT_SCAN_EXTENSIONS:
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, REPO_ROOT)
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except OSError as e:
                errors.append(f"{rel}: could not read ({e})")
                continue
            for marker in ARTIFACT_MARKERS:
                if marker in content:
                    errors.append(f"{rel}: contains tool artifact {marker!r}")
    return errors


def check_js_syntax() -> list[str]:
    """Run `node -c` on every JS file under /assets/js/. Returns errors.
    Silently skips the check if `node` is not available on PATH (e.g. in a
    minimal CI environment) — scan_for_tool_artifacts() will still catch the
    specific artifact class that motivated this check."""
    errors: list[str] = []
    node = shutil.which("node")
    js_dir = os.path.join(REPO_ROOT, "assets", "js")
    if not os.path.isdir(js_dir):
        return errors
    js_files = sorted(
        os.path.join(js_dir, n) for n in os.listdir(js_dir) if n.endswith(".js")
    )
    if not js_files:
        return errors
    if not node:
        print("  (node not on PATH — skipping JS syntax check; artifact scan still runs)")
        return errors
    for path in js_files:
        rel = os.path.relpath(path, REPO_ROOT)
        result = subprocess.run(
            [node, "-c", path], capture_output=True, text=True
        )
        if result.returncode != 0:
            errors.append(f"{rel}: node -c failed\n    {result.stderr.strip()}")
    return errors


def main() -> int:
    files = collect_html_files()
    titles_seen: dict[str, list[str]] = {}
    file_results: list[tuple[str, list[str]]] = []

    print(f"Novak Technologies smoke test")
    print(f"Repo root: {REPO_ROOT}")
    print(f"Auditing {len(files)} HTML file(s)")
    print("=" * 72)

    for path in files:
        rel = os.path.relpath(path, REPO_ROOT)
        errors = check_file(path, titles_seen)
        file_results.append((rel, errors))
        if errors:
            print(f"FAIL  {rel}")
            for e in errors:
                print(f"        - {e}")
        else:
            print(f"PASS  {rel}")

    # Duplicate title detection (after all files parsed)
    dup_errors: list[str] = []
    for title, paths in titles_seen.items():
        if len(paths) > 1:
            dup_errors.append(
                f"duplicate <title> {title!r} used by: {', '.join(paths)}"
            )

    print("=" * 72)
    total = len(file_results)
    failed = sum(1 for _, e in file_results if e)
    passed = total - failed
    print(f"Per-file: {passed} passed, {failed} failed, {total} total")

    if dup_errors:
        print("Duplicate titles across files:")
        for e in dup_errors:
            print(f"  - {e}")
    else:
        print("All page titles are unique.")

    # Scan for tool-call artifacts that leaked into source files.
    print("-" * 72)
    print("Scanning for tool-call artifacts in source files...")
    artifact_errors = scan_for_tool_artifacts()
    if artifact_errors:
        print("Tool artifact scan FAILED:")
        for e in artifact_errors:
            print(f"  - {e}")
    else:
        print("No tool-call artifacts found.")

    # JS syntax check via `node -c` (skipped gracefully if node is absent).
    print("-" * 72)
    print("Checking JS syntax with `node -c`...")
    js_errors = check_js_syntax()
    if js_errors:
        print("JS syntax check FAILED:")
        for e in js_errors:
            print(f"  - {e}")
    else:
        print("JS syntax check passed.")

    print("=" * 72)
    if failed == 0 and not dup_errors and not artifact_errors and not js_errors:
        print("RESULT: GREEN")
        return 0
    print("RESULT: RED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
