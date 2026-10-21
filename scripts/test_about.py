#!/usr/bin/env python3
"""Offline regression checks for disclosure provenance and safe rendering."""
import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from bs4 import BeautifulSoup
from render_about import load_discoveries, render


class AboutResearchTests(unittest.TestCase):
    def setUp(self):
        self.data = load_discoveries()

    def test_complete_attributed_snapshot(self):
        self.assertEqual(len(self.data['discoveries']), 40)
        self.assertEqual(sum(r['selected'] for r in self.data['discoveries']), 6)
        self.assertEqual(sum(r['score_source'] == 'Wordfence' for r in self.data['discoveries']), 9)
        self.assertEqual(sum(r['score_source'] == 'Patchstack' for r in self.data['discoveries']), 31)
        for row in self.data['discoveries']:
            self.assertIn(row['primary_reference'], row['references'])
            self.assertIn(row['cve'], row['attribution_source'])

    def test_duplicate_and_unsafe_url_rejected(self):
        for mutation in ('duplicate', 'unsafe'):
            data = copy.deepcopy(self.data)
            if mutation == 'duplicate':
                data['discoveries'][1] = data['discoveries'][0]
            else:
                data['discoveries'][0]['primary_reference'] = 'javascript:alert(1)'
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'data.json'
                path.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    load_discoveries(path)

    def test_untrusted_product_is_text(self):
        self.data['discoveries'][0]['product'] = '<img src=x onerror=alert(1)>'
        selected, index = render(self.data)
        soup = BeautifulSoup(selected + index, 'html.parser')
        self.assertFalse(soup.select('img, script, [onerror]'))
        self.assertIn('<img src=x onerror=alert(1)>', soup.get_text())

    def test_generated_page_contract(self):
        page = BeautifulSoup((Path(os.environ.get('ABOUT_OUTPUT', 'output')) / 'about/index.html').read_text(), 'html.parser')
        self.assertEqual(len(page.select('h1')), 1)
        self.assertEqual(len(page.select('#disclosure-records > li')), 40)
        self.assertEqual(len(page.select('.about-selected-grid article')), 6)
        self.assertTrue(page.select_one('.about-filter').has_attr('hidden'))
        self.assertEqual([o.get('value') for o in page.select('#disclosure-severity option')], ['', 'High', 'Medium'])
        self.assertFalse(page.select_one('#disclosure-index').has_attr('open'))
        for row in page.select('#disclosure-records > li'):
            self.assertTrue(row.select_one('time[datetime]'))
            self.assertEqual(len(row.select('a')), 3)
        graph = json.loads(page.select_one('script[type="application/ld+json"]').string)['@graph']
        person = next(n for n in graph if n['@type'] == 'Person')
        about = next(n for n in graph if n['@type'] == 'AboutPage')
        self.assertEqual(about['mainEntity']['@id'], person['@id'])
        self.assertEqual(len([n for n in graph if n['@type'] == 'SoftwareSourceCode']), 4)
        self.assertEqual(page.select_one('link[rel="canonical"]')['href'], 'https://robertdevore.com/about/')


if __name__ == '__main__':
    unittest.main()
