# Trendyol seller-outreach email

A bilingual (Arabic + English), mobile-first HTML email inviting marketplace sellers in
Saudi Arabia to open a store on Trendyol, sent by Tarik Alotay (Business Development
Executive, Trendyol). Designed to the standard of big-brand mass emails: one bold hero with
product imagery, a single ask, big numbers, one dominant CTA repeated at the end.

Brand tokens come straight from the Trendyol deck (orange `#FF6720`, Inter, black wordmark).
Full rationale, copy and layout rules are in `DESIGN.md`.

## What is in this folder

| File | Purpose |
|---|---|
| `email.html` | The sendable template. Contains `{{merge_fields}}`. |
| `sample-data.json` | Sample merge values (OKWAN) used for the preview renders. |
| `render.js` | Playwright script: merges sample data, renders phone + PC PNGs. |
| `output/trendyol-seller-email-phone.png` | Phone preview (390 px viewport, 2x). |
| `output/trendyol-seller-email-desktop.png` | PC preview (960 px reading-pane viewport, 2x). |
| `output/email-okwan-sample.html` | Merged sample, openable in a browser. |
| `output/email-okwan-send.html` | Merged sample with images pointing at this branch's GitHub raw URLs; what was sent as the Gmail test. Re-host the images on a permanent CDN before the mass send. |
| `assets/` | Wordmark, hero and app images (from the Trendyol deck), WhatsApp icons, fonts for offline rendering. |
| `DESIGN.md` | Brand study, big-brand benchmark, final copy in both languages, layout and engineering rules. |

## Merge fields

| Field | Example | Notes |
|---|---|---|
| `{{seller_name}}` | `OKWAN` | Store or brand name exactly as the seller writes it. Shown in English at the top of the hero and in both greetings. |
| `{{seller_name_url}}` | `OKWAN` | URL-encoded seller name for the WhatsApp and mailto links. Most ESPs can derive it; `render.js` does. |

Subject lines (A/B):

- A: `{{seller_name}} × Trendyol: open your store · افتحوا متجركم على ترينديول`
- B: `Tarik from Trendyol · طارق من ترينديول — {{seller_name}}`

## Before sending

1. **Host the five images** and replace the relative `assets/...` paths in `email.html`
   with absolute HTTPS URLs: `trendyol-logo.png`, `hero-hand-phone.jpg`, `app-hand-phone.jpg`,
   `whatsapp-icon-orange.png`, `whatsapp-icon-white.png`. Base64 images are blocked by Gmail.
2. **Check the sender address.** The template signs as `tarik.alotay@trendyol.com`.
   Send from that mailbox so replies land in the right inbox and DKIM/SPF align.
3. **Fill `seller_name` per row** from the lead sheet. It is the only per-seller field. Never name
   another marketplace; the copy only says "sales channels".
4. Send a test to yourself on iPhone Mail, Gmail app (Android), Gmail web and Outlook.
   Tap both buttons: WhatsApp opens a chat with a pre-filled message; the reply button
   opens a pre-addressed email.
5. Keep the opt-out line in the footer.

## Re-rendering the previews

```bash
cd trendyol-seller-outreach-email
# Playwright 1.56 + Chromium are already installed in the Claude environment:
NODE_PATH=/opt/node22/lib/node_modules node render.js
# Elsewhere: npm i playwright && npx playwright install chromium && node render.js
```

Edit `sample-data.json` to preview a different seller.

## Facts used in the copy and where they come from

| Claim | Source |
|---|---|
| 4M+ active shoppers in the Gulf, 2025 | Trendyol About-us deck, "Trendyol in the Gulf Region" |
| 35M units sold in the Gulf, 2025 | Same deck page |
| Saudi Arabia is Trendyol's second-largest market worldwide | Bazaar Times, 23 March 2025 ("Saudi Arabia emerging as its second-largest market globally"); The National, Oct 2024 (Trendyol: "Saudi Arabia is our largest market" in the Gulf) |
| Onboarding takes roughly 1–2 weeks | Trendyol Seller Information Center (KSA) |

No fees, commissions, ads, campaign or incentive claims appear in the copy.
