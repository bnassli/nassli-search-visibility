"""Small, dependency-free, intentionally bounded technical SEO auditor.

This is a diagnostic tool, not an indexer, rank tracker or production deployment system.
It fetches only the exact configured pages plus common discovery files.
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


@dataclass
class PageHTML(HTMLParser):
    title_text: str = ""
    headings: list = field(default_factory=list)
    metas: list = field(default_factory=list)
    links: list = field(default_factory=list)
    images: list = field(default_factory=list)
    jsonld: list = field(default_factory=list)
    html_lang: str = ""
    _title: bool = False
    _heading: str | None = None
    _ld: bool = False
    _ld_buffer: list = field(default_factory=list)

    def __post_init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)

    def handle_starttag(self, tag, attrs):
        values = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html":
            self.html_lang = values.get("lang", "")
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
        elif tag == "script" and values.get("type", "").lower() == "application/ld+json":
            self._ld = True
            self._ld_buffer = []

    def handle_endtag(self, tag):
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


def _normalize(s):
    return re.sub(r"\s+", " ", s or "").strip()


def analyze_html(html: str, url: str) -> dict:
    p = PageHTML()
    p.feed(html)
    p.close()
    metas = {m.get("name", "").lower(): m.get("content", "") for m in p.metas if m.get("name")}
    canonicals = [x.get("href", "") for x in p.links if "canonical" in x.get("rel", "").lower().split()]
    alternates = [{"hreflang": x.get("hreflang"), "href": x.get("href")} for x in p.links
                  if "alternate" in x.get("rel", "").lower().split() and x.get("hreflang")]
    h1 = [_normalize(x["text"]) for x in p.headings if x["level"] == "h1"]
    img_without_alt = sum("alt" not in x or not x["alt"].strip() for x in p.images)
    description = _normalize(metas.get("description", ""))
    title = _normalize(p.title_text)
    x_robots = metas.get("robots", "")
    issues = []
    if not title:
        issues.append("missing_title")
    if not description:
        issues.append("missing_meta_description")
    if not h1:
        issues.append("missing_h1")
    elif len(h1) > 1:
        issues.append("multiple_h1_review")
    if len(canonicals) != 1:
        issues.append("canonical_missing_or_multiple")
    if not p.html_lang:
        issues.append("missing_html_lang")
    if img_without_alt:
        issues.append("images_missing_alt_review")
    if "noindex" in x_robots.lower():
        issues.append("page_declares_noindex_review")
    if any(x.get("parse_error") for x in p.jsonld):
        issues.append("invalid_jsonld_syntax")
    for canonical in canonicals:
        if canonical and urlparse(urljoin(url, canonical)).netloc != urlparse(url).netloc:
            issues.append("cross_domain_canonical_review")
    return {
        "url": url, "title": title, "title_characters": len(title),
        "meta_description": description, "description_characters": len(description),
        "html_lang": p.html_lang, "h1": h1, "headings_count": len(p.headings),
        "canonical": canonicals, "hreflang": alternates, "robots_meta": x_robots,
        "images": len(p.images), "images_missing_alt": img_without_alt,
        "jsonld_blocks": len(p.jsonld), "issues": issues,
    }


def fetch_text(url: str, user_agent: str, timeout: int = 15) -> dict:
    req = Request(url, headers={"User-Agent": user_agent, "Accept": "text/html,application/xml,text/plain;q=0.9"})
    start = time.monotonic()
    try:
        with urlopen(req, timeout=timeout) as response:
            media_type = response.headers.get("Content-Type", "").split(";")[0].lower()
            # Limit size to prevent unexpected large responses.
            data = response.read(2_000_001)
            if len(data) > 2_000_000:
                return {"url": url, "status": response.status, "error": "response_over_2mb", "duration_ms": round((time.monotonic()-start)*1000)}
            encoding = response.headers.get_content_charset() or "utf-8"
            return {"url": response.url, "status": response.status, "content_type": media_type,
                    "body": data.decode(encoding, errors="replace"),
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


def run_audit(config: dict) -> dict:
    validate_config(config)
    base = config["base_url"].rstrip("/")
    agent = config.get("user_agent", "NassliSEOAudit/0.1")
    timeout = int(config.get("requests_timeout_seconds", 15))
    delay = float(config.get("delay_seconds", 1))
    report = {"generated_at": datetime.now(timezone.utc).isoformat(), "base_url": base,
              "scope": "configured_urls_only_read_only", "discovery": {}, "pages": []}
    for path in ["/robots.txt", "/sitemap_index.xml", "/wp-sitemap.xml"]:
        fetched = fetch_text(base+path, agent, timeout)
        report["discovery"][path] = {k: v for k, v in fetched.items() if k != "body"}
        if fetched.get("status") == 200 and path == "/robots.txt":
            report["discovery"][path]["sitemap_directives"] = re.findall(r"(?im)^\s*Sitemap:\s*(\S+)", fetched.get("body", ""))
        if fetched.get("status") == 200 and path.endswith("xml"):
            try:
                root = ET.fromstring(fetched.get("body", ""))
                report["discovery"][path]["root_element"] = root.tag.split("}")[-1]
            except ET.ParseError:
                report["discovery"][path]["xml_parse_error"] = True
        time.sleep(delay)
    for page in config["pages"]:
        url = urljoin(base+"/", page["path"].lstrip("/"))
        fetched = fetch_text(url, agent, timeout)
        record = {"path": page["path"], "kind": page.get("kind"), "status": fetched.get("status"),
                  "duration_ms": fetched.get("duration_ms"), "final_url": fetched.get("url", url)}
        if fetched.get("error"):
            record["error"] = fetched["error"]
        elif fetched.get("content_type", "") != "text/html":
            record["error"] = "non_html_response"
        else:
            record.update(analyze_html(fetched.get("body", ""), fetched.get("url", url)))
        if record.get("status") != 200:
            record.setdefault("issues", []).append("page_not_http_200")
        report["pages"].append(record)
        time.sleep(delay)
    return report


def to_markdown(report: dict) -> str:
    lines = ["# Nassli technical SEO scan", "", f"- Generated: {report['generated_at']}",
             f"- Scope: {report['scope']}", f"- Website: {report['base_url']}",
             "- Read-only scan; HTML checks are hints, not ranking predictions.", "",
             "## Discovery", "", "| Path | Status | Notes |", "|---|---|---|"]
    for path, row in report["discovery"].items():
        notes = row.get("error", "") or row.get("root_element", "") or ", ".join(row.get("sitemap_directives", []))
        lines.append(f"| `{path}` | {row.get('status')} | {str(notes).replace('|', '/')} |")
    lines.extend(["", "## Page audit", "", "| URL | HTTP | Title | H1 | Issues |", "|---|---:|---|---|---|"])
    for p in report["pages"]:
        lines.append("| {} | {} | {} | {} | {} |".format(
            p["path"], p.get("status"), p.get("title", "-").replace("|", "/")[:70],
            "; ".join(p.get("h1", []))[:70].replace("|", "/"),
            ", ".join(p.get("issues", [])) or "—"))
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
