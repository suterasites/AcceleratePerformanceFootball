#!/usr/bin/env python3
"""
Suburb landing-page generator for Accelerate Performance Football.

Renders one local landing page per target suburb under ../suburbs/<slug>.html,
matching the hand-built reference page (suburbs/altona.html) exactly for chrome
(nav, footer, schema graph, scripts, styles) and injecting unique per-suburb copy.

Each page targets BOTH "football coaching <suburb>" and "soccer coaching <suburb>"
(synonyms in Australia) from a single page - no duplicate content. Football is the
headline term, soccer is woven through the meta, the local section and the schema.

The 5 original suburb pages (altona, hoppers-crossing, point-cook, werribee,
williamstown) are HAND-MAINTAINED and are NOT written by this script - it only
emits the suburbs listed in NEW_SUBURBS. Run:  python3 .build/suburb_render.py
Add --all to also (re)write the originals from this template (not the default;
they carry bespoke copy).
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
OUT_DIR = os.path.join(ROOT, "suburbs")

# ── Shared facts ──────────────────────────────────────────────────────────────
SIBLING_ANSWER = ("Yes. Siblings booking Small Unit sessions together pay the discounted sibling "
                  "rate - $55/session on the Tune Up ($275 for 5), $55/session on the Game Changer "
                  "5-pack ($715), and $50/session on the Total 90 13-week block ($1,300).")
CLUB_ANSWER = ("Yes. We don't replace club training, we run alongside it. Most players use our "
               "sessions to sharpen specific skills club training doesn't have time to drill, prep "
               "for selection, or build conditioning across the season. Players from any local club "
               "are welcome, whatever code you call it - football or soccer.")

# ── Target suburbs (the 9 new ones) ───────────────────────────────────────────
# Fields: name, slug, postcode, lat, lon, drive_short, drive_caption,
# hero_sub, why1_title/body, why2_title/body, local_h2, local_p1/2/3 (p3 carries
# the soccer term), faq_drive_q, faq_drive_a, junior_micro, venue_dir, neighbors
NEW_SUBURBS = [
    {
        "name": "Williams Landing", "slug": "williams-landing", "postcode": "3027",
        "lat": "-37.8676", "lon": "144.7469",
        "drive_short": "~8 min", "drive_caption": "~8 min via Point Cook Rd",
        "venue_dir": "a ~8-minute drive south via Point Cook Road",
        "hero_sub": "Barely 8 minutes south down Point Cook Road. Our home training venue is West Point Soccer Club at 2 Webster St, Point Cook - the same pocket our coaches are based in. Quick, direct run from Williams Landing with free on-site parking.",
        "why1_title": "8 minutes south", "why1_body": "Straight down Point Cook Road and you're at West Point SC. No freeway, no fuss - it is one of the closest suburbs to our venue, so a weeknight session barely touches your evening.",
        "why2_title": "A fast-growing football pocket", "why2_body": "Williams Landing has grown quickly, and with it a wave of junior and senior players. Plenty already train with us, coming from whichever club they turn out for on the weekend.",
        "local_h2": "Right on our doorstep.",
        "local_p1": "Williams Landing sits just north of the venue, a short run south down Point Cook Road. For families here it is about the most convenient private session in the west.",
        "local_p2": "We don't compete with club training, we supplement it. Most Williams Landing players run a Tune Up block before a selection window, or commit to a Game Changer across the season to depth-build the skills club volume can't drill in isolation.",
        "local_p3": "Whether you call it football or soccer, the work is the same - private, one-on-one attention on the things that actually move a player forward. Soccer coaching this close to home is rare, and the drive back after a session is a short one.",
        "faq_drive_q": "What's the drive from Williams Landing like?",
        "faq_drive_a": "Straight south down Point Cook Road, around 8 minutes. No freeway involved, so it stays predictable at any hour. Free on-site parking when you arrive at West Point SC.",
        "junior_micro": "Younger Williams Landing players preparing for senior football and rep selection.",
        "neighbors": [("point-cook", "Point Cook"), ("laverton", "Laverton"), ("altona-meadows", "Altona Meadows"), ("truganina", "Truganina"), ("tarneit", "Tarneit")],
    },
    {
        "name": "Altona Meadows", "slug": "altona-meadows", "postcode": "3028",
        "lat": "-37.8790", "lon": "144.7830",
        "drive_short": "~12 min", "drive_caption": "~12 min via Point Cook Rd",
        "venue_dir": "a ~12-minute drive west via Point Cook Road",
        "hero_sub": "About 12 minutes west via Point Cook Road. Our home training venue is West Point Soccer Club at 2 Webster St, Point Cook - where our coaches are based. A direct run from Altona Meadows with free on-site parking.",
        "why1_title": "12 minutes west", "why1_body": "Central Avenue onto Point Cook Road and you are at West Point SC in around 12 minutes. Suburban roads the whole way, no freeway to plan around.",
        "why2_title": "Deep junior football roots", "why2_body": "Altona Meadows has long been strong junior football country. Players from across the suburb drive in regularly - whatever club they wear on the weekend.",
        "local_h2": "A short run west.",
        "local_p1": "Altona Meadows borders Point Cook, so the venue is genuinely close - a straight run down Point Cook Road. Weeknight and weekend sessions both work without eating the evening.",
        "local_p2": "Our sessions sit alongside club training, not instead of it. Most Altona Meadows players use a Tune Up block to sharpen for selection, or a full Game Changer to build across the season.",
        "local_p3": "Football or soccer, the label doesn't change the work - private coaching that drills the detail a squad session never gets to. For Altona Meadows families it is quality soccer coaching a few minutes from home.",
        "faq_drive_q": "What's the drive from Altona Meadows like?",
        "faq_drive_a": "Central Avenue to Point Cook Road, around 12 minutes on suburban roads. No freeway, so it holds steady through peak. Free on-site parking at West Point SC.",
        "junior_micro": "Younger Altona Meadows players preparing for senior football and rep selection.",
        "neighbors": [("point-cook", "Point Cook"), ("altona", "Altona"), ("laverton", "Laverton"), ("williams-landing", "Williams Landing"), ("altona-north", "Altona North")],
    },
    {
        "name": "Laverton", "slug": "laverton", "postcode": "3028",
        "lat": "-37.8637", "lon": "144.7686",
        "drive_short": "~13 min", "drive_caption": "~13 min via Point Cook Rd",
        "venue_dir": "a ~13-minute drive south via Point Cook Road",
        "hero_sub": "Around 13 minutes south via Point Cook Road. Our home training venue is West Point Soccer Club at 2 Webster St, Point Cook - the base our coaches work from. Direct run from Laverton, free on-site parking.",
        "why1_title": "13 minutes south", "why1_body": "Point Cook Road runs straight from Laverton down to the venue in around 13 minutes. Predictable suburban route, easy to slot a session into a weeknight.",
        "why2_title": "Players from every local club", "why2_body": "Laverton sits in the middle of the west's football belt. Players from across the suburb come to us to work on the detail their weekend club can't cover.",
        "local_h2": "Straight down Point Cook Road.",
        "local_p1": "Laverton feeds almost directly onto Point Cook Road, so the venue is a short, simple drive south. No freeway detours to think about.",
        "local_p2": "We run alongside club training rather than replacing it. Laverton players tend to book a Tune Up before a comp window or commit to a season-long block to build consistency.",
        "local_p3": "Call it football or soccer - the coaching is the same private, one-on-one work on technique, decisions and conditioning. Soccer coaching this accessible is hard to find close to Laverton.",
        "faq_drive_q": "What's the drive from Laverton like?",
        "faq_drive_a": "South down Point Cook Road, around 13 minutes. Suburban the whole way with no freeway, so timing stays reliable. Free on-site parking at West Point SC.",
        "junior_micro": "Younger Laverton players preparing for senior football and rep selection.",
        "neighbors": [("point-cook", "Point Cook"), ("altona-meadows", "Altona Meadows"), ("williams-landing", "Williams Landing"), ("altona", "Altona"), ("truganina", "Truganina")],
    },
    {
        "name": "Altona North", "slug": "altona-north", "postcode": "3025",
        "lat": "-37.8290", "lon": "144.8410",
        "drive_short": "~18 min", "drive_caption": "~18 min via Princes Fwy",
        "venue_dir": "a ~18-minute drive southwest via the Princes Freeway",
        "hero_sub": "About 18 minutes southwest via the Princes Freeway. Our home training venue is West Point Soccer Club at 2 Webster St, Point Cook - where our coaches are based. Direct freeway run from Altona North, free on-site parking.",
        "why1_title": "18 minutes on the freeway", "why1_body": "Princes Freeway westbound, exit toward Point Cook, and you are at West Point SC in around 18 minutes. A direct freeway run keeps the drive predictable.",
        "why2_title": "A strong football community", "why2_body": "Altona North has real football history and a steady stream of junior and senior players. Plenty already make the short freeway trip to train with us.",
        "local_h2": "A short freeway hop.",
        "local_p1": "From Altona North it is a quick jump onto the Princes Freeway and a straight run west to the venue - around 18 minutes door to door off-peak.",
        "local_p2": "Our work supplements club training, it doesn't replace it. Altona North players often run a Tune Up block before selection or a Game Changer to build depth across the season.",
        "local_p3": "Football, soccer, same game - and the same private coaching that targets exactly what a player needs. For Altona North families it is proper soccer coaching a short freeway trip away.",
        "faq_drive_q": "What's the drive from Altona North like?",
        "faq_drive_a": "Onto the Princes Freeway westbound toward Point Cook, around 18 minutes off-peak. Add 5-10 minutes at evening peak. Free on-site parking at West Point SC.",
        "junior_micro": "Younger Altona North players preparing for senior football and rep selection.",
        "neighbors": [("altona", "Altona"), ("newport", "Newport"), ("williamstown", "Williamstown"), ("altona-meadows", "Altona Meadows"), ("point-cook", "Point Cook")],
    },
    {
        "name": "Newport", "slug": "newport", "postcode": "3015",
        "lat": "-37.8430", "lon": "144.8840",
        "drive_short": "~20 min", "drive_caption": "~20 min via Princes Fwy",
        "venue_dir": "a ~20-minute drive southwest via the Princes Freeway",
        "hero_sub": "Around 20 minutes southwest via the Princes Freeway. Our home training venue is West Point Soccer Club at 2 Webster St, Point Cook - the base our coaches work from. Direct freeway run from Newport, free on-site parking.",
        "why1_title": "20 minutes west", "why1_body": "Onto the Princes Freeway and a direct run toward Point Cook, around 20 minutes off-peak. One freeway, no surface-street maze to navigate.",
        "why2_title": "Football-mad from juniors up", "why2_body": "Newport turns out plenty of players across juniors and seniors. Families make the freeway trip to add private coaching on top of their weekend club.",
        "local_h2": "A direct run down the freeway.",
        "local_p1": "From Newport it is a straightforward Princes Freeway drive west to the venue - around 20 minutes when the traffic is clear.",
        "local_p2": "We sit alongside club training rather than competing with it. Newport players commonly use a Tune Up to sharpen for a comp window or a season block to keep building.",
        "local_p3": "Whether it is football or soccer to you, the coaching is identical - private, individual attention on technique and decision-making. Soccer coaching worth the short freeway run from Newport.",
        "faq_drive_q": "What's the drive from Newport like?",
        "faq_drive_a": "Princes Freeway westbound toward Point Cook, around 20 minutes off-peak. Add 5-10 minutes at evening peak. Free on-site parking when you arrive at West Point SC.",
        "junior_micro": "Younger Newport players preparing for senior football and rep selection.",
        "neighbors": [("williamstown", "Williamstown"), ("altona-north", "Altona North"), ("altona", "Altona"), ("point-cook", "Point Cook"), ("werribee", "Werribee")],
    },
    {
        "name": "Truganina", "slug": "truganina", "postcode": "3029",
        "lat": "-37.8180", "lon": "144.7420",
        "drive_short": "~16 min", "drive_caption": "~16 min via Dohertys Rd",
        "venue_dir": "a ~16-minute drive south via Dohertys Road and Point Cook Road",
        "hero_sub": "About 16 minutes south via Dohertys Road onto Point Cook Road. Our home training venue is West Point Soccer Club at 2 Webster St, Point Cook - where our coaches are based. Direct run from Truganina, free on-site parking.",
        "why1_title": "16 minutes south", "why1_body": "Dohertys Road down to Point Cook Road and you reach West Point SC in around 16 minutes. A clean run south, easy to slot into a weeknight.",
        "why2_title": "One of the west's fastest-growing", "why2_body": "Truganina has boomed, and its junior and senior football numbers with it. A growing group of players already make the short trip to train with us.",
        "local_h2": "A clean run south.",
        "local_p1": "From Truganina it is Dohertys Road onto Point Cook Road and a direct run south to the venue - around 16 minutes with the newer arterials moving well.",
        "local_p2": "Our sessions add to club training, they don't replace it. Truganina players often run a Tune Up before selection or a Game Changer to build across a full season.",
        "local_p3": "Football or soccer, the name changes nothing about the work - private coaching drilled around one player at a time. For a fast-growing suburb like Truganina, soccer coaching this close is a real advantage.",
        "faq_drive_q": "What's the drive from Truganina like?",
        "faq_drive_a": "Dohertys Road to Point Cook Road, around 16 minutes south. Newer arterials so it moves well outside peak. Free on-site parking at West Point SC.",
        "junior_micro": "Younger Truganina players preparing for senior football and rep selection.",
        "neighbors": [("tarneit", "Tarneit"), ("point-cook", "Point Cook"), ("williams-landing", "Williams Landing"), ("werribee", "Werribee"), ("laverton", "Laverton")],
    },
    {
        "name": "Tarneit", "slug": "tarneit", "postcode": "3029",
        "lat": "-37.8330", "lon": "144.6660",
        "drive_short": "~20 min", "drive_caption": "~20 min via Sayers Rd",
        "venue_dir": "a ~20-minute drive southeast via Sayers Road and Point Cook Road",
        "hero_sub": "Around 20 minutes southeast via Sayers Road onto Point Cook Road. Our home training venue is West Point Soccer Club at 2 Webster St, Point Cook - the base our coaches work from. Direct run from Tarneit, free on-site parking.",
        "why1_title": "20 minutes southeast", "why1_body": "Sayers Road across to Point Cook Road and down to West Point SC, around 20 minutes. A straightforward arterial run with no freeway needed.",
        "why2_title": "Booming football numbers", "why2_body": "Tarneit is one of the country's fastest-growing suburbs, and its junior football scene is huge. More Tarneit players are adding private coaching to their weekly club load.",
        "local_h2": "Across and down to Point Cook.",
        "local_p1": "From Tarneit it is Sayers Road east onto Point Cook Road and a run down to the venue - around 20 minutes when the arterials are clear.",
        "local_p2": "We supplement club training rather than compete with it. Tarneit players tend to book a Tune Up before a comp window or a full season block to build consistency.",
        "local_p3": "You might call it football or soccer - either way the coaching is private and built around one player. With Tarneit's numbers climbing, focused soccer coaching nearby is worth the short trip.",
        "faq_drive_q": "What's the drive from Tarneit like?",
        "faq_drive_a": "Sayers Road onto Point Cook Road, around 20 minutes southeast. Arterial roads the whole way, no freeway. Free on-site parking when you arrive at West Point SC.",
        "junior_micro": "Younger Tarneit players preparing for senior football and rep selection.",
        "neighbors": [("truganina", "Truganina"), ("werribee", "Werribee"), ("point-cook", "Point Cook"), ("wyndham-vale", "Wyndham Vale"), ("williams-landing", "Williams Landing")],
    },
    {
        "name": "Wyndham Vale", "slug": "wyndham-vale", "postcode": "3024",
        "lat": "-37.8890", "lon": "144.6220",
        "drive_short": "~20 min", "drive_caption": "~20 min via Princes Fwy",
        "venue_dir": "a ~20-minute drive east via the Princes Freeway",
        "hero_sub": "About 20 minutes east via the Princes Freeway. Our home training venue is West Point Soccer Club at 2 Webster St, Point Cook - where our coaches are based. Direct freeway run from Wyndham Vale, free on-site parking.",
        "why1_title": "20 minutes on the freeway", "why1_body": "Onto the Princes Freeway eastbound and a direct run toward Point Cook, around 20 minutes. One freeway keeps the trip simple and predictable.",
        "why2_title": "A growing football community", "why2_body": "Wyndham Vale's junior and senior football is growing fast with the suburb. Families make the freeway trip to add private coaching to their weekend club.",
        "local_h2": "A straight freeway run east.",
        "local_p1": "From Wyndham Vale it is a quick hop onto the Princes Freeway and a direct eastbound run to the venue - around 20 minutes off-peak.",
        "local_p2": "Our coaching runs alongside club training, not instead of it. Wyndham Vale players often use a Tune Up block to sharpen for selection or a Game Changer across the season.",
        "local_p3": "Football or soccer, same sport and the same private, individual coaching. For Wyndham Vale families it is quality soccer coaching a short freeway run away.",
        "faq_drive_q": "What's the drive from Wyndham Vale like?",
        "faq_drive_a": "Princes Freeway eastbound toward Point Cook, around 20 minutes off-peak. Add a few minutes at peak. Free on-site parking at West Point SC.",
        "junior_micro": "Younger Wyndham Vale players preparing for senior football and rep selection.",
        "neighbors": [("werribee", "Werribee"), ("manor-lakes", "Manor Lakes"), ("point-cook", "Point Cook"), ("tarneit", "Tarneit"), ("hoppers-crossing", "Hoppers Crossing")],
    },
    {
        "name": "Manor Lakes", "slug": "manor-lakes", "postcode": "3024",
        "lat": "-37.8790", "lon": "144.5850",
        "drive_short": "~24 min", "drive_caption": "~24 min via Princes Fwy",
        "venue_dir": "a ~24-minute drive east via the Princes Freeway",
        "hero_sub": "Around 24 minutes east via the Princes Freeway. Our home training venue is West Point Soccer Club at 2 Webster St, Point Cook - the base our coaches work from. Direct freeway run from Manor Lakes, free on-site parking.",
        "why1_title": "A direct freeway run", "why1_body": "Ballan Road onto the Princes Freeway and a straight eastbound run to Point Cook, around 24 minutes. It is a longer trip, but a simple one - one freeway most of the way.",
        "why2_title": "Football growing with the suburb", "why2_body": "Manor Lakes is one of the newest growth pockets in the west, and its football numbers are climbing. Committed players make the trip for coaching they can't get closer to home.",
        "local_h2": "Worth the run east.",
        "local_p1": "From Manor Lakes it is Ballan Road onto the Princes Freeway and a direct run east to the venue - around 24 minutes when the freeway is clear.",
        "local_p2": "We add to club training rather than replace it. Manor Lakes players who make the trip tend to commit to a Game Changer or season block, getting real value from every session.",
        "local_p3": "Whether it is football or soccer to you, the coaching is the same - private, one-on-one work on the details that matter. For Manor Lakes players, dedicated soccer coaching is worth the run east.",
        "faq_drive_q": "What's the drive from Manor Lakes like?",
        "faq_drive_a": "Ballan Road onto the Princes Freeway eastbound, around 24 minutes to Point Cook. A longer but simple freeway run. Free on-site parking at West Point SC.",
        "junior_micro": "Younger Manor Lakes players preparing for senior football and rep selection.",
        "neighbors": [("wyndham-vale", "Wyndham Vale"), ("werribee", "Werribee"), ("point-cook", "Point Cook"), ("tarneit", "Tarneit"), ("hoppers-crossing", "Hoppers Crossing")],
    },
]

DOMAIN = "https://www.accelerateperformancefootball.com.au"

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <!-- Google tag (gtag.js) - GA4 G-7P2NC2YGW2 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-7P2NC2YGW2"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-7P2NC2YGW2');
  </script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>@@TITLE@@</title>
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="96x96" href="/Assets/favicon-96.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#0A0A0A">
  <meta name="description" content="@@META_DESC@@">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="@@DOMAIN@@/suburbs/@@SLUG@@">
  <link rel="apple-touch-icon" href="/Assets/apple-touch-icon.png">

  <meta property="og:type" content="website">
  <meta property="og:title" content="@@OG_TITLE@@">
  <meta property="og:description" content="@@OG_DESC@@">
  <meta property="og:url" content="@@DOMAIN@@/suburbs/@@SLUG@@">
  <meta property="og:image" content="@@DOMAIN@@/Assets/Logo.png">
  <meta property="og:locale" content="en_AU">
  <meta property="og:site_name" content="Accelerate Performance Football">
  <meta name="geo.region" content="AU-VIC">
  <meta name="geo.placename" content="@@NAME@@, Victoria">
  <meta name="ICBM" content="@@LAT@@, @@LON@@">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="@@OG_TITLE@@">
  <meta name="twitter:description" content="@@TW_DESC@@">
  <meta name="twitter:image" content="@@DOMAIN@@/Assets/Logo.png">

  <link rel="stylesheet" href="../styles.css">

  <link rel="preload" href="../Assets/fonts/bebas-neue-latin-400.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="../Assets/fonts/inter-latin-variable.woff2" as="font" type="font/woff2" crossorigin>

  <style>
    html { scroll-behavior: smooth; }
    body { font-family: 'Inter', system-ui, sans-serif; color: #F5F5F5; background: #0A0A0A; font-weight: 300; }
    h1, h2, h3, .font-display { font-family: 'Bebas Neue', system-ui, sans-serif; font-weight: 400; letter-spacing: 0.04em; }
    h4, .font-sans-bold { font-family: 'Inter', system-ui, sans-serif; font-weight: 700; }
    .grain::after { content: ''; position: absolute; inset: 0; opacity: 0.025; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); pointer-events: none; z-index: 1; }
    .shadow-lift { box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 12px 32px rgba(0,0,0,0.2), 0 28px 56px rgba(0,0,0,0.12); }
    .ease-spring { transition-timing-function: cubic-bezier(0.34, 1.56, 0.64, 1); }
    .btn:focus-visible { outline: 3px solid #FFFFFF; outline-offset: 3px; }
    .reveal { opacity: 0; transform: translateY(28px); transition: opacity 0.8s ease, transform 0.8s cubic-bezier(0.22, 1, 0.36, 1); }
    .reveal.visible { opacity: 1; transform: translateY(0); }
    ::-webkit-scrollbar { width: 7px; } ::-webkit-scrollbar-track { background: #0A0A0A; } ::-webkit-scrollbar-thumb { background: #2A2A2A; border-radius: 4px; } ::-webkit-scrollbar-thumb:hover { background: #444; }
    .accent-line { width: 40px; height: 1px; background: #FFFFFF; }
    .skip-link { position: absolute; left: -9999px; top: 0; z-index: 9999; padding: 8px 16px; background: #0A0A0A; color: #F5F5F5; text-decoration: none; } .skip-link:focus { left: 0; }
    .num-badge { font-family: 'Bebas Neue', system-ui, sans-serif; font-size: clamp(3rem, 6vw, 4.5rem); line-height: 1; letter-spacing: 0.02em; }
    .tier-faq summary { list-style: none; cursor: pointer; padding: 1.25rem 0; display: flex; justify-content: space-between; align-items: flex-start; gap: 2rem; border-bottom: 1px solid rgba(255,255,255,0.08); }
    .tier-faq summary::-webkit-details-marker { display: none; } .tier-faq summary:hover { color: #fff; }
    .tier-faq .plus { width: 18px; height: 18px; position: relative; flex-shrink: 0; margin-top: 4px; }
    .tier-faq .plus::before, .tier-faq .plus::after { content: ''; position: absolute; top: 50%; left: 50%; width: 12px; height: 1px; background: rgba(255,255,255,0.55); transform-origin: center; transition: transform 0.3s ease; }
    .tier-faq .plus::before { transform: translate(-50%, -50%); } .tier-faq .plus::after { transform: translate(-50%, -50%) rotate(90deg); }
    .tier-faq[open] .plus::after { transform: translate(-50%, -50%); }
    .tier-faq .answer { padding: 1rem 0 1.25rem 0; color: rgba(245,245,245,0.55); font-size: 0.95rem; line-height: 1.8; max-width: 60ch; border-bottom: 1px solid rgba(255,255,255,0.08); }
    .tier-faq .answer a { color: #fff; text-decoration: underline; text-underline-offset: 3px; }
  </style>
  <script src="https://elfsightcdn.com/platform.js" async></script>

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Service",
        "@id": "@@DOMAIN@@/suburbs/@@SLUG@@#service",
        "name": "@@SERVICE_NAME@@",
        "description": "@@SERVICE_DESC@@",
        "serviceType": "Private Football and Soccer Coaching",
        "url": "@@DOMAIN@@/suburbs/@@SLUG@@",
        "provider": { "@id": "@@DOMAIN@@/#business" },
        "areaServed": { "@type": "Place", "name": "@@NAME@@, Victoria, Australia", "address": { "@type": "PostalAddress", "addressLocality": "@@NAME@@", "addressRegion": "VIC", "postalCode": "@@POSTCODE@@", "addressCountry": "AU" } }
      },
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Home", "item": "@@DOMAIN@@/" },
          { "@type": "ListItem", "position": 2, "name": "Service Areas", "item": "@@DOMAIN@@/suburbs" },
          { "@type": "ListItem", "position": 3, "name": "@@NAME@@", "item": "@@DOMAIN@@/suburbs/@@SLUG@@" }
        ]
      },
      {
        "@type": "FAQPage",
        "mainEntity": @@FAQ_JSONLD@@
      }
    ]
  }
  </script>
  <!-- Sutera lead events (GA4) -->
  <script>/* SUTERA_LEAD_EVENTS */
  (function(){
    function ev(n, p){ if (typeof window.gtag === 'function') { window.gtag('event', n, Object.assign({transport_type:'beacon'}, p||{})); } }
    document.addEventListener('click', function(e){
      var a = e.target.closest ? e.target.closest('a[href^="tel:"]') : null;
      if (a) ev('click_to_call', { link_url: a.getAttribute('href') });
    }, true);
    document.addEventListener('submit', function(e){
      var f = e.target;
      if (!f || f.tagName !== 'FORM' || f.hasAttribute('data-no-lead')) return;
      var action = f.getAttribute('action') || '';
      var isLead = /formspree/i.test(action) || f.querySelector('input[type="email"], input[type="tel"], textarea');
      if (isLead) ev('generate_lead', { form_id: f.id || f.getAttribute('name') || 'contact' });
    }, true);
  })();
  </script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "@@DOMAIN@@/#business",
  "name": "Accelerate Performance Football",
  "description": "Private football (soccer) coaching business based in West Melbourne offering technique and performance coaching for footballers of all levels.",
  "url": "@@DOMAIN@@/",
  "image": "@@DOMAIN@@/Assets/Logo.png",
  "logo": "@@DOMAIN@@/Assets/Logo.png",
  "telephone": "+61401117862",
  "email": "info.accelerateperformance@gmail.com",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "West Melbourne",
    "addressRegion": "VIC",
    "addressCountry": "AU"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": -37.7996,
    "longitude": 144.9353
  },
  "areaServed": [
    {
      "@type": "Place",
      "name": "Melbourne"
    },
    {
      "@type": "Place",
      "name": "West Melbourne"
    },
    {
      "@type": "Place",
      "name": "Victoria"
    }
  ],
  "serviceType": [
    "Private Football Coaching",
    "Private Soccer Coaching",
    "Junior Football Training",
    "Senior Football Training",
    "Off-Season Conditioning",
    "Injury Return Training"
  ],
  "priceRange": "$$",
  "sameAs": [
    "https://www.instagram.com/accelerate.performance_/"
  ]
}
</script>
</head>
<body class="antialiased overflow-x-hidden">

  <a href="#main" class="skip-link">Skip to main content</a>

  <!-- NAV -->
  <nav id="main-nav" class="fixed top-0 w-full z-50 transition-all duration-500" role="navigation" aria-label="Main navigation">
    <div class="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
      <div class="flex items-center justify-between h-20 lg:h-24">
        <a href="../index.html" class="relative z-10 flex items-center gap-3" aria-label="Accelerate Performance Football home"><img width="500" height="500" src="../Assets/Logo.png" alt="Accelerate Performance Football" class="h-10 lg:h-12 w-auto"></a>
        <div class="hidden lg:flex items-center gap-10">
          <div class="relative group/services">
            <a href="../services.html" class="text-[13px] font-medium tracking-widest uppercase text-white/60 hover:text-white transition-colors duration-300 flex items-center gap-1.5">What We Do<svg class="w-3 h-3 opacity-50 group-hover/services:opacity-100 transition-opacity duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg></a>
            <div class="absolute top-full left-1/2 -translate-x-1/2 pt-5 opacity-0 invisible group-hover/services:opacity-100 group-hover/services:visible transition-[opacity,visibility] duration-300 pointer-events-none group-hover/services:pointer-events-auto">
              <div class="border border-white/8 p-5 w-[480px] shadow-lift" style="backdrop-filter: blur(16px); background: rgba(20,20,20,0.97);">
                <div class="grid grid-cols-2 gap-2">
                  <a href="../services/junior-prep.html" class="flex items-start gap-3 p-3.5 rounded-lg hover:bg-white/5 transition-colors duration-200"><span class="font-display text-xl text-white/10 mt-0.5 shrink-0">01</span><div><p class="text-sm font-semibold text-white mb-0.5">Junior Prep</p><p class="text-[11px] text-white/30 leading-relaxed">Getting younger players ready for senior football</p></div></a>
                  <a href="../services/senior-refinement.html" class="flex items-start gap-3 p-3.5 rounded-lg hover:bg-white/5 transition-colors duration-200"><span class="font-display text-xl text-white/10 mt-0.5 shrink-0">02</span><div><p class="text-sm font-semibold text-white mb-0.5">Senior Refinement</p><p class="text-[11px] text-white/30 leading-relaxed">Level up what already makes you dangerous</p></div></a>
                  <a href="../services/off-season-conditioning.html" class="flex items-start gap-3 p-3.5 rounded-lg hover:bg-white/5 transition-colors duration-200"><span class="font-display text-xl text-white/10 mt-0.5 shrink-0">03</span><div><p class="text-sm font-semibold text-white mb-0.5">Off-Season Conditioning</p><p class="text-[11px] text-white/30 leading-relaxed">Gain an edge while others rest</p></div></a>
                  <a href="../services/injury-return.html" class="flex items-start gap-3 p-3.5 rounded-lg hover:bg-white/5 transition-colors duration-200"><span class="font-display text-xl text-white/10 mt-0.5 shrink-0">04</span><div><p class="text-sm font-semibold text-white mb-0.5">Injury Return</p><p class="text-[11px] text-white/30 leading-relaxed">Structured recovery to come back stronger</p></div></a>
                </div>
                <div class="mt-3 pt-3 border-t border-white/5"><a href="../services.html" class="text-xs text-white/30 hover:text-white/60 transition-colors duration-200 inline-flex items-center gap-1">View all programs <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg></a></div>
              </div>
            </div>
          </div>
          <a href="../about.html" class="text-[13px] font-medium tracking-widest uppercase text-white/60 hover:text-white transition-colors duration-300">About</a>
          <a href="../pricing.html" class="text-[13px] font-medium tracking-widest uppercase text-white/60 hover:text-white transition-colors duration-300">Pricing</a>
          <a href="../faq.html" class="text-[13px] font-medium tracking-widest uppercase text-white/60 hover:text-white transition-colors duration-300">FAQ</a>
          <a href="../blog.html" class="text-[13px] font-medium tracking-widest uppercase text-white/60 hover:text-white transition-colors duration-300">Blog</a>
          <a href="../contact.html" class="text-[13px] font-medium tracking-widest uppercase text-white/60 hover:text-white transition-colors duration-300">Contact</a>
        </div>
        <div class="flex items-center gap-4">
          <a href="../contact.html" class="btn hidden sm:inline-flex items-center gap-2 bg-white hover:bg-white/90 active:bg-white/80 text-brand-black font-semibold text-[13px] tracking-wide px-6 py-2.5 transition-transform duration-300 ease-spring hover:scale-[1.03] active:scale-[0.97]">Book a Session</a>
          <button id="mobile-menu-btn" class="lg:hidden flex items-center justify-center w-10 h-10 text-white hover:text-white/70 focus-visible:outline focus-visible:outline-2 focus-visible:outline-white active:scale-95 transition-transform duration-200" aria-label="Open menu" aria-expanded="false"><svg id="hamburger-icon" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg><svg id="close-icon" class="w-6 h-6 hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button>
        </div>
      </div>
    </div>
    <div id="mobile-menu" class="lg:hidden overflow-hidden transition-[max-height] duration-300 ease-out max-h-0 bg-brand-black/97 backdrop-blur-xl border-t border-white/5">
      <div class="px-6 py-6 flex flex-col gap-1">
        <div>
          <button id="mobile-services-toggle" class="w-full flex items-center justify-between px-4 py-3.5 text-[13px] font-medium tracking-widest uppercase text-white/60 hover:text-white hover:bg-white/5 rounded-lg transition-colors duration-200 bg-transparent border-none cursor-pointer text-left" type="button">What We Do<svg id="mobile-services-chevron" class="w-4 h-4 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg></button>
          <div id="mobile-services-panel" class="overflow-hidden max-h-0 transition-[max-height] duration-300">
            <div class="pl-8 pr-4 pb-2 space-y-1">
              <a href="../services/junior-prep.html" class="mobile-nav-link block px-4 py-2.5 text-[12px] font-medium tracking-wider uppercase text-white/40 hover:text-white hover:bg-white/5 rounded-lg transition-colors duration-200">Junior Prep</a>
              <a href="../services/senior-refinement.html" class="mobile-nav-link block px-4 py-2.5 text-[12px] font-medium tracking-wider uppercase text-white/40 hover:text-white hover:bg-white/5 rounded-lg transition-colors duration-200">Senior Refinement</a>
              <a href="../services/off-season-conditioning.html" class="mobile-nav-link block px-4 py-2.5 text-[12px] font-medium tracking-wider uppercase text-white/40 hover:text-white hover:bg-white/5 rounded-lg transition-colors duration-200">Off-Season Conditioning</a>
              <a href="../services/injury-return.html" class="mobile-nav-link block px-4 py-2.5 text-[12px] font-medium tracking-wider uppercase text-white/40 hover:text-white hover:bg-white/5 rounded-lg transition-colors duration-200">Injury Return</a>
              <a href="../services.html" class="mobile-nav-link block px-4 py-2.5 text-[12px] font-medium tracking-wider uppercase text-white/30 hover:text-white hover:bg-white/5 rounded-lg transition-colors duration-200">View All Programs</a>
            </div>
          </div>
        </div>
        <a href="../about.html" class="mobile-nav-link block px-4 py-3.5 text-[13px] font-medium tracking-widest uppercase text-white/60 hover:text-white hover:bg-white/5 rounded-lg transition-colors duration-200">About</a>
        <a href="../pricing.html" class="mobile-nav-link block px-4 py-3.5 text-[13px] font-medium tracking-widest uppercase text-white/60 hover:text-white hover:bg-white/5 rounded-lg transition-colors duration-200">Pricing</a>
        <a href="../faq.html" class="mobile-nav-link block px-4 py-3.5 text-[13px] font-medium tracking-widest uppercase text-white/60 hover:text-white hover:bg-white/5 rounded-lg transition-colors duration-200">FAQ</a>
        <a href="../blog.html" class="mobile-nav-link block px-4 py-3.5 text-[13px] font-medium tracking-widest uppercase text-white/60 hover:text-white hover:bg-white/5 rounded-lg transition-colors duration-200">Blog</a>
        <a href="../contact.html" class="mobile-nav-link block px-4 py-3.5 text-[13px] font-medium tracking-widest uppercase text-white/60 hover:text-white hover:bg-white/5 rounded-lg transition-colors duration-200">Contact</a>
        <div class="mt-4 px-4"><a href="../contact.html" class="btn flex items-center justify-center gap-2 bg-white text-brand-black font-semibold text-sm px-6 py-3.5 w-full">Book a Session</a></div>
      </div>
    </div>
  </nav>

  <script>
    (function(){var b=document.getElementById('mobile-menu-btn'),m=document.getElementById('mobile-menu'),h=document.getElementById('hamburger-icon'),c=document.getElementById('close-icon'),ls=m.querySelectorAll('a.mobile-nav-link');function t(){var o=m.style.maxHeight&&m.style.maxHeight!=='0px';m.style.maxHeight=o?'0px':m.scrollHeight+'px';h.classList.toggle('hidden',!o);c.classList.toggle('hidden',o);b.setAttribute('aria-expanded',String(!o))}b.addEventListener('click',t);ls.forEach(function(l){l.addEventListener('click',function(){m.style.maxHeight='0px';h.classList.remove('hidden');c.classList.add('hidden');b.setAttribute('aria-expanded','false')})})})();
    (function(){var t=document.getElementById('mobile-services-toggle'),p=document.getElementById('mobile-services-panel'),ch=document.getElementById('mobile-services-chevron');if(t&&p){t.addEventListener('click',function(){var o=p.style.maxHeight&&p.style.maxHeight!=='0px';p.style.maxHeight=o?'0px':p.scrollHeight+'px';ch.style.transform=o?'':'rotate(180deg)'})}})();
    (function(){var n=document.getElementById('main-nav'),l=0;window.addEventListener('scroll',function(){var y=window.scrollY;if(y>80){n.style.background='rgba(10,10,10,0.92)';n.style.backdropFilter='blur(16px)'}else{n.style.background='';n.style.backdropFilter=''}n.style.transform=(y>l&&y>300)?'translateY(-100%)':'translateY(0)';l=y})})();
  </script>

  <main id="main">

  <nav class="breadcrumbs" aria-label="Breadcrumb">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-28 lg:pt-32 pb-3 text-sm text-brand-muted">
      <a href="/" class="hover:text-brand-white">Home</a>
      <span class="mx-2 text-brand-grey">/</span>
      <a href="/suburbs" class="hover:text-brand-white">Service Areas</a>
      <span class="mx-2 text-brand-grey">/</span>
      <span class="text-brand-white">@@NAME@@</span>
    </div>
  </nav>

  <!-- HERO -->
  <header id="main-content" class="bg-brand-black">
    <div class="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12 pt-6 lg:pt-10 pb-14 lg:pb-20">
      <div class="grid lg:grid-cols-12 gap-10 lg:gap-16 items-start">
        <div class="lg:col-span-7 reveal">
          <div class="inline-flex items-center gap-4 mb-6">
            <div class="accent-line"></div>
            <span class="text-white/40 text-xs font-medium tracking-[0.3em] uppercase">@@NAME@@</span>
          </div>
          <h1 class="font-display text-5xl sm:text-6xl lg:text-7xl text-white leading-[0.95] mb-6">Private football coaching in @@NAME@@.</h1>
          <p class="text-white/45 text-base sm:text-lg max-w-xl mb-8" style="line-height: 1.8;">@@HERO_SUB@@</p>
          <div class="flex flex-col sm:flex-row gap-3 sm:gap-4">
            <a href="../contact.html?suburb=@@SLUG@@" class="btn inline-flex items-center justify-center gap-2.5 bg-white hover:bg-white/90 active:bg-white/80 text-brand-black font-semibold text-sm tracking-wide px-8 py-4 transition-transform duration-300 ease-spring hover:scale-[1.02] active:scale-[0.98]">Book a Session<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg></a>
            <a href="../pricing.html" class="btn inline-flex items-center justify-center gap-2 border border-white/15 hover:border-white/40 hover:bg-white/5 text-white font-medium text-sm tracking-wide px-7 py-4 transition-colors duration-200">View Pricing</a>
          </div>
        </div>
        <div class="lg:col-span-5 reveal space-y-5">
          <div class="relative aspect-[4/5] overflow-hidden border border-white/8 shadow-lift">
            <img width="500" height="624" src="../Assets/Chris and Senior Player.webp" alt="Coach Chris running a senior 1-on-1 session at the Point Cook venue" class="w-full h-full object-cover" loading="lazy">
            <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/10 to-transparent pointer-events-none"></div>
            <div class="absolute bottom-0 left-0 right-0 p-5 sm:p-6">
              <p class="text-[10px] uppercase tracking-[0.3em] text-white/60 mb-1.5">From @@NAME@@</p>
              <p class="text-white text-sm font-medium">@@DRIVE_CAPTION@@</p>
            </div>
          </div>
          <div class="border border-white/8 p-6 sm:p-8 relative grain bg-brand-dark/80">
            <div class="relative z-10">
              <p class="text-[10px] uppercase tracking-[0.3em] text-white/35 mb-4">Quick reference</p>
              <div class="space-y-4">
                <div class="flex justify-between items-baseline border-b border-white/8 pb-3"><span class="text-[12px] text-white/40 uppercase tracking-wider">Base</span><span class="text-sm text-white">Point Cook</span></div>
                <div class="flex justify-between items-baseline border-b border-white/8 pb-3"><span class="text-[12px] text-white/40 uppercase tracking-wider">Venue</span><span class="text-sm text-white">West Point SC, Point Cook</span></div>
                <div class="flex justify-between items-baseline"><span class="text-[12px] text-white/40 uppercase tracking-wider">Drive time</span><span class="text-sm text-white">@@DRIVE_SHORT@@</span></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>

  <!-- WHY US FROM HERE -->
  <section class="bg-brand-dark py-20 lg:py-28 border-t border-white/5">
    <div class="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
      <div class="max-w-2xl mb-12 reveal">
        <div class="inline-flex items-center gap-4 mb-6"><div class="accent-line"></div><span class="text-white/40 text-xs font-medium tracking-[0.3em] uppercase">01 &middot; Why @@NAME@@ players choose us</span></div>
        <h2 class="font-display text-4xl sm:text-5xl text-white">Direct drive. Private coach.</h2>
      </div>
      <div class="grid md:grid-cols-3 gap-4 lg:gap-6">
        <div class="reveal border border-white/8 p-7 lg:p-8 hover:border-white/15 transition-colors duration-300"><span class="num-badge text-white/15">01</span><h3 class="font-display text-2xl text-white mt-3 mb-3">@@WHY1_TITLE@@</h3><p class="text-white/40 text-[14px]" style="line-height: 1.75;">@@WHY1_BODY@@</p></div>
        <div class="reveal border border-white/8 p-7 lg:p-8 hover:border-white/15 transition-colors duration-300"><span class="num-badge text-white/15">02</span><h3 class="font-display text-2xl text-white mt-3 mb-3">@@WHY2_TITLE@@</h3><p class="text-white/40 text-[14px]" style="line-height: 1.75;">@@WHY2_BODY@@</p></div>
        <div class="reveal border border-white/8 p-7 lg:p-8 hover:border-white/15 transition-colors duration-300"><span class="num-badge text-white/15">03</span><h3 class="font-display text-2xl text-white mt-3 mb-3">125+ players, 92% progression</h3><p class="text-white/40 text-[14px]" style="line-height: 1.75;">Across 4+ years we've worked with 125+ athletes from right across the west. 92% show measurable progression by the end of a block.</p></div>
      </div>
    </div>
  </section>

  <!-- WHAT WE COACH -->
  <section class="bg-brand-black py-20 lg:py-28 border-t border-white/5">
    <div class="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
      <div class="max-w-2xl mb-12 reveal">
        <div class="inline-flex items-center gap-4 mb-6"><div class="accent-line"></div><span class="text-white/40 text-xs font-medium tracking-[0.3em] uppercase">02 &middot; Programs available to @@NAME@@ players</span></div>
        <h2 class="font-display text-4xl sm:text-5xl text-white">Four programs. Every level.</h2>
      </div>
      <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
        <a href="../services/junior-prep.html" class="reveal border border-white/8 p-7 hover:border-white/20 hover:bg-white/[0.02] transition-all duration-300 group"><span class="num-badge text-white/15">01</span><h3 class="font-display text-xl text-white mt-3 mb-2">Junior Prep</h3><p class="text-white/40 text-[13px]" style="line-height: 1.7;">@@JUNIOR_MICRO@@</p></a>
        <a href="../services/senior-refinement.html" class="reveal border border-white/8 p-7 hover:border-white/20 hover:bg-white/[0.02] transition-all duration-300 group"><span class="num-badge text-white/15">02</span><h3 class="font-display text-xl text-white mt-3 mb-2">Senior Refinement</h3><p class="text-white/40 text-[13px]" style="line-height: 1.7;">Sharpening experienced players from across the western suburbs.</p></a>
        <a href="../services/off-season-conditioning.html" class="reveal border border-white/8 p-7 hover:border-white/20 hover:bg-white/[0.02] transition-all duration-300 group"><span class="num-badge text-white/15">03</span><h3 class="font-display text-xl text-white mt-3 mb-2">Off-Season Conditioning</h3><p class="text-white/40 text-[13px]" style="line-height: 1.7;">Build the physical engine while comp's quiet. October to March block options.</p></a>
        <a href="../services/injury-return.html" class="reveal border border-white/8 p-7 hover:border-white/20 hover:bg-white/[0.02] transition-all duration-300 group"><span class="num-badge text-white/15">04</span><h3 class="font-display text-xl text-white mt-3 mb-2">Injury Return</h3><p class="text-white/40 text-[13px]" style="line-height: 1.7;">Structured return-to-play. We work alongside your medical team where needed.</p></a>
      </div>
    </div>
  </section>

  <!-- LOCAL CONTEXT -->
  <section class="bg-brand-dark py-20 lg:py-28 border-t border-white/5 relative grain">
    <div class="max-w-4xl mx-auto px-6 sm:px-8 lg:px-12 reveal relative z-10">
      <div class="inline-flex items-center gap-4 mb-6"><div class="accent-line"></div><span class="text-white/40 text-xs font-medium tracking-[0.3em] uppercase">03 &middot; Football and soccer in @@NAME@@</span></div>
      <h2 class="font-display text-4xl sm:text-5xl text-white mb-6">@@LOCAL_H2@@</h2>
      <div class="space-y-5 text-white/45 text-[15px]" style="line-height: 1.85;">
        <p>@@LOCAL_P1@@</p>
        <p>@@LOCAL_P2@@</p>
        <p>@@LOCAL_P3@@</p>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="bg-brand-black py-20 lg:py-28 border-t border-white/5">
    <div class="max-w-3xl mx-auto px-6 sm:px-8 lg:px-12">
      <div class="mb-10 reveal">
        <div class="inline-flex items-center gap-4 mb-6"><div class="accent-line"></div><span class="text-white/40 text-xs font-medium tracking-[0.3em] uppercase">04 &middot; Common questions from @@NAME@@</span></div>
        <h2 class="font-display text-4xl sm:text-5xl text-white">Quick answers.</h2>
      </div>
      <div>
@@FAQ_HTML@@
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section class="bg-brand-dark py-20 lg:py-28 border-t border-white/5">
    <div class="max-w-3xl mx-auto px-6 sm:px-8 text-center reveal">
      <h2 class="font-display text-4xl sm:text-5xl lg:text-6xl text-white mb-5">Book your first session.</h2>
      <p class="text-white/35 text-base sm:text-lg mb-10 max-w-xl mx-auto" style="line-height: 1.75;">First session is an assessment - no commitment beyond that. We'll reply within 24 hours by call, text, or email.</p>
      <div class="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center">
        <a href="../contact.html?suburb=@@SLUG@@" class="btn inline-flex items-center justify-center gap-2.5 bg-white hover:bg-white/90 active:bg-white/80 text-brand-black font-semibold text-sm tracking-wide px-8 py-4 transition-transform duration-300 ease-spring hover:scale-[1.02] active:scale-[0.98]">Book a Session<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg></a>
        <a href="tel:0401117862" class="btn inline-flex items-center justify-center gap-2.5 border border-white/15 hover:border-white/40 hover:bg-white/5 text-white font-medium text-sm tracking-wide px-8 py-4 transition-colors duration-200"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>0401 117 862</a>
      </div>
    </div>
  </section>

  <!-- OTHER SUBURBS -->
  <section class="bg-brand-black py-16 border-t border-white/5">
    <div class="max-w-5xl mx-auto px-6 sm:px-8 lg:px-12">
      <p class="text-[10px] uppercase tracking-[0.3em] text-white/40 mb-6 text-center reveal">Other service areas</p>
      <div class="flex flex-wrap justify-center gap-x-6 gap-y-3 reveal">
@@OTHER_AREAS@@
      </div>
      <p class="text-center mt-6 reveal"><a href="index.html" class="text-sm text-white/55 hover:text-white transition-colors duration-200">View all service areas</a></p>
    </div>
  </section>

  <!-- SPONSORS -->
  <section class="bg-white py-16">
    <div class="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
      <p class="text-center text-neutral-400 text-xs font-medium tracking-[0.2em] uppercase mb-10">Our Partners</p>
      <div class="flex flex-wrap items-center justify-center gap-x-14 gap-y-8">
        <a href="https://www.loutakis.com.au/" target="_blank" rel="noopener noreferrer"><img width="510" height="99" src="../Assets/Sponsors/Loutakis Real Estate.png" alt="Loutakis Real Estate" class="h-14 w-auto object-contain grayscale opacity-70 hover:grayscale-0 hover:opacity-100 transition-[filter,opacity] duration-300" loading="lazy"></a>
        <a href="https://www.instagram.com/kstruct_/?hl=en" target="_blank" rel="noopener noreferrer"><img width="163" height="133" src="../Assets/Sponsors/K-Struct New.png" alt="K-Struct" class="h-20 w-auto object-contain grayscale opacity-70 hover:grayscale-0 hover:opacity-100 transition-[filter,opacity] duration-300" loading="lazy"></a>
        <a href="https://www.westernmitsubishi.com.au/" target="_blank" rel="noopener noreferrer"><img width="418" height="120" src="../Assets/Sponsors/Western Mitsubishi.jpeg" alt="Western Mitsubishi" class="h-14 w-auto object-contain grayscale opacity-70 hover:grayscale-0 hover:opacity-100 transition-[filter,opacity] duration-300" loading="lazy"></a>
        <a href="https://www.dilalloelectrical.com.au/" target="_blank" rel="noopener noreferrer"><img width="367" height="137" src="../Assets/Sponsors/Di Lallo Electrical Services.jpeg" alt="Di Lallo Electrical Services" class="h-14 w-auto object-contain grayscale opacity-70 hover:grayscale-0 hover:opacity-100 transition-[filter,opacity] duration-300" loading="lazy"></a>
        <a href="https://hcdistributors.com.au/" target="_blank" rel="noopener noreferrer"><img width="300" height="300" src="../Assets/Sponsors/cropped-HCD_Logo_New.webp" alt="HC Distributors" class="h-14 w-auto object-contain grayscale opacity-70 hover:grayscale-0 hover:opacity-100 transition-[filter,opacity] duration-300" loading="lazy"></a>
      </div>
    </div>
  </section>

  </main>

  <div class="fixed bottom-4 left-4 z-50"><div class="elfsight-app-aefd1437-8568-466c-9489-4de114840c19" data-elfsight-app-lazy></div></div>

  <!-- FOOTER -->
  <footer class="bg-brand-black pt-16 pb-8 border-t border-white/5" role="contentinfo">
    <div class="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
      <div class="grid sm:grid-cols-2 lg:grid-cols-5 gap-10 lg:gap-8 mb-14">
        <div class="lg:col-span-2">
          <div class="flex items-center gap-3 mb-5"><img width="500" height="500" src="../Assets/Logo.png" alt="Accelerate Performance Football" class="h-10 w-auto" loading="lazy"></div>
          <p class="text-sm text-white/35 mb-5" style="line-height: 1.7;">Private football coaching in Point Cook. Sessions run at West Point Soccer Club, 2 Webster St, Point Cook. Dedicated technique and performance training for footballers who want more.</p>
          <a href="https://www.instagram.com/accelerate.performance_/" target="_blank" rel="noopener noreferrer" class="inline-flex items-center justify-center w-9 h-9 rounded-lg bg-white/5 text-white/45 hover:bg-white/10 hover:text-white transition-colors duration-200" aria-label="Follow us on Instagram"><svg class="w-[18px] h-[18px]" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg></a>
        </div>
        <div>
          <h3 class="apf-sub text-xs font-medium text-white/45 uppercase tracking-[0.15em] mb-5">Programs</h3>
          <nav class="space-y-2.5" aria-label="Programs">
            <a href="../services/junior-prep.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">Junior Prep</a>
            <a href="../services/senior-refinement.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">Senior Refinement</a>
            <a href="../services/off-season-conditioning.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">Off-Season Conditioning</a>
            <a href="../services/injury-return.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">Injury Return</a>
            <a href="../online.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">Online Training</a>
          </nav>
        </div>
        <div>
          <h3 class="apf-sub text-xs font-medium text-white/45 uppercase tracking-[0.15em] mb-5">Service Areas</h3>
          <nav class="space-y-2.5" aria-label="Service areas">
            <a href="point-cook.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">Point Cook</a>
            <a href="altona.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">Altona</a>
            <a href="williamstown.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">Williamstown</a>
            <a href="werribee.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">Werribee</a>
            <a href="hoppers-crossing.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">Hoppers Crossing</a>
          </nav>
        </div>
        <div>
          <h3 class="apf-sub text-xs font-medium text-white/45 uppercase tracking-[0.15em] mb-5">Navigation</h3>
          <nav class="space-y-2.5" aria-label="Footer navigation">
            <a href="../about.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">About</a>
            <a href="../coaches/chris-sutera.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">Chris Sutera</a>
            <a href="../coaches/james-sutera.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">James Sutera</a>
            <a href="../pricing.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">Pricing</a>
            <a href="../faq.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">FAQ</a>
            <a href="../blog.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">Blog</a>
            <a href="../contact.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">Contact</a>
            <a href="../privacy.html" class="block text-sm text-white/35 hover:text-white transition-colors duration-200">Privacy Policy</a>
          </nav>
        </div>
      </div>
      <div class="border-t border-white/5 pt-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <p class="text-xs text-white/20">&copy; 2026 Accelerate Performance Football. All rights reserved.</p>
        <p class="text-xs text-white/20">Based in Point Cook, Victoria, Australia</p>
        <p class="text-xs text-white/20">Built by <a href="https://suterasites.com.au/" target="_blank" rel="noopener noreferrer" class="hover:text-white transition-colors duration-200">Sutera Sites</a></p>
      </div>
    </div>
  </footer>

  <!-- STICKY MOBILE CTA -->
  <div class="lg:hidden h-20" aria-hidden="true"></div>
  <div class="lg:hidden fixed bottom-0 inset-x-0 z-40 bg-brand-black/95 backdrop-blur border-t border-white/10" style="padding-bottom: env(safe-area-inset-bottom);" role="region" aria-label="Quick contact actions">
    <div class="flex items-stretch gap-2 px-4 py-3">
      <a href="../contact.html?suburb=@@SLUG@@" class="btn flex-1 inline-flex items-center justify-center gap-2 bg-white hover:bg-white/90 active:bg-white/80 text-brand-black font-semibold text-sm tracking-wide px-5 py-3 transition-transform duration-200 ease-spring active:scale-[0.98]">Book a Session</a>
      <a href="tel:0401117862" aria-label="Call 0401 117 862" class="inline-flex items-center justify-center gap-2 text-white font-medium text-sm tracking-wide px-5 py-3 border border-white/15 hover:border-white/30 hover:bg-white/5 transition-colors duration-200"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>Call</a>
    </div>
  </div>

  <script>
    (function(){var e=document.querySelectorAll('.reveal');var o=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting)en.target.classList.add('visible')})},{threshold:0.08,rootMargin:'0px 0px -30px 0px'});e.forEach(function(el){o.observe(el)})})();
  </script>

</body>
</html>
"""


def faq_list(s):
    """The 4 Q&As, used identically for schema JSON-LD and visible HTML."""
    return [
        ("Where exactly is the training venue?",
         "West Point Soccer Club, 2 Webster St, Point Cook VIC 3030. For {n} players that's {dir}. Direct route, free on-site parking.".format(n=s["name"], dir=s["venue_dir"])),
        ("Can I train with you alongside my regular club?", CLUB_ANSWER),
        (s["faq_drive_q"], s["faq_drive_a"]),
        ("Do sibling discounts apply for {n} families?".format(n=s["name"]), SIBLING_ANSWER),
    ]


def faq_jsonld(s):
    items = [{"@type": "Question", "name": q,
              "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_list(s)]
    return json.dumps(items, ensure_ascii=False, indent=10).rstrip()


def faq_html(s):
    rows = []
    for q, a in faq_list(s):
        rows.append(
            '        <details class="tier-faq"><summary><span class="text-base sm:text-lg '
            'text-white/80 font-medium">' + q + '</span><span class="plus" aria-hidden="true">'
            '</span></summary><div class="answer">' + a + '</div></details>')
    return "\n".join(rows)


def other_areas_html(s):
    links = []
    for i, (slug, name) in enumerate(s["neighbors"]):
        if i:
            links.append('        <span class="text-white/15">&middot;</span>')
        links.append('        <a href="' + slug + '.html" class="text-sm text-white/55 '
                     'hover:text-white transition-colors duration-200">' + name + '</a>')
    return "\n".join(links)


def title_for(s):
    t = "Football & Soccer Coaching " + s["name"] + " | Accelerate Performance"
    # Keep the visible <title> tight; long suburb names get the shorter suffix.
    if len(t) > 62:
        t = "Football & Soccer Coaching " + s["name"] + " | APF"
    return t


def render(s):
    faqj = faq_jsonld(s)
    meta = ("Private football and soccer coaching for {n} players. About {d} to our venue at West "
            "Point Soccer Club, Point Cook. Juniors to senior-league.").format(n=s["name"], d=s["drive_short"].replace("~", "").strip())
    og_title = "Private Football & Soccer Coaching " + s["name"] + " | Accelerate Performance Football"
    og_desc = ("Private football and soccer coaching for {n} players. {cap} to our home venue West "
               "Point Soccer Club, Point Cook.").format(n=s["name"], cap=s["drive_caption"])
    tw_desc = ("Private football and soccer coaching for {n} players. {cap} to West Point SC, Point "
               "Cook.").format(n=s["name"], cap=s["drive_caption"])
    service_name = "Private Football and Soccer Coaching - " + s["name"]
    service_desc = ("Private football and soccer coaching for {n} players. Sessions run at our home "
                    "venue West Point Soccer Club at 2 Webster St, Point Cook - {dir}. 1-on-1 and "
                    "Small Unit sessions, juniors through to senior-league.").format(n=s["name"], dir=s["venue_dir"])
    repl = {
        "@@DOMAIN@@": DOMAIN,
        "@@TITLE@@": title_for(s),
        "@@META_DESC@@": meta,
        "@@OG_TITLE@@": og_title,
        "@@OG_DESC@@": og_desc,
        "@@TW_DESC@@": tw_desc,
        "@@SLUG@@": s["slug"],
        "@@NAME@@": s["name"],
        "@@LAT@@": s["lat"],
        "@@LON@@": s["lon"],
        "@@POSTCODE@@": s["postcode"],
        "@@SERVICE_NAME@@": service_name,
        "@@SERVICE_DESC@@": service_desc,
        "@@FAQ_JSONLD@@": faqj,
        "@@HERO_SUB@@": s["hero_sub"],
        "@@DRIVE_CAPTION@@": s["drive_caption"],
        "@@DRIVE_SHORT@@": s["drive_short"],
        "@@WHY1_TITLE@@": s["why1_title"],
        "@@WHY1_BODY@@": s["why1_body"],
        "@@WHY2_TITLE@@": s["why2_title"],
        "@@WHY2_BODY@@": s["why2_body"],
        "@@JUNIOR_MICRO@@": s["junior_micro"],
        "@@LOCAL_H2@@": s["local_h2"],
        "@@LOCAL_P1@@": s["local_p1"],
        "@@LOCAL_P2@@": s["local_p2"],
        "@@LOCAL_P3@@": s["local_p3"],
        "@@FAQ_HTML@@": faq_html(s),
        "@@OTHER_AREAS@@": other_areas_html(s),
    }
    out = TEMPLATE
    for k, v in repl.items():
        out = out.replace(k, v)
    if "@@" in out:
        leftover = set(t.split("@@")[1] for t in out.split("@@")[1::2])
        raise SystemExit("Unfilled tokens in {}: {}".format(s["slug"], leftover))
    return out


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    written = []
    for s in NEW_SUBURBS:
        path = os.path.join(OUT_DIR, s["slug"] + ".html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(render(s))
        written.append(s["slug"])
    print("Wrote {} suburb pages: {}".format(len(written), ", ".join(written)))


if __name__ == "__main__":
    main()
