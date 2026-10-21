import unittest
from src.nassli_audit.audit import (PageHTML, analyze_html, validate_config, to_markdown, schema_issues,
                                    schema_facts, is_placeholder_sku, cross_page_checks, classify_sitemap_urls,
                                    summarize_sitemap, sitemap_site_issues)

SAMPLE = '''<!doctype html><html lang="en"><head><title>Nassli LED | Project Lighting</title>
<meta name="description" content="Saudi lighting solutions for projects">
<link rel="canonical" href="https://nassli-led.com.sa/">
<link rel="alternate" hreflang="ar-SA" href="https://nassli-led.com.sa/ar/">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"Nassli"}</script>
</head><body><h1>Lighting for Projects</h1><img src="/a.jpg" alt="LED lights"/></body></html>'''

# Mirrors what WPML + no SEO plugin output served on 2026-10-21 for the (translated) Arabic homepage.
LIVE_AR_HOME = '''<html dir="rtl" lang="ar"><head><title>nassli-led.com.sa</title>
<link rel="alternate" hreflang="ar" href="https://nassli-led.com.sa/ar/" />
<link rel="alternate" hreflang="en" href="https://nassli-led.com.sa/" />
<meta property="og:title" content="front"/>
<link rel="canonical" href="https://nassli-led.com.sa/" />
</head><body><h1>مرحبًا بكم في ناسلي</h1><p>حلول إنارة للمشاريع التجارية والمعمارية في السعودية</p></body></html>'''

# Mirrors /ar/product/led-up-light/: Arabic URL and lang, but the body is still the English original (3% Arabic).
LIVE_AR_FALLBACK_PRODUCT = '''<html dir="rtl" lang="ar"><head><title>LED UP LIGHT &#8211; nassli-led.com.sa</title>
<link rel="alternate" hreflang="ar" href="https://nassli-led.com.sa/ar/product/led-up-light/" />
<link rel="alternate" hreflang="en" href="https://nassli-led.com.sa/product/led-up-light/" />
<link rel="canonical" href="https://nassli-led.com.sa/product/led-up-light/" />
</head><body><h2>LED UP LIGHT</h2><p>Ground-recessed LED uplight, engineered for precise landscape and
architectural illumination with IP65 protection and dimming compatibility.</p><span>اطلب</span></body></html>'''

LIVE_PRODUCT_SCHEMA = {"@context": "https://schema.org/", "@type": "Product", "name": "LED UP LIGHT",
                       "sku": "1234567812-1-1-1-1-1-2-1-1-1-1-1-1-1-1-1-1-1-1-1",
                       "description": "building fa�ades",
                       "offers": [{"@type": "Offer", "availability": "https://schema.org/InStock",
                                   "priceSpecification": [{"@type": "UnitPriceSpecification",
                                                           "price": "0.00", "priceCurrency": "USD"}]}]}

PRICED_PRODUCT = {"@context": "https://schema.org", "@type": "Product", "name": "LED Driver 24V",
                  "sku": "NSL-DRV-24V-100W",
                  "offers": {"@type": "Offer", "price": "120.00", "priceCurrency": "SAR",
                             "availability": "https://schema.org/InStock"}}


def page_with_schema(schema, extra_body=""):
    import json
    return SAMPLE.replace('{"@context":"https://schema.org","@type":"Organization","name":"Nassli"}',
                          json.dumps(schema)).replace('</body>', extra_body + '</body>')


class TestAnalysis(unittest.TestCase):
    def test_good_document(self):
        result = analyze_html(SAMPLE, 'https://nassli-led.com.sa/')
        self.assertEqual(result['h1'], ['Lighting for Projects'])
        self.assertEqual(result['jsonld_blocks'], 1)
        self.assertEqual(result['jsonld_types'], ['Organization'])
        self.assertEqual(result['issues'], [])
        self.assertEqual(result['hreflang'][0]['hreflang'], 'ar-SA')
        self.assertEqual(result['arabic_share'], 0.0)

    def test_missing_metadata(self):
        result = analyze_html('<html><body><img src="a"></body></html>', 'https://nassli-led.com.sa/')
        for warning in ['missing_title','missing_h1','missing_meta_description','missing_html_lang', 'canonical_missing', 'images_missing_alt_review']:
            self.assertIn(warning, result['issues'])

    def test_duplicate_canonical(self):
        html = SAMPLE.replace('</head>', '<link rel="canonical" href="https://nassli-led.com.sa/other/"></head>')
        self.assertIn('canonical_multiple', analyze_html(html, 'https://nassli-led.com.sa/')['issues'])

    def test_noindex(self):
        result = analyze_html(SAMPLE.replace('</head>', '<meta name="robots" content="noindex"/></head>'), 'https://nassli-led.com.sa/')
        self.assertIn('page_declares_noindex_review', result['issues'])

    def test_invalid_schema(self):
        result = analyze_html(SAMPLE.replace('{"@context":"https://schema.org","@type":"Organization","name":"Nassli"}', '{bad json}'), 'https://nassli-led.com.sa/')
        self.assertIn('invalid_jsonld_syntax', result['issues'])

    def test_translated_arabic_page_canonical_to_english_is_critical(self):
        result = analyze_html(LIVE_AR_HOME, 'https://nassli-led.com.sa/ar/')
        self.assertGreater(result['arabic_share'], 0.9)
        for warning in ['canonical_conflicts_with_hreflang', 'generic_title', 'generic_og_title',
                        'generic_h1', 'missing_meta_description']:
            self.assertIn(warning, result['issues'])
        self.assertNotIn('arabic_page_missing_rtl', result['issues'])
        self.assertNotIn('arabic_page_mostly_untranslated', result['issues'])

    def test_untranslated_fallback_is_review_not_critical(self):
        result = analyze_html(LIVE_AR_FALLBACK_PRODUCT, 'https://nassli-led.com.sa/ar/product/led-up-light/')
        self.assertLess(result['arabic_share'], 0.3)
        self.assertIn('arabic_page_mostly_untranslated', result['issues'])
        self.assertIn('canonical_to_original_on_untranslated_review', result['issues'])
        self.assertNotIn('canonical_conflicts_with_hreflang', result['issues'])

    def test_translated_menu_does_not_hide_untranslated_main_content(self):
        # Live case: Arabic header/footer around an English product body gave 62% body-wide but 3% in <main>.
        chrome = '<header>' + 'الرئيسية المنتجات المشاريع تواصل معنا ' * 20 + '</header>'
        html = LIVE_AR_FALLBACK_PRODUCT.replace('<body>', '<body>' + chrome + '<main>').replace('</body>', '</main></body>')
        result = analyze_html(html, 'https://nassli-led.com.sa/ar/product/led-up-light/')
        self.assertLess(result['arabic_share'], 0.3)
        self.assertIn('arabic_page_mostly_untranslated', result['issues'])

    def test_script_text_is_not_counted_as_content(self):
        p = PageHTML()
        p.feed('<html lang="ar"><body><p>مرحبا</p><script>var englishOnlyCode = 1;</script><style>.a{color:red}</style></body></html>')
        self.assertEqual((p.arabic_letters, p.latin_letters), (5, 0))

    def test_canonical_elsewhere_without_hreflang_is_only_review(self):
        html = SAMPLE.replace('<link rel="alternate" hreflang="ar-SA" href="https://nassli-led.com.sa/ar/">', '')
        result = analyze_html(html, 'https://nassli-led.com.sa/page/?utm=x')
        self.assertNotIn('canonical_conflicts_with_hreflang', result['issues'])
        self.assertIn('canonical_not_self_review', result['issues'])

    def test_arabic_without_rtl(self):
        html = SAMPLE.replace('lang="en"', 'lang="ar"').replace('Lighting for Projects', 'إنارة للمشاريع التجارية')
        self.assertIn('arabic_page_missing_rtl', analyze_html(html, 'https://nassli-led.com.sa/')['issues'])

    def test_domain_as_site_name(self):
        html = SAMPLE.replace('Nassli LED | Project Lighting', 'LED UP LIGHT &#8211; nassli-led.com.sa')
        self.assertIn('title_uses_domain_as_site_name', analyze_html(html, 'https://nassli-led.com.sa/')['issues'])

    def test_config_rejects_external_paths(self):
        c = {"base_url": "https://nassli-led.com.sa", "pages": [{"path":"//evil.test"}]}
        with self.assertRaises(ValueError): validate_config(c)
        c['pages'][0]['path'] = '/products/'
        validate_config(c)

    def test_report_render(self):
        report = {"generated_at": "2026-10-20", "scope":"sample", "base_url":"https://nassli-led.com.sa", "discovery":{},
                  "pages":[{"path":"/", "status":200, "title":"Home", "h1":["Home"], "issues":[], "arabic_share": 0.92,
                            "schema_facts": {"currencies": ["USD"], "availability": ["InStock"]}}]}
        self.assertIn('| / | - | 200 | 92% | Home | Home | USD, InStock | — |', to_markdown(report))

    def test_report_puts_critical_issues_first(self):
        report = {"generated_at": "x", "scope": "s", "base_url": "https://nassli-led.com.sa", "discovery": {},
                  "pages": [{"path": "/ar/", "status": 200, "issues": ["missing_h1", "canonical_conflicts_with_hreflang"]}]}
        self.assertIn('**canonical_conflicts_with_hreflang**, missing_h1', to_markdown(report))


class TestSchema(unittest.TestCase):
    def test_live_quote_only_product(self):
        self.assertEqual(schema_issues([LIVE_PRODUCT_SCHEMA], quote_only=True, kind='product'),
                         ['schema_encoding_error', 'schema_offer_on_quote_only_page', 'schema_offer_price_zero',
                          'schema_sku_placeholder'])
        facts = schema_facts([LIVE_PRODUCT_SCHEMA])
        self.assertEqual((facts['currencies'], facts['availability']), (['USD'], ['InStock']))

    def test_quote_ui_detected_from_html(self):
        html = page_with_schema(LIVE_PRODUCT_SCHEMA, '<a class="add-request-quote-button">Request a Quote</a>')
        result = analyze_html(html, 'https://nassli-led.com.sa/product/led-up-light/', kind='product')
        self.assertTrue(result['quote_only_ui'])
        self.assertIn('schema_offer_on_quote_only_page', result['issues'])

    def test_quote_class_inside_site_wide_css_is_not_quote_ui(self):
        # Live homepage: `.add-request-quote-button{width:300px}` sits in a global <style> block.
        html = SAMPLE.replace('</head>', '<style>.add-request-quote-button{width:300px}</style></head>')
        self.assertFalse(analyze_html(html, 'https://nassli-led.com.sa/')['quote_only_ui'])

    def test_genuinely_priced_product_is_not_flagged(self):
        self.assertEqual(schema_issues([PRICED_PRODUCT], quote_only=False, kind='product'), [])

    def test_truthful_quote_only_product_without_offer_is_clean(self):
        clean = {"@type": "Product", "name": "LED UP LIGHT", "sku": "NSL-UPL-XDD-24W-XXK-SMD-DON-IP65"}
        self.assertEqual(schema_issues([clean], quote_only=True, kind='product'), [])

    def test_nested_graph_is_inspected(self):
        graph = {"@context": "https://schema.org", "@graph": [{"@type": "WebPage"}, LIVE_PRODUCT_SCHEMA]}
        self.assertIn('schema_sku_placeholder', schema_issues([graph]))
        self.assertIn('schema_offer_price_zero', schema_issues([graph]))

    def test_sku_rules(self):
        self.assertTrue(is_placeholder_sku('1234567812-1-1-1'))
        self.assertTrue(is_placeholder_sku('0000'))
        self.assertFalse(is_placeholder_sku('NSL-UPL-XDD-24W-XXK-SMD-DON-IP65-EXTRA-LONG-CODE'))
        product = {"@type": "Product", "name": "X", "sku": "ABC-123"}
        self.assertEqual(schema_issues([product], approved_sku_pattern=r"NSL-[A-Z0-9-]+"), ['schema_sku_not_in_approved_format'])
        self.assertEqual(schema_issues([product]), [])

    def test_missing_and_duplicate_product_output(self):
        self.assertEqual(schema_issues([{"@type": "Organization", "name": "Nassli"}], kind='product'), ['schema_product_missing'])
        two = [{"@type": "Product", "name": "A"}, {"@type": "Product", "name": "A"}]
        self.assertEqual(schema_issues(two, kind='product'), ['schema_duplicate_product_review'])


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


SITEMAP_INDEX = '''<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<sitemap><loc>https://nassli-led.com.sa/wp-sitemap-posts-product-1.xml</loc></sitemap>
<sitemap><loc>https://nassli-led.com.sa/wp-sitemap-posts-product-2.xml</loc></sitemap>
<sitemap><loc>https://nassli-led.com.sa/wp-sitemap-users-1.xml</loc></sitemap>
</sitemapindex>'''

URLSET_WITH_ALTERNATES = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
<url><loc>https://nassli-led.com.sa/product/led-up-light/</loc>
<xhtml:link rel="alternate" hreflang="en" href="https://nassli-led.com.sa/product/led-up-light/"/>
<xhtml:link rel="alternate" hreflang="ar" href="https://nassli-led.com.sa/ar/product/led-up-light/"/></url>
<url><loc>https://nassli-led.com.sa/ar/product/led-up-light/</loc></url>
</urlset>'''

URLSET_ENGLISH_ONLY = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://nassli-led.com.sa/product/led-linear/</loc></url>
<url><loc>https://nassli-led.com.sa/bar/</loc></url>
<url><loc>https://nassli-led.com.sa/?porto_builder=header</loc></url>
</urlset>'''


class TestSitemaps(unittest.TestCase):
    def test_flags_users_and_theme_templates(self):
        locs = ["https://nassli-led.com.sa/wp-sitemap-users-1.xml",
                "https://nassli-led.com.sa/wp-sitemap-posts-porto_builder-1.xml",
                "https://nassli-led.com.sa/?porto_builder=header"]
        self.assertEqual(classify_sitemap_urls(locs), ['sitemap_contains_query_urls', 'sitemap_exposes_user_archives',
                                                       'sitemap_lists_theme_templates'])
        self.assertEqual(classify_sitemap_urls(["https://nassli-led.com.sa/product/led-up-light/"]), [])

    def test_individual_excluded_url_is_caught_inside_a_child(self):
        summary = summarize_sitemap(URLSET_ENGLISH_ONLY)
        self.assertIn('sitemap_lists_theme_templates', classify_sitemap_urls(summary['locs']))

    def test_nested_index_and_alternates(self):
        index = summarize_sitemap(SITEMAP_INDEX)
        self.assertEqual((index['type'], index['url_count']), ('sitemapindex', 3))
        child = summarize_sitemap(URLSET_WITH_ALTERNATES)
        self.assertEqual((child['type'], child['url_count'], child['arabic_locs']), ('urlset', 2, 1))
        self.assertEqual((child['hreflang_links'], child['arabic_hreflang_links']), (2, 1))
        self.assertEqual(summarize_sitemap(URLSET_ENGLISH_ONLY)['arabic_locs'], 0)  # '/bar/' is not Arabic

    def test_tree_issues(self):
        en_only = summarize_sitemap(URLSET_ENGLISH_ONLY)
        children = {"a.xml": en_only, "b.xml": en_only, "c.xml": None}
        self.assertEqual(sitemap_site_issues(children, ["en", "ar"]),
                         ['sitemap_child_unreachable', 'sitemap_duplicate_urls', 'sitemap_has_no_arabic_urls'])
        self.assertEqual(sitemap_site_issues({"a.xml": en_only}, ["en"]), [])

    def test_arabic_via_xml_hreflang_counts(self):
        # Hreflang moved from HTML to the sitemap is a legitimate setup, not a failure.
        self.assertEqual(sitemap_site_issues({"p.xml": summarize_sitemap(URLSET_WITH_ALTERNATES)}, ["en", "ar"]), [])


if __name__ == '__main__':
    unittest.main()
