#!/usr/bin/env python3
"""Build the static site: wraps content/pages/*.html and content/posts/*.html in the shared
header/footer and writes the output next to this repo's index.html.  Run: python3 tools/build.py"""
import json, os, re, html, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://www.megmaginnlcsw.com'
NAME = 'Meg Maginn L.C.S.W'
PHONE = '6317247152'
PHONE_FMT = '+1 (631) 724-7152'
EMAIL = 'office@megmaginnlcsw.com'
YEAR = datetime.date.today().year

NAV = [('/', 'Home'), ('/offerings/', 'Offerings'), ('/bio/', 'Bio'), ('/contact/', 'Contact'), ('/resources/', 'Resources')]

SOCIAL = '''<div class="social">
  <a href="https://www.linkedin.com/in/meg-maginn/" aria-label="LinkedIn" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.13 1.45-2.13 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.55V9h3.57v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg></a>
  <a href="https://www.instagram.com/megmaginnlcsw/" aria-label="Instagram" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 3.25.15 4.77 1.69 4.92 4.92.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.15 3.23-1.66 4.77-4.92 4.92-1.27.06-1.64.07-4.85.07s-3.58-.01-4.85-.07c-3.26-.15-4.77-1.7-4.92-4.92C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85C2.38 3.92 3.9 2.38 7.15 2.23 8.42 2.17 8.8 2.16 12 2.16zM12 0C8.74 0 8.33.01 7.05.07 2.7.27.27 2.69.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.2 4.36 2.62 6.78 6.98 6.98C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c4.35-.2 6.78-2.62 6.98-6.98.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.2-4.35-2.62-6.78-6.98-6.98C15.67.01 15.26 0 12 0zm0 5.84A6.16 6.16 0 1 0 12 18.16 6.16 6.16 0 0 0 12 5.84zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.4-11.85a1.44 1.44 0 1 0 0 2.88 1.44 1.44 0 0 0 0-2.88z"/></svg></a>
  <a href="https://www.facebook.com/megmaginn" aria-label="Facebook" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.8-4.7 4.54-4.7 1.31 0 2.68.24 2.68.24v2.97h-1.5c-1.5 0-1.96.93-1.96 1.88v2.26h3.32l-.53 3.49h-2.8V24C19.62 23.1 24 18.1 24 12.07z"/></svg></a>
</div>'''

def header(cur):
    links = ''.join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == cur else '', t) for h, t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="top" id="top">
  <div class="wrap">
    <a class="logo" href="/" aria-label="{NAME} — home"><img src="/img/logo.png" alt="Meg Maginn L.C.S.W" width="900" height="232"></a>
    <nav class="nav" aria-label="Main">{links}<a class="btn" href="sms:{PHONE}">Send a Text</a></nav>
    {SOCIAL}
    <a class="btn" href="sms:{PHONE}">Send a Text</a>
    <button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="top"><span></span><span></span><span></span></button>
  </div>
</header>'''

FOOTER = f'''<footer class="foot">
  <div class="wrap">
    <h4>Copyright © Meg Maginn {YEAR}</h4>
    <div class="links"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:{PHONE}">{PHONE_FMT}</a></div>
  </div>
</footer>
<script src="/site.js"></script>'''

def page(path, title, desc, body, cur=None, og_image='/img/meg-bio.jpg', extra_head='', ptype='website', out=None):
    full = NAME if path == '/' else f'{title} — {NAME}'
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="{ptype}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#fafafa">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="stylesheet" href="/style.css">
{extra_head}</head>
<body>
{header(cur)}
<main id="main">
{body}
</main>
{FOOTER}
</body>
</html>
'''
    out = out or (ROOT / path.strip('/') / 'index.html' if path != '/' else ROOT / 'index.html')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding='utf-8')
    return path

def read_meta(p):
    t = p.read_text(encoding='utf-8')
    m = re.match(r'<!--META\s*(\{.*?\})\s*-->\s*', t, re.S)
    return json.loads(m.group(1)), t[m.end():]

def nice_date(d):
    return datetime.date.fromisoformat(d).strftime('%B %-d, %Y')

def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

# ---------- posts ----------
posts = []
for p in sorted((ROOT / 'content' / 'posts').glob('*.html')):
    meta, body = read_meta(p); meta['slug'] = p.stem; meta['body'] = body; posts.append(meta)
posts.sort(key=lambda m: m['date'], reverse=True)
cats = sorted({m['category'] for m in posts})

def post_card(m):
    return f'''<article class="post" data-cat="{slugify(m['category'])}">
  <a href="/resources/{m['slug']}/"><img src="/img/{m['image']}" alt="" loading="lazy" width="1200" height="1500"></a>
  <p class="meta"><a href="/resources/?c={slugify(m['category'])}">{html.escape(m['category'])}</a> · {nice_date(m['date'])}</p>
  <h2><a href="/resources/{m['slug']}/">{html.escape(m['title'])}</a></h2>
  <p class="excerpt">{html.escape(m['excerpt'])}</p>
  <a class="more" href="/resources/{m['slug']}/">Read More</a>
</article>'''

urls = []
for i, m in enumerate(posts):
    newer = posts[i - 1] if i > 0 else None
    older = posts[i + 1] if i + 1 < len(posts) else None
    pager = ''
    if newer or older:
        pager = '<nav class="pager" aria-label="More articles">'
        if older: pager += f'<a class="prev" href="/resources/{older["slug"]}/"><span>Previous</span>{html.escape(older["title"])}</a>'
        if newer: pager += f'<a class="next" href="/resources/{newer["slug"]}/"><span>Next</span>{html.escape(newer["title"])}</a>'
        pager += '</nav>'
    tags = ''.join(f'<li>{html.escape(t)}</li>' for t in m['tags'])
    ld = json.dumps({"@context": "https://schema.org", "@type": "BlogPosting", "headline": m['title'], "datePublished": m['date'],
                     "author": {"@type": "Person", "name": "Meg Maginn"}, "image": f"{SITE}/img/{m['image']}", "description": m['description'],
                     "mainEntityOfPage": f"{SITE}/resources/{m['slug']}/"})
    body = f'''<section class="section">
  <article class="wrap article">
    <header>
      <h1>{html.escape(m['title'])}</h1>
      <p class="meta"><a href="/resources/?c={slugify(m['category'])}">{html.escape(m['category'])}</a> · {nice_date(m['date'])} · Written by Meg Maginn</p>
    </header>
    <img class="lead" src="/img/{m['image']}" alt="" width="1800" height="1200">
    <div class="body">
{m['body']}
    </div>
    <ul class="tags" aria-label="Tags">{tags}</ul>
    <div class="author"><img src="/img/meg-bio.jpg" alt=""><div><strong>Meg Maginn, L.C.S.W</strong><br>Psychotherapist, life coach, eating-disorder specialist. <a href="/bio/">About Meg</a></div></div>
    {pager}
  </article>
</section>'''
    urls.append(page(f'/resources/{m["slug"]}/', m['title'], m['description'], body, cur='/resources/',
                     og_image=f'/img/{m["image"]}', ptype='article',
                     extra_head=f'<script type="application/ld+json">{ld}</script>\n'))

# ---------- resources listing ----------
filters = '<li><a href="/resources/" data-cat="" aria-current="true">All</a></li>' + ''.join(
    f'<li><a href="/resources/?c={slugify(c)}" data-cat="{slugify(c)}">{html.escape(c)}</a></li>' for c in cats)
listing = f'''<section class="section tight"><div class="wrap call-row"><a class="btn" href="tel:{PHONE}">Call Now</a></div></section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <h1 class="visually-hidden" style="position:absolute;left:-999px">Resources</h1>
    <ul class="filters" id="filters">{filters}</ul>
    <div class="posts" id="posts">
{''.join(post_card(m) for m in posts)}
    </div>
  </div>
</section>'''
urls.append(page('/resources/', 'Resources', 'Articles by Meg Maginn, L.C.S.W on eating disorders, trauma, EMDR, ketamine integration and emotional wellbeing.',
                 listing, cur='/resources/', og_image='/img/post-emdr.jpg'))

# ---------- regular pages ----------
PAGES = [
    ('/', 'index', 'Meg Maginn L.C.S.W | Unlock Your True Story', 'Discover transformative psychotherapy and coaching with Meg Maginn, L.C.S.W., to reshape your narrative and embrace authentic living. Explore offerings and contact today.', '/img/meg-home.jpg'),
    ('/offerings/', 'offerings', 'Offerings', 'Virtual Eating Disorder Recovery Program, Psychotherapy / Transformational Coaching, Virtual EMDR Therapy, Ketamine/Psychedelic Integration Therapy.', '/img/banner-offerings.jpg'),
    ('/bio/', 'bio', 'Bio', 'Meg Maginn, LCSW, is a distinguished psychotherapist with over 30 years of experience in mental health treatment. Founder and director of Eating Disorder Associates and Lifeworks NY.', '/img/meg-bio.jpg'),
    ('/contact/', 'contact', 'Contact', 'Feeling overwhelmed, stuck, or uncertain about your path forward can be a challenging and isolating experience. You don’t have to navigate those changes alone.', '/img/banner-contact.jpg'),
    ('/recovery/', 'recovery', 'Virtual Eating Disorder Recovery Program', 'This virtual recovery program is designed to help you break free from destructive patterns and reclaim your life, using evidence-based treatment, neuroscience-rooted interventions and personalized coaching.', '/img/recovery.jpg'),
    ('/psychotherapy/', 'psychotherapy', 'Psychotherapy / Transformational Coaching', 'Embark on a journey dedicated to personal healing and growth. This program is designed for individuals or couples seeking profound change and navigating challenges in their personal lives and relationship.', '/img/psychotherapy.jpg'),
    ('/emdr/', 'emdr', 'Virtual EMDR Therapy', 'Eye Movement Desensitization and Reprocessing (EMDR) therapy is a groundbreaking treatment traditionally used for trauma but also effective for anxiety, depression, phobias, stress, and more. Virtual EMDR offers flexible scheduling and privacy.', '/img/emdr.jpg'),
    ('/integration/', 'integration', 'Ketamine/Psychedelic Integration Therapy', 'Embark on a transformative journey of healing through Ketamine and Psychedelic Integration Therapy with a pioneering psychotherapist at the forefront of psychedelic-assisted therapy.', '/img/integration.jpg'),
    ('/404.html', '404', 'Page not found', 'That page does not exist.', '/img/meg-bio.jpg'),
]
STAIR = '''<section class="section bright stair">
  <div class="wrap">
    <blockquote>“You don’t have to see the whole staircase, just take the first step.”<cite>Martin Luther King Jr.</cite></blockquote>
    <img src="/img/staircase.jpg" alt="Spiral staircase seen from above" loading="lazy" width="1800" height="1202">
  </div>
</section>'''
cur_of = {'/recovery/': '/offerings/', '/psychotherapy/': '/offerings/', '/emdr/': '/offerings/', '/integration/': '/offerings/'}
for path, frag, title, desc, og in PAGES:
    body = (ROOT / 'content' / 'pages' / f'{frag}.html').read_text(encoding='utf-8')
    body = body.replace('{{PHONE}}', PHONE).replace('{{EMAIL}}', EMAIL).replace('{{STAIRCASE}}', STAIR)
    if path == '/404.html':  # GitHub Pages serves /404.html for missing URLs
        page(path, title, desc, body, og_image=og, out=ROOT / '404.html')
    else:
        urls.append(page(path, title, desc, body, cur=cur_of.get(path, path), og_image=og))

# ---------- sitemap / robots ----------
today = datetime.date.today().isoformat()
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
    f'  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n' for u in sorted(set(urls))) + '</urlset>\n'
(ROOT / 'sitemap.xml').write_text(sm)
(ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
print(f'built {len(urls)} pages, {len(posts)} posts')
