import unittest
from src.nassli_audit.audit import PageHTML, analyze_html, validate_config, to_markdown

SAMPLE = '''<!doctype html><html lang="en"><head><title>Nassli LED | Project Lighting</title>
<meta name="description" content="Saudi lighting solutions for projects">
<link rel="canonical" href="https://nassli-led.com.sa/">
<link rel="alternate" hreflang="ar-SA" href="https://nassli-led.com.sa/ar/">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"Nassli"}</script>
</head><body><h1>Lighting for Projects</h1><img src="/a.jpg" alt="LED lights"/></body></html>'''

class TestAnalysis(unittest.TestCase):
    def test_good_document(self):
        result = analyze_html(SAMPLE, 'https://nassli-led.com.sa/')
        self.assertEqual(result['h1'], ['Lighting for Projects'])
        self.assertEqual(result['jsonld_blocks'], 1)
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

    def test_config_rejects_external_paths(self):
        c = {"base_url": "https://nassli-led.com.sa", "pages": [{"path":"//evil.test"}]}
        with self.assertRaises(ValueError): validate_config(c)
        c['pages'][0]['path'] = '/products/'
        validate_config(c)

    def test_report_render(self):
        report = {"generated_at": "2026-10-20", "scope":"sample", "base_url":"https://nassli-led.com.sa", "discovery":{}, "pages":[{"path":"/", "status":200, "title":"Home", "h1":["Home"], "issues":[]}]}
        self.assertIn('| / | 200 | Home |', to_markdown(report))

if __name__ == '__main__':
    unittest.main()
