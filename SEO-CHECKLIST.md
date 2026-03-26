# SEO Checklist — Website Launch & Ongoing

> Drop this file into any project repo. Work through each section before launch, then revisit monthly.

---

## 1. Technical Foundations

- [ ] Site loads over HTTPS (SSL certificate active)
- [ ] All HTTP URLs redirect to HTTPS
- [ ] `www` and non-`www` versions resolve to one canonical domain
- [ ] Favicon is set (`.ico` + `.png` for Apple touch)
- [ ] Custom 404 page exists with navigation back to key pages
- [ ] `robots.txt` is present and not blocking important pages
- [ ] XML sitemap is generated and accessible at `/sitemap.xml`
- [ ] Sitemap submitted to Google Search Console
- [ ] Site is verified in Google Search Console
- [ ] No orphan pages (every page is reachable from at least one internal link)
- [ ] No broken internal links (run a crawl check)
- [ ] Canonical tags (`<link rel="canonical">`) set on every page
- [ ] Structured data / JSON-LD schema added (see Section 7)
- [ ] No duplicate content issues across pages

---

## 2. Page Speed & Core Web Vitals

- [ ] Images are compressed and served in modern formats (WebP / AVIF)
- [ ] Images use `width` and `height` attributes (prevents layout shift)
- [ ] Lazy loading enabled on below-the-fold images (`loading="lazy"`)
- [ ] CSS is minified
- [ ] JavaScript is minified and deferred where possible (`defer` / `async`)
- [ ] No render-blocking resources in the critical path
- [ ] Fonts are self-hosted or use `font-display: swap`
- [ ] Largest Contentful Paint (LCP) < 2.5s
- [ ] Cumulative Layout Shift (CLS) < 0.1
- [ ] Interaction to Next Paint (INP) < 200ms
- [ ] Test with Google PageSpeed Insights — aim for 90+ on mobile
- [ ] Test with GTmetrix as a secondary check

---

## 3. On-Page SEO — Every Page

- [ ] Unique, descriptive `<title>` tag (50–60 characters)
- [ ] Title includes primary keyword near the front
- [ ] Unique `<meta name="description">` (120–155 characters)
- [ ] Meta description includes a call to action or value prop
- [ ] URL is short, lowercase, hyphenated, and keyword-relevant
- [ ] One `<h1>` tag per page containing the primary keyword
- [ ] Logical heading hierarchy (`h1` → `h2` → `h3`, no skipping)
- [ ] Primary keyword appears naturally in the first 100 words
- [ ] Images have descriptive `alt` text (not keyword-stuffed)
- [ ] Internal links to other relevant pages on the site
- [ ] External links to authoritative sources where appropriate (open in new tab)
- [ ] Content is a minimum of 300 words on service/landing pages
- [ ] No thin or duplicate content

---

## 4. Local SEO (Critical for Tradies & Service Businesses)

- [ ] Google Business Profile created and verified
- [ ] Business name, address, phone (NAP) are consistent everywhere
- [ ] NAP is in the site footer or contact page as crawlable text (not just an image)
- [ ] Service areas / suburbs listed on relevant pages
- [ ] Location-specific keywords used naturally (e.g., "Plumber in Cranbourne")
- [ ] Google Maps embed on the contact page
- [ ] Encourage and link to Google Reviews
- [ ] Listed on key Australian directories:
  - [ ] Yellow Pages (yellowpages.com.au)
  - [ ] True Local (truelocal.com.au)
  - [ ] Yelp Australia
  - [ ] HiPages (if relevant trade)
  - [ ] Oneflare
- [ ] Schema `LocalBusiness` or `HomeAndConstructionBusiness` markup added (see Section 7)

---

## 5. Mobile & Accessibility

- [ ] Site is fully responsive — test at 320px, 375px, 768px, 1024px, 1440px
- [ ] Tap targets are at least 48×48px with adequate spacing
- [ ] Text is readable without zooming (base font ≥ 16px)
- [ ] No horizontal scrolling on any device
- [ ] Click-to-call link on phone numbers (`tel:`)
- [ ] Click-to-email link on email addresses (`mailto:`)
- [ ] Colour contrast meets WCAG AA (4.5:1 for body text)
- [ ] All interactive elements are keyboard-accessible
- [ ] Forms have associated `<label>` elements
- [ ] Skip-to-content link for screen readers

---

## 6. Content & Copywriting

- [ ] Homepage clearly states: who, what, where, and why choose them
- [ ] Each service has its own dedicated page (not all lumped on one page)
- [ ] Service pages include: description, benefits, process, and a CTA
- [ ] Calls to action are clear and above the fold ("Get a Free Quote", "Call Now")
- [ ] Testimonials / reviews displayed on site
- [ ] Before-and-after project photos where applicable
- [ ] About page builds trust (photo of owner, licences, insurance, experience)
- [ ] FAQ section with real questions customers ask
- [ ] Blog or news section planned for ongoing content (not required for launch)

---

## 7. Structured Data / Schema Markup (JSON-LD)

Add to the `<head>` or bottom of `<body>` on every page:

- [ ] `LocalBusiness` (or more specific type like `Plumber`, `Electrician`, `Painter`)
  - `name`, `image`, `telephone`, `email`
  - `address` (street, city, state, postcode, country)
  - `geo` (latitude, longitude)
  - `url`, `openingHours`
  - `areaServed` (list of suburbs/regions)
  - `priceRange` (e.g., "$$")
- [ ] `WebSite` with `SearchAction` (if site has search)
- [ ] `BreadcrumbList` on interior pages
- [ ] `FAQPage` on pages with an FAQ section
- [ ] `Review` / `AggregateRating` if displaying testimonials
- [ ] Validate with Google Rich Results Test: https://search.google.com/test/rich-results

---

## 8. Social & Sharing

- [ ] Open Graph tags set on every page:
  - `og:title`, `og:description`, `og:image`, `og:url`, `og:type`
- [ ] `og:image` is at least 1200×630px
- [ ] Twitter card meta tags set (`twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`)
- [ ] Test with Facebook Sharing Debugger & Twitter Card Validator
- [ ] Social media profile links on the site (footer or contact page)

---

## 9. Analytics & Tracking

- [ ] Google Analytics 4 (GA4) installed and receiving data
- [ ] GA4 conversion events set up (form submissions, phone clicks, email clicks)
- [ ] Google Search Console linked to GA4
- [ ] Google Tag Manager installed (optional but recommended)
- [ ] Form submission tracking confirmed working
- [ ] Phone call click tracking confirmed working
- [ ] No analytics scripts firing on staging / dev environments

---

## 10. Pre-Launch Final Checks

- [ ] Proofread all content — no typos, no lorem ipsum
- [ ] All links work (internal + external)
- [ ] All images load correctly
- [ ] Forms submit successfully and notifications reach the client
- [ ] Staging / dev robots noindex tags removed
- [ ] Environment is set to production
- [ ] Check site in Chrome, Safari, Firefox, and Edge
- [ ] Check site on a real phone (not just browser dev tools)
- [ ] Backup / version control in place before going live
- [ ] DNS propagation confirmed after domain switch

---

## 11. Post-Launch & Ongoing (Monthly)

- [ ] Monitor Google Search Console for crawl errors and indexing issues
- [ ] Check Core Web Vitals report in Search Console
- [ ] Review GA4 for traffic trends and top-performing pages
- [ ] Update content seasonally or when services change
- [ ] Add new project photos / case studies
- [ ] Request Google Reviews from happy customers
- [ ] Build backlinks through local directories, supplier pages, community sponsorships
- [ ] Refresh meta titles and descriptions on underperforming pages
- [ ] Audit and fix any new broken links
- [ ] Keep CMS, plugins, and dependencies updated

---

## Quick Reference — Meta Tag Template

```html
<!-- Primary Meta Tags -->
<title>{Business Name} — {Primary Service} in {Location}</title>
<meta name="description" content="{Brief pitch, 120-155 chars. Include service + location + CTA.}" />
<link rel="canonical" href="https://www.example.com/{page-slug}" />

<!-- Open Graph -->
<meta property="og:type" content="website" />
<meta property="og:title" content="{Same as title or slightly varied}" />
<meta property="og:description" content="{Same as meta description}" />
<meta property="og:image" content="https://www.example.com/og-image.jpg" />
<meta property="og:url" content="https://www.example.com/{page-slug}" />

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{Same as og:title}" />
<meta name="twitter:description" content="{Same as og:description}" />
<meta name="twitter:image" content="https://www.example.com/og-image.jpg" />
```

---

## Quick Reference — LocalBusiness Schema Template

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "image": "https://www.example.com/logo.jpg",
  "telephone": "+61 4XX XXX XXX",
  "email": "info@example.com",
  "url": "https://www.example.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Example St",
    "addressLocality": "Melbourne",
    "addressRegion": "VIC",
    "postalCode": "3000",
    "addressCountry": "AU"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": -37.8136,
    "longitude": 144.9631
  },
  "openingHours": "Mo-Fr 07:00-17:00",
  "areaServed": ["Suburb 1", "Suburb 2", "Suburb 3"],
  "priceRange": "$$",
  "sameAs": [
    "https://www.facebook.com/yourbusiness",
    "https://www.instagram.com/yourbusiness"
  ]
}
```

---

*Last updated: March 2026*
