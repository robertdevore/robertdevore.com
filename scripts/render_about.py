#!/usr/bin/env python3
"""Render the reviewed disclosure snapshot into the generated About page, offline."""
import datetime as dt
from html import escape
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'assets/data/security-discoveries.json'


def load_discoveries(path=DATA):
    data = json.loads(path.read_text())
    records = data['discoveries']
    ids = [r['cve'] for r in records]
    if len(ids) != len(set(ids)) or len(ids) != data['wordfence_discoveries']:
        raise ValueError('Discovery count or duplicate CVE mismatch')
    for r in records:
        if not re.fullmatch(r'CVE-\d{4}-\d{4,}', r['cve']):
            raise ValueError('Invalid CVE ID')
        if not any('Robert DeVore' in credit for credit in r['attribution']):
            raise ValueError('Missing researcher credit')
        for key in ('published', 'wordfence_published', 'verified_on'):
            dt.date.fromisoformat(r[key])
        score = r['cvss_score']
        expected = 'Critical' if score >= 9 else 'High' if score >= 7 else 'Medium' if score >= 4 else 'Low'
        if not 0 <= score <= 10 or r['severity'] != expected:
            raise ValueError('Invalid severity or score')
        for key in ('primary_reference', 'attribution_source', 'cve_record', 'wordfence_profile'):
            url = urlparse(r[key])
            if url.scheme != 'https' or url.hostname not in {'github.com', 'www.wordfence.com', 'patchstack.com'} or url.username or url.password:
                raise ValueError('Unapproved research URL')
    return data


def render(data):
    records = sorted(data['discoveries'], key=lambda r: (r['published'], r['cve']), reverse=True)
    selected, rows = [], []
    for record in records:
        r = {k: escape(str(v), quote=True) for k, v in record.items()}
        score = f'{r["severity"]} · {r["cvss_score"]}'
        if record['selected']:
            selected.append(f'<article><p class="about-record-id">{r["cve"]} <span>{score}</span></p><h4>{r["product"]}</h4><p>{r["vulnerability_type"]}</p><a href="{r["primary_reference"]}">Read advisory <span class="sk-visually-hidden">for {r["cve"]}</span>↗</a></article>')
        rows.append(f'<li data-severity="{r["severity"]}"><div class="about-record-heading"><h4><a href="{r["cve_record"]}">{r["cve"]}</a></h4><span class="sk-badge">{score}</span></div><p class="about-record-product">{r["product"]}</p><p>{r["vulnerability_type"]}</p><dl><div><dt>Published</dt><dd><time datetime="{r["published"]}">{r["published"]}</time></dd></div><div><dt>CVSS 3.1 source</dt><dd>{r["score_source"]}</dd></div></dl><p class="about-record-links"><a href="{r["primary_reference"]}">Advisory</a><a href="{r["attribution_source"]}">Researcher credit</a></p></li>')
    return '<div class="about-selected-grid" data-no-scramble>'+''.join(selected)+'</div>', '<ul id="disclosure-records" class="about-records" data-no-scramble>'+''.join(rows)+'</ul>'


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'output'
    data = load_discoveries()
    selected, index = render(data)
    path = root / 'about/index.html'
    text = path.read_text()
    for marker, value in {'<!-- SECURITY_SELECTED -->': selected, '<!-- SECURITY_INDEX -->': index, '<!-- DISCOVERY_COUNT -->': str(len(data['discoveries']))}.items():
        if text.count(marker) != 1:
            raise ValueError(f'Expected one About marker: {marker}')
        text = text.replace(marker, value)
    path.write_text(text)
    print(f'About: rendered {len(data["discoveries"])} verified disclosures offline')


if __name__ == '__main__':
    main()
