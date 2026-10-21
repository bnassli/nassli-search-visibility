import unittest
from src.nassli_audit.audit import (PageHTML, analyze_html, validate_config, to_markdown,
                                    schema_issues, cross_page_checks, classify_sitemap_urls)

SAMPLE = '''<!doctype html><html lang="en"><head><title>Nassli LED | Project Lighting</title>
<meta name="description" content="Saudi lighting solutions for projects">
<link rel="canonical" href="https://nassli-led.com.sa/">
<link rel="alternate" hreflang="ar-SA" href="https://nassli-led.com.sa/ar/">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"Nassli"}</script>
</head><body><h1>Lighting for Projects</h1><img src="/a.jpg" alt="LED lights"/></body></html>'''

# Mirrors what WPML + no SEO plugin served on 2026-10-21 for the Arabic homepage.
LIVE_AR_HOME = '''<html dir="rtl" lang="ar"><head><title>nassli-led.com.sa</title>
<link rel="alternate" hreflang="ar" href="https://nassli-led.com.sa/ar/" />
<link rel="alternate" hreflang="en" href="https://nassli-led.com.sa/" />
<meta property="og:title" content="front"/>
<link rel="canonical" href="https://nassli-led.com.sa/" />
</head><body><h1>مرحبًا بكم في ناسلي</h1></body></html>'''

LIVE_PRODUCT_SCHEMA = {"@context": "https://schema.org/", "@type": "Product", "name": "LED UP LIGHT",
                       "sku": "1234567812-1-1-1-1-1-2-1-1-1-1-1-1-1-1-1-1-1-1-1",
                       "description": "building fa�ades",
                       "offers": [{"@type": "Offer", "priceSpecification": [
                           {"@type": "UnitPriceSpecification", "price": "0.00", "priceCurrency": "SAR"}]}]}


class TestAnalysis(unittest.TestCase):
    def test_good_document(self):
        result = analyze_html(SAMPLE, 'https://nassli-led.com.sa/')
        self.assertEqual(result['h1'], ['Lighting for Projects'])
        self.assertEqual(result['jsonld_blocks'], 1)
        self.assertEqual(result['jsonld_types'], ['Organization'])
        self.assertEqual(result['issues'], [])
        self.assertEqual(result['hreflang'][0]['hreflang'], 'ar-SA')

    def test_missing_metadata(self):
        result = analyze_html('<html><body><img src="a"></body></html>', 'https://nassli-led.com.sa/')
        for warning in ['missing_title','missing_h1','missing_meta_description','missing_html_lang', 'canonical_missing_or_multiple', 'images_missing_alt_review']:
            self.assertIn(warning, result['issues'])

    def test_noindex(self):
        result = analyze_html(SAMPLE.replace('</head>', '<meta name="robots" content="noindex"/></head>'), 'https://nassli-led.com.sa/')
        self.assertIn('page_declares_noindex_review', result['issues'])

    def test_invalid_schema(self):
        result = analyze_html(SAMPLE.replace('{"@context":"https://schema.org","@type":"Organization","name":"Nassli"}', '{bad json}'), 'https://nassli-led.com.sa/')
        self.assertIn('invalid_jsonld_syntax', result['issues'])

    def test_arabic_page_canonical_to_english_is_critical(self):
        result = analyze_html(LIVE_AR_HOME, 'https://nassli-led.com.sa/ar/')
        for warning in ['canonical_conflicts_with_hreflang', 'generic_title', 'generic_og_title',
                        'generic_h1', 'missing_meta_description']:
            self.assertIn(warning, result['issues'])
        self.assertNotIn('arabic_page_missing_rtl', result['issues'])

    def test_canonical_elsewhere_without_hreflang_is_only_review(self):
        html = SAMPLE.replace('<link rel="alternate" hreflang="ar-SA" href="https://nassli-led.com.sa/ar/">', '')
        result = analyze_html(html, 'https://nassli-led.com.sa/page/?utm=x')
        self.assertNotIn('canonical_conflicts_with_hreflang', result['issues'])
        self.assertIn('canonical_not_self_review', result['issues'])

    def test_arabic_without_rtl(self):
        result = analyze_html(SAMPLE.replace('lang="en"', 'lang="ar"'), 'https://nassli-led.com.sa/')
        self.assertIn('arabic_page_missing_rtl', result['issues'])

    def test_domain_as_site_name(self):
        html = SAMPLE.replace('Nassli LED | Project Lighting', 'LED UP LIGHT &#8211; nassli-led.com.sa')
        self.assertIn('title_uses_domain_as_site_name', analyze_html(html, 'https://nassli-led.com.sa/')['issues'])

    def test_product_schema_content(self):
        self.assertEqual(schema_issues([LIVE_PRODUCT_SCHEMA]),
                         ['schema_encoding_error', 'schema_offer_price_zero', 'schema_sku_suspicious'])
        clean = {"@type": "Product", "name": "LED UP LIGHT", "sku": "NSL-UPL-XDD-9W-XXK-SMD-DON-IP65"}
        self.assertEqual(schema_issues([clean]), [])

    def test_config_rejects_external_paths(self):
        c = {"base_url": "https://nassli-led.com.sa", "pages": [{"path":"//evil.test"}]}
        with self.assertRaises(ValueError): validate_config(c)
        c['pages'][0]['path'] = '/products/'
        validate_config(c)

    def test_report_render(self):
        report = {"generated_at": "2026-10-20", "scope":"sample", "base_url":"https://nassli-led.com.sa", "discovery":{}, "pages":[{"path":"/", "status":200, "title":"Home", "h1":["Home"], "issues":[]}]}
        self.assertIn('| / | - | 200 | Home |', to_markdown(report))

    def test_report_puts_critical_issues_first(self):
        report = {"generated_at": "x", "scope": "s", "base_url": "https://nassli-led.com.sa", "discovery": {},
                  "pages": [{"path": "/ar/", "status": 200, "issues": ["missing_h1", "canonical_conflicts_with_hreflang"]}]}
        self.assertIn('**canonical_conflicts_with_hreflang**, missing_h1', to_markdown(report))


class TestCrossPage(unittest.TestCase):
    def test_duplicate_titles_and_missing_return_link(self):
        en = {"status": 200, "final_url": "https://nassli-led.com.sa/", "title": "nassli-led.com.sa", "issues": [],
              "hreflang": [{"hreflang": "ar", "href": "https://nassli-led.com.sa/ar/"}]}
        ar = {"status": 200, "final_url": "https://nassli-led.com.sa/ar/", "title": "nassli-led.com.sa", "issues": [],
              "hreflang": []}
        cross_page_checks([en, ar])
        self.assertIn('duplicate_title_across_pages', en['issues'])
        self.assertIn('duplicate_title_across_pages', ar['issues'])
        self.assertIn('hreflang_missing_return_link', en['issues'])

    def test_reciprocal_hreflang_is_clean(self):
        links = [{"hreflang": "ar", "href": "https://nassli-led.com.sa/ar/"}, {"hreflang": "en", "href": "https://nassli-led.com.sa/"}]
        en = {"status": 200, "final_url": "https://nassli-led.com.sa/", "title": "A", "issues": [], "hreflang": links}
        ar = {"status": 200, "final_url": "https://nassli-led.com.sa/ar/", "title": "B", "issues": [], "hreflang": links}
        cross_page_checks([en, ar])
        self.assertEqual(en['issues'] + ar['issues'], [])


class TestSitemaps(unittest.TestCase):
    def test_flags_users_and_theme_templates(self):
        locs = ["https://nassli-led.com.sa/wp-sitemap-users-1.xml",
                "https://nassli-led.com.sa/wp-sitemap-posts-porto_builder-1.xml",
                "https://nassli-led.com.sa/?porto_builder=header"]
        self.assertEqual(classify_sitemap_urls(locs), ['sitemap_contains_query_urls', 'sitemap_exposes_user_archives',
                                                       'sitemap_lists_theme_templates'])
        self.assertEqual(classify_sitemap_urls(["https://nassli-led.com.sa/product/led-up-light/"]), [])


if __name__ == '__main__':
    unittest.main()
