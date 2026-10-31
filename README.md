# megmaginnlcsw.com

Static rebuild of Meg Maginn's site (formerly Squarespace), hosted on GitHub Pages.

## Editing
- Page text lives in `content/pages/*.html` (one fragment per page).
- Articles live in `content/posts/<slug>.html`: a `<!--META {…} -->` block (title, description, date, category, tags, image, excerpt) followed by plain HTML. Add a file, drop its image in `img/`, rebuild.
- Shared header, footer, nav, SEO tags and the sitemap come from `tools/build.py`.
- Styles: `style.css` (self-hosted Epilogue + Pontano Sans in `fonts/`). Behaviour: `site.js`.

## Build & preview
```
python3 tools/build.py          # regenerates every index.html, 404.html, sitemap.xml, robots.txt
python3 -m http.server 8791     # http://localhost:8791/
```
Commit the generated files too; GitHub Pages serves the repo as-is (`.nojekyll`).

## Domain
Add a `CNAME` file containing `www.megmaginnlcsw.com` when the DNS is moved off Squarespace.
