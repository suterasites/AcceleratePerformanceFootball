# APF Blog - Content Plan & Automation (canonical)

This file lives **inside the APF site repo** so the weekly cloud routine is fully
self-contained. The Sutera-Sites CRM keeps a pointer copy for visibility, but THIS is
the operational source of truth for the backlog and published log.

**Cadence:** one new post auto-published every **Wednesday** (Melbourne time).
**Mode:** auto-write + auto-publish, no review gate (chosen 2026-07-22).
**Goal:** local SEO + lead-gen for west-Melbourne football coaching (Point Cook, Werribee,
Altona, Williamstown, Hoppers Crossing). Every post routes to a service and the Book a Session CTA.

## How it works (do not improvise)

1. Post source = one JSON file in `blog/_posts/YYYY-MM-DD-slug.json` (schema in `blog/_posts/README.md`).
2. From the site root run `python3 .build/blog_render.py` - it renders `blog/<slug>.html`,
   rebuilds `blog.html`, and refreshes the `/blog` entries in `sitemap.xml`.
3. `git add blog blog.html sitemap.xml && git commit && git push` -> Cloudflare Pages auto-deploys.
4. The renderer strips em/en dashes and reuses the verified sitewide nav/footer chrome, so
   auto-published pages never drift structurally.

## Writing rules

- 700-1100 words. Useful, specific, APF voice: precise, results-focused, no fluff, no consultant-speak.
- No em dashes (hard rule, also auto-enforced by the renderer).
- Anchor locally where natural (western suburbs; venue West Point SC, 2 Webster St, Point Cook).
- Never fabricate results, testimonials, athlete names, stats beyond the site's own
  (125+ athletes, 92% progression, 4+ years), or club affiliations (West Point SC is a hired venue only).
- One in-body link to the routing service page + the `cta` object. Use `../` paths in post links.
- Meta `description` <=160 chars, keyword-rich. Byline `author`: "APF Coaching Team".
- Take the top unstarted backlog topic (or a clearly better timely one), then move it to the Published log.

## Published log

| Date | Title | Slug | Category | Routes to |
|------|-------|------|----------|-----------|
| 2026-07-22 | From Junior to Senior Football: What Changes and How to Prepare | junior-to-senior-football | Junior Development | Junior Prep |
| 2026-07-29 | 5 First-Touch Drills You Can Practise at Home | 5-first-touch-drills-at-home | Skills & Drills | Junior Prep |
| 2026-08-05 | Why Private Coaching Beats Group Training for Fast Improvement | why-private-coaching-beats-group-training | Senior Performance | Senior Refinement |
| 2026-08-12 | How to Prepare for Football Preseason in Melbourne | how-to-prepare-football-preseason-melbourne | Conditioning & Fitness | Off-Season Conditioning |
| 2026-08-19 | Coming Back From a Football Injury: A Player's Return Roadmap | coming-back-from-football-injury | Injury & Recovery | Injury Return |

## Topic backlog (pick the top unstarted one each week)

| # | Working title | Category | Target search intent | Routes to |
|---|---------------|----------|----------------------|-----------|
| 1 | What to Look for in a Football Coach in the Western Suburbs | Local Football | "football coach Point Cook / Werribee" | Contact |
| 2 | Scanning: The Habit That Separates Good Players From Great Ones | Senior Performance | "how to scan in football" | Senior Refinement |
| 3 | Off-Season Is Where Next Season Is Won | Conditioning & Fitness | "football off season training" | Off-Season Conditioning |
| 4 | A Parent's Guide to Supporting a Young Footballer | Junior Development | "helping my child improve at soccer" | Junior Prep |
| 5 | Weak Foot Training: How to Become Genuinely Two-Footed | Skills & Drills | "how to improve weak foot football" | Junior Prep |
| 6 | Speed and Agility for Footballers: Training the First Two Steps | Conditioning & Fitness | "football speed agility training" | Off-Season Conditioning |
| 7 | How Many Sessions Does It Take to See Improvement? | Senior Performance | "how long to improve at football" | Pricing |
| 8 | Position-Specific Training: Why a Striker and a Defender Train Differently | Senior Performance | "position specific soccer training" | Senior Refinement |
| 9 | Football Training in Point Cook: Your Local Options | Local Football | "football training Point Cook" | suburbs/point-cook |
| 10 | Building Match Fitness That Lasts 90 Minutes | Conditioning & Fitness | "how to build match fitness soccer" | Off-Season Conditioning |
| 11 | Confidence on the Ball: Coaching the Mental Side of Football | Junior Development | "building confidence young footballer" | Junior Prep |
| 12 | Passing Under Pressure: Drills to Keep the Ball Moving | Skills & Drills | "passing drills under pressure" | Senior Refinement |
| 13 | Small-Group vs 1-on-1 Coaching: Which Is Right for Your Player | Senior Performance | "small group football coaching" | Pricing |
| 14 | Getting Scouted: What Selectors Actually Look For | Senior Performance | "how to get scouted soccer Australia" | Senior Refinement |

Keep at least ~8 topics here. When it runs low, append a fresh batch before the next Wednesday.
