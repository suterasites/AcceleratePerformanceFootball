#!/usr/bin/env python3
"""
One-time (idempotent) patch: add a "Blog" link to the nav (desktop + mobile) and the
footer Navigation column on every existing page, so the blog is discoverable sitewide.

The generated blog pages (blog.html, blog/*.html) already include the Blog link, so they
are skipped here. Safe to re-run: it only inserts a link that is not already present.

Run from the site root:  python3 .build/add_blog_nav.py
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", ".build", "node_modules", "temporary screenshots", "blog", "seo", "Assets", "src"}

# (name, faq_anchor_template, blog_anchor_template) - {P} is the page's relative prefix.
CONTEXTS = [
    (
        "desktop-nav",
        '<a href="{P}faq.html" class="text-[13px] font-medium tracking-widest uppercase text-white/60 hover:text-white transition-colors duration-300">FAQ</a>',
        '<a href="{P}blog.html" class="text-[13px] font-medium tracking-widest uppercase text-white/60 hover:text-white transition-colors duration-300">Blog</a>',
    ),
    (
        "mobile-nav",
        '<a href="{P}faq.html" class="mobile-nav-link block px-4 py-3.5 text-[13px] font-medium tracking-widest uppercase text-white/60 hover:text-white hover:bg-white/5 rounded-lg transition-colors duration-200">FAQ</a>',
        '<a href="{P}blog.html" class="mobile-nav-link block px-4 py-3.5 text-[13px] font-medium tracking-widest uppercase text-white/60 hover:text-white hover:bg-white/5 rounded-lg transition-colors duration-200">Blog</a>',
    ),
    (
        "footer-nav",
        '<a href="{P}faq.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">FAQ</a>',
        '<a href="{P}blog.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">Blog</a>',
    ),
]


def html_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def main():
    total_inserts = 0
    for path in sorted(html_files()):
        rel = os.path.relpath(path, ROOT)
        if rel == "blog.html":
            continue
        prefix = "../" if os.sep in rel else ""

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        original = content
        inserted_here = []

        for name, faq_tmpl, blog_tmpl in CONTEXTS:
            faq = faq_tmpl.format(P=prefix)
            blog = blog_tmpl.format(P=prefix)
            if blog in content:
                continue  # already present -> idempotent skip
            if faq not in content:
                continue  # this page lacks that context -> leave it
            # Insert Blog right after FAQ, reusing FAQ's leading newline+indent.
            pat = re.compile(r"(\n[ \t]*)" + re.escape(faq))
            new_content, n = pat.subn(lambda m: m.group(0) + m.group(1) + blog, content, count=1)
            if n == 1:
                content = new_content
                inserted_here.append(name)

        if content != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            total_inserts += len(inserted_here)
            print(f"[add_blog_nav] {rel:42s} + {', '.join(inserted_here)}")
        else:
            print(f"[add_blog_nav] {rel:42s} (no change)")

    print(f"\n[add_blog_nav] done - {total_inserts} link insertion(s)")


if __name__ == "__main__":
    main()
