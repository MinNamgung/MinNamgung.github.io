#!/usr/bin/env python3
"""Build static HTML from content/*.md. Requires Python 3 standard library only."""
from pathlib import Path
import re
from hashlib import sha256
from html import escape, unescape
ROOT = Path(__file__).resolve().parent

SECTION_EMOJI = {'news': '📰', 'research': '✒️', 'service': '📝', 'recent-work': '✨', 'teaching': '📚'}

def section_emoji(name):
    emoji = SECTION_EMOJI.get(name)
    return f'<span class="section-emoji" aria-hidden="true">{emoji}</span>' if emoji else ''

SOCIAL_ICONS = {
    'Google Scholar': '<path d="m2 9 10-6 10 6-10 6L2 9Z"/><path d="M6 12v6c4 3 8 3 12 0v-6M22 9v8"/>',
    'GitHub': '<path d="M9 19c-4 1-4-2-6-2m12 5v-4c0-1 .1-1.4-.5-2 3-.3 6-1.5 6-6a5 5 0 0 0-1.4-3.5A4.6 4.6 0 0 0 19 3s-1 0-3 1.5a12 12 0 0 0-7 0C7 3 6 3 6 3a4.6 4.6 0 0 0-.1 3.5A5 5 0 0 0 4.5 10c0 4.5 3 5.7 6 6-.6.6-.5 1-.5 2v4"/>',
    'LinkedIn': '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 10v7M7 7v.01M11 17v-7m0 3a3 3 0 0 1 6 0v4"/>',
}

def link_html(match):
    label = match[1]
    glyph = ('<svg class="social-icon" width="14" height="14" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'+SOCIAL_ICONS[label]+'</svg>') if label in SOCIAL_ICONS else ''
    return f'<a href="{escape(unescape(match[2]), quote=True)}">{glyph}{label}</a>'

def inline(text):
    text = escape(text, quote=False)
    text = re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)', link_html, text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
    return text

def markdown(text):
    """Supported: paragraphs, headings, flat lists, links, bold and italic."""
    out, paragraph, listing = [], [], False
    def flush():
        if paragraph:
            out.append('<p>'+inline(' '.join(paragraph)).replace('␤', '<br>')+'</p>')
            paragraph.clear()
    for line in text.strip().splitlines()+['']:
        if line.startswith('- '):
            flush()
            if not listing: out.append('<ul>'); listing=True
            out.append('<li>'+inline(line[2:])+'</li>')
        else:
            if listing: out.append('</ul>'); listing=False
            heading = re.match(r'^(#{1,6}) (.+)$',line)
            if heading:
                flush(); level=len(heading[1]); out.append(f'<h{level}>'+inline(heading[2])+f'</h{level}>')
            elif not line.strip(): flush()
            else: paragraph.append(line.rstrip()+'␤' if line.endswith('  ') else line)
    return '\n'.join(out)

def content(name):
    text = (ROOT/'content'/f'{name}.md').read_text()
    if text.startswith('---\n'):
        _, header, text = text.split('---', 2)
        meta = dict(line.split(': ', 1) for line in header.strip().splitlines())
        return f'<article class="publication"><a class="pub-figure" href="{escape(meta["image"], quote=True)}" aria-label="View recent work figure"><img src="{escape(meta["image"], quote=True)}" alt="{escape(meta["image_alt"], quote=True)}" width="200" height="140" loading="lazy"></a><div class="pub-body">{markdown(text)}</div></article>'
    return markdown(text)
def section(id,title,body,extra=''):
    return f'<section id="{id}" aria-labelledby="{id}-title"><div class="section-heading"><h2 id="{id}-title">{section_emoji(id)}{title}</h2>{extra}</div>{body}</section>'

articles=[]
for file in sorted((ROOT/'content/publications').glob('*.md')):
    _, header, body=file.read_text().split('---',2)
    meta=dict(line.split(': ',1) for line in header.strip().splitlines())
    body=body.strip(); title,body=body.split('\n',1)
    title=title.removeprefix('# ')
    visual = (f'<a class="pub-figure" href="{escape(meta["image"], quote=True)}" aria-label="View figure: {escape(title, quote=True)}"><img src="{escape(meta["image"], quote=True)}" alt="{escape(meta.get("image_alt", title), quote=True)}" width="200" height="140" loading="lazy"></a>' if meta.get('image') else f'<div class="pub-meta"><span class="pub-year">{escape(meta["year"])}</span><span class="pub-type">{escape(meta["type"])}</span></div>')
    articles.append(f'''<article class="publication" data-selected="{meta['selected']}">
    {visual}
    <div class="pub-body"><h3>{inline(title)}</h3>{markdown(body)}<div class="venue">{escape(meta['venue'])} · {escape(meta['year'])}</div></div></article>''')
profile_html = content('profile')
profile_links = re.findall(r'<a href="([^"]+)">(?:<svg.*?</svg>)?([^<]+)</a>', profile_html)
social_links = []
cv_html = ''
for url, label in profile_links:
    if label == 'Curriculum vitae':
        cv_html = f'<div class="cv-row"><a class="cv-link" href="{url}"><span aria-hidden="true">📄</span> Curriculum vitae</a></div>'
    else:
        glyph = '<svg class="social-icon" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'+SOCIAL_ICONS[label]+'</svg>'
        social_links.append(f'<a href="{url}">{glyph}{label}</a>')
links_html = ''.join(social_links)
style_version = sha256((ROOT/'style.css').read_bytes()).hexdigest()[:10]
page=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Min Namgung's Homepage</title>
<meta name="description" content="Min Namgung is a Ph.D. candidate at the University of Minnesota researching multimodal representation learning and spatial AI.">
<meta name="theme-color" content="#87384b"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css?v={style_version}"></head>
<body><a class="skip-link" href="#main">Skip to content</a>

<main id="main" class="page-layout"><header class="intro"><div class="intro-text"><h1>Min Namgung</h1>{content('about')}<p class="email">Email: namgu007 AT umn.edu</p><nav class="profile-links" aria-label="Profile links">{links_html}</nav>{cv_html}</div><img class="portrait" src="assets/portrait.jpg" alt="Min Namgung" width="270"></header>
{section('news','News',content('news'))}
{section('research','Selected publications','<div class="publications">'+''.join(articles)+'</div>')}
{section('recent-work','Recent work',content('recent-work'))}
{section('teaching','Teaching',content('teaching'))}
{section('service','Service','<p class="section-note">Program committee & reviewing</p>'+content('service'))}
<footer><span>© 2026 Min Namgung</span><span>Updated November 2026</span></footer>
</main></body></html>'''
(ROOT/'index.html').write_text(page)
print(f'Built concise homepage with {len(articles)} selected publications.')
