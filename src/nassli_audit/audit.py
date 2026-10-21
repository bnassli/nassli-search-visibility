"""Small, dependency-free, intentionally bounded technical SEO auditor.

This is a diagnostic tool, not an indexer, rank tracker or production deployment system.
It fetches only the exact configured pages, host variants and the sitemaps declared in robots.txt.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
import argparse
import json
import re
import time
import xml.etree.ElementTree as ET

# Titles/og:titles that say nothing about the business (theme or WordPress defaults).
GENERIC_TITLES = {"home", "front", "front page", "homepage", "welcome", "untitled"}
# Sitemap sections that should normally not be indexable (WordPress core / Porto theme).
SITEMAP_REVIEW_MARKERS = {"users": "sitemap_exposes_user_archives",
                          "porto_builder": "sitemap_lists_theme_templates"}
MAX_CHILD_SITEMAPS = 30
# Pages declaring lang=ar but with less Arabic than this share of letters are treated as
# untranslated WPML fallbacks, where canonical-to-original is expected rather than a defect.
MIN_TRANSLATED_ARABIC_SHARE = 0.30
# CSS classes of a quote (RFQ) button on the page itself — YITH Request a Quote on the live site.
# Matched on element class attributes only: the same names also appear in site-wide <style> blocks.
# Overridable with config "quote_markers".
DEFAULT_QUOTE_MARKERS = ["add-request-quote-button", "yith-ywraq-add-button", "yith-ywraq-add-to-quote"]
NON_TEXT_TAGS = {"script", "style", "noscript", "svg", "template"}

# Issues that can actively remove pages from search; sorted first in reports.
CRITICAL_ISSUES = {"canonical_conflicts_with_hreflang", "page_declares_noindex_review",
                   "header_noindex_review", "page_not_http_200", "schema_offer_price_zero",
                   "schema_offer_on_quote_only_page", "sitemap_child_unreachable"}


@dataclass
class PageHTML(HTMLParser):
    title_text: str = ""
    headings: list = field(default_factory=list)
    metas: list = field(default_factory=list)
    links: list = field(default_factory=list)
    images: list = field(default_factory=list)
    jsonld: list = field(default_factory=list)
    html_lang: str = ""
    html_dir: str = ""
    _title: bool = False
    _heading: str | None = None
    _ld: bool = False
    _ld_buffer: list = field(default_factory=list)
    arabic_letters: int = 0
    latin_letters: int = 0
    # Same counts restricted to <main>, so translated menus and footers
    # don't make an untranslated page body look Arabic.
    main_arabic_letters: int = 0
    main_latin_letters: int = 0
    has_main: bool = False
    _in_body: bool = False
    _skip: int = 0
    _main_depth: int = 0
    quote_classes: list = field(default_factory=lambda: list(DEFAULT_QUOTE_MARKERS))
    quote_ui: bool = False

    def __post_init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)

    def handle_starttag(self, tag, attrs):
        values = {k.lower(): (v or "") for k, v in attrs}
        if not self.quote_ui and values.get("class"):
            classes = values["class"].split()
            self.quote_ui = any(marker in classes for marker in self.quote_classes)
        if tag == "html":
            self.html_lang = values.get("lang", "")
            self.html_dir = values.get("dir", "")
        elif tag == "body":
            self._in_body = True
        elif tag == "title":
            self._title = True
        elif re.fullmatch(r"h[1-6]", tag):
            self._heading = tag
            self.headings.append({"level": tag, "text": ""})
        elif tag == "meta":
            self.metas.append(values)
        elif tag == "link":
            self.links.append(values)
        elif tag == "img":
            self.images.append(values)
        if tag in NON_TEXT_TAGS:
            self._skip += 1
        if tag == "main":
            self.has_main = True
            self._main_depth += 1
        if tag == "script" and values.get("type", "").lower() == "application/ld+json":
            self._ld = True
            self._ld_buffer = []

    def handle_endtag(self, tag):
        if tag in NON_TEXT_TAGS and self._skip:
            self._skip -= 1
        if tag == "main" and self._main_depth:
            self._main_depth -= 1
        if tag == "title":
            self._title = False
        if self._heading == tag:
            self._heading = None
        if tag == "script" and self._ld:
            raw = "".join(self._ld_buffer).strip()
            if raw:
                try:
                    self.jsonld.append(json.loads(raw))
                except json.JSONDecodeError:
                    self.jsonld.append({"parse_error": True})
            self._ld = False
            self._ld_buffer = []

    def handle_data(self, data):
        if self._title:
            self.title_text += data
        if self._heading and self.headings:
            self.headings[-1]["text"] += data
        if self._ld:
            self._ld_buffer.append(data)
        elif self._in_body and not self._skip:
            arabic = len(re.findall(r"[\u0621-\u064A]", data))
            latin = len(re.findall(r"[A-Za-z]", data))
            self.arabic_letters += arabic
            self.latin_letters += latin
            if self._main_depth:
                self.main_arabic_letters += arabic
                self.main_latin_letters += latin


def _normalize(s):
    return re.sub(r"\s+", " ", s or "").strip()


def _same_url(a: str, b: str) -> bool:
    pa, pb = urlparse(a), urlparse(b)
    return (pa.scheme, pa.netloc.lower(), pa.path or "/") == (pb.scheme, pb.netloc.lower(), pb.path or "/")


def _jsonld_nodes(data):
    """Yield every dict in a JSON-LD block, including @graph members and nested values."""
    if isinstance(data, dict):
        yield data
        for value in data.values():
            yield from _jsonld_nodes(value)
    elif isinstance(data, list):
        for item in data:
            yield from _jsonld_nodes(item)


def _types(node) -> list:
    t = node.get("@type", [])
    return t if isinstance(t, list) else [t]


def is_placeholder_sku(sku: str) -> bool:
    """Copied/generated placeholders, e.g. 1234567812-1-1-1. Length alone is not a signal:
    real order codes such as NSL-UPL-XDD-24W-XXK-SMD-DON-IP65 are long."""
    return bool(re.search(r"(-1){3,}", sku) or re.match(r"^1234567", sku) or re.fullmatch(r"(\d)\1{3,}", sku))


def schema_facts(blocks: list) -> dict:
    """Commercial claims made in JSON-LD, reported so reviewers see them without reading raw markup."""
    facts = {"product_nodes": 0, "offer_nodes": 0, "currencies": set(), "availability": set(), "skus": []}
    for node in _jsonld_nodes(blocks):
        types = _types(node)
        if "Product" in types:
            facts["product_nodes"] += 1
            if node.get("sku"):
                facts["skus"].append(str(node["sku"]))
        if "Offer" in types or "AggregateOffer" in types:
            facts["offer_nodes"] += 1
        if node.get("priceCurrency"):
            facts["currencies"].add(str(node["priceCurrency"]))
        if node.get("availability"):
            facts["availability"].add(str(node["availability"]).rsplit("/", 1)[-1])
    facts["currencies"] = sorted(facts["currencies"])
    facts["availability"] = sorted(facts["availability"])
    return facts


def schema_issues(blocks: list, quote_only: bool = False, kind: str | None = None,
                  approved_sku_pattern: str | None = None) -> list:
    """Content checks for JSON-LD: values Google may treat as misleading or broken."""
    issues = []
    facts = schema_facts(blocks)
    for sku in facts["skus"]:
        if is_placeholder_sku(sku):
            issues.append("schema_sku_placeholder")
        elif approved_sku_pattern and not re.fullmatch(approved_sku_pattern, sku):
            issues.append("schema_sku_not_in_approved_format")
    if kind == "product" and facts["product_nodes"] == 0:
        issues.append("schema_product_missing")
    if facts["product_nodes"] > 1:
        issues.append("schema_duplicate_product_review")
    if quote_only and facts["offer_nodes"]:
        # Quote-only pages cannot truthfully publish price/stock; expected result is no Offer.
        issues.append("schema_offer_on_quote_only_page")
    for node in _jsonld_nodes(blocks):
        types = _types(node)
        if "Offer" in types or "UnitPriceSpecification" in types:
            price = node.get("price")
            try:
                if price is not None and float(price) == 0:
                    issues.append("schema_offer_price_zero")
            except (TypeError, ValueError):
                pass
    if "�" in json.dumps(blocks, ensure_ascii=False):
        issues.append("schema_encoding_error")
    return sorted(set(issues))


def analyze_html(html: str, url: str, host: str | None = None, kind: str | None = None,
                 quote_markers: list | None = None, approved_sku_pattern: str | None = None) -> dict:
    p = PageHTML(quote_classes=quote_markers or list(DEFAULT_QUOTE_MARKERS))
    p.feed(html)
    p.close()
    metas = {m.get("name", "").lower(): m.get("content", "") for m in p.metas if m.get("name")}
    og = {m.get("property", "").lower(): m.get("content", "") for m in p.metas if m.get("property", "").startswith("og:")}
    canonicals = [x.get("href", "") for x in p.links if "canonical" in x.get("rel", "").lower().split()]
    alternates = [{"hreflang": x.get("hreflang"), "href": x.get("href")} for x in p.links
                  if "alternate" in x.get("rel", "").lower().split() and x.get("hreflang")]
    h1 = [_normalize(x["text"]) for x in p.headings if x["level"] == "h1"]
    img_without_alt = sum("alt" not in x or not x["alt"].strip() for x in p.images)
    description = _normalize(metas.get("description", ""))
    title = _normalize(p.title_text)
    og_title = _normalize(og.get("og:title", ""))
    x_robots = metas.get("robots", "")
    host = (host or urlparse(url).netloc).lower()
    arabic, latin = ((p.main_arabic_letters, p.main_latin_letters) if p.has_main
                     else (p.arabic_letters, p.latin_letters))
    letters = arabic + latin
    arabic_share = round(arabic / letters, 2) if letters else None
    untranslated = (p.html_lang.lower().startswith("ar") and arabic_share is not None
                    and arabic_share < MIN_TRANSLATED_ARABIC_SHARE)
    quote_only = p.quote_ui
    issues = []
    if not title:
        issues.append("missing_title")
    else:
        # "LED UP LIGHT – nassli-led.com.sa": the site name part is the bare domain.
        parts = [s.strip().lower() for s in re.split(r"\s[–|\-]\s", title)]
        if title.lower() == host or title.lower() in GENERIC_TITLES:
            issues.append("generic_title")
        elif host in parts:
            issues.append("title_uses_domain_as_site_name")
    if og_title.lower() in GENERIC_TITLES:
        issues.append("generic_og_title")
    if not description:
        issues.append("missing_meta_description")
    if not h1:
        issues.append("missing_h1")
    elif len(h1) > 1:
        issues.append("multiple_h1_review")
    elif h1[0].lower().startswith(("welcome", "مرحب")):
        issues.append("generic_h1")
    if not canonicals:
        issues.append("canonical_missing")
    elif len(canonicals) > 1:
        issues.append("canonical_multiple")
    if untranslated:
        issues.append("arabic_page_mostly_untranslated")
    if not p.html_lang:
        issues.append("missing_html_lang")
    elif p.html_lang.lower().startswith("ar") and p.html_dir.lower() != "rtl":
        issues.append("arabic_page_missing_rtl")
    if img_without_alt:
        issues.append("images_missing_alt_review")
    if "noindex" in x_robots.lower():
        issues.append("page_declares_noindex_review")
    if any(isinstance(x, dict) and x.get("parse_error") for x in p.jsonld):
        issues.append("invalid_jsonld_syntax")
    valid_blocks = [x for x in p.jsonld if not (isinstance(x, dict) and x.get("parse_error"))]
    issues.extend(schema_issues(valid_blocks, quote_only, kind, approved_sku_pattern))
    for canonical in canonicals:
        target = urljoin(url, canonical)
        if canonical and urlparse(target).netloc != urlparse(url).netloc:
            issues.append("cross_domain_canonical_review")
        elif canonical and not _same_url(target, url):
            # A page listed as its own language alternate must canonicalize to itself,
            # otherwise Google is told the translation is a duplicate (WPML misconfiguration).
            if untranslated:
                # WPML fallback: body is still the original language, so pointing at the original
                # is expected until the page is translated (then it must self-canonicalize).
                issues.append("canonical_to_original_on_untranslated_review")
            elif any(a.get("href") and _same_url(urljoin(url, a["href"]), url) for a in alternates):
                issues.append("canonical_conflicts_with_hreflang")
            else:
                issues.append("canonical_not_self_review")
    jsonld_types = sorted({t for n in _jsonld_nodes(p.jsonld) for t in _types(n) if isinstance(t, str)})
    return {
        "url": url, "title": title, "title_characters": len(title),
        "meta_description": description, "description_characters": len(description),
        "og_title": og_title, "html_lang": p.html_lang, "html_dir": p.html_dir,
        "h1": h1, "headings_count": len(p.headings),
        "canonical": canonicals, "hreflang": alternates, "robots_meta": x_robots,
        "images": len(p.images), "images_missing_alt": img_without_alt,
        "jsonld_blocks": len(p.jsonld), "jsonld_types": jsonld_types,
        "arabic_share": arabic_share, "quote_only_ui": quote_only, "schema_facts": schema_facts(valid_blocks),
        "issues": sorted(set(issues), key=issues.index),
    }


def cross_page_checks(pages: list) -> None:
    """Checks needing several pages: duplicate titles and hreflang return links. Mutates pages."""
    by_url = {p.get("final_url") or p.get("url"): p for p in pages if p.get("status") == 200}
    titles: dict = {}
    for page in by_url.values():
        if page.get("title"):
            titles.setdefault(page["title"].lower(), []).append(page)
    for group in titles.values():
        if len(group) > 1:
            for page in group:
                page.setdefault("issues", []).append("duplicate_title_across_pages")
    for url, page in by_url.items():
        for alt in page.get("hreflang", []):
            target = urljoin(url, alt.get("href") or "")
            other = next((p for u, p in by_url.items() if _same_url(u, target)), None)
            if other is None or other is page:
                continue
            if not any(_same_url(urljoin(target, a.get("href") or ""), url) for a in other.get("hreflang", [])):
                page.setdefault("issues", []).append("hreflang_missing_return_link")
                break


def classify_sitemap_urls(locs: list) -> list:
    issues = set()
    for loc in locs:
        lowered = loc.lower()
        for marker, issue in SITEMAP_REVIEW_MARKERS.items():
            if marker in lowered:
                issues.add(issue)
        if "?" in loc:
            issues.add("sitemap_contains_query_urls")
    return sorted(issues)


def summarize_sitemap(xml_text: str) -> dict:
    """Parse one sitemap or sitemap index, including xhtml:link hreflang alternates."""
    root = ET.fromstring(xml_text)
    kind = root.tag.split("}")[-1]
    locs = [_normalize(el.text) for el in root.iter() if el.tag.split("}")[-1] == "loc" and el.text]
    alternates = [el.attrib for el in root.iter()
                  if el.tag.split("}")[-1] == "link" and el.attrib.get("rel") == "alternate" and el.attrib.get("hreflang")]
    return {"type": kind, "locs": locs, "url_count": len(locs),
            "arabic_locs": sum((urlparse(u).path + "/").startswith("/ar/") for u in locs),
            "hreflang_links": len(alternates),
            "arabic_hreflang_links": sum(a.get("hreflang", "").lower().startswith("ar") for a in alternates)}


def sitemap_site_issues(children: dict, languages: list | None = None) -> list:
    """Checks across the whole sitemap tree. `children` maps child URL -> summarize_sitemap() or None if unreachable."""
    issues = set()
    seen: dict = {}
    for url, summary in children.items():
        if summary is None:
            issues.add("sitemap_child_unreachable")
            continue
        if summary["type"] != "urlset":
            continue
        for loc in summary["locs"]:
            seen[loc] = seen.get(loc, 0) + 1
    if any(count > 1 for count in seen.values()):
        issues.add("sitemap_duplicate_urls")
    if "ar" in (languages or []):
        reachable = [c for c in children.values() if c and c["type"] == "urlset"]
        if reachable and not any(c["arabic_locs"] or c["arabic_hreflang_links"] for c in reachable):
            issues.add("sitemap_has_no_arabic_urls")
    return sorted(issues)


def fetch_text(url: str, user_agent: str, timeout: int = 15) -> dict:
    req = Request(url, headers={"User-Agent": user_agent, "Accept": "text/html,application/xml,text/plain;q=0.9"})
    start = time.monotonic()
    try:
        with urlopen(req, timeout=timeout) as response:
            media_type = response.headers.get("Content-Type", "").split(";")[0].lower()
            x_robots = response.headers.get("X-Robots-Tag", "")
            # Limit size to prevent unexpected large responses.
            data = response.read(2_000_001)
            if len(data) > 2_000_000:
                return {"url": url, "status": response.status, "error": "response_over_2mb", "duration_ms": round((time.monotonic()-start)*1000)}
            encoding = response.headers.get_content_charset() or "utf-8"
            return {"url": response.url, "status": response.status, "content_type": media_type,
                    "x_robots_tag": x_robots, "body": data.decode(encoding, errors="replace"),
                    "duration_ms": round((time.monotonic()-start)*1000)}
    except HTTPError as exc:
        return {"url": url, "status": exc.code, "error": f"HTTP {exc.code}", "duration_ms": round((time.monotonic()-start)*1000)}
    except (URLError, TimeoutError, ValueError) as exc:
        return {"url": url, "status": None, "error": str(exc), "duration_ms": round((time.monotonic()-start)*1000)}


def validate_config(config: dict) -> None:
    base = config.get("base_url", "")
    parsed = urlparse(base)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("base_url must be an HTTPS URL with a hostname")
    pages = config.get("pages", [])
    maximum = int(config.get("max_pages", 12))
    if maximum < 1 or maximum > 50 or len(pages) > maximum:
        raise ValueError("pages exceed maximum (50); bounded audit only")
    for page in pages:
        path = page.get("path", "")
        check = urlparse(path)
        if not path.startswith("/") or path.startswith("//") or check.scheme or check.netloc:
            raise ValueError(f"Only same-origin absolute paths are allowed: {path}")
    if not 1 <= float(config.get("requests_timeout_seconds", 15)) <= 60:
        raise ValueError("timeout must be between 1 and 60 seconds")
    if float(config.get("delay_seconds", 1)) < 0.5:
        raise ValueError("delay must be >= 0.5 seconds")


def _audit_discovery(base: str, agent: str, timeout: int, delay: float, languages: list | None = None) -> dict:
    host = urlparse(base).netloc
    discovery: dict = {"host_variants": {}, "sitemaps": {}, "issues": []}
    # Every variant should end on the canonical https host.
    bare = host[4:] if host.startswith("www.") else host
    for variant in {f"http://{bare}/", f"https://www.{bare}/", f"http://www.{bare}/"}:
        fetched = fetch_text(variant, agent, timeout)
        ok = fetched.get("status") == 200 and _same_url(fetched.get("url", ""), base + "/")
        discovery["host_variants"][variant] = {"final_url": fetched.get("url"), "status": fetched.get("status"), "ok": ok}
        if not ok and fetched.get("status") is not None:
            discovery["issues"].append("host_variant_not_redirected_to_canonical")
        time.sleep(delay)
    robots = fetch_text(base + "/robots.txt", agent, timeout)
    discovery["robots"] = {k: v for k, v in robots.items() if k != "body"}
    declared = re.findall(r"(?im)^\s*Sitemap:\s*(\S+)", robots.get("body", "")) if robots.get("status") == 200 else []
    discovery["robots"]["sitemap_directives"] = declared
    if not declared:
        discovery["issues"].append("robots_declares_no_sitemap")
    time.sleep(delay)
    queue = [u for u in declared if urlparse(u).netloc == host][:3] or [base + "/wp-sitemap.xml"]
    seen = 0
    summaries: dict = {}
    while queue and seen < MAX_CHILD_SITEMAPS:
        sm_url = queue.pop(0)
        seen += 1
        fetched = fetch_text(sm_url, agent, timeout)
        row = {"status": fetched.get("status")}
        if fetched.get("status") == 200:
            try:
                summary = summarize_sitemap(fetched.get("body", ""))
                summaries[sm_url] = summary
                locs = summary["locs"]
                row.update({k: v for k, v in summary.items() if k != "locs"})
                if summary["type"] == "sitemapindex":
                    queue.extend(u for u in locs if urlparse(u).netloc == host)
                else:
                    row["sample"] = locs[:3]
                flagged = classify_sitemap_urls(locs)
                row["issues"] = flagged
                discovery["issues"].extend(flagged)
            except ET.ParseError:
                row["xml_parse_error"] = True
                discovery["issues"].append("sitemap_xml_parse_error")
        else:
            row["error"] = fetched.get("error")
            summaries[sm_url] = None
        discovery["sitemaps"][sm_url] = row
        time.sleep(delay)
    discovery["issues"].extend(sitemap_site_issues(summaries, languages))
    discovery["issues"] = sorted(set(discovery["issues"]))
    return discovery


def run_audit(config: dict) -> dict:
    validate_config(config)
    base = config["base_url"].rstrip("/")
    agent = config.get("user_agent", "NassliSEOAudit/0.1")
    timeout = int(config.get("requests_timeout_seconds", 15))
    delay = float(config.get("delay_seconds", 1))
    report = {"generated_at": datetime.now(timezone.utc).isoformat(), "base_url": base,
              "scope": "configured_urls_and_declared_sitemaps_read_only",
              "discovery": _audit_discovery(base, agent, timeout, delay, config.get("languages")), "pages": []}
    for page in config["pages"]:
        url = urljoin(base+"/", page["path"].lstrip("/"))
        fetched = fetch_text(url, agent, timeout)
        record = {"path": page["path"], "kind": page.get("kind"), "lang": page.get("primary_language"),
                  "status": fetched.get("status"), "duration_ms": fetched.get("duration_ms"),
                  "final_url": fetched.get("url", url)}
        if fetched.get("error"):
            record["error"] = fetched["error"]
        elif fetched.get("content_type", "") not in ("text/html", "application/xhtml+xml"):
            record["error"] = "non_html_response"
        else:
            record.update(analyze_html(fetched.get("body", ""), fetched.get("url", url), urlparse(base).netloc,
                                       page.get("kind"), config.get("quote_markers"), config.get("approved_sku_pattern")))
            if "noindex" in fetched.get("x_robots_tag", "").lower():
                record["issues"].append("header_noindex_review")
        if record.get("status") != 200:
            record.setdefault("issues", []).append("page_not_http_200")
        report["pages"].append(record)
        time.sleep(delay)
    cross_page_checks(report["pages"])
    return report


def _sorted_issues(issues: list) -> list:
    return sorted(set(issues), key=lambda i: (i not in CRITICAL_ISSUES, i))


def to_markdown(report: dict) -> str:
    discovery = report.get("discovery", {})
    lines = ["# Nassli technical SEO scan", "", f"- Generated: {report['generated_at']}",
             f"- Scope: {report['scope']}", f"- Website: {report['base_url']}",
             "- Read-only scan; HTML checks are hints, not ranking predictions.",
             "- Issues marked **bold** can remove pages from search and should be reviewed first.", ""]
    lines.extend(["## Discovery", "", "| Item | Status | Notes |", "|---|---|---|"])
    for variant, row in discovery.get("host_variants", {}).items():
        lines.append(f"| `{variant}` | {row.get('status')} | → {row.get('final_url')} {'✓' if row.get('ok') else '✗'} |")
    robots = discovery.get("robots", {})
    if robots:
        lines.append(f"| `robots.txt` | {robots.get('status')} | {', '.join(robots.get('sitemap_directives', [])) or robots.get('error', '')} |")
    for sm_url, row in discovery.get("sitemaps", {}).items():
        notes = f"{row.get('type', '')} {row.get('url_count', '')} URLs"
        if row.get("type") == "urlset":
            notes += f", /ar/ {row.get('arabic_locs', 0)}, hreflang {row.get('hreflang_links', 0)}"
        notes = f"{notes} {', '.join(row.get('issues', []))}".strip()
        lines.append(f"| `{sm_url}` | {row.get('status')} | {(notes or row.get('error') or '').replace('|', '/')} |")
    if discovery.get("issues"):
        lines.extend(["", "**Site-level issues:** " + ", ".join(discovery["issues"])])
    lines.extend(["", "## Page audit", "",
                  "| URL | Lang | HTTP | Arabic share | Title | H1 | Schema claims | Issues |",
                  "|---|---|---:|---:|---|---|---|---|"])
    for p in report["pages"]:
        issues = [f"**{i}**" if i in CRITICAL_ISSUES else i for i in _sorted_issues(p.get("issues", []))]
        facts = p.get("schema_facts") or {}
        claims = ", ".join(facts.get("currencies", []) + facts.get("availability", []))
        share = p.get("arabic_share")
        lines.append("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
            p["path"], p.get("html_lang") or p.get("lang") or "-", p.get("status"),
            "-" if share is None else f"{share:.0%}",
            p.get("title", "-").replace("|", "/")[:70],
            "; ".join(p.get("h1", []))[:70].replace("|", "/"),
            claims or "—", ", ".join(issues) or "—"))
    lines.extend(["", "## Limitations", "", "Configured page sample only; no Google index status, Core Web Vitals, GA4 or AI citations are measured.",
                  "A missing title/meta warning does not automatically mean poor ranking; prioritize with traffic and conversions."])
    return "\n".join(lines)+"\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Read-only bounded SEO audit")
    ap.add_argument("--config", default="config/site.json")
    ap.add_argument("--output", default="reports/current")
    args = ap.parse_args(argv)
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    report = run_audit(cfg)
    folder = Path(args.output)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (folder / "audit.md").write_text(to_markdown(report), encoding="utf-8")
    failed = sum(p.get("status") != 200 for p in report["pages"])
    print(f"Scanned {len(report['pages'])} configured pages; {failed} non-200 responses. Report: {folder / 'audit.md'}")
    return 0  # Don't fail CI due to temporary remote network errors; review the report.


if __name__ == "__main__":
    raise SystemExit(main())
