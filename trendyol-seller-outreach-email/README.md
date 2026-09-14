# Trendyol seller-outreach email

A personalised, mobile-first HTML email inviting marketplace sellers in Saudi Arabia to
open a store on Trendyol, sent by Tarik Alotay (Business Development Executive, Trendyol).

Built to Trendyol's deck branding (orange `#FF6720`, Inter, off-white `#FAFAFA`, black
wordmark). Full rationale, copy and tokens are in `DESIGN.md`.

## What is in this folder

| File | Purpose |
|---|---|
| `email.html` | The sendable template. Contains `{{merge_fields}}`. |
| `sample-data.json` | Sample merge values (OKWAN) used for the preview renders. |
| `render.js` | Playwright script: merges sample data, renders phone + desktop PNGs. |
| `output/trendyol-seller-email-phone.png` | Phone preview (390 px wide, 2x). |
| `output/trendyol-seller-email-desktop.png` | PC preview (1280 px wide, 2x). |
| `output/email-okwan-sample.html` | Merged sample, openable in a browser. |
| `assets/` | Logo PNGs, WhatsApp icon PNGs, fonts used only for offline rendering. |
| `DESIGN.md` | Brand study, conversion strategy, final copy, layout and engineering rules. |

## Merge fields

| Field | Example | Notes |
|---|---|---|
| `{{seller_name}}` | `OKWAN` | Store or brand name exactly as the seller writes it. |
| `{{category}}` | `Travel & Lifestyle Accessories` | The seller's main category on their current channels. |
| `{{item_count}}` | `100+` | Live item count on their current channels. Keep it honest; round down. |
| `{{seller_name_url}}` | `OKWAN` | URL-encoded seller name for the WhatsApp and mailto links. Most ESPs can derive it; `render.js` does. |

Subject lines (A/B, both in `DESIGN.md`):

- A: `{{seller_name}} + Trendyol: your {{category}} range in front of 4M+ Gulf shoppers`
- B: `Tarik from Trendyol — a quick idea for {{seller_name}}`

## Before sending

1. **Host the two images** and replace the relative paths in `email.html`:
   `assets/trendyol-logo.png` → `https://<your-cdn>/trendyol-logo.png`
   `assets/whatsapp-icon-white.png` → `https://<your-cdn>/whatsapp-icon-white.png`
   Base64 images are blocked by Gmail, so hosting is required.
2. **Check the sender address.** The template signs as `tarik.alotay@trendyol.com`.
   Send from that mailbox so replies land in the right inbox and DKIM/SPF align.
3. **Fill the three seller fields per row** from the lead sheet. Never name another
   marketplace in the copy; the template only says "sales channels".
4. **Verify OKWAN's item count** (the sample uses `100+` as a placeholder).
5. Send a test to yourself on iPhone Mail, Gmail app (Android), Gmail web and Outlook.
   Tap both buttons: the WhatsApp link opens a chat with a pre-filled message, the
   reply button opens a pre-addressed email.
6. Keep the opt-out line in the footer. Mass B2B email in KSA still needs a clear
   way to say no, and it protects sender reputation.

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
| 40M+ active shoppers, 35 countries, 250K sellers | Trendyol About-us deck, LTM Dec 2025 |
| Gulf 2025: 4M+ active shoppers, 35M units sold, 2M+ DAU, 10M+ downloads | Deck, "Trendyol in the Gulf Region" |
| ~$1B marketing and campaign investment in the Gulf in 2025 | Deck, marketing channels page |
| 15K influencers in the Gulf network | Deck, influencer pages |
| Legendary Friday peak: 5M DAU, 3.5M units in one day | Deck, Gulf page |
| 150K+ sellers used on-site ads in 2025, returns up to 12x | Deck, Trendyol Marketing Solutions page |
| No setup or monthly fees, category-based commission | Trendyol Seller Information Center (KSA) |
| Onboarding takes roughly 1–2 weeks | Trendyol Seller Information Center (KSA) |
| Saudi Arabia is Trendyol's second-largest market worldwide | Bazaar Times, 23 March 2025 ("Saudi Arabia emerging as its second-largest market globally"); The National, Oct 2024 (Trendyol: "Saudi Arabia is our largest market" in the Gulf) |
