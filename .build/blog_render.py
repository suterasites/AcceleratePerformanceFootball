#!/usr/bin/env python3
"""
Accelerate Performance Football - blog generator.

Deterministic. Reads structured post sources from blog/_posts/*.json and renders:
  - blog/<slug>.html         (one full article page per post, brand chrome + BlogPosting schema)
  - blog.html                (index page: hero + newest-first card grid)
  - sitemap.xml              (adds/refreshes /blog and every /blog/<slug> entry)

Run from the site root:  python3 .build/blog_render.py

Why a generator (not hand-written HTML each week): posts auto-publish weekly with no
human review, so the page chrome (nav, footer, head, schema) must be identical and correct
every time. The weekly agent only authors one JSON file; everything structural is locked here.

Post JSON schema (see blog/_posts/README for the canonical copy):
{
  "slug": "junior-to-senior-football",     # url-safe, no spaces
  "title": "From Junior to Senior Football: What Changes and How to Prepare",
  "description": "<=160 chars meta description",
  "category": "Junior Development",         # shows as the kicker label
  "date": "2026-07-22",                     # YYYY-MM-DD, Melbourne date
  "author": "APF Coaching Team",            # optional, defaults to APF Coaching Team
  "read_minutes": 0,                         # optional, 0 = auto from word count
  "blocks": [                                # article body, in order
    {"type": "lead", "text": "..."},        # opening paragraph, larger
    {"type": "h2", "text": "..."},
    {"type": "h3", "text": "..."},
    {"type": "p", "text": "..."},
    {"type": "ul", "items": ["...", "..."]},
    {"type": "ol", "items": ["...", "..."]},
    {"type": "quote", "text": "..."}
  ],
  "cta": {"heading": "Ready to make the jump?", "text": "One line under the heading."}
}
Inline markup allowed inside any text/item: **bold** and [label](url). Em dashes are
auto-normalised to hyphens (hard brand rule).
"""

import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_chrome  # the top bar, menu and footer shared with every other page

SITE = "https://www.accelerateperformancefootball.com.au"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(ROOT, "blog", "_posts")
BLOG_OUT_DIR = os.path.join(ROOT, "blog")
INDEX_OUT = os.path.join(ROOT, "blog.html")
SITEMAP = os.path.join(ROOT, "sitemap.xml")

DEFAULT_AUTHOR = "APF Coaching Team"


# ----------------------------------------------------------------------------- helpers

def no_dashes(s: str) -> str:
    """Enforce the hard no-em-dash / no-en-dash brand rule everywhere."""
    return s.replace("—", " - ").replace("–", "-")


def inline(text: str) -> str:
    """Escape text, then re-enable a tiny safe markup subset: **bold** and [label](url)."""
    text = no_dashes(text)
    out = html.escape(text, quote=False)
    # links: [label](url)  ->  <a href="url">label</a>
    out = re.sub(
        r"\[([^\]]+)\]\((https?://[^\s)]+|[^\s)]+\.html[^\s)]*|/[^\s)]*)\)",
        r'<a href="\2">\1</a>',
        out,
    )
    # bold: **text**
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    return out


def word_count(post: dict) -> int:
    n = 0
    for b in post.get("blocks", []):
        if b.get("type") in ("lead", "h2", "h3", "p", "quote"):
            n += len(re.findall(r"\w+", b.get("text", "")))
        elif b.get("type") in ("ul", "ol"):
            for it in b.get("items", []):
                n += len(re.findall(r"\w+", it))
    return n


def read_minutes(post: dict) -> int:
    if post.get("read_minutes"):
        return int(post["read_minutes"])
    return max(1, round(word_count(post) / 200))


def pretty_date(iso: str) -> str:
    y, m, d = iso.split("-")
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    return f"{int(d)} {months[int(m) - 1]} {y}"


# ----------------------------------------------------------------------------- seo helpers

def normalize_headings(doc: str) -> str:
    """Renumber the heading outline so no level is skipped (the on-page audit
    flags H2->H4 / H1->H3 jumps). A stack maps each original level to a tight
    emitted level, so sibling headings stay consistent."""
    norm: list = []
    pair: list = []

    def rep(m):
        tag = m.group(0)
        lvl = int(m.group(2))
        if m.group(1) == "/":
            return f"</h{pair.pop() if pair else lvl}>"
        while norm and norm[-1][0] >= lvl:
            norm.pop()
        emitted = min(norm[-1][1] + 1 if norm else 1, 6)
        norm.append((lvl, emitted))
        pair.append(emitted)
        if emitted == lvl:
            return tag
        return f"<h{emitted}{tag[3:-1]}>"

    return re.sub(r"<(/?)h([1-6])\b[^>]*>", rep, doc)


def breadcrumb_ld(trail: list) -> str:
    """A BreadcrumbList JSON-LD block. trail = [(name, url_or_None), ...]."""
    items = []
    for i, (name, url) in enumerate(trail, 1):
        it = {"@type": "ListItem", "position": i, "name": no_dashes(name)}
        if url is not None:
            it["item"] = url
        items.append(it)
    obj = {"@context": "https://schema.org", "@type": "BreadcrumbList",
           "itemListElement": items}
    return ('  <script type="application/ld+json">\n  '
            + json.dumps(obj, indent=2).replace("\n", "\n  ") + "\n  </script>\n")


# ----------------------------------------------------------------------------- chrome

def head(prefix: str, *, title: str, description: str, canonical: str,
         og_type: str, extra_schema: str) -> str:
    description = no_dashes(html.escape(description, quote=True))
    title = no_dashes(html.escape(title, quote=True))
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <!-- Google tag (gtag.js) - GA4 G-7P2NC2YGW2 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-7P2NC2YGW2"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-7P2NC2YGW2');
  </script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="96x96" href="/Assets/favicon-96.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#0A0A0A">
  <meta name="description" content="{description}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canonical}">
  <link rel="apple-touch-icon" href="/Assets/apple-touch-icon.png">

  <meta property="og:type" content="{og_type}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/Assets/Logo.png">
  <meta property="og:locale" content="en_AU">
  <meta property="og:site_name" content="Accelerate Performance Football">
  <meta name="geo.region" content="AU-VIC">
  <meta name="geo.placename" content="West Melbourne, Victoria">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{SITE}/Assets/Logo.png">

{extra_schema}
{site_chrome.head_assets(prefix)}  <!-- Sutera lead events (GA4) -->
  <script>/* SUTERA_LEAD_EVENTS */
  (function(){{
    function ev(n, p){{ if (typeof window.gtag === 'function') {{ window.gtag('event', n, Object.assign({{transport_type:'beacon'}}, p||{{}})); }} }}
    document.addEventListener('click', function(e){{
      var a = e.target.closest ? e.target.closest('a[href^="tel:"]') : null;
      if (a) ev('click_to_call', {{ link_url: a.getAttribute('href') }});
    }}, true);
    document.addEventListener('submit', function(e){{
      var f = e.target;
      if (!f || f.tagName !== 'FORM' || f.hasAttribute('data-no-lead')) return;
      var action = f.getAttribute('action') || '';
      var isLead = /formspree/i.test(action) || f.querySelector('input[type="email"], input[type="tel"], textarea');
      if (isLead) ev('generate_lead', {{ form_id: f.id || f.getAttribute('name') || 'contact' }});
    }}, true);
  }})();
  </script>
</head>
<body>

  <a href="#main" class="skip-link">Skip to main content</a>
"""


def nav(prefix: str) -> str:
    return "\n  " + site_chrome.nav(prefix) + "\n"


def footer(prefix: str) -> str:
    return "\n  " + site_chrome.footer(prefix) + "\n\n</body>\n</html>\n"


# ----------------------------------------------------------------------------- blocks

def render_blocks(blocks: list) -> str:
    parts = []
    for b in blocks:
        t = b.get("type")
        if t == "lead":
            parts.append(f'<p class="lead">{inline(b["text"])}</p>')
        elif t == "p":
            parts.append(f"<p>{inline(b['text'])}</p>")
        elif t == "h2":
            parts.append(f"<h2>{inline(b['text'])}</h2>")
        elif t == "h3":
            parts.append(f"<h3>{inline(b['text'])}</h3>")
        elif t == "quote":
            parts.append(f"<blockquote>{inline(b['text'])}</blockquote>")
        elif t in ("ul", "ol"):
            items = "".join(f"<li>{inline(it)}</li>" for it in b.get("items", []))
            parts.append(f"<{t}>{items}</{t}>")
    return "\n            ".join(parts)


# ----------------------------------------------------------------------------- pages

def post_schema(post: dict, canonical: str) -> str:
    obj = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
        "headline": no_dashes(post["title"]),
        "description": no_dashes(post["description"]),
        "datePublished": post["date"],
        "dateModified": post["date"],
        "author": {"@type": "Organization", "name": post.get("author", DEFAULT_AUTHOR),
                   "url": SITE + "/"},
        "publisher": {
            "@type": "Organization",
            "name": "Accelerate Performance Football",
            "logo": {"@type": "ImageObject", "url": SITE + "/Assets/Logo.png"},
        },
        "image": SITE + "/Assets/Logo.png",
        "articleSection": post.get("category", "Football Coaching"),
        "url": canonical,
    }
    crumb = breadcrumb_ld([("Home", SITE + "/"), ("Blog", SITE + "/blog"),
                           (post["title"], None)])
    return ('  <script type="application/ld+json">\n  '
            + json.dumps(obj, indent=2).replace("\n", "\n  ")
            + "\n  </script>\n" + crumb)


def render_post(post: dict, others: list) -> str:
    slug = post["slug"]
    canonical = f"{SITE}/blog/{slug}"
    # Post titles are descriptive enough on their own; appending the site name
    # pushes them past the 60-char target. Allow a per-post seo_title override.
    title_tag = post.get("seo_title", post["title"])
    cta = post.get("cta", {})
    cta_heading = no_dashes(cta.get("heading", "Ready to get to work?"))
    cta_text = no_dashes(cta.get("text",
                          "Book a session and we'll build a plan around exactly where you want to go."))

    # up to two "related" posts (newest others)
    related = [o for o in others if o["slug"] != slug][:2]
    related_html = ""
    if related:
        cards = []
        for o in related:
            cards.append(f"""      <a class="post-card reveal" href="{o['slug']}.html">
        <span class="label">{html.escape(no_dashes(o.get('category','')))}</span>
        <h3 class="h3">{html.escape(no_dashes(o['title']))}</h3>
        <span class="post-card-meta">Read article</span>
      </a>""")
        related_html = f"""
  <!-- RELATED -->
  <section class="band">
    <div class="head reveal"><div><p class="label label-soft">Keep reading</p></div><div></div></div>
    <div class="post-grid post-grid-2">
{chr(10).join(cards)}
    </div>
  </section>
"""

    doc = head(
        "../",
        title=title_tag,
        description=post["description"],
        canonical=canonical,
        og_type="article",
        extra_schema=post_schema(post, canonical),
    )
    doc += nav("../")
    doc += f"""
  <main id="main">

  <!-- ARTICLE -->
  <article>
    <header id="main-content" class="page-head">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / <a href="../blog.html">Blog</a> / <span>{html.escape(no_dashes(post['title']))}</span></nav>
      <p class="label label-soft">{html.escape(no_dashes(post.get('category','')))}</p>
      <h1 class="h1-page">{html.escape(no_dashes(post['title']))}</h1>
    </header>

    <div class="article on-white">
      <div class="article-meta label">
        <span>{pretty_date(post['date'])}</span>
        <span>{read_minutes(post)} min read</span>
        <span>{html.escape(no_dashes(post.get('author', DEFAULT_AUTHOR)))}</span>
      </div>
      <div>
        <div class="prose reveal">
            {render_blocks(post['blocks'])}
        </div>

        <!-- inline CTA -->
        <div class="article-cta">
          <h2 class="h3">{html.escape(cta_heading)}</h2>
          <p class="text">{html.escape(cta_text)}</p>
          <div class="btn-row">
            <a class="btn" href="../contact.html">Book a Session</a>
            <a class="btn btn-line" href="../services.html">View Programs</a>
          </div>
        </div>

        <p class="links label article-back"><a href="../blog.html"><span>All articles</span></a></p>
      </div>
    </div>
  </article>
{related_html}
  </main>
"""
    doc += footer("../")
    return no_dashes(doc)


def render_index(posts: list) -> str:
    canonical = f"{SITE}/blog"
    schema = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "@id": canonical,
        "name": "Accelerate Performance Football Blog",
        "description": "Football coaching insights, drills, and player development guides from a private coaching team in West Melbourne.",
        "url": canonical,
        "publisher": {"@type": "Organization", "name": "Accelerate Performance Football",
                      "logo": {"@type": "ImageObject", "url": SITE + "/Assets/Logo.png"}},
        "blogPost": [
            {"@type": "BlogPosting", "headline": no_dashes(p["title"]),
             "url": f"{SITE}/blog/{p['slug']}", "datePublished": p["date"]}
            for p in posts
        ],
    }
    schema_tag = ('  <script type="application/ld+json">\n  '
                  + json.dumps(schema, indent=2).replace("\n", "\n  ")
                  + "\n  </script>\n"
                  + breadcrumb_ld([("Home", SITE + "/"), ("Blog", None)]))

    doc = head(
        "",
        title="Football Coaching Blog | Accelerate Performance Football",
        description="Football coaching insights, skills drills, and player development guides for juniors and seniors across West Melbourne. New articles every week.",
        canonical=canonical,
        og_type="website",
        extra_schema=schema_tag,
    )
    doc += nav("")
    doc += """
  <main id="main">

  <!-- HERO -->
  <header id="main-content" class="hero hero-page frame">
    <img class="frame-media" width="500" height="625" src="Assets/Chris and Senior Players.jpeg" alt="" fetchpriority="high" style="object-position: 55% 62%;">
    <div class="frame-scrim" aria-hidden="true"></div>
    <div class="frame-copy">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <span>Blog</span></nav>
      <p class="label hero-label">The Blog</p>
      <h1 class="display">Coaching notes<br>and player guides.</h1>
      <p class="text hero-text">Practical football insight from our Melbourne-based coaches. Technique, conditioning, decision-making, and how to actually get better between sessions. New articles every week.</p>
    </div>
  </header>

  <!-- POSTS -->
"""
    if not posts:
        doc += '  <section class="band"><p class="text band-text">Articles are on the way. Check back soon.</p></section>\n'
    else:
        feat = posts[0]
        doc += f"""  <section class="band">
    <a class="post-feature reveal" href="blog/{feat['slug']}.html">
      <div class="post-feature-meta label"><span>Latest</span><span>{html.escape(no_dashes(feat.get('category','')))}</span><span>{pretty_date(feat['date'])}</span><span>{read_minutes(feat)} min read</span></div>
      <h2 class="h1-page">{html.escape(no_dashes(feat['title']))}</h2>
      <p class="text">{html.escape(no_dashes(feat['description']))}</p>
      <span class="btn">Read article</span>
    </a>
  </section>
"""
        rest = posts[1:]
        if rest:
            cards = []
            for post in rest:
                cards.append(f"""      <a class="post-card reveal" href="blog/{post['slug']}.html">
        <span class="label">{html.escape(no_dashes(post.get('category','')))}</span>
        <h3 class="h3">{html.escape(no_dashes(post['title']))}</h3>
        <p class="text">{html.escape(no_dashes(post['description']))}</p>
        <span class="post-card-meta">{pretty_date(post['date'])} / {read_minutes(post)} min read</span>
      </a>""")
            doc += '  <section class="band on-white">\n    <div class="post-grid">\n'
            doc += "\n".join(cards)
            doc += "\n    </div>\n  </section>\n"
    doc += """
  <!-- CTA -->
  <section class="cta-frame frame">
    <img class="frame-media" width="1440" height="1800" src="Assets/Chris.jpeg" alt="" loading="lazy" style="object-position: 50% 62%;">
    <div class="frame-scrim" aria-hidden="true"></div>
    <div class="frame-copy reveal">
      <h2 class="h2">Reading is good. Reps are better.</h2>
      <p class="text">Turn these ideas into real progress. Book a session and train with a coach who builds the plan around you.</p>
      <div class="btn-pair"><a class="btn" href="contact.html">Book a Session</a></div>
    </div>
  </section>

  </main>
"""
    doc += footer("")
    return no_dashes(doc)


# ----------------------------------------------------------------------------- sitemap

def update_sitemap(posts: list) -> None:
    with open(SITEMAP, "r", encoding="utf-8") as f:
        xml = f.read()

    def block(loc, lastmod, changefreq, priority):
        return (f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n"
                f"    <changefreq>{changefreq}</changefreq>\n    <priority>{priority}</priority>\n  </url>")

    # Strip any previously-generated blog block so this is idempotent.
    xml = re.sub(r"\n  <!-- BLOG:START -->.*?<!-- BLOG:END -->", "", xml, flags=re.DOTALL)

    latest = posts[0]["date"] if posts else "2026-01-01"
    lines = ["\n  <!-- BLOG:START -->",
             block(f"{SITE}/blog", latest, "weekly", "0.8")]
    for p in posts:
        lines.append(block(f"{SITE}/blog/{p['slug']}", p["date"], "monthly", "0.7"))
    lines.append("  <!-- BLOG:END -->")
    blog_xml = "\n".join(lines)

    xml = xml.replace("</urlset>", blog_xml + "\n</urlset>")
    with open(SITEMAP, "w", encoding="utf-8") as f:
        f.write(xml)


# ----------------------------------------------------------------------------- main

def load_posts() -> list:
    posts = []
    if not os.path.isdir(POSTS_DIR):
        return posts
    for fn in os.listdir(POSTS_DIR):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(POSTS_DIR, fn), "r", encoding="utf-8") as f:
            data = json.load(f)
        for key in ("slug", "title", "description", "category", "date", "blocks"):
            if key not in data:
                raise SystemExit(f"[blog_render] {fn} is missing required key: {key}")
        posts.append(data)
    # newest first, tiebreak by slug for determinism
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts


def main() -> None:
    posts = load_posts()
    os.makedirs(BLOG_OUT_DIR, exist_ok=True)

    for post in posts:
        out = os.path.join(BLOG_OUT_DIR, f"{post['slug']}.html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(normalize_headings(render_post(post, posts)))
        print(f"[blog_render] wrote {os.path.relpath(out, ROOT)}")

    with open(INDEX_OUT, "w", encoding="utf-8") as f:
        f.write(normalize_headings(render_index(posts)))
    print(f"[blog_render] wrote {os.path.relpath(INDEX_OUT, ROOT)}")

    update_sitemap(posts)
    print(f"[blog_render] updated sitemap.xml ({len(posts)} post(s))")


if __name__ == "__main__":
    main()
