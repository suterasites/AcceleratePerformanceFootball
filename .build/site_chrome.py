#!/usr/bin/env python3
"""
Accelerate Performance Football - the parts every page shares.

The top bar, menu, partners strip, footer and page scripts live here and nowhere else,
so they stay identical across the site. blog_render.py imports them for the blog pages.
For the hand-kept pages, change a function below and run this from the site root:

    python3 .build/site_chrome.py

It rewrites everything between the SITE-* markers on every page, using the right path
prefix for the page's depth. Styles are in apf.css at the site root.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Standalone pages with no top bar or footer, on purpose.
STANDALONE = {"404.html", "thank-you.html"}


def head_assets(p: str = "") -> str:
    return f"""  <script>document.documentElement.classList.add('js')</script>
  <link rel="stylesheet" href="{p}apf.css">
  <link rel="preload" href="{p}Assets/fonts/inter-tight-latin-variable.woff2" as="font" type="font/woff2" crossorigin>
"""


def nav(p: str = "") -> str:
    return f"""<!-- SITE-NAV:START -->
  <nav id="main-nav" class="site-nav" role="navigation" aria-label="Main navigation">
    <div class="nav-start">
      <button id="menu-btn" class="menu-btn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="site-menu"><span></span><span></span></button>
      <a href="{p}index.html" class="nav-brand" aria-label="Accelerate Performance Football home">
        <img width="209" height="213" src="{p}Assets/Logo Mark.png" alt="Accelerate Performance Football">
      </a>
    </div>

    <div class="nav-links">
      <div class="nav-group">
        <a href="{p}services.html" class="nav-link">What We Do</a>
        <div class="nav-panel">
          <div class="nav-panel-body">
            <div class="nav-panel-grid">
              <a href="{p}services/junior-prep.html" class="nav-panel-item">
                <span class="nav-panel-name">Junior Prep</span>
                <span class="nav-panel-desc">Getting younger players ready for senior football</span>
              </a>
              <a href="{p}services/senior-refinement.html" class="nav-panel-item">
                <span class="nav-panel-name">Senior Refinement</span>
                <span class="nav-panel-desc">Level up what already makes you dangerous</span>
              </a>
              <a href="{p}services/off-season-conditioning.html" class="nav-panel-item">
                <span class="nav-panel-name">Off-Season Conditioning</span>
                <span class="nav-panel-desc">Gain an edge while others rest</span>
              </a>
              <a href="{p}services/injury-return.html" class="nav-panel-item">
                <span class="nav-panel-name">Injury Return</span>
                <span class="nav-panel-desc">Structured recovery to come back stronger</span>
              </a>
            </div>
            <a href="{p}services.html" class="nav-panel-all">View all programs</a>
          </div>
        </div>
      </div>
      <a href="{p}about.html" class="nav-link">About</a>
      <a href="{p}contact.html" class="nav-link">Contact</a>
    </div>

    <div class="nav-end">
      <a href="{p}contact.html" class="btn btn-sm">Book a Session</a>
    </div>
  </nav>

  <!-- Menu, opened by the two-line button -->
  <div id="site-menu" class="menu" inert>
    <div class="menu-scrim" data-menu-close></div>
    <div class="menu-panel" role="dialog" aria-modal="true" aria-label="Menu">
      <button id="menu-close" class="menu-close label" type="button" data-menu-close>Close</button>
      <ul class="menu-list">
        <li>
          <a href="{p}services.html" class="menu-item">What We Do</a>
          <div class="menu-sub">
            <a href="{p}services/junior-prep.html">Junior Prep</a>
            <a href="{p}services/senior-refinement.html">Senior Refinement</a>
            <a href="{p}services/off-season-conditioning.html">Off-Season Conditioning</a>
            <a href="{p}services/injury-return.html">Injury Return</a>
          </div>
        </li>
        <li><a href="{p}about.html" class="menu-item">About</a></li>
        <li><a href="{p}faq.html" class="menu-item">FAQ</a></li>
        <li><a href="{p}blog.html" class="menu-item">Blog</a></li>
        <li><a href="{p}contact.html" class="menu-item">Contact</a></li>
      </ul>
      <div class="menu-end">
        <a href="{p}contact.html" class="btn">Book a Session</a>
        <p class="links label">
          <a href="tel:0401117862"><span>0401 117 862</span></a>
          <a href="sms:+61401117862?body=Hi%20APF%2C%20I%27d%20like%20to%20book%20a%20session."><span>Text</span></a>
        </p>
      </div>
    </div>
  </div>

  <script>
    (function(){{var b=document.getElementById('menu-btn'),m=document.getElementById('site-menu'),c=document.getElementById('menu-close'),r=document.documentElement;function s(o){{m.classList.toggle('is-open',o);m.inert=!o;b.setAttribute('aria-expanded',o?'true':'false');r.classList.toggle('menu-lock',o);(o?c:b).focus({{preventScroll:true}})}}b.addEventListener('click',function(){{s(true)}});m.querySelectorAll('[data-menu-close],a').forEach(function(e){{e.addEventListener('click',function(){{s(false)}})}});document.addEventListener('keydown',function(e){{if(e.key==='Escape'&&m.classList.contains('is-open'))s(false)}})}})();
    (function(){{var n=document.getElementById('main-nav'),l=0;window.addEventListener('scroll',function(){{var y=window.scrollY;n.classList.toggle('is-solid',y>80);n.style.transform=(y>l&&y>300)?'translateY(-100%)':'translateY(0)';l=y}},{{passive:true}})}})();
  </script>
  <!-- SITE-NAV:END -->"""


def partners(p: str = "") -> str:
    return f"""<!-- SITE-PARTNERS:START -->
  <section class="partners on-white" aria-labelledby="partners-title">
    <h2 id="partners-title" class="label label-soft reveal">Partners</h2>
    <div class="partner-row reveal">
      <a class="partner" href="https://www.loutakis.com.au/" target="_blank" rel="noopener noreferrer"><img width="510" height="99" src="{p}Assets/Sponsors/Loutakis Real Estate.png" alt="Loutakis Real Estate" loading="lazy"></a>
      <a class="partner" href="https://www.instagram.com/kstruct_/?hl=en" target="_blank" rel="noopener noreferrer"><img width="163" height="133" src="{p}Assets/Sponsors/K-Struct New.png" alt="K-Struct" loading="lazy"></a>
      <a class="partner" href="https://www.westernmitsubishi.com.au/" target="_blank" rel="noopener noreferrer"><img width="418" height="120" src="{p}Assets/Sponsors/Western Mitsubishi.jpeg" alt="Western Mitsubishi" loading="lazy"></a>
      <a class="partner" href="https://www.dilalloelectrical.com.au/" target="_blank" rel="noopener noreferrer"><img width="367" height="137" src="{p}Assets/Sponsors/Di Lallo Electrical Services.jpeg" alt="Di Lallo Electrical Services" loading="lazy"></a>
      <a class="partner" href="https://hcdistributors.com.au/" target="_blank" rel="noopener noreferrer"><img width="300" height="300" src="{p}Assets/Sponsors/cropped-HCD_Logo_New.webp" alt="HC Distributors" loading="lazy"></a>
    </div>
  </section>
  <!-- SITE-PARTNERS:END -->"""


def footer(p: str = "") -> str:
    return f"""<!-- SITE-FOOTER:START -->
  <footer class="site-footer" role="contentinfo">
    <div class="footer-top">
      <div class="footer-brand">
        <a href="{p}index.html" aria-label="Accelerate Performance Football home"><img width="209" height="213" src="{p}Assets/Logo Mark.png" alt="Accelerate Performance Football" loading="lazy"></a>
        <p class="text">Melbourne-based private football coaching. Dedicated technique and performance training for footballers who want more.</p>
        <p class="links label"><a href="https://www.instagram.com/accelerate.performance_/" target="_blank" rel="noopener noreferrer" aria-label="Follow us on Instagram"><span>Instagram</span></a></p>
      </div>

      <div class="footer-col">
        <h2 class="label">Programs</h2>
        <nav class="footer-links" aria-label="Programs">
          <a href="{p}services/junior-prep.html">Junior Prep</a>
          <a href="{p}services/senior-refinement.html">Senior Refinement</a>
          <a href="{p}services/off-season-conditioning.html">Off-Season Conditioning</a>
          <a href="{p}services/injury-return.html">Injury Return</a>
          <a href="{p}online.html">Online Training</a>
        </nav>
      </div>

      <div class="footer-col">
        <h2 class="label">Navigation</h2>
        <nav class="footer-links" aria-label="Footer navigation">
          <a href="{p}about.html">About</a>
          <a href="{p}coaches/chris-sutera.html">Chris Sutera</a>
          <a href="{p}coaches/james-sutera.html">James Sutera</a>
          <a href="{p}faq.html">FAQ</a>
          <a href="{p}blog.html">Blog</a>
          <a href="{p}contact.html">Contact</a>
          <a href="{p}privacy.html">Privacy Policy</a>
        </nav>
      </div>

      <div class="footer-col footer-col-contact">
        <h2 class="label">Contact</h2>
        <div class="footer-links">
          <a href="tel:0401117862">0401 117 862</a>
          <a href="mailto:info.accelerateperformance@gmail.com">info.accelerateperformance@gmail.com</a>
          <p>Melbourne based</p>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <p>&copy; 2026 Accelerate Performance Football. All rights reserved.</p>
      <p>Melbourne, Victoria, Australia</p>
      <p>Built by <a href="https://suterasites.com.au/" target="_blank" rel="noopener noreferrer">Sutera Sites</a></p>
    </div>
  </footer>

  <!-- Reveal on scroll -->
  <script>
    (function() {{
      var els = document.querySelectorAll('.reveal');
      var observer = new IntersectionObserver(function(entries) {{
        entries.forEach(function(e) {{
          if (e.isIntersecting) e.target.classList.add('visible');
        }});
      }}, {{ threshold: 0.08, rootMargin: '0px 0px -30px 0px' }});
      els.forEach(function(el) {{ observer.observe(el); }});
    }})();
  </script>
  <!-- SITE-FOOTER:END -->"""


def sync() -> None:
    blocks = {"NAV": nav, "PARTNERS": partners, "FOOTER": footer}
    changed = 0
    for folder, _, files in os.walk(ROOT):
        rel_folder = os.path.relpath(folder, ROOT)
        top = rel_folder.split(os.sep)[0]
        if top.startswith(".") or top in ("Assets", "seo", "src", "temporary screenshots"):
            continue
        depth = 0 if rel_folder == "." else len(rel_folder.split(os.sep))
        for name in files:
            if not name.endswith(".html") or (depth == 0 and name in STANDALONE):
                continue
            path = os.path.join(folder, name)
            with open(path, encoding="utf-8") as f:
                doc = f.read()
            new = doc
            for key, fn in blocks.items():
                new = re.sub(rf"<!-- SITE-{key}:START -->.*?<!-- SITE-{key}:END -->",
                             lambda _: fn("../" * depth), new, flags=re.S)
            if new != doc:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)
                changed += 1
    print(f"[site_chrome] updated {changed} page(s)")


if __name__ == "__main__":
    sys.exit(sync())
