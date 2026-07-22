# Blog post sources

Each `*.json` file in this folder is one article. `python3 .build/blog_render.py`
(run from the site root) turns them into `blog/<slug>.html`, rebuilds `blog.html`,
and refreshes the `/blog` entries in `sitemap.xml`. Do not hand-edit the generated
HTML - edit the JSON and re-run.

## Schema

```json
{
  "slug": "url-safe-no-spaces",
  "title": "Sentence-case headline",
  "description": "Meta description, <=160 chars, keyword-rich.",
  "category": "Junior Development",
  "date": "2026-07-22",
  "author": "APF Coaching Team",
  "read_minutes": 0,
  "blocks": [
    { "type": "lead",  "text": "Opening paragraph, rendered larger." },
    { "type": "h2",    "text": "Section heading" },
    { "type": "p",     "text": "Body paragraph." },
    { "type": "h3",    "text": "Sub-heading" },
    { "type": "ul",    "items": ["point one", "point two"] },
    { "type": "ol",    "items": ["step one", "step two"] },
    { "type": "quote", "text": "Pull quote." }
  ],
  "cta": { "heading": "Ready to make the jump?", "text": "One supporting line." }
}
```

Inline markup inside any `text`/`items` string: `**bold**` and `[label](url)`.
Em dashes and en dashes are auto-converted to hyphens (hard brand rule) by the renderer.

Categories in use: Junior Development, Senior Performance, Conditioning & Fitness,
Injury & Recovery, Skills & Drills, Local Football.

Filename convention: `YYYY-MM-DD-slug.json` (the date inside the JSON is what actually
drives ordering and the sitemap; the filename prefix just keeps the folder sorted).
